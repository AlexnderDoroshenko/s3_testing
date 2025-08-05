import pytest
from botocore.exceptions import ClientError


# def test_delete_nonexistent_object(s3_client, temp_bucket):
#     """
#     Attempt to delete a non-existent object from S3.
#     Expects a ClientError with NoSuchKey or 404 error code.
#     """
#     with pytest.raises(ClientError) as e:
#         s3_client.delete_object(temp_bucket, "missing.txt")
#     assert e.value.response['Error']['Code'] in ["NoSuchKey", "404"], (
#         f"Expected error code 'NoSuchKey' or '404', got '{e.value.response['Error']['Code']}'"
#     )

def test_delete_nonexistent_object_idempotent(s3_client, temp_bucket):
    """
    Deleting a non-existent object should be idempotent and not affect the bucket.
    """
    # Create a bucket with no objects
    initial_objects = s3_client.list_objects(temp_bucket)

    # Delete missing object
    s3_client.delete_object(temp_bucket, "missing.txt")

    # List objects again
    after_objects = s3_client.list_objects(temp_bucket)

    assert initial_objects == after_objects, \
        f"Bucket contents changed after deleting non-existent object: {after_objects}"

def test_invalid_credentials(tmp_path):
    """
    Attempt to list buckets with invalid credentials.
    Expects a ClientError due to authentication failure.
    """
    from s3_testing.s3_client import S3Client
    bad_client = S3Client(
        endpoint_url='http://localhost:9000',
        access_key='wrong',
        secret_key='wrong'
    )
    with pytest.raises(ClientError, match="InvalidAccessKeyId|SignatureDoesNotMatch"):
        bad_client.list_buckets()

def test_get_nonexistent_object(s3_client, temp_bucket):
    """
    Getting a non-existent object should return None (custom S3Client behavior).
    """
    result = s3_client.get_object(temp_bucket, "missing.txt")
    assert result is None or result == b"", \
        f"Expected None or empty bytes for missing object, got: {result}"

def test_download_nonexistent_object(s3_client, temp_bucket, tmp_path):
    """
    Attempt to download a non-existent object from S3.
    Expects a ClientError with NoSuchKey or 404 error code.
    """
    download_path = tmp_path / "should_not_exist.txt"
    with pytest.raises(ClientError) as e:
        s3_client.download_file(temp_bucket, "missing.txt", str(download_path))
    assert e.value.response['Error']['Code'] in ["NoSuchKey", "404"], (
        f"Expected error code 'NoSuchKey' or '404', got '{e.value.response['Error']['Code']}'"
    )

def test_create_bucket_invalid_name(s3_client):
    """
    Attempt to create a bucket with an invalid name.
    Expects a ClientError due to invalid bucket name.
    """
    with pytest.raises(ClientError, match="InvalidBucketName|InvalidBucket"):
        s3_client.create_bucket("Invalid_Bucket_Name!")
