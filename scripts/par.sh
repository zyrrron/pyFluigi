#!/bin/sh

echo "Place and route the MINT Files"

for f in ~/CIDAR/MINT-TestCases/chthesis/*.mint;

do
    echo "Runnign File $f";
    fluigi $f --out ~/Desktop/MINT-to-par/chthesis
done

for f in ~/CIDAR/MINT-TestCases/grid/*.mint;

do
    echo "Runnign File $f";
    fluigi $f --out ~/Desktop/MINT-to-par/grid
done