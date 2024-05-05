from cryptography.fernet import Fernet
import json

# Генерация ключа Fernet
def generate_key():
    return Fernet.generate_key()

# Функция для шифрования данных
def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(json.dumps(data).encode())
    return encrypted_data

# Функция для дешифрования данных
def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)


data = {

    "type": "task_data",
    "deliver-from": "",
    "deliver-to": "all",
    "data": {}

}

# Генерация ключа
drone_key = generate_key()
print(drone_key)

# Шифрование данных
data_encr = encrypt_data(data, drone_key)
print("Зашифрованные данные:", data_encr)

# Дешифрование данных
data_decr = decrypt_data(data_encr, drone_key)
print("Дешифрованные данные:", data_decr)
