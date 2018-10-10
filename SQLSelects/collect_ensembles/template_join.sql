
FROM
    landed.sb_ensemble_TIME_pgm AS sb
INNER JOIN
    landed.ns_ensemble_TIME_pgm AS ns
ON
    sb.pg_id=ns.pg_id
AND
    sb.month_id=ns.month_id
INNER JOIN
    landed.os_ensemble_TIME_pgm AS os
ON
    sb.pg_id=os.pg_id
AND
    sb.month_id=os.month_id
INNER JOIN 
    landed.ebma_TIME_pgm AS ebma
ON
    sb.pg_id=ebma.pg_id
AND
    sb.month_id=ebma.month_id
;