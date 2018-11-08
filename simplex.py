#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from numpy import array, eye, concatenate, zeros, empty, matmul, append, flatnonzero, ones

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
            Q[i,l] = 1/T[l,c]
        else:
            Q[i,l] = -T[i,c]/T[l,c]

    # Retornar Tableau atualizado
    return matmul(Q, T)

# Identificar coluna no Tableau que entra na base.
# Retorna o índice da coluna no Tableau ou -1 se nenhuma coluna atende ao critério.
# Parâmetros:
# T: Tableau Simplex
# N: Lista dos índices não-básicos
# s: Sentido do PL: -1 é maximização e 1 é minimização
def tabEntra(T, N, s):
    # Quantidade de colunas no Tableau
    n = T.shape[1]
    N.sort()
    for i in N:
        # Regra de Bland para evitar ciclagem.
        # Tomar a primeira coluna que apresenta melhora.
        if s * T[0,i + 1] < 0:
            # Custo reduzido da i-ésima coluna melhora a função objetivo
            return i + 1
    # Retorna -1 se nenhum custo reduzido melhora a função objetivo
    return -1

# Identificar linha no Tableau correspondente à coluna que sai base.
# Retorna o índice da linha no Tableau ou -1 se nenhuma linha atende ao critério.
# Parâmetros:
# T: Tableau Simplex
# c: Índice da coluna no Tableau correspondente à direção viável (coluna que entra)
def tabSai(T, c):
    # Quantidade de linhas no Tableau
    m = T.shape[0]
    # Avaliar apenas para os componentes positivos da direção viável
    L = empty(0, dtype=int)
    for i in range(1,m):
        if T[i,c] > 0:
            L = append(L, i)
    # Determinar coluna que sai pelo critério da razão
    if len(L) > 0:
        # Existe componente positivo
        l = L[0]
        if len(L) > 1:
            # Comparar com demais componentes positivos
            for i in L[1:]:
                # Critério da razão
                if T[i,0]/T[i,c] < T[l,0]/T[l,c]:
                    l = i
        return l 
    else:
        # Direção viável melhora mas é ilimitada
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