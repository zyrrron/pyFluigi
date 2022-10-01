#!/bin/sh

echo "Running PRIMITIVE TESTS"

date

echo "-----------------------"

for f in ~/CIDAR/MINT-TestCases/dropx/*.mint;

do
    echo "Running File $f";
    fluigi $f -c --out ~/Desktop/MINT-to-json/dropx
    fluigi $f --out ~/Desktop/MINT-to-par/dropx
done
