CREATE OR REPLACE FUNCTION
  public.interpolate_priogrid_year(schema_name VARCHAR(200), table_name VARCHAR(200), variable_name VARCHAR(200), priogrid_in BIGINT, year_in BIGINT)
RETURNS DOUBLE PRECISION AS
  -- This MUST to be run on indexed tables with the main index on priogrid_gid, year_in.
  -- Otherwise it takes a few years to run.
  -- Expects the standard priogrid_year table format using year and priogrid_gid.
  $$
  DECLARE scratch_query text;
  DECLARE prev_filled_year int;
  DECLARE prev_value DOUBLE PRECISION;
  DECLARE next_filled_year int;
  DECLARE extrapolated_year int;
  DECLARE next_value DOUBLE PRECISION;
  DECLARE return_value DOUBLE PRECISION;
  DECLARE rate DOUBLE PRECISION;
  BEGIN
  scratch_query := format ('SELECT year,%I::DOUBLE PRECISION FROM %I.%I WHERE %I IS NOT NULL AND gid=%s AND year<=%s ORDER BY year DESC LIMIT 1',variable_name,schema_name,table_name,variable_name,priogrid_in,year_in);
	EXECUTE scratch_query INTO prev_filled_year,prev_value;
	scratch_query := format ('SELECT year,%I::DOUBLE PRECISION FROM %I.%I WHERE %I IS NOT NULL AND gid=%s AND year>=%s ORDER BY year ASC LIMIT 1',variable_name,schema_name,table_name,variable_name,priogrid_in,year_in);
  EXECUTE scratch_query INTO next_filled_year,next_value;

  IF prev_filled_year = next_filled_year THEN
      -- we're at a cell with actual values. Don't interpolate; just take the value.
      scratch_query := format ('SELECT %I::DOUBLE PRECISION FROM %I.%I WHERE gid=%s AND year=%s',variable_name,schema_name,table_name,priogrid_in,year_in);
      EXECUTE scratch_query INTO return_value;
      RETURN return_value;
  END IF;

  IF prev_filled_year IS NOT NULL AND next_filled_year IS NOT NULL THEN
      -- we're between two values, so interpolate
      rate := (next_value-prev_value)/(next_filled_year-prev_filled_year);
      return_value := prev_value+(rate*(year_in-prev_filled_year));
      RETURN return_value;
  END IF;

  IF prev_filled_year IS NULL AND next_filled_year IS NOT NULL THEN
      -- we're at the bottom of the time series. Extrapolate down.
      scratch_query := format('SELECT %I::DOUBLE PRECISION FROM %I.%I WHERE gid=%s AND year=%s',variable_name,schema_name,table_name,priogrid_in,next_filled_year);
      EXECUTE scratch_query INTO prev_value;
      scratch_query := format('SELECT year, %I::DOUBLE PRECISION FROM %I.%I WHERE %I IS NOT NULL AND gid=%s AND year>%s ORDER BY year ASC LIMIT 1',variable_name,schema_name,table_name,variable_name,priogrid_in,next_filled_year);
      EXECUTE scratch_query INTO extrapolated_year,next_value;
      rate := (next_value-prev_value)/(extrapolated_year-next_filled_year);
      return_value := prev_value - (rate*(next_filled_year-year_in));
      RETURN return_value;
  END IF;

  IF prev_filled_year IS NOT NULL AND next_filled_year IS NULL THEN
      -- we're at the top of the time series. Extrapolate up.
      scratch_query := format('SELECT %I::DOUBLE PRECISION FROM %I.%I WHERE gid=%s AND year=%s',variable_name,schema_name,table_name,priogrid_in,prev_filled_year);
      EXECUTE scratch_query INTO next_value;
      scratch_query := format('SELECT year, %I::DOUBLE PRECISION FROM %I.%I WHERE %I IS NOT NULL AND gid=%s AND year<%s ORDER BY year DESC LIMIT 1',variable_name,schema_name,table_name,variable_name,priogrid_in,prev_filled_year);
      EXECUTE scratch_query INTO extrapolated_year,prev_value;
      rate := (next_value-prev_value)/(prev_filled_year-extrapolated_year);
      return_value := next_value + (rate*(year_in-prev_filled_year));
      RETURN return_value;
  END IF;

  IF prev_filled_year IS NULL AND next_filled_year IS NULL THEN
    -- empty field? Do nothing.
    RETURN NULL;
  END IF;
  END;
  $$
LANGUAGE 'plpgsql' IMMUTABLE;
