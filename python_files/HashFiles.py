"""
HashFiles.py

Hashes a given file tree one file at a time.
"""

import hashlib
import json
from os import walk
from os.path import join


class HashDirectory:
    def __init__(self, BUFF_SIZE=65536):
        # BUF_SIZE is totally arbitrary, change for your app!
        # BUF_SIZE allows large files to be read in smaller chunks,
        # that way a 2GB file doesn't take 2GB of memory
        self.BUFF_SIZE = BUFF_SIZE  # default is lets read stuff in 64kb chunks!

        # TODO: choose option for algorithm
        self.md5 = hashlib.md5()
        self.sha1 = hashlib.sha1()
        self.sha256 = hashlib.sha256()

    def HashDir(self, folder_to_hash="../Misc_Project_Files/test_files"):
        HashDict = []
        file_counter = 0
        for dirpath, subdirs, files in walk(folder_to_hash):
            for file in files:
                with open(join(dirpath, file).replace('\\', '/'), 'rb') as f:
                    while True:
                        data = f.read(self.BUFF_SIZE)
                        if not data:
                            break
                        self.md5.update(data)
                        self.sha1.update(data)
                        self.sha256.update(data)
                        # print(os.path.join(dirpath, file))
                #print("\nfilename is: {}".format(join(dirpath, file)))
                file_counter += 1
                #print("MD5: {0}".format(self.md5.hexdigest()))
                #print("SHA1: {0}".format(self.sha1.hexdigest()))
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
