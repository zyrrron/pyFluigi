#!/bin/sh

echo "Converting the MINT Files"

for f in ~/CIDAR/MINT-TestCases/chthesis/*.mint;

do
    echo "Runnign File $f";
    fluigi --c $f --out ~/Desktop/MINT/chthesis
done