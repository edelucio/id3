import os
import csv
import sys


def carregar_csv_d_cabecalho(n_arq):
    fpath = os.path.join(os.getcwd(), n_arq)
    fs = csv.reader(open(fpath, newline='\n'))

    linhas = []
    for r in fs:
        linhas.append(r)

    cabecalhos = linhas[0]
    idx_p_nome, nome_p_idx = gerar_mapa_indices(cabecalhos)

    d_cabecalho = {
        'cabecalho': cabecalhos,
        'linhas': linhas[1:],
        'nome_p_idx': nome_p_idx,
        'idx_p_nome': idx_p_nome
    }
    return d_cabecalho


def gerar_mapa_indices(cabecalhos):
    nome_p_idx = {}
    idx_p_nome = {}
    for i in range(0, len(cabecalhos)):
        nome_p_idx[cabecalhos[i]] = i
        idx_p_nome[i] = cabecalhos[i]

    return idx_p_nome, nome_p_idx
    
def valores_unicos(data):
    idx_p_nome = data['idx_p_nome']
    idxs = idx_p_nome.keys()

    v_map = {}
    for idx in iter(idxs):
        v_map[idx_p_nome[idx]] = set()

    for linha in data['linhas']:
        for idx in idx_p_nome.keys():
            n_atr = idx_p_nome[idx]
            val = linha[idx]
            if val not in v_map.keys():
                v_map[n_atr].add(val)
    return v_map


def montar_d_csv(d, colunas_d_csv):
    d_c = list(d['cabecalho'])
    d_l = list(d['linhas'])

    colunas = list(range(0, len(d_c)))

    colunas_d_csv_idx = [d['nome_p_idx'][nome] for nome in colunas_d_csv]
    colunas_removidas = [cidx for cidx in colunas if cidx not in colunas_d_csv_idx]

    for col_del in sorted(colunas_removidas, reverse=True):
        del d_c[col_del]
        for l in d_l:
            del l[col_del]

    idx_p_nome, nome_p_idx = gerar_mapa_indices(d_c)

    return {'cabecalho': d_c, 'linhas': d_l,
            'idx_p_nome': idx_p_nome,
            'nome_p_idx': nome_p_idx}