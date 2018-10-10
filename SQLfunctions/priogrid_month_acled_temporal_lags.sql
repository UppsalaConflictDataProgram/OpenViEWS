create or replace function make_priogrid_month_acled_temporal_lags(months integer, make_columns boolean, lower_month_bound integer, higher_month_bound integer) returns void
LANGUAGE plpgsql
AS $$
DECLARE query text;
BEGIN

IF make_columns THEN

query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_sb_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_ns_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_os_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_pr_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_prp_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_prr_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_prx_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_pry_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_sb_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_ns_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_os_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_pr_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_prp_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_prr_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_prx_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_pry_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_sb_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_ns_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_os_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_prp_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_prr_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_prx_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_pry_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_sb_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_ns_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_os_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_pr_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_prp_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_prr_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_prx_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_pry_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_sb_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_ns_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_os_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_pr_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_prp_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_prr_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_prx_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_count_pry_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_sb_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_ns_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_os_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_pr_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_prp_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_prr_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_prx_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS acled_fat_pry_lag2_tlag%s ;',months); EXECUTE(query);

query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_sb_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_ns_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_os_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_pr_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_prp_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_prr_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_prx_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_pry_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_sb_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_ns_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_os_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_pr_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_prp_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_prr_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_prx_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_pry_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_sb_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_ns_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_os_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_pr_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_prp_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_prr_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_prx_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_pry_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_sb_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_ns_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_os_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_pr_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_prp_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_prr_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_prx_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_pry_lag1_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_sb_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_ns_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_os_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_pr_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_prp_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_prr_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_prx_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_pry_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_sb_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_ns_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_os_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_pr_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_prp_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_prr_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_prx_lag2_tlag%s INT;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_pry_lag2_tlag%s INT;',months); EXECUTE(query);

END IF;

query:=format('UPDATE staging.priogrid_month SET
acled_count_sb_tlag%1$s = a.acled_count_sb,
acled_count_ns_tlag%1$s = a.acled_count_ns,
acled_count_os_tlag%1$s = a.acled_count_os,
acled_count_pr_tlag%1$s = a.acled_count_pr,
acled_count_prp_tlag%1$s = a.acled_count_prp,
acled_count_prr_tlag%1$s = a.acled_count_prr,
acled_count_prx_tlag%1$s = a.acled_count_prx,
acled_count_pry_tlag%1$s = a.acled_count_pry,
acled_fat_sb_tlag%1$s = a.acled_fat_sb,
acled_fat_ns_tlag%1$s = a.acled_fat_ns,
acled_fat_os_tlag%1$s = a.acled_fat_os,
acled_fat_pr_tlag%1$s = a.acled_fat_pr,
acled_fat_prp_tlag%1$s = a.acled_fat_prp,
acled_fat_prr_tlag%1$s = a.acled_fat_prr,
acled_fat_prx_tlag%1$s = a.acled_fat_prx,
acled_fat_pry_tlag%1$s = a.acled_fat_pry,
acled_count_sb_lag1_tlag%1$s = a.acled_count_sb_lag1,
acled_count_ns_lag1_tlag%1$s = a.acled_count_ns_lag1,
acled_count_os_lag1_tlag%1$s = a.acled_count_os_lag1,
acled_count_pr_lag1_tlag%1$s = a.acled_count_pr_lag1,
acled_count_prp_lag1_tlag%1$s = a.acled_count_prp_lag1,
acled_count_prr_lag1_tlag%1$s = a.acled_count_prr_lag1,
acled_count_prx_lag1_tlag%1$s = a.acled_count_prx_lag1,
acled_count_pry_lag1_tlag%1$s = a.acled_count_pry_lag1,
acled_fat_sb_lag1_tlag%1$s = a.acled_fat_sb_lag1,
acled_fat_ns_lag1_tlag%1$s = a.acled_fat_ns_lag1,
acled_fat_os_lag1_tlag%1$s = a.acled_fat_os_lag1,
acled_fat_pr_lag1_tlag%1$s = a.acled_fat_pr_lag1,
acled_fat_prp_lag1_tlag%1$s = a.acled_fat_prp_lag1,
acled_fat_prr_lag1_tlag%1$s = a.acled_fat_prr_lag1,
acled_fat_prx_lag1_tlag%1$s = a.acled_fat_prx_lag1,
acled_fat_pry_lag1_tlag%1$s = a.acled_fat_pry_lag1,
acled_count_sb_lag2_tlag%1$s = a.acled_count_sb_lag2,
acled_count_ns_lag2_tlag%1$s = a.acled_count_ns_lag2,
acled_count_os_lag2_tlag%1$s = a.acled_count_os_lag2,
acled_count_pr_lag2_tlag%1$s = a.acled_count_pr_lag2,
acled_count_prp_lag2_tlag%1$s = a.acled_count_prp_lag2,
acled_count_prr_lag2_tlag%1$s = a.acled_count_prr_lag2,
acled_count_prx_lag2_tlag%1$s = a.acled_count_prx_lag2,
acled_count_pry_lag2_tlag%1$s = a.acled_count_pry_lag2,
acled_fat_sb_lag2_tlag%1$s = a.acled_fat_sb_lag2,
acled_fat_ns_lag2_tlag%1$s = a.acled_fat_ns_lag2,
acled_fat_os_lag2_tlag%1$s = a.acled_fat_os_lag2,
acled_fat_pr_lag2_tlag%1$s = a.acled_fat_pr_lag2,
acled_fat_prp_lag2_tlag%1$s = a.acled_fat_prp_lag2
acled_fat_prr_lag2_tlag%1$s = a.acled_fat_prr_lag2
acled_fat_prx_lag2_tlag%1$s = a.acled_fat_prx_lag2
acled_fat_pry_lag2_tlag%1$s = a.acled_fat_pry_lag2
FROM staging.priogrid_month a
WHERE
(
staging.priogrid_month.month_id = a.month_id+%1$s
AND
staging.priogrid_month.priogrid_gid = a.priogrid_gid
AND
staging.priogrid_month.month_id BETWEEN  %2$s AND %3$s
AND
a.month_id BETWEEN %2$s-12 AND %3$s);',months, lower_month_bound, higher_month_bound);
EXECUTE(query);
END;
$$;
