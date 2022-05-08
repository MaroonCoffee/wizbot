import stdiomask
from cryptography.fernet import Fernet
from stdiomask import getpass

# Template file to insert your encrypted passwords

encrypted_password = ''

encrypted_username = ''

encrypted_wizard_name = ''

folder_path = ''

fast_empower_buy = True
lag_mode = False
in_game = False
min_mem_status = False


def encrypted_password_creator():
    usr_input = stdiomask.getpass("Enter your encyrption key, or 'N' to have one generated for you: ")
    if usr_input == 'N' or usr_input == 'n':
        key = Fernet.generate_key()
        print("Your generated password is:", key)
    else:
        key = usr_input
    cipher_suite = Fernet(key)
    passwords = bytes(getpass('Enter your combined string formatted as follows:\n'
                              'For Passwords: Main Bot1 Bot2 Bot3 Bot4\n'
                              'For Wizard Names: Main,Bot1,Bot2,Bot3,Bot4\n'
                              'For User Names: Main Bot1 Bot2 Bot3 Bot4\n'
                              ': '), 'utf-8')
    e_text = cipher_suite.encrypt(passwords)
    print("Encoded text is:", e_text)


if __name__ == "__main__":
    encrypted_password_creator()
