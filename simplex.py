#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy

from numpy import array, eye, concatenate, zeros, empty, matmul, append, flatnonzero, ones

# O arredondamento dos resultados pode não produzir zero, mas um valor ínfimo que deve ser tratado 
# como zero, pois pode quebrar o algoritmo (seria zero não fosse o erro de arredondamento da máquina).
INFIMO = 1e-12

# Trocar coluna básica por coluna não-básica no Tableau.
# Retorna o Tableau atualizado.
# Parâmetros:
# T: Tableau Simplex
# l: Linha do Tableau correspondente à coluna básica que sai
# c: Coluna do Tableau correspondente à coluna não-básica que entra
def tabTrocar(T, l, c):
    # Quantidade de linhas no Tableau
    m = T.shape[0]
    # Matriz de conversão
    Q = eye(m)
    for i in range(m):
        if i == l:
            # Inverso do pivô, resultará em 1.
            Q[i,l] = 1/T[l,c]
        else:
            # Componente da solução básica dividida pela componente correspondente 
            # na coluna que entra (negativo). Resultará em zero.
            Q[i,l] = -T[i,c]/T[l,c]

    # Retornar Tableau atualizado pela matriz de conversão Q
    return matmul(Q, T)

# Identificar coluna no Tableau que entra na base.
# Retorna o índice da coluna no Tableau ou -1 se nenhuma coluna atende ao critério.
# Parâmetros:
# T: Tableau Simplex
# N: Lista dos índices não-básicos
# s: Sentido do PL: -1 é maximização e 1 é minimização
def tabEntra(T, N, s):
    # Quantidade de colunas no Tableau.
    n = T.shape[1]
    # Regra de Bland para evitar ciclagem.
    # Ordenar o conjunto dos índices não-básicos.
    N.sort()
    # Percorrer o vetor de custos reduzidos, na primeira 
    # linha do Tableau e a partir da segunda coluna.
    for i in N:
        # Pela ordem, verificar se algum custo reduzido melhora a função objetivo.
        if s * T[0,i + 1] < 0 and abs(T[0,i + 1]) > INFIMO:
            # Custo reduzido da i-ésima coluna melhora a função objetivo.
            return i + 1
    # Retorna -1 se nenhum custo reduzido melhora a função objetivo
    return -1

# Identificar linha no Tableau correspondente à coluna que sai base.
# Retorna o índice da linha no Tableau ou -1 se nenhuma linha atende ao critério.
# Parâmetros:
# T: Tableau Simplex
# c: Índice da coluna no Tableau correspondente à direção viável (coluna que entra)
def tabSai(T, c):
    # Quantidade de linhas no Tableau.
    m = T.shape[0]
    # Avaliar apenas para os componentes positivos da direção viável.
    # Conjunto L armazena os índices das linhas onde o valor da direção viável é positivo.
    L = empty(0, dtype=int)
    for i in range(1,m):
        # Incluir valor positivo
        if T[i,c] > INFIMO:
            L = append(L, i)
    # Determinar coluna que sai pelo critério da razão, usando 
    # como denominador os valores positivos da direção viável.
    if len(L) > 0:
        # Existe pelo menos uma componente positiva na direção.
        # É o índice escolhido se não houverem outros.
        l = L[0]
        # Comparar com demais componentes positivas (se houverem).
        if len(L) > 1:
            for i in L[1:]:
                # Trocar o índice escolhido se satisfizer o critério da razão.
                if T[i,0]/T[i,c] < T[l,0]/T[l,c]:
                    l = i
        return l 
    else:
        # Não existe componente positiva.
        # Direção viável melhora mas é ilimitada
        print(T[:,c])
        return -1

# Iterar no Tableau até um critério de parada.
# Retorna o Tableau final, lista de índices básicos e não básicos e o erro (0: Sem erro, 2: Problema ilimitado)
# Parâmetros:
# T: Tableau Simplex
# B: Lista inicial de índices básicos
# N: Lista inicial de índices não-básicos
# s: Sentido do PL: -1 é maximização e 1 é minimização
def tabRodar(T, B, N, s):
    # Identificar coluna no Tableau que entra na base
    c = tabEntra(T, N, s)
    while c > 0:
        # Converter para índice da nova variável básica
        k = c - 1
        l = tabSai(T, c)
        if l > 0:
            # Trocar base
            T = tabTrocar(T, l, c)
            # Atualizar lista de índices não-básicos
            N[N.index(k)] = B[l - 1]
            # Atualizar lista de índices básicos
            B[l - 1] = k
            # Procurar outra direção viável
            c = tabEntra(T, N, s)
        else:
            # Problema ilimitado
            return T, B, N, 2
    # Solução ótima encontrada
    return T, B, N, 0

def otimo(s,c,A,b,comp):
    # Quantidade de linhas na matriz de restrições
    m = A.shape[0]
    # Quantidade de colunas na matriz de restrições
    n = A.shape[1]
    # Identificar componentes negativas de b
    for i in range(m):
        if b[i] < 0:
            # Trocar sinal da componente de b
            b[i] = b[i] * -1
            # Trocar o sinal da linha de A correspondente
            A[i,:] = A[i,:] * -1
            # Trocar comparação
            comp[i] = comp[i] * -1
    # Incluir variáveis de folga nas desigualdades
    slack = 0
    for i in range(len(comp)):
        if comp[i] != 0:
            A = concatenate((A, comp[i] * eye(m)[i,:].reshape(-1,1)), axis=1)
            c = append(c, 0)
            slack = slack + 1
    # Construir Tableau do problema auxiliar
    T_aux = empty((1+m, 1+n+slack+m))
    # Valor da função objetivo:
    T_aux[0,0] = -matmul(ones((1, m)), b)[0]
    # Variáveis ativas da solução:
    T_aux[1:,0] = b
    # Colunas correspondentes às direções viáveis e não viáveis:
    T_aux[1:,1:] = concatenate((A, eye(m)), axis=1)
    # Lista dos índices das variáveis não-básicas
    N_aux = range(n+slack)
    # Lista dos índices das variáveis básicas
    B_aux = range(n+slack, n+slack+m)
    # Custos reduzidos do problema auxiliar:
    c_aux = zeros(n+slack+m)
    c_aux[n+slack:] = 1
    T_aux[0,1:] = c_aux - matmul(c_aux[B_aux], T_aux[1:,1:])
    # Encontrar uma solução viável:
    T_aux, B_aux, N_aux, err = tabRodar(T_aux, B_aux, N_aux, 1)
    if err != 0:
        # Não foi possível encontrar solução do problema auxiliar
        return T_aux[1:,0], T_aux[0,0], err + 2
    # Construir Tableau do problema original
    T = T_aux[:,:-m]
    # Índices básicos permanecem
    B = B_aux
    # Remover índices não-básicos auxiliares
    N_aux.sort()
    N = N_aux[:-m]
    # Valor da função objetivo:
    T[0,0] = -matmul(c[B], b)
    # Custos reduzidos:
    T[0,1:] = c - matmul(c[B], T[1:,1:])
    # Encontrar solução ótima do problema original:
    T, B, N, err = tabRodar(T, B, N, s)
    if err != 0:
        # Não foi possível encontrar solução do problema original
        return T_aux[1:,0], T_aux[0,0], err
    # Compor solução a partir das variáveis ativas
    x = zeros(n)
    for i in range(m):
        # Ignorar variáveis de folga na base
        if B[i] < n:
            x[B[i]] = T[1+i,0]
    return x, -T[0,0], err
