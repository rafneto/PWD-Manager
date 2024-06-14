# Password Manager

A simple yet secure password manager written in Python. This password manager allows users to store, retrieve, update, and delete passwords for various services securely. It uses AES encryption to protect stored passwords and allows copying passwords to the clipboard for easy use.

## Features

- Generate random passwords
- Encrypt and decrypt passwords
- Store and manage passwords in a SQLite database
- Copy passwords to clipboard
- Simple command-line interface

## Installation

1. Clone the repository:
```sh
   git clone https://github.com/rafneto/PWD-Manager.git
   cd PWD-Manager
```

2. Install the required dependencies:
```sh
    pip install -r requirements.txt
```

## Usage

1. Run the password manager:
```sh
    python pwd_manager.py
```

2. Follow the prompts to perform various operations:
- List all services
- Retrieve a password
- Create a new password entry
- Update an existing password
- Delete a password entry

## File Descriptions

### `pwd_manager.py`

This is the main script to run the password manager. It includes functions to interact with the user and perform various password management operations.

### `crypto_utils.py`

This module contains utility functions for encrypting and decrypting passwords using AES encryption.

### `db_utils.py`

This module contains utility functions for interacting with the SQLite database where passwords are stored.

## Security

- Passwords are encrypted using AES encryption before being stored in the database.
- The encryption key is derived using PBKDF2 and stored in a file (`key.bin`). Ensure that this file is kept secure.
- The master password is used to protect access to the password manager.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or new features to suggest.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements

- PyCryptodome for encryption and decryption
- Clipboard for clipboard operations

## Contact

If you have any questions or feedback, please feel free to reach out.