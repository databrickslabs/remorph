-- bigquery sql:
SELECT
  FORMAT_DATE("%A", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS full_weekday_name,
  FORMAT_DATE("%a", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS abbreviated_weekday_name,
  FORMAT_DATE("%B", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS full_month_name,
  FORMAT_DATE("%b", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS abbreviated_month_name,
  FORMAT_DATE("%C", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS century,
  FORMAT_DATE("%c", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS date_time_representation,
  FORMAT_DATE("%D", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS date_mm_dd_yy,
  FORMAT_DATE("%d", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS day_of_month_two_digits,
  FORMAT_DATE("%e", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS day_of_month_single_digit,
  FORMAT_DATE("%F", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS iso_8601_date,
  FORMAT_DATE("%H", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS hour_24,
  FORMAT_DATE("%h", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS abbreviated_month_name_duplicate,
  FORMAT_DATE("%I", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS hour_12,
  FORMAT_DATE("%j", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS day_of_year,
  FORMAT_DATE("%k", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS hour_24_no_leading_zero,
  FORMAT_DATE("%l", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS hour_12_no_leading_zero,
  FORMAT_DATE("%M", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS minutes,
  FORMAT_DATE("%m", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS month_2_digits,
  FORMAT_DATE("%P", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS am_pm_lowercase,
  FORMAT_DATE("%p", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS am_pm_uppercase,
  FORMAT_DATE("%Q", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS quarter,
  FORMAT_DATE("%R", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS time_hh_mm,
  FORMAT_DATE("%S", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS seconds,
  FORMAT_DATE("%s", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS ephoc_seconds,
  FORMAT_DATE("%T", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS time_hh_mm_ss,
  FORMAT_DATE("%u", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS iso_weekday_monday_start,
  FORMAT_DATE("%V", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS iso_week_number,
  FORMAT_DATE("%w", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS weekday_sunday_start,
  FORMAT_DATE("%X", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS time_representation,
  FORMAT_DATE("%x", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS date_representation,
  FORMAT_DATE("%Y", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS year_with_century,
  FORMAT_DATE("%y", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS year_without_century,
  FORMAT_DATE("%Z", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS time_zone_name,
  FORMAT_DATE("%Ez", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS rfc3339_time_zone,
  FORMAT_DATE("%E*S", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS seconds_with_full_fractional,
  FORMAT_DATE("%E4Y", TIMESTAMP("2008-12-28 16:44:12.277404 UTC")) AS four_character_years;

-- databricks sql:
SELECT
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'EEEE') AS full_weekday_name,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'EEE') AS abbreviated_weekday_name,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'MMMM') AS full_month_name,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'MMM') AS abbreviated_month_name,
  ROUND(EXTRACT(YEAR FROM TIMESTAMP('2008-12-28 16:44:12.277404 UTC')) / 100) AS century,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'EEE MMM dd HH:mm:ss yyyy') AS date_time_representation,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'MM/dd/yy') AS date_mm_dd_yy,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'dd') AS day_of_month_two_digits,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'd') AS day_of_month_single_digit,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'yyyy-MM-dd') AS iso_8601_date,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'HH') AS hour_24,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'MMM') AS abbreviated_month_name_duplicate,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'hh') AS hour_12,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'DDD') AS day_of_year,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'H') AS hour_24_no_leading_zero,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'h') AS hour_12_no_leading_zero,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'mm') AS minutes,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'MM') AS month_2_digits,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'a') AS am_pm_lowercase,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'a') AS am_pm_uppercase,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'q') AS quarter,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'HH:mm') AS time_hh_mm,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'ss') AS seconds,
  UNIX_TIMESTAMP(TIMESTAMP('2008-12-28 16:44:12.277404 UTC')) AS ephoc_seconds,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'HH:mm:ss') AS time_hh_mm_ss,
  EXTRACT(DAYOFWEEK_ISO FROM TIMESTAMP('2008-12-28 16:44:12.277404 UTC')) AS iso_weekday_monday_start,
  EXTRACT(W FROM TIMESTAMP('2008-12-28 16:44:12.277404 UTC')) AS iso_week_number,
  EXTRACT(DAYOFWEEK FROM TIMESTAMP('2008-12-28 16:44:12.277404 UTC')) - 1 AS weekday_sunday_start,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'HH:mm:ss') AS time_representation,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'MM/dd/yy') AS date_representation,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'yyyy') AS year_with_century,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'yy') AS year_without_century,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'z') AS time_zone_name,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'xxx') AS rfc3339_time_zone,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'ss.SSSSSS') AS seconds_with_full_fractional,
  DATE_FORMAT(TIMESTAMP('2008-12-28 16:44:12.277404 UTC'), 'yyyy') AS four_character_years;
