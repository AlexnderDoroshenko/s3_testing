import pytest
from s3_client import S3Client
from os import environ
from utils.s3_utils import cleanup_bucket


@pytest.fixture(scope="session")
def s3_client():
    """
    Pytest fixture for S3Client.
    Returns a client connected to local MinIO.
    """
    client = S3Client(
        endpoint_url=f"http://{environ.get('MINIO_HOST_NAME')}:{environ.get('MINIO_HOST_PORT')}",
        access_key=environ.get('MINIO_ROOT_USER', 'minio'),
        secret_key=environ.get('MINIO_ROOT_PASSWORD', 'minio123')
    )
    return client


@pytest.fixture
def temp_bucket(s3_client):
    """Create a temporary bucket for test and cleanup after."""
    import uuid
    bucket = f"test-{uuid.uuid4().hex[:8]}"
    s3_client.create_bucket(bucket)
    yield bucket
    cleanup_bucket(s3_client, bucket)
