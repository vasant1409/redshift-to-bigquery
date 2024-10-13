import os
from google.cloud import bigquery
from google.cloud import storage
import functions_framework

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    # Get data from the event
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    # Extract bucket and file name from the event data
    bucket_name = data["bucket"]
    file_name = data["name"]

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    # Log event details
    print(f"Processing file: {file_name} in bucket: {bucket_name}")

    # Initialize BigQuery client
    client = bigquery.Client()
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # Hardcoded dataset_id and project_id
    dataset_id = 'bq_stereo'
    project_id = 'cloudside-academy'

    # List all files in the bucket
    blobs = bucket.list_blobs()

    for blob in blobs:
        file_name = blob.name

        # Check if the file is in CSV or compressed CSV format and starts with 'awstogcs'
        if file_name.startswith('awstogcs'):
            # Extract table name from the file path, ensure valid parsing
            parts = file_name.split('/')
            if len(parts) > 1 and '_' in parts[1]:
                table_name = parts[1].split('_')[0]  # Adjust based on your file naming
            else:
                print(f"Invalid file naming structure for file {file_name}. Skipping.")
                continue

            print(f"Tablename: {table_name}")
            table_id = f"{project_id}.{dataset_id}.{table_name}"

            # Construct the GCS URI for the file
            uri = f'gs://{bucket_name}/{file_name}'

            # Configure the load job settings
            job_config = bigquery.LoadJobConfig(
               # source_format=bigquery.SourceFormat.CSV,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Changed to append to avoid truncation
                skip_leading_rows=1,  # Assuming the first row is headers
                autodetect=True,  # Let BigQuery infer the schema
                max_bad_records=10,  # Allow up to 10 bad records
                ignore_unknown_values=True  # Ignore extra columns not in schema
            )

            # Ensure table_id is valid before loading data
                # Load data into BigQuery table from GCS URI
            load_job = client.load_table_from_uri(
                uri,
                table_id,
                job_config=job_config
            )

            # Wait for the load job to complete
            load_job.result()

            print(f"File {file_name} successfully loaded into table {table_id}.")
        else:
            print(f"File {file_name} is not a CSV or gzipped CSV file. Skipping.")
