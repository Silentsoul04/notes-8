---
# kafka的基本命令


```shell script
ssh -p36000 kafka-00.ag.awsor


# 创建主题
bin/kafka-topics.sh --create --zookeeper 192.168.1.100:2181 --replication-factor 2 --partitions 2 --topic partopic

# 主题信息
bin/kafka-topics.sh --describe --zookeeper 192.168.1.100:2181 --topic partopic

# 命令行生产者
./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic mykafka

# 消费者
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic mykafka --from-beginning

# 获取主题情况
bin/kafka-topics.sh --zookeeper 172.16.8.4:2181 --list

# 获取消费者消费情况
bin/kafka-consumer-groups.sh --describe --bootstrap-server localhost:9092 --group common

# 更改topic的配置
kafka-topics.sh --zookeeper 172.16.8.4:2181 --alter --topic <topic name> --config retention.ms=1000

# 获取topic的配置
kafka-configs --zookeeper 172.16.8.4:2181 --entity-type topics --describe --entity-name web_log

# e.g.:
kafka-consumer-groups.sh --bootstrap-server <kafka_broker_host:9091> --group <group_name> --reset-offsets --to-offset 1000 --topic <my-topic> --execute


--topic t1:0,1,2（为指定的topic分区调整位移）

--to-earliest
--to-latest
--to-offset 100
--shift-by -10

bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group common --reset-offsets --to-offset 100 --topic addata.ad_heat --execute    



./bin/kafka-topics.sh --describe --zookeeper 172.19.33.30:2181/kafka/ag --topic binlog-db40-adData-ad-heat

./bin/kafka-consumer-groups.sh --describe --bootstrap-server 172.19.33.10:9092 --group common

./bin/kafka-consumer-groups.sh --bootstrap-server 172.19.33.10:9092 --group common --reset-offsets --shift-by -10 --topic binlog-db40-adData-ad-heat:0 --execute

```


--- 
# kafka介绍

在大数据中，使用了大量的数据。 关于数据，我们有两个主要挑战。第一个挑战是如何收集大量的数据，第二个挑战是分析收集的数据。 为了克服这些挑战，您必须需要一个消息系统。

物理上把Topic分成一个或多个Partition，每个Partition在物理上对应一个文件夹，该文件夹下存储这个Partition的所有消息和索引文件。

这里要注意，因为Kafka读取特定消息的时间复杂度为O(1)，即与文件大小无关，所以这里删除过期文件与提高Kafka性能无关。选择怎样的删除策略只与磁盘以及具体的需求有关。另外，Kafka会为每一个Consumer Group保留一些metadata信息——当前消费的消息的position，也即offset。这个offset由Consumer控制。正常情况下Consumer会在消费完一条消息后递增该offset。当然，Consumer也可将offset设成一个较小的值，重新消费一些消息。因为offet由Consumer控制，所以Kafka broker是无状态的，它不需要标记哪些消息被哪些消费过，也不需要通过broker去保证同一个Consumer Group只有一个Consumer能消费某一条消息，因此也就不需要锁机制，这也为Kafka的高吞吐率提供了有力保障。


每一个分区都是一个顺序的、不可变的消息队列， 并且可以持续的添加。分区中的消息都被分配了一个序列号，称之为偏移量(offset),在每个分区中此偏移量都是唯一的。

Kafka集群保持所有的消息，直到它们过期， 无论消息是否被消费了。

实际上消费者所持有的仅有的元数据就是这个偏移量，也就是消费者在这个log中的位置。 这个偏移量由消费者控制：正常情况当消费者消费消息的时候，偏移量也线性的的增加。但是实际偏移量由消费者控制，消费者可以将偏移量重置为更老的一个偏移量，重新读取消息。

可以看到这种设计对消费者来说操作自如， 一个消费者的操作不会影响其它消费者对此log的处理。


Kafka采用了一种分而治之的策略：分区。 因为Topic分区中消息只能由消费者组中的唯一一个消费者处理，所以消息肯定是按照先后顺序进行处理的。但是它也仅仅是保证Topic的一个分区顺序处理，不能保证跨分区的消息先后处理顺序。

同一Topic的一条消息只能被同一个Consumer Group内的一个Consumer消费，但多个Consumer Group可同时消费这一消息。


作为一个消息系统，Kafka遵循了传统的方式，选择由Producer向broker push消息并由Consumer从broker pull消息。一些logging-centric system，比如Facebook的Scribe和Cloudera的Flume，采用push模式。事实上，push模式和pull模式各有优劣。
　　push模式很难适应消费速率不同的消费者，因为消息发送速率是由broker决定的。push模式的目标是尽可能以最快速度传递消息，但是这样很容易造成Consumer来不及处理消息，典型的表现就是拒绝服务以及网络拥塞。而pull模式则可以根据Consumer的消费能力以适当的速率消费消息。
　　对于Kafka而言，pull模式更合适。pull模式可简化broker的设计，Consumer可自主控制消费消息的速率，同时Consumer可以自己控制消费方式——即可批量消费也可逐条消费，同时还能选择不同的提交方式从而实现不同的传输语义。 　　


---
# 消费者分区分配策略

同一时刻，一条消息只能被组中的一个消费者实例消费

消费者组订阅这个主题，意味着主题下的所有分区都会被组中的消费者消费到，如果按照从属关系来说的话就是，主题下的每个分区只从属于组中的一个消费者，不可能出现组中的两个消费者负责同一个分区。

问题： 如果分区数小于组中的消费者实例数

那么按照默认的策略（PS：之所以强调默认策略是因为你也可以自定义策略），有一些消费者是多余的，一直接不到消息而处于空闲状态。


- http://www.jasongj.com/2015/03/10/KafkaColumn1/
- [Kafka分区与消费者的关系](https://www.cnblogs.com/cjsblog/p/9664536.html)