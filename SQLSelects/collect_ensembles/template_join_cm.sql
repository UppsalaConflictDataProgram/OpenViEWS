
FROM
    landed.sb_ensemble_TIME_cm AS sb
INNER JOIN
    landed.ns_ensemble_TIME_cm AS ns
ON
    sb.country_id=ns.country_id
AND
    sb.month_id=ns.month_id
INNER JOIN
    landed.os_ensemble_TIME_cm AS os
ON
    sb.country_id=os.country_id
AND
    sb.month_id=os.month_id;