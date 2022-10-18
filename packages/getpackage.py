from os import path, remove
import subprocess
import hashlib

filePath = "packages.csv"

with open(filePath) as file:
    for line in file:
        data = line.split(';')

        packageName = data[0]
        packageVersion = data[1]
        packageURL = data[2].replace('@',packageVersion) #implement @ replacement
        packageMD5SUM = data[3].rstrip()

        cache = packageURL.rsplit('/', 1)[-1]
        #print(cache)

        if not path.exists(cache):
            print("Downloading %s." % cache)

            try:
                dest = ['wget', packageURL]
                subprocess.check_call(dest)
            except:
                print("Failed to download %s." % packageURL)
                exit(1)
     
            with open(cache, 'rb') as downloadedFile:
                data = downloadedFile.read()    
                returnedMD5SUM = hashlib.md5(data).hexdigest()
            
            if returnedMD5SUM != packageMD5SUM:
                remove(cache)
                print("Verification of %s failed! MD5 mismatch!" % cache) #potential man in the middle attack
                print("expected MD5: %s, got: %s." % (packageMD5SUM, returnedMD5SUM))
                exit(1)

        else:
            print("%s already exists, skipping." % cache)