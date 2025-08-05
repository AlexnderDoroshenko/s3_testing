import hashlib
from pathlib import Path


def create_file(path: Path, size_bytes: int, content: bytes = None):
    """Create a file with specific size or repeating content."""
    if content:
        path.write_bytes(content * (size_bytes // len(content)))
    else:
        path.write_bytes(b"A" * size_bytes)
    return path

def md5sum(file_path: Path):
    """Calculate md5 hash of a file."""
    h = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            h.update(chunk)
    return h.hexdigest()
