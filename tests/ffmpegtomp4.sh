#!/bin/bash
FILES=*.h264
for filename in $FILES; do
    ffmpeg -loglevel info -f h264 -y -i ${filename} -vcodec copy -r 25 ${filename%.*}.mp4
done
