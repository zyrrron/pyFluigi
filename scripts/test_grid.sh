#!/bin/sh

echo "Running grid TESTS"

date

echo "-----------------------"

for f in ~/CIDAR/MINT-TestCases/grid/*.mint;

do
    echo "Runnign File $f";
    fluigi $f convert-to-parchmint --outpath ~/Desktop/MINT-to-json/grid
    fluigi $f mint-compile --outpath ~/Desktop/MINT-to-par/grid
done
