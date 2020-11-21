#!/bin/bash
export OUTPUT_FILE="output.csv"
echo $OUTPUT_FILE

touch $OUTPUT_FILE

mc 1 5
ps 1 100 by 5

for d in {3..9} # test deleteMoves
do
	for pk in {1..33..3} # test percentKeep
	do
		for mc in {1..5} # test mutationChance
		do
			for ps in {1..100..5} # test populationSize
			do
				#test each 10 times

				#also print out vars
				python3 GeoGame.py -g -d $a -pk $(bc <<< $pk/100) -mc $(bc <<< $mc/100) -ps $ps >> $OUTPUT_FILE
			done
		done
	done
done
