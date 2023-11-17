from google.cloud import storage
import os
import logging

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

def list_of_buckets():
    storage_client = storage.Client()
    return list(storage_client.list_buckets())

def list_files_in_bucket(bucket_name: str):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)
    return [{"name": blob.name, "path": blob.path} for blob in blobs]

def upload_blob_file_to_bucket(bucket_name: str, destination_path: str, filename: str):
    storage_client = storage.Client()
    bucket_to_use = storage_client.get_bucket(bucket_or_name=bucket_name)
    blob = bucket_to_use.blob(f"{destination_path}/{filename}")
    try:
        blob.upload_from_filename(filename=filename)
        return f"The file {filename} has been uploaded successfully!"
    except Exception as e:
        return f"An error: {e}"
