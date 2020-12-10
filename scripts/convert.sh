#!/bin/sh

echo "Converting the MINT Files"

for f in ~/CIDAR/pyfluigi/test/chthesis/*.mint;

do
    echo "Runnign File $f";
    fluigi --c $f --out ~/Desktop/MINT/chthesis
done