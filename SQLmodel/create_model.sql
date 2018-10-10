CREATE TABLE "staging"."year" (
"year" int4 NOT NULL,
PRIMARY KEY ("year") 
)
WITHOUT OIDS;

CREATE TABLE "staging"."month" (
"id" serial8 NOT NULL,
"month" int4 NOT NULL,
"year_id" int4,
PRIMARY KEY ("id") 
)
WITHOUT OIDS;

CREATE TABLE "staging"."priogrid" (
"gid" int8 NOT NULL,
"col" int4,
"row" int4,
"latitude" numeric(6,2),
"longitude" numeric(6,2),
"geom" public.geometry(polygon,4326),
PRIMARY KEY ("gid") 
)
WITHOUT OIDS;

CREATE TABLE "staging"."priogrid_year" (
"id" serial8 NOT NULL,
"priogrid_gid" int8 NOT NULL,
"year_id" int8 NOT NULL,
"country_year_id" int8,
PRIMARY KEY ("id") 
)
WITHOUT OIDS;

CREATE TABLE "staging"."priogrid_month" (
"id" serial8 NOT NULL,
"priogrid_gid" int8,
"month_id" int8,
"country_month_id" int8,
PRIMARY KEY ("id") 
)
WITHOUT OIDS;

CREATE TABLE "staging"."country" (
"id" serial8 NOT NULL,
"gwno" int8,
"name" varchar(999),
"isocode" varchar(999),
"geom" public.geometry(polygon,4326),
PRIMARY KEY ("id") 
)
WITHOUT OIDS;

CREATE TABLE "staging"."country_year" (
"id" serial8 NOT NULL,
"year_id" int8,
"country_id" int8,
PRIMARY KEY ("id") 
)
WITHOUT OIDS;

CREATE TABLE "staging"."country_month" (
"id" serial8 NOT NULL,
"month_id" int8,
"country_id" int8,
PRIMARY KEY ("id") 
)
WITHOUT OIDS;


ALTER TABLE "staging"."month" ADD CONSTRAINT "year_year_fk" FOREIGN KEY ("year_id") REFERENCES "staging"."year" ("year") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."priogrid_year" ADD CONSTRAINT "priogrid_gid_fk" FOREIGN KEY ("priogrid_gid") REFERENCES "staging"."priogrid" ("gid") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."priogrid_year" ADD CONSTRAINT "year_year_fk" FOREIGN KEY ("year_id") REFERENCES "staging"."year" ("year") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."priogrid_month" ADD CONSTRAINT "priogrid_gid_fk" FOREIGN KEY ("priogrid_gid") REFERENCES "staging"."priogrid" ("gid") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."priogrid_month" ADD CONSTRAINT "month_id_fk" FOREIGN KEY ("month_id") REFERENCES "staging"."month" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."country_year" ADD CONSTRAINT "country_id_fk" FOREIGN KEY ("country_id") REFERENCES "staging"."country" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."country_year" ADD CONSTRAINT "year_year_fk" FOREIGN KEY ("year_id") REFERENCES "staging"."year" ("year") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."priogrid_year" ADD CONSTRAINT "country_year_id_fk" FOREIGN KEY ("country_year_id") REFERENCES "staging"."country_year" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."country_month" ADD CONSTRAINT "month_id_fk" FOREIGN KEY ("month_id") REFERENCES "staging"."month" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."country_month" ADD CONSTRAINT "country_id_fk" FOREIGN KEY ("country_id") REFERENCES "staging"."country" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."priogrid_month" ADD CONSTRAINT "country_month_id_fk" FOREIGN KEY ("country_month_id") REFERENCES "staging"."country_month" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
