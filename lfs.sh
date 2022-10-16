#!/bin/bash

export LFS=/mnt/lfs
export LFS_TARGET=x86_64-lfs-linux-gnu
export LFS_DISK=/dev/sdb

if ! grep -q "$LFS" /proc/mounts; then
    source setup-disk.sh "$LFS_DISK"
    sudo mkdir -pv "$LFS"
    sudo mount -v -t ext4 "${LFS_DISK}2" "$LFS"
    sudo chown -v $USER "$LFS"      #disk ownership to user 
fi

mkdir -pv $LFS/sources  #tarball location
mkdir -pv $LFS/tools    #crosscompiler

#Linux dirs
mkdir -pv $LFS/boot
mkdir -pv $LFS/etc
mkdir -pv $LFS/bin
mkdir -pv $LFS/lib
mkdir -pv $LFS/sbin
mkdir -pv $LFS/usr
mkdir -pv $LFS/var

case $(uname -m) in
    x86_64) mkdir -pv $LFS/lib64 ;;
esac