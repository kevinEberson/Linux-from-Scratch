#!/bin/bash
#use check_call check_output of py + use parted

cat packages.csv | while read line; do
echo "$line"
    NAME=echo "$line" | cut -d, -f1
    # VERSION="'echo $line | cut -d\; -f2'"
    # URL="'echo $line | cut -d\; -f3 | sed "s/@/$version/g"'"
    # MD5SUM="'echo $line | cut -d\; -f4'"

    echo "name: $NAME" 
    #, version: ${VERSION}, url: ${URL}, md5sum: ${MD5SUM}"

    CACHEFILE="$(basename "$URL")"

    if [ ! -f "$CACHEFILE" ]; then
        echo "Downloading $URL"
        #wget "$URL"
        if ! echo "$MD5SUM $CHACHEFILE" | md5sum -c > /dev/null; then
            rm -f "$CACHEFILE"
            echo "Verification of ${CHACHEFILE}failed! MD5 mismatch!"
            exit 1
        fi
    fi
done
