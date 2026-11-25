import hashlib
import re
from pathlib import Path


def evaluate(data, fixture_path):
    supplied = Path(data["backup_file"])
    expected = data["sha256"]
    if supplied.is_absolute() or not re.fullmatch(r"[a-f0-9]{64}", expected):
        raise ValueError("expected a relative file and a lowercase SHA-256 digest")
    root = fixture_path.resolve().parent
    candidate = (root / supplied).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        return [{"code": "backup_missing_or_outside_fixture_directory"}]
    with candidate.open("rb") as backup:
        actual = hashlib.file_digest(backup, "sha256").hexdigest()
    return [] if actual == expected else [{"code": "checksum_mismatch"}]
