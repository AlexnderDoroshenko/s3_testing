# S3 Testing Project

This project provides a simple Python client for working with S3-compatible storage (such as MinIO), along with automated tests and containerized setup for local development and CI.

## Features

- S3 client for bucket and object operations: create, delete, upload, download, list, get.
- Pytest-based test suite for all client methods.
- Docker Compose setup for running MinIO and tests locally.
- GitHub Actions workflow for CI with MinIO service.

## Project Structure

```
s3_testing/
├── s3_client.py         # S3 client implementation
├── conftest.py          # Pytest fixture for S3 client
├── tests/
│   └── test_s3_client.py  # Unit tests for S3 client methods
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container for running tests
├── docker-compose.yml   # Compose file for MinIO + pytest service
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions workflow
└── README.md            # Project documentation
```

## Getting Started

### 1. Run Locally with Docker Compose

```sh
docker-compose up --build
```

- MinIO will be available at [http://localhost:9001](http://localhost:9001) (console).
- S3 API endpoint: `http://localhost:9000`
- Default credentials:  
  - Access key: `minio`  
  - Secret key: `minio123`

### 2. Run Tests Locally (without Docker)

1. Start MinIO manually (see [MinIO Quickstart](https://min.io/docs/minio/linux/index.html#quickstart)).
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run tests:
   ```sh
   pytest
   ```

### 3. Run Tests in CI

On every push or pull request to `main` or `develop`, GitHub Actions will:
- Start MinIO service
- Install dependencies
- Wait for MinIO to be healthy
- Run all pytest tests

## S3 Client Usage Example

```python
from s3_client import S3Client

client = S3Client(
    endpoint_url='http://localhost:9000',
    access_key='minio',
    secret_key='minio123'
)

client.create_bucket('test-bucket')
client.upload_file('test-bucket', 'local_file.txt')
print(client.list_objects('test-bucket'))
client.download_file('test-bucket', 'local_file.txt', 'downloaded.txt')
client.delete_object('test-bucket', 'local_file.txt')
client.delete_bucket('test-bucket')
```

## Configuration

- **Docker Compose:**  
  - `minio` service runs MinIO server.
  - `pytest` service builds and runs tests in a container, connecting to MinIO.
- **Pytest Fixture:**  
  - Reads MinIO connection info from environment variables for flexibility.

## Useful Links

- [MinIO Documentation](https://min.io/docs/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Pytest Documentation](https://docs.pytest.org/en/latest/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

**Feel free to contribute or open issues for enhancements and bugs. Let's improve S3 testing together!**