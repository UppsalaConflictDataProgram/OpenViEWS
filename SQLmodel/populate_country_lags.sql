-- creates a table of country spatial lags (i.e. neighboring countries to one another).
-- a neighbor is defined as a country located at <0.1 dec. degrees distance using cshapes geometry.

CREATE INDEX country_gidx ON staging.country USING GIST(geom);

DROP TABLE IF EXISTS staging.country_spatial_lag;
CREATE TABLE staging.country_spatial_lag AS
SELECT a.id as country_id_a, b.id as country_id_b FROM
  staging.country a, staging.country b
WHERE
  a.id<>b.id AND
  a.geom && b.geom AND
  st_distance(a.geom, b.geom) < 0.1;
