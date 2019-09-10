#!/bin/bash

# echo "$PWD$0"
# cat "$PWD$0"

DIRNAME=`readlink -f $0` 
DIRNAME=`dirname $DIRNAME`

echo $DIRNAME
