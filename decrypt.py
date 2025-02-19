import os
import threading
from gnupg import GPG
from ranger.api.commands import Command
import subprocess
import tarfile


class decrypt(Command):
    """:decrypts

    Decrypts a file with GPG or a directory by extracting a tar file and decrypting it.
    """

    def execute(self):
        gpg_home = os.path.join(os.path.expanduser('~'), '.gnupg/')
        gpg = GPG(gnupghome=gpg_home)

        paths = [os.path.basename(f.path) for f in self.fm.thistab.get_selection()]

        self.fm.notify("Please wait, the file/directory is being decrypted...")

        thread = threading.Thread(target=self.decrypt_files, args=(paths, gpg))
        thread.start()

    def decrypt_files(self, paths, gpg):
        for p in paths:
            if p.endswith('.gpg'):
                self.fm.notify(f"Decrypting file: {p}...")
                with open(p, 'rb') as enc:
                    dec_b = gpg.decrypt_file(enc)

                out_fname = os.path.splitext(p)[0]
                with open(out_fname, 'wb+') as dec_f:
                    dec_f.write(dec_b.data)

                if tarfile.is_tarfile(out_fname):
                    self.fm.notify(f"Extracting archive: {out_fname}...")
                    with tarfile.open(out_fname) as tar:
                        tar.extractall(path=os.path.dirname(out_fname))

                    os.remove(out_fname)

            self.fm.notify(f'Decrypted {p} successfully.')

