import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from typing import List, Optional, Dict, Any

class S3Client:
    """
    S3 client for working with S3-compatible storage (e.g., MinIO).
    Supports bucket and object operations: create, delete, upload, download, list, get.
    """

    def __init__(self, endpoint_url: str, access_key: str, secret_key: str) -> None:
        """
        Initialize S3 client.

        :param endpoint_url: S3 server URL
        :param access_key: access key
        :param secret_key: secret key
        """
        self.s3: BaseClient = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def create_bucket(self, bucket_name: str) -> None:
        """
        Create a bucket.

        :param bucket_name: Bucket name
        """
        try:
            self.s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        except ClientError as e:
            print(e)

    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all buckets.

        :return: List of buckets
        """
        return self.s3.list_buckets().get('Buckets', [])

    def delete_bucket(self, bucket_name: str) -> None:
        """
        Delete a bucket.

        :param bucket_name: Bucket name
        """
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' deleted.")
        except ClientError as e:
            print(e)

    def upload_file(self, bucket_name: str, file_path: str, object_name: Optional[str] = None) -> None:
        """
        Upload a file to a bucket.

        :param bucket_name: Bucket name
        :param file_path: Local file path
        :param object_name: Object name in bucket (if not specified, uses file_path)
        """
        if object_name is None:
            object_name = file_path
        try:
            self.s3.upload_file(file_path, bucket_name, object_name)
            print(f"File '{file_path}' uploaded as '{object_name}'.")
        except ClientError as e:
            print(e)

    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> None:
        """
        Download a file from a bucket.

        :param bucket_name: Bucket name
        :param object_name: Object name in bucket
        :param file_path: Local file path to save
        """
        try:
            self.s3.download_file(bucket_name, object_name, file_path)
            print(f"File '{object_name}' downloaded to '{file_path}'.")
        except ClientError as e:
            print(e)

    def list_objects(self, bucket_name: str) -> List[Dict[str, Any]]:
        """
        List objects in a bucket.

        :param bucket_name: Bucket name
        :return: List of objects
        """
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            return response.get('Contents', [])
        except ClientError as e:
            print(e)
            return []

    def delete_object(self, bucket_name: str, object_name: str) -> None:
        """
        Delete an object from a bucket.

        :param bucket_name: Bucket name
        :param object_name: Object name
        """
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=object_name)
            print(f"Object '{object_name}' deleted from bucket '{bucket_name}'.")
        except ClientError as e:
            print(e)

    def get_object(self, bucket_name: str, object_name: str) -> Optional[bytes]:
        """
        Get an object from a bucket.

        :param bucket_name: Bucket name
        :param object_name: Object name
        :return: Object content as bytes or None
        """
        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=object_name)
            return response['Body'].read()
        except ClientError as e:
            print(e)
            return None

# Example usage:
if __name__ == "__main__":
    client = S3Client(
        endpoint_url='http://localhost:9000',
        access_key='minio',
        secret_key='minio123'
    )

    client.create_bucket('test-bucket')
    print("Buckets:", client.list_buckets())
    # client.upload_file('test-bucket', 'local_file.txt')
    # print(client.list_objects('test-bucket'))
    # client.download_file('test-bucket', 'local_file.txt', 'downloaded.txt')
    # client.delete_object('test-bucket', 'local_file.txt')
    # client.delete_bucket('test-bucket')
