import hashlib
import base64


def file_to_hash(filename: str, return_type="bytes") -> bytes:
    """
    read in byte data and return the SHA512/256 hash representation
    in base64.

    :param filename -> ``str``: the name of the file to read.
    :param return_type -> ``str``: the type of data to return.

    :return -> ``bytes``: hash repr of bytes.
    """
    file_bytes = open(filename, "rb").read()
    hasher = hashlib.sha256()
    hasher.update(file_bytes)

    if return_type == "bytes":
        return hasher.digest()
    elif return_type == "base64":
        return base64.b64encode(hasher.digest())

print(file_to_hash("__init__.py", "base64"))
