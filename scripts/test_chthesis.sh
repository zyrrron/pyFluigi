#!/bin/sh

echo "Running PRIMITIVE TESTS"

for f in ~/CIDAR/MINT-TestCases/chthesis/*.mint;

do
    echo "Running File $f";
    fluigi $f -c --out ~/Desktop/MINT-to-json/chthesis
    fluigi $f --out ~/Desktop/MINT-to-par/chthesis
done
