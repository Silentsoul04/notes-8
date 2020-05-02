```shell script
$YUGONG_WEB \
-src "$AG_CH_DSN" \
-dst "$DB40_WEB_AD_DSN?parseTime=true&loc=Asia/Shanghai" \


# https://baton-alishh.umlife.net/ui/#/job/edit/yugong/365 的子任务
docker run --rm --cpus=0.5 -m 2g --network host registry.umlife.net:443/adxmi/migo yugong \
-src "clickhouse://default:6t4kRK4S@172.19.30.10:9000/mt" \
-dst "mysql://aso_ro:b77JSf7L4C3jlkI3@db-test.ag.alishh:3306/adData?parseTime=true&loc=Asia/Shanghai" \

$YUGONG_WEB \
-src "$AG_CH_DSN" \
-dst "$DB40_WEB_AD_DSN?parseTime=true&loc=Asia/Shanghai" \
-querydims "select formatDateTime(now(), '%F %T') as now" \
-query "
insert into app_brand_developer (app_id, storefont_type, brand_id, developer_id, modify_time)
on duplicate key update brand_id=VALUES(brand_id), developer_id=VALUES(developer_id), modify_time=VALUES(modify_time)
select campaign_id,   campaign_type,   app_brand_id,   developer_id, '{{now}}' as modify_time
from   ad_aggs_outer where   campaign_id > 0   and campaign_type in (101, 201, 299)
group by campaign_id,   campaign_type,   app_brand_id,   developer_id
;
" \
-after "
delete from app_brand_developer where modify_time < '{{now}}'
"

```