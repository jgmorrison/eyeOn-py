#! /Users/jmorrison/anaconda2/bin/python

import hashlib
import os
import time
import subprocess
import sys

if len(sys.argv) > 1:
    global filename 
    global filepath 
    filename = sys.argv[1]
    filepath = os.path.abspath(filename)
else:
    print "You must provide a file name to watch as an argument."
    sys.exit()
    
#reset watched file and its hash value to None.
def reset():
    global watched_file
    global hashval_current
    watched_file = None
    hashval_current = None

#update watched file and its hash value.
def update(file):
    global watched_file
    global hashval_current
    watched_file = open(file, "r")
    hashval_current = hashlib.md5(watched_file.read()).digest()

#Check if wathced file hash has changed by opening and rehashing.
def check(file):
    file_new = open(file, "r")
    hashval_new = hashlib.md5(file_new.read()).digest()

    #if hash values differ update watched file hash and reopen file.
    if hashval_new != hashval_current:
        reopen(file)
        subprocess.call(["open", filepath, "--background", "--fresh"])
        update(file)

#reopen the file
def reopen(file):
    if sys.platform == "win-32":
        subprocess.call(["start", filepath])
    elif sys.platform == "darwin":
        subprocess.call(["open", filepath, "--background", "--fresh"])
    update(file)
        
#start the application
def start():
    reset()
    print "started watching file {}".format(filepath)
    update(filepath)
    while True:
        check(filepath)
        #1 second delay between checking hash values.
        time.sleep(1)
    
if __name__=='__main__':
    start()