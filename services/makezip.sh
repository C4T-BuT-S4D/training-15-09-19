#!/bin/bash

ZIPNAME=services.zip

find "kekustotal/" -type f | zip -@ "$ZIPNAME"
find "alikekspress/" -type f | zip -@ "$ZIPNAME"
find "kekloud-platform/" -type f | grep -v "vm/" | zip -@ "$ZIPNAME"
