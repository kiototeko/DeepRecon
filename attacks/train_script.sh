#! /bin/bash


if [ "$#" -gt 1 ]; then
	echo -n "$2,$1,"
	./flush_reload . > /dev/null 2>&1 &
	python vgg16alt.py $1 $2 2> /dev/null
	wait
	python process_traces.py
else

	kernel_sz=( 3 5 7 )
	channels=( 8 16 32 64 128 256 512 )

	for i in ${kernel_sz[@]}
	do
		for j in ${channels[@]}
		do
			echo -n "$i,$j,"
			./flush_reload . > /dev/null 2>&1 &
			python vgg16alt.py $j $i 2> /dev/null
			wait
			python process_traces.py

		done
	done
fi

