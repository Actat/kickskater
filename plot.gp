#!/usr/bin/gnuplot

pos_csv = 'output.csv'

set datafile separator ','

set term pdfcairo font 'Times, 8' size 7.5 cm, 5.0 cm
set output 'output.pdf'

n_row = 3
n_col = 1
margin_t = 0.01
margin_b = 0.08
margin_v = 0.09
margin_r = 0.01
margin_l = 0.09
margin_h = 0.09
height = (1. - margin_t - margin_b - margin_v * (n_row - 1)) / n_row
width = (1. - margin_l - margin_r - margin_h * (n_col - 1)) / n_col
lm(row, col) = margin_l + (col - 1.) * (width + margin_h)
rm(row, col) = lm(row, col) + width
tm(row, col) = 1. - margin_t - (row - 1.) * (height + margin_v)
bm(row, col) = tm(row, col) - height
set multiplot
do for [i = 1:n_row]{
    do for [j = 1:n_col]{
        set lmargin screen lm(i, j)
        set rmargin screen rm(i, j)
        set tmargin screen tm(i, j)
        set bmargin screen bm(i, j)

        if (i == 1 && j == 1){
            plot \
                pos_csv u 1:2 w p ps 0.1 pt 7 t 'x', \
                pos_csv u 1:3 w p ps 0.1 pt 7 t 'y', \
                pos_csv u 1:4 w p ps 0.1 pt 7 t 'z'
        }
        if (i == 2 && j == 1) {
            plot \
                pos_csv u 1: 9 w p ps 0.1 pt 7 t 'Roll', \
                pos_csv u 1:10 w p ps 0.1 pt 7 t 'Pitch', \
                pos_csv u 1:11 w p ps 0.1 pt 7 t 'Yaw'
        }
        if (i == 3 && j == 1) {
            plot \
                pos_csv u 1:13 w p ps 0.1 pt 7 t 'Flywheel angle'
        }
    }
}
