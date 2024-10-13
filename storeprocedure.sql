CREATE OR REPLACE PROCEDURE public.unload_all_to_s3()
LANGUAGE plpgsql
AS $$

DECLARE
list RECORD;
sql text;
unload_query varchar(65000);
s3_path VARCHAR(1000);
tablename VARCHAR(100);
starttime datetime;
endtime datetime;
newestRecord datetime;

BEGIN
FOR list IN
SELECT table_schema,
table_name
FROM information_schema.TABLES
WHERE table_type='BASE TABLE'
AND table_schema = 'public' - Since your schema is public
LOOP
sql := 'SELECT * FROM ' || list.table_schema || '.' || list.table_name;
 Start unloading the data
unload_query := 'unload (''' || sql || ''') to
''s3://spinbound/folderredshift/' || list.table_name || '_''
iam_role ''arn:aws:iam::971422673409:role/ReadRedshift''
CSV
HEADER
ALLOWOVERWRITE
PARALLEL OFF ';

EXECUTE unload_query;
END LOOP;
RAISE info: 'Completed sync to S3';
END;
$$;

CALL public.unload_all_to_s3();
