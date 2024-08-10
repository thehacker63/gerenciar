from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def _init_(self, file_path="passwords.json", key_file="key.key"):
        self.file_path = file_path
        self.key_file = key_file
        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        self.passwords = {}
        self.load_passwords()

    def generate_key(self):
        """Gera uma nova chave para criptografia"""
        return Fernet.generate_key()

    def save_key(self):
        """Salva a chave de criptografia em um arquivo"""
        with open(self.key_file, "wb") as file:
            file.write(self.key)

    def load_key(self):
        """Carrega a chave de criptografia de um arquivo ou gera uma nova chave se não existir"""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as file:
                return file.read()
        else:
            self.key = self.generate_key()
            self.save_key()
            return self.key

    def encrypt_data(self, data):
        """Criptografa os dados"""
        return self.cipher.encrypt(json.dumps(data).encode())

    def decrypt_data(self, encrypted_data):
        """Descriptografa os dados"""
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Erro ao descriptografar dados: {e}")
            raise

    def load_passwords(self):
        """Carrega as senhas do arquivo JSON"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "rb") as file:
                    encrypted_data = file.read()
                    self.passwords = self.decrypt_data(encrypted_data)
            except Exception as e:
                print(f"Erro ao carregar senhas: {e}")
                self.passwords = {}
        else:
            self.passwords = {}

    def save_passwords(self):
        """Salva as senhas no arquivo JSON"""
        try:
            with open(self.file_path, "wb") as file:
                encrypted_data = self.encrypt_data(self.passwords)
                file.write(encrypted_data)
        except Exception as e:
            print(f"Erro ao salvar senhas: {e}")

    def email_exists(self, email):
        """Verifica se o email já está armazenado"""
        return email in self.passwords

    def add_password(self, email, password):
        """Adiciona uma senha se o email não existir"""
        if not self.email_exists(email):
            self.passwords[email] = password
            self.save_passwords()
        else:
            raise ValueError("Este email já existe.")

    def remove_password(self, email):
        """Remove a senha associada ao email"""
        if self.email_exists(email):
            del self.passwords[email]
            self.save_passwords()
        else:
            raise ValueError("Email ou senha não encontrado.")

    def get_all_passwords(self):
        """Retorna todos os emails e senhas"""
        return self.passwords.items()