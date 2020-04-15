#!/bin/sh

echo "Running Cassie's Thesis Benchmarks 2D"

for f in ../test/chthesis/*.mint;

do 
	echo "Running File $f";
	python ../cmdline.py $f --outpath ../out
done


echo "Running Cassie's Base Benchmark Set"


for f in ../test/base/*.mint;

do 
	echo "Running File $f";
	python ../cmdline.py $f --outpath ../out
done
