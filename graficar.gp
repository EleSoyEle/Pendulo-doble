set terminal pngcairo size 800,600 enhanced font 'Verdana,12'


set output "grafica.png"
set title "grafica"
set xlabel "Tiempo"
set ylabel "Angulo"
set polar
plot "datos.txt" using 5:1 with lines title "theta vs t",\
"datos.txt" using 5:2 with lines title "phi vs t"

