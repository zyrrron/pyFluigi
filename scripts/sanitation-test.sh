#!/bin/sh

echo "Testing the parchmint Files"

for f in $1/MINT-to-json/chthesis/*.json;

do
    echo "Running File $f";
    python test.py $f
done


for f in $1/MINT-to-json/grid/*.json;

do
    echo "Running File $f";
    python test.py $f
done