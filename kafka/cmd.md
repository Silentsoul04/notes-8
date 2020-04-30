ssh -p36000 kafka-00.ag.alishh


# 海外
ssh -p36000 kafka-00.ag.awsor


## 热度
~/bin/kafka/bin/kafka-consumer-groups.sh --describe --bootstrap-server kafka-00.ag.awsor:9092 --group ag_web_heat

~/bin/kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.awsor:9092 --group ag_web_heat --reset-offsets --shift-by -10 --topic binlog_db_10_adData_ad_heat:0 --execute

./kafka/bin/kafka-consumer-groups.sh --bootstrap-server kafka-00.ag.awsor:9092 --group ag_web_heat --reset-offsets --to-latest --all-topics --execute


----
# 本地

./bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group common --reset-offsets --to-latest --all-topics --execute


./bin/kafka-consumer-groups.sh --describe --bootstrap-server localhost:9092 --group common


## 命令行消费信息

./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic addata.ad_heat --from-beginning

./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic addata.ad_heat  --max-messages 1

./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic addata.ad_heat --offset latest --partition 0 

./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic addata.ad_heat --offset latest --partition 0 --max-messages 1 


----

# 国内

## 重置
./kafka/bin/kafka-consumer-groups.sh --bootstrap-server 172.19.33.10:9092 --group ag_ec_sync_product_qs --reset-offsets --to-latest --all-topics --execute

## 描述
~/kafka/bin/kafka-consumer-groups.sh --describe --bootstrap-server 172.19.33.10:9092 --group ag_ec_sync_product_qs

## 消费消息
~/kafka/bin/kafka-console-consumer.sh --bootstrap-server 172.19.33.10:9092 --topic binlog-db10-ecData-product-qs-growth --from-beginning

~/kafka/bin/kafka-console-consumer.sh --bootstrap-server 172.19.33.10:9092 --topic binlog-db10-ecData-product-qs-growth --max-messages 10


## 偏移
./bin/kafka-consumer-groups.sh --bootstrap-server 172.19.33.10:9092 --group common --reset-offsets --shift-by -10 --topic binlog-db40-adData-ad-heat:0 --execute


