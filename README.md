Batch loading from Redshift to Bigquery

Tools & services utilized:
AWS Redshift cluster
AWS S3 bucket
Job transfer service
GCP cloud storage
GCP Cloud functions
GCP Bigquery

Redshift
	Amazon Redshift is a fully managed, petabyte-scale data warehouse service in the cloud. Amazon Redshift Serverless lets you access and analyze data without all of the configurations of a provisioned data warehouse. 

At Cloudside, we have migrated hundreds of customers from various data warehouses to BigQuery. In this post, I will walk you through one of the migrations I have been part of — Redshift to BigQuery. The steps outlined below ensure smoother data migration from Redshift and S3 to BigQuery, with minimal manual intervention.

To follow along with this guide, I assume you already have a Redshift cluster, so we will start with creation of a stored procedure that iterates through all the existing tables and unloads data to S3
''
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
''
CALL public.unload_all_to_s3();
Transfer Files from S3 to Google Cloud Storage (GCS)
Once the data has been exported to S3, the next step is to transfer it to GCP using a Transfer Job service.

Set up the GCP Transfer Service to move the files from the S3 bucket to a GCS bucket.
The transfer service can be automated or scheduled to ensure timely data migration.
The Job Transfer service need Access ID and secret key to transfer files; we can set it in security credentials in AWS console.
The below procedure will help to create access_key:

aws_console > user_profile > security_credentials > create_access_key

Set Up Cloud Functions to Load Data into Bigquery
With the files now in GCS, the next step is to load them into Bigquery. To automate this process, create a cloud function:

This function will be triggered whenever new files are uploaded to the GCS bucket.
The function should contain a Python script that reads the files from GCS and inserts the data into the desired Bigquery dataset.

Explanation for the trigger used:

Event name: Object finalized

Event type: google.cloud.storage.object.v1.finalized

Description: Occurs when a new object is created or an existing object is overwritten and a new generation of that object is created.

Loading Data into BigQuery
Finally, when the cloud function is triggered, it loads the data from GCS into Bigquery.

The transfer is seamless, and once the data is in Bigquery, you can start querying and analyzing it immediately.
Ensure the function handles potential duplicates or errors during the upload process to maintain data integrity.
Setting the required permissions for Bigquery is listed below:

bigquery.transfers.update
bigquery.datasets.get
bigquery.transfers.update
