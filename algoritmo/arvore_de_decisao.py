import ast
import csv
import sys
import math
import os

class Id3:
    uniqs = None
    atributo_alvo = None

    def __init__(self, uniqs, atributo_alvo):
        self.uniqs = uniqs
        self.atributo_alvo = atributo_alvo

    def get_rotulo_comum(self, rotulos):
        rc = max(rotulos, key=lambda k: rotulos[k])
        return rc

    def get_rotulos(self, d, atributo_alvo):
        linhas = d['linhas']

        col_idx = d['nome_p_idx'][atributo_alvo]
        rotulos = {}

        for linha in linhas:
            val = linha[col_idx]
            if val in rotulos:
                rotulos[val] = rotulos[val] + 1
            else:
                rotulos[val] = 1
        return rotulos

    def entropia_calc(self, n, rotulos):
        ent = 0
        for label in rotulos.keys():
            p_x = rotulos[label] / n
            ent += - p_x * math.log(p_x, 2)
        return ent

    def media_ent_particoes(self, d, at_sep, atributo_alvo):
        linhas = d['linhas']
        l = len(linhas)
        particoes = self.montar_particao(d, at_sep)
        media_ent = 0

        for cp in particoes.keys():
            part = particoes[cp]
            n_part = len(part['linhas'])
            
            rotulos_part = self.get_rotulos(part, atributo_alvo)
            ent_part = self.entropia_calc(n_part, rotulos_part)
            media_ent += n_part / l * ent_part

        return media_ent, particoes

    def montar_particao(self, d, at_sep):
        particoes = {}
        linhas = d['linhas']
        atr_particao_idx = d['nome_p_idx'][at_sep]
        for linha in linhas:
            v_linha = linha[atr_particao_idx]
            if v_linha not in particoes.keys():
                particoes[v_linha] = {
                    'nome_p_idx': d['nome_p_idx'],
                    'idx_p_nome': d['idx_p_nome'],
                    'linhas': list()
                }
            particoes[v_linha]['linhas'].append(linha)
        return particoes

    def montar_id3(self, d, atributos_sep):
        rotulos = self.get_rotulos(d, self.atributo_alvo)
        no = {}

        if len(rotulos.keys()) == 1:
            no['rotulo'] = next(iter(rotulos.keys()))
            return no

        if len(atributos_sep) == 0:
            no['rotulo'] = self.get_rotulo_comum(rotulos)
            return no

        gim = None
        gim_atr = None
        gim_part = None
        l = len(d['linhas'])
        ent = self.entropia_calc(l, rotulos)

        for at_sep in atributos_sep:
            media_ent, particoes = self.media_ent_particoes(d, at_sep, self.atributo_alvo)
            gi = ent - media_ent
            if gim is None or gi > gim:
                gim = gi
                gim_atr = at_sep
                gim_part = particoes

        if gim is None:
            no['rotulo'] = self.get_rotulo_comum(rotulos)
            return no

        no['atributo'] = gim_atr
        no['nos'] = {}

        atributos_sep_sub_arv = set(atributos_sep)
        atributos_sep_sub_arv.discard(gim_atr)

        atrs_uniq = self.uniqs[gim_atr]

        for atr in atrs_uniq:
            if atr not in gim_part.keys():
                no['nos'][atr] = {'rotulo': self.get_rotulo_comum(rotulos)}
                continue
            partition = gim_part[atr]
            no['nos'][atr] = self.montar_id3(partition, atributos_sep_sub_arv)

        return no
    
    def exibir_id3(self, arvore, atr_alvo):
        p_array = []
        set_regras = set()

        def traverse(no, p_array, set_regras):
            if 'rotulo' in no:
                p_array.append(' o ' + atr_alvo + ' É ' + no['rotulo'])
                set_regras.add(''.join(p_array))
                p_array.pop()
            elif 'atributo' in no:
                strif = 'SE ' if not p_array else ' E '
                p_array.append(strif + no['atributo'] + ' IGUAL ')
                for n in no['nos']:
                    p_array.append(n)
                    traverse(no['nos'][n], p_array, set_regras)
                    p_array.pop()
                p_array.pop()

        traverse(arvore, p_array, set_regras)
        print(os.linesep.join(set_regras))

        pass
    
    def realizar_predicao(self, inputs, id3):
        predicao = ''
        renda = self.get_renda(int(inputs[0]))
        garantia = inputs[1]
        divida = inputs[2]
        historiaCredito = inputs[3]

        for n in id3['nos']:
            if n == renda:
                predicao += 'SE a renda for ' + renda
                if 'atributo' in id3['nos'][n]:
                    predicao += ' e a HISTORIA DE CREDITO for ' + historiaCredito
                    for i in id3['nos'][n]['nos']:
                        if i == historiaCredito:
                            if 'atributo' in id3['nos'][n]['nos'][i]:
                                for j in id3['nos'][n]['nos'][i]['nos']:
                                    predicao += ' o RISCO é ' + id3['nos'][n]['nos'][i]['nos'][j]['rotulo']
                                    break
                            else:
                                predicao += ' o RISCO é ' + id3['nos'][n]['nos'][historiaCredito]['rotulo']
                                break
                else:
                    predicao += ' o RISCO é ' + id3['nos'][n]['rotulo'] 
        return predicao

    def get_renda(self, renda):
        if renda > 35000:
            renda = 'acima_de_$35mil'
        elif renda <= 35000 and renda >= 15000:
            renda = '$15_a_$35mil'
        else:
            renda = '$0_a_$15mil'

        return renda
