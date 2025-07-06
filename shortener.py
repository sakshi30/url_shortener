import base62
import hashlib

class Shortener:

    @staticmethod
    def encode_url(url):
        # Create a consistent integer from a URL using SHA256
        hash_object = hashlib.sha256(url.encode())
        url_id =  int(hash_object.hexdigest(), 16) % (10 ** 10)
        return base62.encode(url_id)