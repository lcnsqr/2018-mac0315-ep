#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Construção do problema apresentado no enunciado do EP.
# A discretização é feita a partir de um valor inteiro informado 
# na linha de comando, chamado fator de discretização. O fator de
# discretização deve ser maior ou igual a 2.
# Por exemplo, se o comando for invocado na forma
#   ./ep.py 4
# então o tempo será discretizado em 4 partes. Assim, tomando d = 4, as funções 
# aceleração a(t), velocidade v(t) e distância x(t) estarão discretizadas
# em três vetores, "a", "v" e "x", cada um com 5 (d+1) componentes. 
# Seja "T" o intervalo de tempo analisado, então a relação entre a discretização 
# e o problema contínuo será:
#   a_i = a(i*T/d)
#   v_i = v(i*T/d)
#   x_i = x(i*T/d)
# onde o "i" é um índice de 0 a d.

import sys
import numpy as np

# O algoritmo Simplex está implementado no arquivo simplex.py
from simplex import otimo

# O fator de discretização deve ser informado como parâmetro para o programa.
if len(sys.argv) < 2:
    exit("Informe o fator de discretização")

# d: fator de discretização (número de intervalos no tempo).
# É a partir deste parâmetro que todas as demais dimensões são computadas.
d = int(sys.argv[1])
if d < 2:
    exit("O fator de discretização deve ser maior ou igual a 2")

# Intervalo de tempo
T = 10.0

# Intervalo de espaço
X = 1.0

# Tamanho do passo no tempo
p = T/d

# Lado esquerdo das restrições (matriz A)
A = np.zeros((4*d+4, 5*d+2))

# Restrições originais do problema
for i in range(d):
    # Primeira linha do i-ésimo par de restrições
    # a
    A[2*i,2*i] = p
    A[2*i,2*i+1] = -p
    # v
    A[2*i,2*d+i] = 1
    A[2*i,2*d+i+1] = -1
    # Segunda linha do i-ésimo par de restrições
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
b = np.zeros(4*d+4)
# Apenas a componente correspondente a x_d é igual a 1 (as demais são zero).
b[-1] = 1

# Comparação das restrições
# 0: Igual a b
# 1: Menor que b
# -1: Maior que b
comp = np.zeros(4*d+4)
comp[2*d:4*d] = -1

# Sentido do PL
#  1: Minimizar
# -1: Maximizar
s = 1;

# Coeficientes da função objetivo
c = np.zeros(5*d+2)
c[4*d+2:5*d+2] = 1

# Encontrar a variável y que minimiza o PL e o valor ótimo f
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

# Compor os vetores de interesse a partir da solução encontrada
# Aceleração: Vetor "a"
a = np.zeros(d+1)
for i in range(d):
    # Reunir parte positiva e negativa da variável irrestrita
    a[i] = y[2*i] - y[2*i+1] 
# Velocidade: Vetor "v"
v = y[2*d:3*d+1]
# Distância: Vetor "x"
x = y[3*d+1:4*d+2]

# Exibir o resultado em quatro colunas: t, a(t), v(t), x(t)
print("t\ta(t)\tv(t)\tx(t)")
for i in range(d+1):
    print('{:.2f}\t{:.6f}\t{:.6f}\t{:.6f}'.format(i*p, a[i], v[i], x[i]).replace('.', ','))
# Valor ótimo da função objetivo.
# Soma dos valores absolutos do vetor "a"
f = 0
for i in range(d):
    f = f + abs(a[i])

# Para confecção dos gráficos
print >> sys.stderr, 's/%d%/{:d}/g\ns/%f%/{:.3f}/g'.format(d, f).replace('.', ',')
