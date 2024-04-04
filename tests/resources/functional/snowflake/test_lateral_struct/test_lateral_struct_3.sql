
-- snowflake sql:
SELECT d.value:display_position::NUMBER as item_card_impression_display_position,
                                   i.value:impression_attributes::VARCHAR as item_card_impression_impression_attributes,
                                   cast(current_timestamp() as timestamp_ntz(9)) as dwh_created_date_time_utc,
                                   i.value:propensity::FLOAT as propensity,
                                   candidates
                                 FROM dwh.vw_replacement_customer  d,
                                 LATERAL FLATTEN (INPUT => d.item_card_impressions, OUTER => TRUE) i
                                 WHERE event_date_pt = '{start_date}' and event_name in ('store.replacements_view');

-- databricks sql:
SELECT
                      CAST(d.value.display_position AS DECIMAL(38, 0)) AS item_card_impression_display_position,
                      CAST(i.impression_attributes AS STRING) AS item_card_impression_impression_attributes,
                      CAST(CURRENT_TIMESTAMP() AS TIMESTAMP) AS dwh_created_date_time_utc,
                      CAST(i.propensity AS DOUBLE) AS propensity, candidates
               FROM dwh.vw_replacement_customer AS d LATERAL VIEW OUTER EXPLODE(d.item_card_impressions) AS i
               WHERE event_date_pt = '{start_date}' AND event_name IN ('store.replacements_view');
