```shell script

# https://baton-alishh.umlife.net/ui/#/job/edit/yugong/365 的子任务
$YUGONG_WEB \
-src "$AG_CH_DSN" \
-dst "$DB40_WEB_AD_DSN?parseTime=true&loc=Asia/Shanghai" \
-query "
insert into campaign_record (id, type_id, first_date, last_date, duration)
on duplicate key update first_date=values(first_date), last_date=values(last_date), duration=values(duration)
select 
       id,       
       type_id,
       MIN(first_date) ,
       MAX(last_date),
       SUM(duration)
from
  ( select ad_year_month,
           campaign_id as id,
           campaign_type as type_id ,
           length(bitmaskToArray(groupBitOr(ad_month))) as duration ,
           MIN(first_date) as first_date,
           MAX(last_date) as last_date
   from mt.ad_aggs_outer
   where campaign_id > 0
     and campaign_type > 0
   group by ad_year_month,
            campaign_id,
            campaign_type
   union all select ad_year_month,
                    app_brand_id as id,
                    401 as type_id ,
                    length(bitmaskToArray(groupBitOr(ad_month))) as duration ,
                    MIN(first_date) as first_date,
                    MAX(last_date) as last_date
   from mt.ad_aggs_outer
   where app_brand_id > 0
   group by ad_year_month,
            app_brand_id
   union all select ad_year_month,
                    developer_id as id,
                    501 as type_id ,
                    length(bitmaskToArray(groupBitOr(ad_month))) as duration ,
                    MIN(first_date) as first_date,
                    MAX(last_date) as last_date
   from mt.ad_aggs_outer
   where developer_id > 0
   group by ad_year_month,
            developer_id
   union all select ad_year_month,
                    brand_id as id,
                    400 as type_id ,
                    length(bitmaskToArray(groupBitOr(ad_month))) as duration ,
                    MIN(first_date) as first_date,
                    MAX(last_date) as last_date
   from mt.ad_aggs_outer
   where brand_id > 0
   group by ad_year_month,
            brand_id) t
group by id,
         type_id
" && curl 172.19.33.90:14321/internal/cleanAdAggsCache
```