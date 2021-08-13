#!/bin/sh

echo "Place and route the MINT Files"

for f in ~/CIDAR/MINT-TestCases/chthesis/*.mint;

do
    echo "-----------------------"
    echo "`date +"%d-%m-%Y-%T"`";
    echo "Running File $f";
    fluigi $f --out ~/Desktop/MINT-to-par/chthesis
done

echo "-----------------------"
for f in ~/CIDAR/MINT-TestCases/dropx_ref/*.mint;

do
    echo "-----------------------"
    echo "`date +"%d-%m-%Y-%T"`";
    echo "Running File $f";
    fluigi $f --out ~/Desktop/MINT-to-par/dropx
done


echo "-----------------------"
for f in ~/CIDAR/MINT-TestCases/grid/*.mint;

do
    echo "-----------------------"
    echo "`date +"%d-%m-%Y-%T"`";
    echo "Running File $f";
    fluigi $f --out ~/Desktop/MINT-to-par/grid
done
