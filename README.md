# ranger-gpg-async

**ranger-gpg-async** is a plugin for the ranger file manager (https://ranger.fm) that allows you to encrypt and decrypt files and directories using GPG in asynchronous mode. It keeps the interface responsive during encryption and decryption operations, with real-time process notifications.

## Installation

### Set the Default GPG Recipient

Add your default GPG recipient email to your shell environment. This is required for encryption operations:

```
export DEFAULT_RECIPIENT="email@email.com"
```

### Clone the Repository and Install the Plugin

Run the following commands to clone the repository and install the plugin:

```
git clone https://github.com/soko1/ranger-gpg-async
cd ranger-gpg-async
make install
```

### Install Python Dependencies

Install the required Python dependencies:

```
pip install python-gnupg
```

If you're using macOS and have ranger installed via Homebrew, use the following command to install python-gnupg:

```
/opt/homebrew/Cellar/ranger/1.9.4/libexec/bin/python -m pip install python-gnupg
```

## Usage

**To encrypt** a file or directory, navigate to the desired file or directory in ranger and run the following command:

`:encrypt`

This will create a .tar.gpg encrypted file.

**To decrypt** a .gpg file, navigate to the encrypted file and run the following command:

`:decrypt`

The decrypted files will be extracted into the same directory.

Note: Original files are not deleted automatically after encryption or decryption. You will need to manually delete the original files if desired.

