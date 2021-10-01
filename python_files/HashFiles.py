"""
HashFiles.py

Hashes a given file tree one file at a time.
"""

import hashlib
import json

from os import walk
from os.path import join

import questionary

import dependencies.CustomLog_Classes as Clog


class HashDirectory:
    def __init__(self):
        self.err = Clog.Error()
        self.err.error_setup()

        # BUF_SIZE is totally arbitrary, change for your app!
        # BUF_SIZE allows large files to be read in smaller chunks,
        # that way a 2GB file doesn't take 2GB of memory
        self.BUFF_SIZE = self._GetBuffSize()  # default is lets read stuff in 64kb chunks!

        # TODO: choose option for algorithm
        self.md5 = hashlib.md5()
        self.sha1 = hashlib.sha1()
        self.sha256 = hashlib.sha256()

    def _GetBuffSize(self):
        while True:
            try:
                buffer_size = questionary.text(message="Please enter buffer chunk size in bytes:",
                                               default="65536").ask()
                if str(buffer_size).isdigit():
                    print("{} byte buffer size chosen".format(buffer_size))
                    return buffer_size
                else:
                    print("buffer size must be an integer")

            except questionary.ValidationError as e:
                self.err.error_handle_no_exit_quiet(e)
                pass
            except Exception as e:
                self.err.error_handle(e)

    def HashFile(self, dirpath, file, Mode):
        with open(join(dirpath, file).replace('\\', '/'), 'rb') as f:
            while True:
                data = f.read(self.BUFF_SIZE)
                if not data:
                    break
                self.md5.update(data)
                self.sha1.update(data)
                self.sha256.update(data)
        if Mode.upper() == "F":
            HashDict = [{"filename": join(dirpath, file).replace('\\', '/'),
                         "MD5": self.md5.hexdigest(),
                         "Sha1": self.sha1.hexdigest(),
                         "Sha256": self.sha256.hexdigest()}]

            with open("../Misc_Project_Files/HashFile_{}.json".format(
                    HashDict[0]["filename"].split(".")[0]), "w") as f:
                json.dump(HashDict, fp=f, indent=4)
                print("json dumped to {}".format(f.name))

        elif Mode.upper() == "D":
            pass
        else:
            try:
                raise AttributeError("Mode can only be D or F")
            except AttributeError as e:
                self.err.error_handle(e)

    def HashDir(self, folder_to_hash="../Misc_Project_Files/test_files"):
        HashDict = []
        file_counter = 0
        for dirpath, subdirs, files in walk(folder_to_hash):
            for file in files:
                self.HashFile(dirpath, file, Mode="D")
                file_counter += 1
                # print("MD5: {0}".format(self.md5.hexdigest()))
                # print("SHA1: {0}".format(self.sha1.hexdigest()))
                HashDict.append({"filename": join(dirpath, file).replace('\\', '/'),
                                 "MD5": self.md5.hexdigest(),
                                 "Sha1": self.sha1.hexdigest(),
                                 "Sha256": self.sha256.hexdigest()})
        with open("../Misc_Project_Files/HashDir_{}.json".format(
                folder_to_hash.split("/")[-1]), "w") as f:
            json.dump(HashDict, fp=f, indent=4)
        # print(json.dumps(HashDict, indent=4))
        print("\n{} total files hashed".format(file_counter))
        print("json dumped to {}".format(f.name))

# TODO: add compare hashes method

