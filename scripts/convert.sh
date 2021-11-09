#!/bin/sh

echo "Converting the MINT Files"

for f in ~/CIDAR/MINT-TestCases/chthesis/*.mint;

do
    echo "Runnign File $f";
    fluigi convert-to-parchmint $f --assign-terminals --generate-graph-view --outpath ~/Desktop/MINT-to-json/chthesis
done

for f in ~/CIDAR/MINT-TestCases/dropx_ref/*.mint;

do
    echo "Runnign File $f";
    fluigi convert-to-parchmint $f --assign-terminals --generate-graph-view --outpath ~/Desktop/MINT-to-json/dropx_ref
done

for f in ~/CIDAR/MINT-TestCases/grid/*.mint;

do
    echo "Runnign File $f";
    fluigi convert-to-parchmint $f --assign-terminals --generate-graph-view --outpath ~/Desktop/MINT-to-json/grid
done