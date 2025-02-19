import os
import threading
from gnupg import GPG
from ranger.api.commands import Command
import subprocess


class encrypt(Command):
    """:encrypt

    Encrypts a directory using tar and GPG via pipe. The original directory is not deleted.
    """

    def execute(self):
        gpg_home = os.path.join(os.path.expanduser('~'), '.gnupg/')
        default_recipient = os.environ.get('DEFAULT_RECIPIENT')

        if not default_recipient:
            self.fm.notify('DEFAULT_RECIPIENT environment variable must be set')
            return

        gpg = GPG(gpgbinary='/opt/homebrew/bin/gpg', gnupghome=gpg_home)

        paths = [os.path.basename(f.path) for f in self.fm.thistab.get_selection()]

        self.fm.notify("Please wait, the file/directory is being encrypted...")

        thread = threading.Thread(target=self.encrypt_files, args=(paths, default_recipient, gpg))
        thread.start()

    def encrypt_files(self, paths, default_recipient, gpg):
        for p in paths:
            if os.path.isdir(p):
                self.fm.notify(f"Archiving directory: {p}...")

                tar_command = ['tar', 'cf', '-', p]
                tar_process = subprocess.run(tar_command, stdout=subprocess.PIPE)

                self.fm.notify(f"Encrypting the archive of {p}...")
                gpg_command = [
                    'gpg', '--yes', '--batch', '--encrypt', '--recipient', default_recipient,
                    '--output', f'{p}.tar.gpg'
                ]
                subprocess.run(gpg_command, input=tar_process.stdout)

            else:
                self.fm.notify(f"Encrypting file: {p}...")
                with open(p, 'rb') as f:
                    enc = gpg.encrypt_file(f, default_recipient)

                with open(p + '.gpg', 'wb+') as out:
                    out.write(enc.data)

            self.fm.notify(f'Encrypted {p} successfully.')


