from s3_testing.utils.file_utils import create_file, md5sum


def test_large_file_integrity(s3_client, temp_bucket, tmp_path):
    """
    Uploads a large file to S3, downloads it back, and verifies integrity using MD5 checksum.
    Ensures that the uploaded and downloaded files are identical.
    """
    file_path = create_file(tmp_path / "big.bin", 5_000_000)  # 5MB
    s3_client.upload_file(temp_bucket, str(file_path), file_path.name)
    download_path = tmp_path / "downloaded.bin"
    s3_client.download_file(temp_bucket, file_path.name, str(download_path))
    assert md5sum(file_path) == md5sum(download_path), (
        f"MD5 mismatch: uploaded ({md5sum(file_path)}) != downloaded ({md5sum(download_path)})"
    )

def test_small_file_integrity(s3_client, temp_bucket, tmp_path):
    """
    Uploads a small file to S3, downloads it back, and verifies integrity using MD5 checksum.
    """
    file_path = create_file(tmp_path / "small.txt", 128)  # 128 bytes
    s3_client.upload_file(temp_bucket, str(file_path), file_path.name)
    download_path = tmp_path / "downloaded_small.txt"
    s3_client.download_file(temp_bucket, file_path.name, str(download_path))
    assert md5sum(file_path) == md5sum(download_path), (
        f"MD5 mismatch for small file: uploaded ({md5sum(file_path)}) != downloaded ({md5sum(download_path)})"
    )

def test_multiple_files_integrity(s3_client, temp_bucket, tmp_path):
    """
    Uploads multiple files to S3, downloads them back, and verifies integrity for each using MD5 checksum.
    """
    files = [create_file(tmp_path / f"file_{i}.bin", 1024 * (i + 1)) for i in range(5)]
    for f in files:
        s3_client.upload_file(temp_bucket, str(f), f.name)
    for f in files:
        download_path = tmp_path / f"dl_{f.name}"
        s3_client.download_file(temp_bucket, f.name, str(download_path))
        assert md5sum(f) == md5sum(download_path), (
            f"MD5 mismatch for '{f.name}': uploaded ({md5sum(f)}) != downloaded ({md5sum(download_path)})"
        )

def test_overwrite_file_integrity(s3_client, temp_bucket, tmp_path):
    """
    Uploads a file, overwrites it with new content, downloads it, and verifies integrity.
    """
    file_path = create_file(tmp_path / "overwrite.bin", 2048)
    s3_client.upload_file(temp_bucket, str(file_path), file_path.name)
    # Overwrite with new content
    file_path.write_bytes(b"new content" * 100)
    s3_client.upload_file(temp_bucket, str(file_path), file_path.name)
    download_path = tmp_path / "downloaded_overwrite.bin"
    s3_client.download_file(temp_bucket, file_path.name, str(download_path))
    assert md5sum(file_path) == md5sum(download_path), (
        f"MD5 mismatch after overwrite: uploaded ({md5sum(file_path)}) != downloaded ({md5sum(download_path)})"
    )
