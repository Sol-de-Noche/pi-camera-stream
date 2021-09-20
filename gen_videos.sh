#!/bin/bash

mkdir -p videos
BASE_DIR=`pwd`
TARGET_DIR=$BASE_DIR'/videos/'
echo $TARGET_DIR

for directory in recording/*; do
    dirname=`basename $directory`
    video_name=$dirname'.mp4'
    echo $directory
    cd $directory
    ls *.jpg | sed "s/^/file '/;s/$/'/" > files.txt
    ffmpeg -y -f concat -i files.txt $TARGET_DIR$video_name
    rm files.txt
    cd -
done;