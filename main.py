from google.cloud import storage
from decouple import config
import os
import logging

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


class GCPWrapper:
    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name

    def list_of_buckets(self):
        storage_client = storage.Client()
        return list(storage_client.list_buckets())

    def list_files_in_bucket(self):
        storage_client = storage.Client()
        blobs = storage_client.list_blobs(self.bucket_name)
        return [{"name": blob.name, "path": blob.path} for blob in blobs]

    def upload_blob_file_to_bucket(self, destination_path: str, filename: str):
        storage_client = storage.Client()
        bucket_to_use = storage_client.get_bucket(bucket_or_name=self.bucket_name)
        blob = bucket_to_use.blob(f"{destination_path}/{filename}")
        try:
            blob.upload_from_filename(filename=filename)
            return f"The file {filename} has been uploaded successfully!"
        except Exception as e:
            return f"An error: {e}"


if __name__ == "__main__":
    bucket_name = config("BUCKET_NAME")

    obj_gcp = GCPWrapper(bucket_name=bucket_name)

    logging.warning("Listing the buckets")
    obj_gcp.list_of_buckets()

    logging.warning("Listing files in the bucket")
    obj_gcp.list_files_in_bucket()

    logging.warning("Uploading a file to the bucket")
    obj_gcp.upload_blob_file_to_bucket(
        destination_path="test_folder", filename="credentials.json"
    )
