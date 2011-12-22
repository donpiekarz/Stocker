#!/bin/sh

gnuplot << EOF
set term postscript eps color enhanced
set output "stocker.eps"
set timefmt "%Y%m%d"
set xdata time
set multiplot
set origin 0.0, 0.2
set size 1.0, 0.8
plot "$1" u 2:3 w l
set origin 0.03, 0.0
set size 0.97, 0.2
unset ytics
unset xtics
plot "$1" u 2:7 w boxes
EOF
epstopdf stocker.eps
