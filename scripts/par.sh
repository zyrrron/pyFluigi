#!/bin/sh

echo "Place and route the MINT Files"
echo "-----------------------"

FOLDER=out/par/benchmarking_out_"`date +"%d-%m-%Y-%T"`"

echo "Generating results in $FOLDER"

for f in ./Microfluidics-Benchmarks/MINT-TestCases/chthesis/*.mint;

do
    echo "-----------------------"
    echo "`date +"%d-%m-%Y-%T"`";
    echo "Running File $f";
    fluigi  --outpath "$FOLDER/MINT-to-par/chthesis" $f
done

echo "-----------------------"
for f in ./Microfluidics-Benchmarks/MINT-TestCases/dropx_ref/*.mint;

do
    echo "-----------------------"
    echo "`date +"%d-%m-%Y-%T"`";
    echo "Running File $f";
    fluigi  --outpath "$FOLDER/MINT-to-par/dropx" $f
done


echo "-----------------------"
for f in ./Microfluidics-Benchmarks/MINT-TestCases/grid/*.mint;

do
    echo "-----------------------"
    echo "`date +"%d-%m-%Y-%T"`";
    echo "Running File $f";
    fluigi  --outpath "$FOLDER/MINT-to-par/grid" $f
done
