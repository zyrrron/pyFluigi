#!/bin/sh

echo "Running Cassie's Thesis Benchmarks 2D"

for f in ../test/chthesis/*.mint;

do 
	echo "Running File $f";
	python ../cmdline.py $f -c --outpath ../out
done


echo "Running Cassie's Base Benchmark Set"


for f in ../test/base/*.mint;

do 
	echo "Running File $f";
	python ../cmdline.py $f -c --outpath ../out
done


for f in ../test/constraints/*.mint;

do 
	echo "Running File $f";
	python ../cmdline.py $f -c  --outpath ../out
done


for f in ../test/grid/*.mint;

do 
	echo "Running File $f";
	python ../cmdline.py $f -c --outpath ../out
done


for f in ../test/lfr/*.mint;

do 
	echo "Running File $f";
	python ../cmdline.py $f -c --outpath ../out
done

