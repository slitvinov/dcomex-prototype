set term svg size 400, 660 font 'Arial, 12' background rgb 'white'
set macros
set output "bio.svg"
f(k) = sprintf("<awk '$1 == %g' bio.dat", k)
set key left
set xlabel "shear modulus, kPa"
set ylabel "tumor volume, 10^{-6} m^3"
kl = "growth rate, 1/days: "
u = 'i = i + 1, f(k) u 2:($3*1e6) w lp lt 1 lc "black" pt i t sprintf("%s%.2f", kl, k), kl = ""'
i = 0
plot [0:][0:] \
k = 0.1, @u, \
k = 0.15, @u, \
k = 0.2, @u, \
k = 0.25, @u, \
k = 0.3, @u, \
k = 0.35, @u
