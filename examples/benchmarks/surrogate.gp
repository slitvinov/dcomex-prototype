set term pngcairo monochrome
set log x
set output "surrogate.png"
set xlabel "number of virtual cores"
set ylabel "efficiency, %"
set key bottom

plot [][0:] "<awk '{t[$1] = $2; print $1, 100 * t[1]/$2/$1}' surrogate.0.dat" u 1:2:xtic(1) w lp pt 4 ps 1.5 lt 1 lw 2 t "surrogate"
