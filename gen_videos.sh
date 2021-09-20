#!/bin/bash

BASE_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
TARGET_DIR=$BASE_DIR'/videos/'
echo $TARGET_DIR
mkdir -p $TARGET_DIR

cd $BASE_DIR
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
cd -