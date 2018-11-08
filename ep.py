#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from numpy import zeros, array, linspace

from simplex import otimo

from octave import formatOctave

if len(sys.argv) < 2:
    exit("Informe o fator de discretização")

# Fator de discretização (número de intervalos no tempo)
d = int(sys.argv[1])
if d < 1:
    exit("O fator de discretização deve ser maior ou igual a um")

# Intervalo de tempo
T = 10.0

# Intervalo de espaço
X = 1.0

# Tamanho do passo no tempo
p = T/d

# Lado esquerdo das restrições (matriz A)
A = zeros((4*d+4, 5*d+2))

# Restrições originais
for i in range(d):
    # Primeira linha
    # a
    A[2*i,2*i] = p
    A[2*i,2*i+1] = -p
    # v
    A[2*i,2*d+i] = 1
    A[2*i,2*d+i+1] = -1
    # Segunda linha
    # a
    A[2*i+1,2*i] = -p**2
    A[2*i+1,2*i+1] = p**2
    # v
    A[2*i+1,2*d+i+1] = p
    # x
    A[2*i+1,3*d+1+i] = 1
    A[2*i+1,3*d+2+i] = -1

    # Tratamento do módulo
    A[2*d+2*i,2*i] = -1
    A[2*d+2*i,2*i+1] = 1
    A[2*d+2*i,4*d+2+i] = 1
    A[2*d+2*i+1,2*i] = 1
    A[2*d+2*i+1,2*i+1] = -1
    A[2*d+2*i+1,4*d+2+i] = 1

# Restrições de fronteira
# v_0 = 0
A[4*d,2*d] = 1
# v_d = 0
A[4*d+1,3*d] = 1
# x_0 = 0
A[4*d+2,3*d+1] = 1
# x_d = 1
A[4*d+3,4*d+1] = 1

# Lado direito das restrições (vetor b)
b = zeros(4*d+4)
b[-1] = 1

# Comparação das restrições
# 0: Igual a b
# 1: Menor que b
# -1: Maior que b
comp = zeros(4*d+4)
comp[2*d:4*d] = -1

# Sentido do PL
#  1: Minimizar
# -1: Maximizar
s = 1;

# Coeficientes da função objetivo
c = zeros(5*d+2)
c[4*d+2:5*d+2] = 1

# Produzir saída para testar com Octave
#formatOctave(d, A, b, comp, s, c)

y,f,err = otimo(s,c,A,b,comp)
if err != 0:
    # Não foi possível encontrar solução
    if err == 1:
        # Problema inviável
        print("Problema inviável")
    if err == 2:
        # Problema ilimitado
        print("Problema ilimitado")
    if err == 3:
        # Problema auxiliar inviável
        print("Problema auxiliar inviável")
    if err == 4:
        # Problema auxiliar ilimitado
        print("Problema auxiliar ilimitado")
    sys.exit(err)

# Aceleração
a = zeros(d+1)
for i in range(d):
    a[i] = y[2*i] - y[2*i+1] 
# Velocidade
v = y[2*d:3*d+1]
# Distância
x = y[3*d+1:4*d+2]

print("Tempo\tAceleração\tVelocidade\tDistância")
for i in range(d+1):
    print('{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}'.format(i*p, a[i], v[i], x[i]))
