#!/bin/bash

COUNT=`ls df_tuple*.p | wc -w`
((COUNT--))

for i in `seq 0 $COUNT`; do
    NAME='df_tuple'${i}'.p'

    python3 onerep.py $NAME

done

cd reports

rm *.aux
rm *.log
rm *.tex
