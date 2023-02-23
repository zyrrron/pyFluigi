#!/bin/sh

echo "Running PRIMITIVE TESTS"

date

echo "-----------------------"

for f in ~/CIDAR/MINT-TestCases/primitive/*.mint;

do
    echo "Running File $f";
    fluigi $f convert-to-parchmint --outpath ~/Desktop/MINT-to-json/primitives
    fluigi $f mint-compile --outpath ~/Desktop/MINT-to-par/primitives
done
