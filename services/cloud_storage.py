import os

from google.cloud import storage

STORAGE_CLIENT = storage.Client()


def upload_bytes_to_gcs(
    bucket_name: str, data: bytes, destination_blob_name: str, content_type: str
):
    bucket = STORAGE_CLIENT.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data, content_type)
    print(f"Uploaded data to gs://{bucket_name}/{destination_blob_name}.")


def download_from_gcs(bucket_name: str, blob_name: str, destination_file_path: str):
    bucket = STORAGE_CLIENT.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.download_to_filename(destination_file_path)
    print(f"Downloaded gs://{bucket_name}/{blob_name} to {destination_file_path}.")


def get_files_name(bucket_name: str, folder_name: str):
    bucket = STORAGE_CLIENT.bucket(bucket_name)
    prefix = folder_name + "/"
    files = bucket.list_blobs(prefix=prefix)
    # file名のみ取得する
    files_name = [os.path.basename(file.name) for file in files]
    return files_name
