#!/bin/sh

echo "Running PRIMITIVE TESTS"

date

echo "-----------------------"

for f in ~/CIDAR/MINT-TestCases/chthesis/*.mint;

do
    echo "Running File $f";
    fluigi $f convert-to-parchmint --outpath ~/Desktop/MINT-to-json/chthesis
    fluigi $f mint-compile --outpath ~/Desktop/MINT-to-par/chthesis
done
