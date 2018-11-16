#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Gerar saída para testar no Octave
import sys

def formatOctave(d, A, b, comp, s, c):
    print("d = "+str(d)+";")

    # Coeficientes
    sys.stdout.write("c = [")
    for i in range(c.shape[0]):
        sys.stdout.write(str(c[i]))
        if i < c.shape[0] - 1:
            sys.stdout.write(",")
    sys.stdout.write("]\';\n")

    # Matriz A
    sys.stdout.write("A = [")
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            sys.stdout.write(str(A[i][j]))
            if j < A.shape[1] - 1:
                sys.stdout.write(",")
        if i < A.shape[0] - 1:
            sys.stdout.write(";\n")
    sys.stdout.write("];\n")

    sys.stdout.write("b = [")
    for i in range(b.shape[0]):
        sys.stdout.write(str(b[i]))
        if i < b.shape[0] - 1:
            sys.stdout.write(",")
    sys.stdout.write("]\';\n")

    sys.stdout.write("lb = [")
    for i in range(c.shape[0]):
        sys.stdout.write(str(0))
        if i < c.shape[0] - 1:
            sys.stdout.write(",")
    sys.stdout.write("]\';\n")

    print("s = 1;")
    print("ub = [];")

    sys.stdout.write("ctype = \"")
    for i in range(len(comp)):
        if ( comp[i] == 0 ):
            sys.stdout.write("S")
        else:
            sys.stdout.write("L")
    sys.stdout.write("\";\n")

    sys.stdout.write("vartype = \"")
    for i in range(c.shape[0]):
        sys.stdout.write("C")
    sys.stdout.write("\";\n")
