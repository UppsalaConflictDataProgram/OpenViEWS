-- generate dummy that is true if i is greater or equal to threshold

CREATE OR REPLACE FUNCTION public.to_dummy_threshold(i bigint, threshold int) RETURNS int AS
$$
BEGIN
IF i>=threshold THEN RETURN 1;
ELSE RETURN 0;
END IF;
end
$$
LANGUAGE 'plpgsql' RETURNS NULL ON NULL INPUT IMMUTABLE;