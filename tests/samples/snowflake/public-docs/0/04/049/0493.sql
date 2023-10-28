SELECT x1.i x1_i, 
       x2.i x2_i,
       x1.i=x2.i, 
       iff(x1.i=x2.i, 'Selected', 'Not') "SELECT IF X1.I=X2.I",
       x1.i<>x2.i, 
       iff(not(x1.i=x2.i), 'Selected', 'Not') "SELECT IF X1.I<>X2.I"
    FROM x x1, x x2;