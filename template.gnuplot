set terminal svg size 800,400 enhanced font "sans-serif,14"

set title "Discretização em %d% intervalos\nGasto ótimo: %f%" font ",22" tc rgb "#606060"
#set ylabel "Speed Up"
set xlabel "Tempo discretizado"
set key autotitle columnhead
set key outside
set xtics nomirror right rotate by 45 offset 0,0
set border back

set ytic scale 0
set xtic scale 1
set grid ytics lc rgb "#505050" lw 1
set grid xtics lc rgb "#505050" lw 1

set yrange [-0.4:0.4]

# Aceleração
set style line 1 linecolor rgb '#dc0000' linetype 1 linewidth 2 pointtype 7 pointsize 1
# Velocidade
set style line 2 linecolor rgb '#009100' linetype 1 linewidth 2 pointtype 8 pointsize 1 dt 2
# Deslocamento
set style line 3 linecolor rgb '#0084c8' linetype 1 linewidth 2 pointtype 9 pointsize 1

set decimalsign locale

set output 'graficos/grafico_%d%.svg'
#plot "tabulado.dat" u 2:xtic(1) w lp linestyle 1, "" u 3 w lp linestyle 2, "" u 4 w lp linestyle 3
#plot "tabulado.dat" u 2:xtic(1) w lp linestyle 1
plot "tabulado.dat" u 2:xtic(1) w lp linestyle 1, "" u 3 w lp linestyle 2
