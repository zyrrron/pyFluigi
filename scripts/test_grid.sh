#!/bin/sh

echo "Running grid TESTS"

date

echo "-----------------------"

FOLDER=out/par/benchmarking_out_"`date +"%d-%m-%Y-%T"`"

echo "Generating results in $FOLDER"


for f in ./Microfluidics-Benchmarks/MINT-TestCases/grid/*.mint;

do
    echo "Runnign File $f";
    fluigi  convert-to-parchmint --outpath "$FOLDER/MINT-to-json/grid" $f
    fluigi  mint-compile --outpath "$FOLDER/MINT-to-par/grid" $f
done
