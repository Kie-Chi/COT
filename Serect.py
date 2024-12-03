from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
import json
import zlib

# 准备加密密钥
def generate_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# AES-GCM 加密
def encrypt_json(data: dict, password: str):
    # 压缩 JSON 数据
    compressed_data = zlib.compress(json.dumps(data).encode())

    # 生成加密密钥
    salt = os.urandom(16)
    key = generate_key(password, salt)

    # 加密数据
    iv = os.urandom(12)  # 随机生成初始向量
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(compressed_data) + encryptor.finalize()

    # 返回密文、IV、盐和认证标签
    return {
        'ciphertext': ciphertext,
        'iv': iv,
        'salt': salt,
        'tag': encryptor.tag
    }

# AES-GCM 解密
def decrypt_json(encrypted_data: dict, password: str):
    # 提取数据
    salt = encrypted_data['salt']
    iv = encrypted_data['iv']
    tag = encrypted_data['tag']
    ciphertext = encrypted_data['ciphertext']

    # 生成解密密钥
    key = generate_key(password, salt)

    # 解密数据
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decompressed_data = zlib.decompress(decryptor.update(ciphertext) + decryptor.finalize())

    # 返回解密后的 JSON 数据
    return json.loads(decompressed_data)
