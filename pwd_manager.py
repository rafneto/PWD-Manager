import getpass  # To handle password input securely
import db_utils  # To interact with the database
import crypto_utils  # To handle encryption and decryption of passwords
import clipboard  # To copy passwords to the clipboard
import random  # To generate random passwords
import string  # To use string constants

passwords = {}
key = ""

def generate_password():
    """
    Generate a random password with a length between 8 and 32 characters.

    Returns:
        str: The generated password.
    """
    length = random.randint(8, 32)
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def get_password(key):
    """
    Retrieve and copy the password for a given service and username to the clipboard.

    Args:
        key (str): The encryption key used to decrypt the password.
    """
    service = input("Enter the service: ")
    username = input("Enter your username: ")
    records = db_utils.get_record(service, username)
    if len(records) > 0:
        password = crypto_utils.decrypt_password(records[0][0], key)
        clipboard.copy(password)
        print("Username:", records[0][1])
        input("Password copied!\nType any key to exit...")
    else:
        input("Service doesn't exist!\nType any key to exit...")

def create_password(key):
    """
    Create a new password entry for a given service and username.

    Args:
        key (str): The encryption key used to encrypt the password.
    """
    service = input("Enter the service: ")
    username = input("Enter your username: ")
    print("0 - Generate password")
    print("1 - Insert password")
    option = input("Default is [0]. Your choice: ")
    if option == "1":
        password = getpass.getpass("Enter your password: ")
    else:
        password = generate_password()
    
    hashed_password = crypto_utils.encrypt_password(password, key)
    db_utils.save_record(service, username, hashed_password)
    print("Password created successfully.")
    input("Type any key to exit...")

def update_password(key):
    """
    Update the password for a given service and username.

    Args:
        key (str): The encryption key used to encrypt the new password.
    """
    service = input("Enter the service: ")
    username = input("Enter your username: ")
    
    if len(db_utils.get_record(service, username)) > 0:
        print("0 - Generate password")
        print("1 - Insert password")
        option = input("Default is [0]. Your choice: ")
        if option == "1":
            password = getpass.getpass("Enter your password: ")
        else:
            password = generate_password()
        hashed_password = crypto_utils.encrypt_password(password, key)
        db_utils.update_record(service, username, hashed_password)
    else:
        print("Service not found!")
    input("Type any key to exit...")

def delete_password():
    """
    Delete a password entry for a given service and username.
    """
    service = input("Enter the service: ")
    username = input("Enter your username: ")
    if len(db_utils.get_record(service, username)) > 0:
        choice = input("The service exists.\nAre you sure you want to delete it? Type yes or y... ")
        if choice == "y" or choice == "yes":
            db_utils.delete_record(service, username)
    else:
        print("Service not found!")
    input("Type any key to exit...")

def list_websites():
    """
    List all services stored in the password manager.
    """
    print("\nList of services:")
    passwords = db_utils.get_all_records()
    if len(passwords) <= 1:
        print("No services saved!")
    else:
        for website in passwords:
            if website['SERVICE'] != "pwd_manager":
                print(website['SERVICE'], end="\t")
        print("\n")
    input("Type any key to exit...")

def main():
    """
    Main function to run the password manager. Prompts for master password and displays the menu.
    """
    enable_menu = True
    if db_utils.check_table():
        master = db_utils.get_record("pwd_manager", "master")
        password_master = getpass.getpass("What is your master password: ")
        key = crypto_utils.get_key()
        decrypt_master = crypto_utils.decrypt_password(master[0][0], key)
        if decrypt_master != password_master:
            getpass.getpass("Wrong Password!\nPassword Manager will exit...")
            enable_menu = False
    else:
        print("Database is empty!")
        password_master = getpass.getpass("Create a master password: ")
        key = crypto_utils.create_key()
        db_utils.save_record("pwd_manager", "master", crypto_utils.encrypt_password(password_master, key))

    while enable_menu:
        print("\033[H\033[J", end="")
        print("1. List of services")
        print("2. Get password")
        print("3. Create")
        print("4. Update")
        print("5. Delete")
        print("Q. Quit")

        choice = input("Enter your choice (1-4) or Q to quit: ")
        if choice == "1":
            list_websites()
        elif choice == "2":
            get_password(key)
        elif choice == "3":
            create_password(key)
        elif choice == "4":
            update_password(key)
        elif choice == "5":
            delete_password()
        elif choice == "Q":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()