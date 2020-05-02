```shell script
# 同步ad_aggs到CH供web查询, https://baton-alishh.umlife.net/ui/#/job/edit/ag_web/175 的子任务
$YUGONG_WEB \
-dim "$DB41_AD_DSN" \
-src "$DB41_AD_DSN" \
-dst "$AG_CH_DSN" \
-querydims "select distinct ad_year_month from ad_aggs_outer where modify_time > curdate() order by ad_year_month" \
-prepare "alter table ad_aggs_outer_shadow drop partition {{.ad_year_month}}" \
-query "
insert into ad_aggs_outer_shadow
select ad_id,platform,ad_year_month,ad_format,media_id,channel_id,purpose,material_type,campaign_type,campaign_id,app_brand_id,developer_id,genres,style_app,style_game,brand_id,budget,ad_month,first_date, last_date,UNIX_TIMESTAMP(ad_aggs_outer.modify_time) as modify_time
from ad_aggs_outer where ad_year_month={{.ad_year_month}}
" \
-after "ALTER TABLE ad_aggs_outer REPLACE PARTITION {{.ad_year_month}} FROM ad_aggs_outer_shadow" \
-after "ALTER TABLE ad_aggs_outer_shadow drop partition {{.ad_year_month}}" 

# after 的select操作是查src库的\
#-after "select round(sum(modify_time>today())/count(1), 3) as change_ratio, count(1) from ad_aggs_outer where ad_year_month={{.ad_year_month}}"
```