import os
import pytest

BUCKET = "test-bucket"
OBJECT = "test-object.txt"
CONTENT = b"Hello, S3!"

def test_create_bucket(s3_client):
    s3_client.create_bucket(BUCKET)
    buckets = [b['Name'] for b in s3_client.list_buckets()]
    assert BUCKET in buckets

def test_upload_file(s3_client, tmp_path):
    s3_client.create_bucket(BUCKET)
    file_path = tmp_path / OBJECT
    file_path.write_bytes(CONTENT)
    s3_client.upload_file(BUCKET, str(file_path), OBJECT)
    objects = [o['Key'] for o in s3_client.list_objects(BUCKET)]
    assert OBJECT in objects

def test_get_object(s3_client, tmp_path):
    s3_client.create_bucket(BUCKET)
    file_path = tmp_path / OBJECT
    file_path.write_bytes(CONTENT)
    s3_client.upload_file(BUCKET, str(file_path), OBJECT)
    data = s3_client.get_object(BUCKET, OBJECT)
    assert data == CONTENT

def test_download_file(s3_client, tmp_path):
    s3_client.create_bucket(BUCKET)
    file_path = tmp_path / OBJECT
    file_path.write_bytes(CONTENT)
    s3_client.upload_file(BUCKET, str(file_path), OBJECT)
    download_path = tmp_path / f"downloaded_{OBJECT}"
    s3_client.download_file(BUCKET, OBJECT, str(download_path))
    assert download_path.read_bytes() == CONTENT

def test_delete_object(s3_client, tmp_path):
    s3_client.create_bucket(BUCKET)
    file_path = tmp_path / OBJECT
    file_path.write_bytes(CONTENT)
    s3_client.upload_file(BUCKET, str(file_path), OBJECT)
    s3_client.delete_object(BUCKET, OBJECT)
    objects = [o['Key'] for o in s3_client.list_objects(BUCKET)]
    assert OBJECT not in objects

def test_delete_bucket(s3_client):
    s3_client.create_bucket(BUCKET)
    s3_client.delete_bucket(BUCKET)
    buckets = [b['Name'] for b in s3_client.list_buckets()]
    assert BUCKET not in buckets