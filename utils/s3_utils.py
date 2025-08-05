def cleanup_bucket(s3_client, bucket: str):
    """Delete all objects and the bucket itself."""
    try:
        objects = s3_client.list_objects(bucket)
        for obj in objects:
            s3_client.delete_object(bucket, obj['Key'])
        s3_client.delete_bucket(bucket)
    except Exception:
        pass

def bulk_upload(s3_client, bucket: str, files):
    """Upload multiple files and return keys."""
    keys = []
    for f in files:
        s3_client.upload_file(bucket, str(f), f.name)
        keys.append(f.name)
    return keys
