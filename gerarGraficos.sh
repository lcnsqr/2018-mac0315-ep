#!/usr/bin/env bash

if [ $1 -lt 2 ]; then
  echo "O fator de discretização deve ser maior que 1"
fi

if [ ! -d graficos ]; then
  mkdir graficos
fi

for d in `seq 2 $1`; do
  echo $d
  ./ep.py $d > tabulado.dat 2> labels.sed
  sed -f labels.sed < template.gnuplot | gnuplot 2>/dev/null
done
rm labels.sed tabulado.dat
