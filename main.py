import os
import utils.config as uc
import utils.csv as ucsv
import algoritmo.arvore_de_decisao as ad

class MainProgram:
    d_config = None
    atr_alvo = None
    id3 = None
    arvore = None
    menu_actions = None

    def __init__(self):
        self.d_config = uc.carregar_config_csv('csv.cfg')
        self.atr_alvo = self.d_config['target']
        
        d_csv = ucsv.carregar_csv_d_cabecalho(self.d_config['csv_file'])
        d_csv = ucsv.montar_d_csv(d_csv, self.d_config['csv_columns'])
        
        atributos_separados = set(d_csv['cabecalho'])
        atributos_separados.remove(self.atr_alvo)
        
        self.id3 = ad.Id3(ucsv.valores_unicos(d_csv), self.atr_alvo)
        self.arvore = self.id3.montar_id3(d_csv, atributos_separados)

        self.menu_actions = { 'main_menu': self.main_menu, '1': self.exibir_arvore, '2': self.predicao_menu, '3': self.exit }

    def exibir_arvore(self):
        self.id3.exibir_id3(self.arvore, self.atr_alvo)
        self.main_menu(False)
        return

    def main_menu(self, clear):
        if clear:
            os.system('clear')
        
        print('\nBem vindo,\n')
        print('Selecione a opção desejada:')
        print('1. Exibir árvore de decisão')
        print('2. Realizar predição')
        print('\n3. Sair')
        choice = input(' >>  ')
        self.exec_menu(choice)
    
        return
    
    def exec_menu(self, choice):
        os.system('clear')
        ch = choice.lower()
        if ch == '':
            self.menu_actions['main_menu'](True)
        else:
            try:
                self.menu_actions[ch]()
            except KeyError:
                self.menu_actions['main_menu'](True)
        return
    
    def exit(self):
        exit()
        return

    def back(self):
        self.menu_actions['main_menu']()

    def predicao_menu(self):
        os.system('clear')
        
        print('Informe uma renda, garantia, divida e histórico de crédito, separados por vírgula ou 0 para retornar:')
        choice = input(' >>  ')
        ch = choice.lower()
        
        if ch == '' or ch == '0':
            self.menu_actions['main_menu'](True)
        else:
            try:
                ch = ch.split(',')
                print(self.id3.realizar_predicao(ch, self.arvore))
                self.menu_actions['main_menu'](False)
            except Exception:
                print('Formato inválido!')
                self.menu_actions['2']()

if __name__ == '__main__': 
    prg = MainProgram()
    prg.main_menu(True)