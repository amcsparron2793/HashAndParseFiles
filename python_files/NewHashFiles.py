"""
NewHashFiles.py

Hashes a given file tree one file at a time.
"""

import hashlib
from os import walk
from os.path import join

"""THIS WORKS PERFECTLY AS IS. """
# BUF_SIZE is totally arbitrary, change for your app!
# BUF_SIZE allows large files to be read in smaller chunks,
# that way a 2GB file doesn't take 2GB of memory
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

md5 = hashlib.md5()
sha1 = hashlib.sha1()
folder = "../Misc_Project_Files/test_files"
file_couter = 0
for dirpath, subdirs, files in walk(folder):
    for file in files:
        with open(join(dirpath, file).replace('\\', '/'), 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)
                #print(os.path.join(dirpath, file))
        print("\nfilename is: {}".format(join(dirpath, file)))
        file_couter += 1
        print("MD5: {0}".format(md5.hexdigest()))
        print("SHA1: {0}".format(sha1.hexdigest()))
    print("\n{} files hashed".format(file_couter))
