#!/bin/sh

echo "Running PRIMITIVE TESTS"

for f in ~/CIDAR/MINT-TestCases/primitive/*.mint;

do
    echo "Runnign File $f";
    fluigi $f --out ~/Desktop/MINT/primitives
done
