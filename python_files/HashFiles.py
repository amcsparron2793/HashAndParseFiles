"""
HashFiles.py

Hashes a given file tree
"""

# imports
import hashlib
import os
from os import chdir, getcwd, mkdir, walk, listdir
from os.path import join, isdir, isfile
from dependencies import CustomLog_Classes as Clog
from sys import stderr
from random import randint


# noinspection PyAttributeOutsideInit
class HashDirectory:
    def __init__(self):
        try:
            self.err = Clog.Error()
            self.err.error_setup()

            self.hashlist = []
            self.dupelist = []
            self.test_walk_dir = "../Misc_Project_Files/test_files"

        except TypeError as e:
            self.err.error_handle(e)

    def WalkAndHash(self):
        for dirpath, subdir, files in os.walk(self.test_walk_dir):
            #for d in dirpath:
            for file in files:
                # print(file)
                # TODO: create JSON with file name and hash
                try:
                    with open(join(self.test_walk_dir, file.split('.')[0], file).replace('\\', '/'), "rb") as f:
                        #print(f.name)
                        self.hasher = hashlib.sha256(f.read())
                    self.out_hash = self.hasher.hexdigest()

                    if self.out_hash not in self.hashlist:
                        self.hashlist.append(self.out_hash)
                    else:
                        self.dupelist.append(self.out_hash)
                except Exception as e:
                    stderr.write(str(e))
        print("{} unique hashes found".format(len(self.hashlist)))
        print("{} duplicates found".format(len(self.dupelist)))
        # print(self.hashlist)


def MakeTestFiles():
    test_file_dir = "../Misc_Project_Files/test_files"
    namelist = [str(x) for x in range(1, 100)]

    if isdir(test_file_dir):
        chdir(test_file_dir)
    elif not isdir(test_file_dir):
        mkdir(test_file_dir)
        chdir(test_file_dir)

    for name in namelist:
        if not isdir(name):
            mkdir(name)

    for dirs in listdir(getcwd()):
        chdir(dirs)
        for name in namelist:
            rint = randint(1, 1000)
            if not isfile(name + ".txt"):
                with open((name + ".txt"), "w") as f:
                    f.write(dirs + str(rint) + name)
                #print(getcwd())
        chdir('../')


# FIXME: MakeTestFiles makes HashDirectory() fail silently
#MakeTestFiles()
hd = HashDirectory()
hd.WalkAndHash()
