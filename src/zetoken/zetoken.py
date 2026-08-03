import os
import time
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

class Zetoken:
    def _resolve_keys(self, key_id=None, secret_key=None):
        final_key_id = key_id or os.environ.get('ZETOKEN_ACCESS_KEY_ID')
        final_secret = secret_key or os.environ.get('ZETOKEN_SECRET_KEY')

        try:
            final_iterations = int(os.environ.get('ZETOKEN_ITERATIONS', 1000))
        except (ValueError, TypeError):
            final_iterations = 1000

        if final_iterations < 1:
            final_iterations = 1000

        return final_key_id, final_secret, final_iterations

    def _derive_cryptographic_key(self, start_point, seed, iterations):
        return hashlib.pbkdf2_hmac(
            'sha512',
            seed.encode('utf-8'),
            start_point.encode('utf-8'),
            iterations,
            dklen=16
        )

    def encode(self, text, key_id=None, secret_key=None, ttl=None):
        kid, sec, iterations = self._resolve_keys(key_id, secret_key)

        if not kid or not sec:
            return False

        if ttl is not None and isinstance(ttl, int) and ttl > 0:
            exp_time = int(time.time()) + ttl
            text = f"{text}__ZTX__{exp_time}"

        aes_key = self._derive_cryptographic_key(kid, sec, iterations)
        iv = os.urandom(12)  

        aesgcm = AESGCM(aes_key)
        
        try:
            encrypted = aesgcm.encrypt(iv, text.encode('utf-8'), None)
        except Exception:
            return False

        actual_ciphertext = encrypted[:-16]
        tag = encrypted[-16:]

        payload = iv + tag + actual_ciphertext

        numeric_result = "".join(f"{b:03d}" for b in payload)
        
        return numeric_result

    def decode(self, cipher_text, key_id=None, secret_key=None, leeway=60):
        kid, sec, iterations = self._resolve_keys(key_id, secret_key)

        if not kid or not sec:
            return False

        if len(cipher_text) % 3 != 0 or not cipher_text.isdigit():
            return False

        try:
            payload = bytes(int(cipher_text[i:i+3]) for i in range(0, len(cipher_text), 3))
        except ValueError:
            return False

        if len(payload) < 28:
            return False

        iv = payload[:12]
        tag = payload[12:28]
        actual_ciphertext = payload[28:]

        aes_key = self._derive_cryptographic_key(kid, sec, iterations)
        aesgcm = AESGCM(aes_key)

        cryptography_ciphertext = actual_ciphertext + tag

        try:
            decrypted = aesgcm.decrypt(iv, cryptography_ciphertext, None)
            decrypted_text = decrypted.decode('utf-8')

            if "__ZTX__" in decrypted_text:
                parts = decrypted_text.rsplit('__ZTX__', 1) 
                if len(parts) == 2:
                    try:
                        exp_time = int(parts[1])
                        if (int(time.time()) - leeway) > exp_time:
                            return False 
                        return parts[0] 
                    except ValueError:
                        pass

            return decrypted_text
        except (InvalidTag, Exception):
            return False

    def sign(self, text, key_id, secret_key=None, ttl=None):
        master_access_key, master_secret_key, _ = self._resolve_keys(None, secret_key)

        if not master_access_key or not master_secret_key or not key_id:
            return False

        layered_key_id = f"{master_access_key}::{key_id}"

        return self.encode(text, layered_key_id, master_secret_key, ttl=ttl)

    def verify_sign(self, token, key_id, secret_key=None, leeway=60):
        master_access_key, master_secret_key, _ = self._resolve_keys(None, secret_key)

        if not master_access_key or not master_secret_key or not key_id:
            return False

        layered_key_id = f"{master_access_key}::{key_id}"

        return self.decode(token, layered_key_id, master_secret_key, leeway=leeway)

    verifySign = verify_sign