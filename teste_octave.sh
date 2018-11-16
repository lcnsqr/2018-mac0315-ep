#!/usr/bin/env bash

./ep.py $1 > teste

echo "param.msglev = 1;
param.itlim = 100;

[x, f, status, extra] = glpk(c, A, b, lb, ub, ctype, vartype, s, param);

a = [];
for i = 1:d,
  a(i) = x(2*i-1) - x(2*i);
end;
v = [];
for i = 1:d+1,
  v(i) = x(2*d+i);
end;
s = [];
for i = 1:d+1,
  s(i) = x(3*d+1+i);
end;
f
a
v
s
" >> teste

octave -qW < teste
rm teste
