#!/bin/bash
COUNTER=0
#iterate through all 9 classes
for i in 0 1 2 3 4 5 6 7 8 9; do
	#iterate through all files in the directory
	for f in /mnt/c/Users/Linus/Documents/NMNIST/Train/${i}/*.bin; do 
		OUTFILE=/mnt/c/Users/Linus/Documents/NMNIST/TrainF/${i}/${COUNTER}.txt
		#check if directory exists
		if test ! -d "/mnt/c/Users/Linus/Documents/NMNIST/TrainF/${i}"; then
			mkdir /mnt/c/Users/Linus/Documents/NMNIST/TrainF/${i}
		fi

		#check if file exists
		if test ! -f "$OUTFILE"; then
			touch $OUTFILE
		fi

		#run the data_setup code with 
		./a.out $f $OUTFILE
		echo $OUTFILE completed

		#increment counter
		COUNTER=$[$COUNTER+1]
	done
	#reset the counter
	COUNTER=0
done
echo "COMPLETE!"