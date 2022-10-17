from os import path, remove
import subprocess

filePath = "packages.csv"

with open(filePath) as file:
    for line in file:
        data = line.split(';')

        packageName = data[0]
        packageVersion = data[1]
        packageURL = data[2].replace('@',packageVersion) #implement @ replacement
        packageMD5SUM = data[3]

        cache = packageURL.rsplit('/', 1)[-1]
        print(cache)

        if not path.exists(cache):
            print("Downloading %s." % cache)

            try:
                dest = ['wget', packageURL]
                subprocess.check_call(dest)
            except:
                print("Failed to download %s." % packageURL)
                exit(1)
            try:
                cmd = ['md5sum', cache]
                md5sum = subprocess.check_call(cmd)

                if md5sum != packageMD5SUM: 
                    remove(cache)
                    print("Verification of %s failed! MD5 mismatch!" % cache) #potential man in the middle attack
                    exit(1)
            except:
                print("Error, failed to retrieve md5sum of %s." % cache)
                exit(1)
        else:
            print("%s already exists, skipping." % cache)