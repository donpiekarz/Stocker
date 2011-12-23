#!/bin/sh

gnuplot << EOF
set term postscript eps color enhanced
set output "stocker.eps"
set timefmt "%Y%m%d"
set xdata time
set multiplot
set origin 0.0, 0.2
set size 1.0, 0.5
plot "$1" u 2:3 w l t "Price"
set origin 0.03, 0.0
set size 0.97, 0.2
unset ytics
unset xtics
plot "$1" u 2:7 w boxes t "Volume"
set origin 0.0, 0.68
set size 1.0, 0.34
set ytics 30
unset xtics
set title "Simulation results with $1"
plot "$1" u 2:8 w boxes t "Buy", "$1" u 2:(-\$9) w boxes t "Sell"
EOF
epstopdf stocker.eps
