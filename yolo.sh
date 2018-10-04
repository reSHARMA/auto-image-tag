#!/bin/bash

set -x

OUTPUT=`bash test.sh`
OUTPUT=`sed 's/\.//g' <<< $OUTPUT`
OUTPUT=`sed 's/\%//g' <<< $OUTPUT`
OUTPUT=`sed 's/://g' <<< $OUTPUT`

if test $# -eq 2; then
	OUTPUT=`darknet/darknet cfg/yolov3.cfg yolov3.weights static/img/$1.jpeg`
fi

echo `awk '{split($0, a, "seconds"); print a[2]}' <<< $OUTPUT`
