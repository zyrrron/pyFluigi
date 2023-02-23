#!/bin/sh

echo "Running PRIMITIVE TESTS"

date

echo "-----------------------"

for f in ~/CIDAR/MINT-TestCases/dropx/*.mint;

do
    echo "Running File $f";
    fluigi $f convert-to-parchmint --outpath ~/Desktop/MINT-to-json/dropx
    fluigi $f mint-compile --outpath ~/Desktop/MINT-to-par/dropx
done
