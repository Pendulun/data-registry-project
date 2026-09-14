import hashlib


class SHA256FileHasher:

    def calculate(self, file_path: str) -> str:
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                sha256.update(chunk)

        return sha256.hexdigest()
