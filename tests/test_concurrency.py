import concurrent.futures
from s3_testing.utils.file_utils import create_file


def test_parallel_uploads(s3_client, temp_bucket, tmp_path):
    """
    Test parallel uploads of multiple files to S3 using ThreadPoolExecutor.
    Verifies that all uploaded files are present in the bucket.
    """
    files = [create_file(tmp_path / f"file_{i}.bin", 1_000_000) for i in range(10)]

    def upload(f):
        s3_client.upload_file(temp_bucket, str(f), f.name)
        return f.name

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        keys = list(executor.map(upload, files))

    objects = [o['Key'] for o in s3_client.list_objects(temp_bucket)]
    for key in keys:
        assert key in objects, f"Uploaded file '{key}' not found in the bucket."

def test_parallel_downloads(s3_client, temp_bucket, tmp_path):
    """
    Test parallel downloads of multiple files from S3 using ThreadPoolExecutor.
    Verifies that all downloaded files exist locally.
    """
    # Upload files first
    files = [create_file(tmp_path / f"file_{i}.bin", 500_000) for i in range(5)]
    for f in files:
        s3_client.upload_file(temp_bucket, str(f), f.name)

    def download(key):
        out_path = tmp_path / f"dl_{key}"
        s3_client.download_file(temp_bucket, key, str(out_path))
        return out_path.exists()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(download, [f.name for f in files]))

    assert all(results), "Not all files were downloaded successfully."

def test_parallel_deletes(s3_client, temp_bucket, tmp_path):
    """
    Test parallel deletion of multiple objects from S3.
    Verifies that all objects are removed from the bucket.
    """
    files = [create_file(tmp_path / f"file_{i}.bin", 100_000) for i in range(5)]
    for f in files:
        s3_client.upload_file(temp_bucket, str(f), f.name)

    def delete(key):
        s3_client.delete_object(temp_bucket, key)
        return key

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        deleted = list(executor.map(delete, [f.name for f in files]))

    objects = [o['Key'] for o in s3_client.list_objects(temp_bucket)]
    for key in deleted:
        assert key not in objects, f"Object '{key}' was not deleted."
