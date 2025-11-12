import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


class EncryptionDecryption:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def pad(self, data):
        padding_length = 16 - len(data) % 16
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def unpad(self, data):
        padding_length = data[-1]
        return data[:-padding_length]

    def file_to_string(self, items):
        final_string = b""

        if isinstance(items, str):
            final_string = items.encode("utf-8")
        elif isinstance(items, list) and len(items) > 0 and isinstance(items[0], str):
            final_string = '\n'.join(items).encode("utf-8")
        else:
            final_string += b"### ACCOUNTS\n"
            for entry in items:
                if isinstance(entry, list) and len(entry) == 3:
                    line = f"Website: {entry[0]} | Emails: {entry[1]} | Password: {entry[2]}\n"
                    final_string += line.encode("utf-8")
            final_string += b"\n### API\nAPI = \n### PASSWORD\nPASSWORD = \n### THEME\nTHEME = darkly"

        return final_string

    def encrypt_file_with_password(self, input_data, output_file=None, password=None):
        if output_file is None:
            output_file = f"{self.username}_profile.enc"
        if password is None:
            password = self.password

        input_bytes = self.file_to_string(input_data)

        salt = os.urandom(16)
        iv = os.urandom(16)
        key = PBKDF2(password, salt, 32, count=100000)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        padded_plaintext = self.pad(input_bytes)
        ciphertext = cipher.encrypt(padded_plaintext)

        with open(output_file, "wb") as f:
            f.write(salt + iv + ciphertext)

    def decrypt_file_with_password(self, input_file=None, password=None):
        if input_file is None:
            input_file = f"{self.username}_profile.enc"

        if password is None:
            password = self.password

        try:
            with open(input_file, "rb") as f:
                salt = f.read(16)
                iv = f.read(16)
                encrypted_data = f.read()

            key = PBKDF2(password, salt, 32, count=100000)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_data = self.unpad(cipher.decrypt(encrypted_data))
            line_list = decrypted_data.decode('utf-8').split('\n')

            for line in line_list:
                if "### ACCOUNTS" in line or "### API" in line:
                    return line_list

            return "Decryption didn't work"

        except Exception as e:
            print(f"Decryption error: {e}")
            return "Decryption didn't work"