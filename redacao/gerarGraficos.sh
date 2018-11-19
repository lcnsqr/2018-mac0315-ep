#!/usr/bin/env bash

rm -rf graficos
mkdir graficos

seq 2 $1 | parallel 'd={}; echo $d; \
../ep.py $d > tabulado_${d}.dat 2> labels_${d}.sed; \
sed -f labels_${d}.sed < template.gnuplot | gnuplot 2>/dev/null; \
inkscape -z -A "graficos/grafico_${d}.pdf" "graficos/grafico_${d}.svg"; \
rm labels_${d}.sed tabulado_${d}.dat graficos/grafico_${d}.svg'
