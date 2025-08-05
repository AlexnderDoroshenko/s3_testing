import os
import pytest


BUCKET = "test-bucket"
OBJECT = "test-object.txt"
CONTENT = b"Hello, S3!"

def test_create_bucket(s3_client):
    """
    Create a bucket and verify it appears in the bucket list.
    """
    s3_client.create_bucket(BUCKET)
    buckets = [b['Name'] for b in s3_client.list_buckets()]
    assert BUCKET in buckets, f"Bucket '{BUCKET}' was not found after creation."

def test_upload_file(s3_client, tmp_path):
    """
    Upload a file to the bucket and verify it appears in the object list.
    """
    s3_client.create_bucket(BUCKET)
    file_path = tmp_path / OBJECT
    file_path.write_bytes(CONTENT)
    s3_client.upload_file(BUCKET, str(file_path), OBJECT)
    objects = [o['Key'] for o in s3_client.list_objects(BUCKET)]
    assert OBJECT in objects, f"Object '{OBJECT}' was not found after upload."

def test_get_object(s3_client, tmp_path):
    """
    Upload a file and verify its content can be retrieved.
    """
    s3_client.create_bucket(BUCKET)
    file_path = tmp_path / OBJECT
    file_path.write_bytes(CONTENT)
    s3_client.upload_file(BUCKET, str(file_path), OBJECT)
    data = s3_client.get_object(BUCKET, OBJECT)
    assert data == CONTENT, f"Downloaded content does not match uploaded content for '{OBJECT}'."

def test_download_file(s3_client, tmp_path):
    """
    Upload a file and verify it can be downloaded with correct content.
    """
    s3_client.create_bucket(BUCKET)
    file_path = tmp_path / OBJECT
    file_path.write_bytes(CONTENT)
    s3_client.upload_file(BUCKET, str(file_path), OBJECT)
    download_path = tmp_path / f"downloaded_{OBJECT}"
    s3_client.download_file(BUCKET, OBJECT, str(download_path))
    assert download_path.read_bytes() == CONTENT, f"Downloaded file content does not match for '{OBJECT}'."

def test_delete_object(s3_client, tmp_path):
    """
    Upload and delete an object, then verify it is removed from the bucket.
    """
    s3_client.create_bucket(BUCKET)
    file_path = tmp_path / OBJECT
    file_path.write_bytes(CONTENT)
    s3_client.upload_file(BUCKET, str(file_path), OBJECT)
    s3_client.delete_object(BUCKET, OBJECT)
    objects = [o['Key'] for o in s3_client.list_objects(BUCKET)]
    assert OBJECT not in objects, f"Object '{OBJECT}' was found after deletion."

def test_delete_bucket(s3_client):
    """
    Create and delete a bucket, then verify it is removed from the bucket list.
    """
    s3_client.create_bucket(BUCKET)
    s3_client.delete_bucket(BUCKET)
    buckets = [b['Name'] for b in s3_client.list_buckets()]
    assert BUCKET not in buckets, f"Bucket '{BUCKET}' was found after deletion."
