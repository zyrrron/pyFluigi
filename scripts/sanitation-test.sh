#!/bin/sh

echo "Testing the parchmint Files"

for f in ~/Desktop/MINT-to-json/chthesis/*.json;

do
    echo "Running File $f";
    python test.py $f
done


for f in ~/Desktop/MINT-to-json/grid/*.json;

do
    echo "Running File $f";
    python test.py $f
done