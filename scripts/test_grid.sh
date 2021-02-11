#!/bin/sh

echo "Running grid TESTS"

for f in ~/CIDAR/MINT-TestCases/grid/*.mint;

do
    echo "Runnign File $f";
    fluigi $f -c --out ~/Desktop/MINT-to-json/grid
    fluigi $f --out ~/Desktop/MINT-to-par/grid
done
