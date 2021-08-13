#!/bin/sh

echo "Running PRIMITIVE TESTS"

date

echo "-----------------------"

for f in ~/CIDAR/MINT-TestCases/primitive/*.mint;

do
    echo "Running File $f";
    fluigi $f -c --out ~/Desktop/MINT-to-json/primitives
    fluigi $f --out ~/Desktop/MINT-to-par/primitives
done
