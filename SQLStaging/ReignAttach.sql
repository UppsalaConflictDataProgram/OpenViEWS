-- TODO: Change data type of columns to correct types
-- TODO: Write tests that verify correct insertion of the data with know good
-- TODO: remove the drop table rows before movin to staging from staging_test

-- Reign data attachment script
-- This script attaches the reign dataset to the staging.country_month level

DROP TABLE IF EXISTS staging_test.country_month;
CREATE TABLE staging_test.country_month AS SELECT * FROM staging.country_month;

ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_leader;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_elected;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_age;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_male;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_militarycareer;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_tenure_months;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_government;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_anticipation;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_ref_ant;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_leg_ant;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_exec_ant;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_irreg_lead_ant;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_election_now;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_election_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_leg_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_exec_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_lead_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_ref_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_direct_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_indirect_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_victory_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_defeat_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_change_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_nochange_recent;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_delayed;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_lastelection;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_loss;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_irregular;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_prev_conflict;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_pt_suc;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_pt_attempt;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_precip;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_couprisk;
ALTER TABLE staging_test.country_month DROP COLUMN IF EXISTS rgn_pctile_risk;

ALTER TABLE staging_test.country_month ADD COLUMN rgn_leader varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_elected varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_age varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_male varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_militarycareer varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_tenure_months varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_government varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_anticipation varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_ref_ant varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_leg_ant varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_exec_ant varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_irreg_lead_ant varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_election_now varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_election_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_leg_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_exec_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_lead_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_ref_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_direct_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_indirect_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_victory_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_defeat_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_change_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_nochange_recent varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_delayed varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_lastelection varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_loss varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_irregular varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_prev_conflict varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_pt_suc varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_pt_attempt varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_precip varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_couprisk varchar;
ALTER TABLE staging_test.country_month ADD COLUMN rgn_pctile_risk varchar;



UPDATE staging_test.country_month as cm
  SET
    rgn_leader = subquery.leader,
    rgn_elected = subquery.elected,
    rgn_age = subquery.age,
    rgn_male = subquery.male,
    rgn_militarycareer = subquery.militarycareer,
    rgn_tenure_months = subquery.tenure_months,
    rgn_government = subquery.government,
    rgn_anticipation = subquery.anticipation,
    rgn_ref_ant = subquery.ref_ant,
    rgn_leg_ant = subquery.leg_ant,
    rgn_exec_ant = subquery.exec_ant,
    rgn_irreg_lead_ant = subquery.irreg_lead_ant,
    rgn_election_now = subquery.election_now,
    rgn_election_recent = subquery.election_recent,
    rgn_leg_recent = subquery.leg_recent,
    rgn_exec_recent = subquery.exec_recent,
    rgn_lead_recent = subquery.lead_recent,
    rgn_ref_recent = subquery.ref_recent,
    rgn_direct_recent = subquery.direct_recent,
    rgn_indirect_recent = subquery.indirect_recent,
    rgn_victory_recent = subquery.victory_recent,
    rgn_defeat_recent = subquery.defeat_recent,
    rgn_change_recent = subquery.change_recent,
    rgn_nochange_recent = subquery.nochange_recent,
    rgn_delayed = subquery.delayed,
    rgn_lastelection = subquery.lastelection,
    rgn_loss = subquery.loss,
    rgn_irregular = subquery.irregular,
    rgn_prev_conflict = subquery.prev_conflict,
    rgn_pt_suc = subquery.pt_suc,
    rgn_pt_attempt = subquery.pt_attempt,
    rgn_precip = subquery.precip,
    rgn_couprisk = subquery.couprisk,
    rgn_pctile_risk = subquery.pctile_risk
  FROM (
  SELECT
    cm.country_id,
    cm.month_id,
    data.*
  FROM
  dataprep.reign as data,
  staging.country  as c,
  staging_test.country_month as cm,
  staging.month as m
WHERE
  data.ccode=c.gwcode
  AND c.id=cm.country_id
  AND data.month=m.month
  AND data.year=m.year_id
  AND m.id=cm.month_id) as subquery
WHERE
  subquery.month_id=cm.month_id
  AND subquery.country_id=cm.country_id
;

SELECT * FROM staging_test.country_month
WHERE month_id>390 AND month_id<410
ORDER BY country_id, month_id;
