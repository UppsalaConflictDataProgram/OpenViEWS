-- takes a latitude and longitude (float) and returns a PrioGRID code.
-- (float, float) -> int

CREATE OR REPLACE FUNCTION priogrid(float, float) RETURNS integer AS
'SELECT ((((90 + (floor($1*2)/2))*2)::int+1)-1)*720 + ((180+(floor($2*2)/2))*2)::int + 1;'
LANGUAGE SQL
IMMUTABLE
RETURNS NULL ON NULL INPUT;

-- tests
--
-- SELECT priogrid (-1.4,120.75);  --128042
-- SELECT priogrid (-10, -76); --115409
-- SELECT priogrid (-1.16, -71.5); --127658
-- SELECT priogrid (5.55, 95.31); --138071
-- SELECT priogrid (9, -75); --142771
-- SELECT priogrid (1.2, -77.41); --131246
