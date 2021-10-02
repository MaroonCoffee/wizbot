from cryptography.fernet import Fernet
from stdiomask import getpass

# Template file to insert your encrypted passwords

encrypted_password = ''


def encrypted_password_creator():
    key = Fernet.generate_key()
    print("Your generated password is:", key)
    cipher_suite = Fernet(key)
    passwords = bytes(getpass('Enter your combined password string formatted as follows '
                              '(Main Bot1 Bot2 Bot3 Bot4): '), 'utf-8')
    e_text = cipher_suite.encrypt(passwords)
    print("Encoded text is:", e_text)


if __name__ == "__main__":
    encrypted_password_creator()
