-- takes a date and returns the date of the last day in that month
-- example: last_day_month('2012-08-12'::date) -> '2012-08-31'
-- date -> date

CREATE OR REPLACE FUNCTION last_day_month(date) RETURNS date AS
$$
select (date_trunc('month', $1) + interval '1 month -1 day')::date;
$$
LANGUAGE SQL
IMMUTABLE
RETURNS NULL ON NULL INPUT;

--tests
-- SELECT last_day_month('2016-02-01'::date) -> 2016-02-29
-- SELECT last_day_month('2012-08-12'::date) -> 2012-08-31
