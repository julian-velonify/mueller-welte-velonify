#!/bin/sh
# Baut die Seite neu und spiegelt sie in den Preview-Ordner
cd "$(dirname "$0")" && python3 build.py && rsync -a --exclude _src --exclude build.py --exclude sync.sh ./ "$1/"
