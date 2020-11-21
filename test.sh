#!/bin/bash
export OUTPUT_FILE="output.csv"
echo $OUTPUT_FILE

touch $OUTPUT_FILE

for a in {1..5} # test deleteMoves
do
	python3 GeoGame.py -na -ng -deleteMoves $a >> $OUTPUT_FILE
done
