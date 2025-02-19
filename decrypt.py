import os
from ranger.api.commands import Command
import subprocess
import tarfile
import getpass

class decrypt(Command):
    """:decrypts

    Decrypts a file with GPG or a directory by extracting a tar file and decrypting it.
    """

    def execute(self):
        paths = [os.path.basename(f.path) for f in self.fm.thistab.get_selection()]

        self.fm.notify("Please wait, the file/directory is being decrypted...")

        # Start the decryption function
        self.decrypt_files(paths)

    def decrypt_files(self, paths):
        for p in paths:
            if p.endswith('.gpg'):
                self.fm.notify(f"Decrypting file: {p}...")
                out_fname = os.path.splitext(p)[0]

                # Attempt decryption with gpg-agent
                result = self.try_decrypt_with_agent(p, out_fname)

                # If decryption via gpg-agent fails, ask for passphrase
                if not result:
                    passphrase = getpass.getpass("Enter passphrase for decryption: ")
                    result = self.try_decrypt_with_passphrase(p, out_fname, passphrase)

                if result:
                    self.fm.notify(f"Successfully decrypted: {p}")

                    # Check if the file is a tar archive
                    if tarfile.is_tarfile(out_fname):
                        self.fm.notify(f"Extracting archive: {out_fname}...")
                        try:
                            with tarfile.open(out_fname) as tar:
                                tar.extractall(path=os.path.dirname(out_fname))
                            self.fm.notify(f"Successfully extracted: {out_fname}")
                        except Exception as e:
                            self.fm.notify(f"Error extracting {out_fname}: {e}")

                    # Remove the temporary decrypted file
                    if os.path.exists(out_fname):
                        os.remove(out_fname)

                else:
                    self.fm.notify(f"Decryption failed for {p}. Invalid passphrase or file.")

            self.fm.notify(f'Decrypted {p} successfully.')

    def try_decrypt_with_agent(self, p, out_fname):
        """Try to decrypt using gpg-agent."""
        try:
            result = subprocess.run(
                ['gpg', '--batch', '--use-agent', '--no-tty', '-d', p],
                stdout=open(out_fname, 'wb'),
                stderr=subprocess.PIPE,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            # If an error occurs, decryption failed
            return False

    def try_decrypt_with_passphrase(self, p, out_fname, passphrase):
        """Try to decrypt the file by manually providing a passphrase."""
        try:
            result = subprocess.run(
                ['gpg', '--batch', '--use-agent', '--no-tty', '--passphrase', passphrase, '-d', p],
                stdout=open(out_fname, 'wb'),
                stderr=subprocess.PIPE,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            return False

