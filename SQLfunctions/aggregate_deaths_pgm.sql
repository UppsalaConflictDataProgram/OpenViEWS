
CREATE OR REPLACE FUNCTION public.aggregate_deaths_on_date_end (priogrid bigint, month_id BIGINT, count bool, high bool, lags int, type_of_violence integer)
  RETURNS INTEGER AS
  $$
  DECLARE query_bit text := 'SELECT ';
  DECLARE calculatedres integer;
  BEGIN
  IF count THEN query_bit := query_bit || 'count(*)::integer';
  ELSEIF high THEN query_bit := query_bit || 'sum(high)::integer';
  ELSE query_bit := query_bit || 'sum(best)::integer';
  END IF;
  query_bit := query_bit || ' FROM preflight.ged_attached WHERE month_id_end='||month_id||' AND type_of_violence='||type_of_violence;
  IF lags=0 THEN
    query_bit := query_bit || ' AND priogrid_gid = ' || priogrid;
  END IF;
  IF lags=1 THEN
    query_bit := query_bit || ' AND priogrid_gid in (' || priogrid-1 ||','|| priogrid+1 ||','|| priogrid+720 ||','|| priogrid+721 ||','|| priogrid+719 ||','|| priogrid-721 ||','|| priogrid-720 ||','|| priogrid-719 || ')';
  END IF;
  IF lags=2 THEN
    query_bit := query_bit || ' AND priogrid_gid in (' || priogrid-2 ||','|| priogrid+2 ||','|| priogrid+722 ||','|| priogrid+718 ||','|| priogrid-722 ||','|| priogrid-718 ||','|| priogrid-1442 ||','|| priogrid+1442 ||','|| priogrid-1441 ||','|| priogrid+1441 ||','|| priogrid-1440 ||','|| priogrid+1440 ||','|| priogrid-1439 ||','|| priogrid+1439 ||','|| priogrid-1438 ||','|| priogrid+1438 || ')';
  END IF;
  EXECUTE query_bit INTO calculatedres;
  RETURN COALESCE(calculatedres,0)::integer;
  END;
  $$
  LANGUAGE 'plpgsql' IMMUTABLE;



CREATE OR REPLACE FUNCTION public.aggregate_deaths_on_date_start (priogrid bigint, month_id BIGINT, count bool, high bool, lags int, type_of_violence integer)
  RETURNS INTEGER AS
  $$
  DECLARE query_bit text := 'SELECT ';
  DECLARE calculatedres integer;
  BEGIN
  IF count THEN query_bit := query_bit || 'count(*)::integer';
  ELSEIF high THEN query_bit := query_bit || 'sum(high)::integer';
  ELSE query_bit := query_bit || 'sum(best)::integer';
  END IF;
  query_bit := query_bit || ' FROM preflight.ged_attached WHERE month_id_start='||month_id||' AND type_of_violence='||type_of_violence;
  IF lags=0 THEN
    query_bit := query_bit || ' AND priogrid_gid = ' || priogrid;
  END IF;
  IF lags=1 THEN
    query_bit := query_bit || ' AND priogrid_gid in (' || priogrid-1 ||','|| priogrid+1 ||','|| priogrid+720 ||','|| priogrid+721 ||','|| priogrid+719 ||','|| priogrid-721 ||','|| priogrid-720 ||','|| priogrid-719 || ')';
  END IF;
  IF lags=2 THEN
    query_bit := query_bit || ' AND priogrid_gid in (' || priogrid-2 ||','|| priogrid+2 ||','|| priogrid+722 ||','|| priogrid+718 ||','|| priogrid-722 ||','|| priogrid-718 ||','|| priogrid-1442 ||','|| priogrid+1442 ||','|| priogrid-1441 ||','|| priogrid+1441 ||','|| priogrid-1440 ||','|| priogrid+1440 ||','|| priogrid-1439 ||','|| priogrid+1439 ||','|| priogrid-1438 ||','|| priogrid+1438 || ')';
  END IF;
  EXECUTE query_bit INTO calculatedres;
  RETURN COALESCE(calculatedres,0)::integer;
  END;
  $$
  LANGUAGE 'plpgsql' IMMUTABLE;
