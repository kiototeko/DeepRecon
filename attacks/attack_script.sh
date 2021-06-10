#! /bin/bash


./flush_reload . > /dev/null 2>&1 &

if [ "$#" -gt 0 ]; then
	python ../defenses/obfuscations/unravel_resnet50.py 2> /dev/null
else
	python ../models/vgg16.py 2> /dev/null
fi

wait
python attack_traces.py


