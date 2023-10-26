#!/bin/sh

echo "Converting the MINT Files"

echo "-----------------------"

FOLDER=out/convert/benchmarking_out_"`date +"%d-%m-%Y-%T"`"

echo "Generating results in $FOLDER"


for f in Microfluidics-Benchmarks/MINT-TestCases/chthesis/hasty.mint;

do
    echo "Runnign File $f";
    fluigi convert-to-parchmint --assign-terminals --generate-graph-view --outpath "$FOLDER/MINT-to-json/chthesis" $f
done

# for f in Microfluidics-Benchmarks/MINT-TestCases/dropx_ref/*.mint;

# do
#     echo "Runnign File $f";
#     fluigi convert-to-parchmint --assign-terminals --generate-graph-view --outpath "$FOLDER/MINT-to-json/dropx_ref" $f
# done

# for f in Microfluidics-Benchmarks/MINT-TestCases/new_grid/grid_02.mint;

# do
#     echo "Runnign File $f";
#     fluigi convert-to-parchmint --assign-terminals --generate-graph-view --outpath "$FOLDER/MINT-to-json/grid" $f
# done

for f in ./Microfluidics-Benchmarks/MINT-TestCases/dropx_ref/*.mint;

do
    echo "Runnign File $f";
    fluigi convert-to-parchmint  --assign-terminals --generate-graph-view --outpath "$FOLDER/MINT-to-json/dropx_ref" $f
done

for f in ./Microfluidics-Benchmarks/MINT-TestCases/grid/*.mint;

do
    echo "Runnign File $f";
    fluigi convert-to-parchmint --assign-terminals --generate-graph-view --outpath "$FOLDER/MINT-to-json/grid" $f
done
