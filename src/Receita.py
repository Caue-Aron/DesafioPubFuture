from Padroes import executa_query
from datetime import date
from Padroes import clear
from Padroes import tipo_receitas

class Receita:
    valor = 0.0
    data_recebimento = None
    data_recebimento_esperado = ''
    tipo = ""
    descricao = ""
    id = None

    def __init__(self, id:int, valor:float, data_recebimento_esperado:str, tipo:str, descricao:str, data_recebimento:str = None) -> None:
        self.set_receita(id, valor, data_recebimento_esperado, tipo, descricao, data_recebimento)
    
    def set_receita(self, id:int, valor:float, data_recebimento_esperado:str, tipo:str, descricao:str, data_recebimento:str) -> None:
        self.id = id
        self.valor = valor
        self.data_recebimento_esperado = data_recebimento_esperado
        self.tipo = tipo
        self.data_recebimento = data_recebimento
        self.descricao = descricao
        
# ---------------------------------------
# gui
    def acessa(self, conta_id:int):  
        while True:
            clear()
            print('Descrição da receita: ')
            print(f'{self.descricao}\n')
            print('O que você deseja fazer? Pressione qualquer outra tecla para sair\n')
            
            print('[1] Receber receita.')
            print('[2] Editar receita.')
            print('[3] Deletar receita.')
            
            try:
                decisao = int(input())
            except ValueError:
                decisao = -1

            if decisao == 1:
                if not self.data_recebimento:
                    clear()
                    print('Deseja mesmo receber a receita? [S/N]')
                    
                    while True:
                        try:
                            decisao = str(input())
                        except ValueError:
                            decisao = -1
                            
                        if decisao.lower() == 's':
                            self.data_recebimento = str(date.today().strftime('%Y-%m-%d'))
                            executa_query(f"update RECEITAS set DATA_RECEBIMENTO = '{self.data_recebimento}' where ID = {self.id}")
                            clear()
                            print('receita recebida com sucesso! Pressione qualquer tecla para continuar')
                            input()
                            return self.valor
                                    
                        elif decisao.lower() == 'n':
                            clear()
                            break
                        
                        else:
                            print('Digite uma opção válida.')

                else:
                    clear()
                    print(f'Essa receita já foi recebida em {self.data_recebimento}. Pressione qualquer tecla para retornar')
                    input()
                    clear()
                
            elif decisao == 2:                
                valor, data_recebimento_esperado, tipo, descricao = Receita.input_receita()
                data_recebimento = Receita.input_data_recebimento(self.id)
                
                if valor and data_recebimento_esperado and tipo and data_recebimento and descricao:
                    executa_query(f"update RECEITAS set VALOR = {valor}, DATA_RECEBIMENTO = '{data_recebimento}', DATA_RECEBIMENTO_ESPERADO = '{data_recebimento_esperado}', TIPO = '{tipo}', DESCRICAO = '{descricao}' where ID = {self.id}")
                    self.set_receita(self.id, valor, data_recebimento_esperado, tipo, data_recebimento)
                               
            elif decisao == 3:
                print('Deseja mesmo deletar essa receita? [S/N]')
                while True:
                    try:
                        decisao = str(input())
                    except ValueError:
                        decisao = -1
                        
                    if decisao.lower() == 's':
                        sql = f"delete from RECEITAS where ID_CONTA = {conta_id} and ID = {self.id}"
                        executa_query(sql)
                        clear()
                        print('receita excluída com sucesso! Pressione qualquer tecla para continuar.')
                        input()
                        return 'a'
                        
                    elif decisao.lower() == 'n':
                        clear()
                        return 'a'
                    
                    else:
                        print('Digite uma opção válida')

            else:
                return

    def print(self):
        print(f"|{self.get_tipo()}\t|{self.get_data_pgmto_esperado()}\t\t\t|{self.get_valor()}\t\t|{self.get_situacao()}")
        
# ---------------------------------------
# getters, setters e
# loaders e savers para o banco
# método load traz o valor do banco para programa
# e save leva o valor do programa para o banco
# -------
    def get_situacao(self):
        if self.data_recebimento == None and str(self.data_recebimento_esperado) > date.today().strftime('%Y-%m-%d'):
            return f'Esperando recebimento em {self.data_recebimento_esperado}'       
              
        elif str(self.data_recebimento_esperado) < date.today().strftime('%Y-%m-%d'):
            if self.data_recebimento:
                return f'Receita recebida com atraso (em {self.data_recebimento})'
            else:                
                return 'Receita atrasada'

        elif self.data_recebimento:
            return f'Receita recebida em {self.data_recebimento}'
            
    def input_receita():
        valor = Receita.input_valor()
        if not valor:
            return None, None, None, None

        data_recebimento_esperado = Receita.input_data_recebimento_esperado()
        if not data_recebimento_esperado:
            return
        
        tipo = Receita.input_tipo()
        if not tipo:
            return None, None, None, None
        
        descricao = Receita.input_descricao()
        if not descricao:
            return None, None, None, None
        

        return valor, data_recebimento_esperado, tipo, descricao

# ---------
# valor
    def input_valor():
        valor = 0
        print('Digite o valor da receita: ')
        while True:
            try:
                valor = float(input())
            except ValueError:
                valor = -1
                
            if valor == 0:
                return
            
            elif valor < 0:
                print('Digite uma opção válida')
                
            else:
                return valor

    def set_valor(self, valor) -> None:
        self.valor = valor

    def get_valor(self) -> float:
        return self.valor

# -------
# tipo
    def input_tipo():
        tipo = ''
        
        print('Selecione o tipo da receita')
        print('[1] Salário.')
        print('[2] Presente.')
        print('[3] Prêmio.')
        print('[4] Outro.')
        
        while True:   
            try:
                decisao = int(input())
            except ValueError:
                decisao = -1
                
            if decisao == 0:
                return
                
            elif decisao >= 1 and decisao <= 3:
                tipo = tipo_receitas[decisao - 1]
                break
            
            elif decisao == 4:
                print('Digite o tipo da receita: ')
                tipo = str(input())
                break
                
            else:
                print('Digite uma opção válida.')
        
        return tipo
    
    def set_tipo(self, tipo:str) -> None:
        self.tipo = tipo

    def get_tipo(self) -> str:
        return self.tipo

# -------
# descricao
    def input_descricao():
        descricao = ''
        
        print('Insira a descrição da receita. Aperte enter apenas quando terminar a digitação.')
        
        descricao = str(input())
        return descricao
    
    def set_descricao(self, descricao:str) -> None:
        self.descricao = descricao

    def get_descricao(self) -> str:
        return self.descricao

# -------
# data do recebimento
    def input_data_recebimento():
        print("Digite a data do recebimento no formato 'AAAA-MM-DD' ou digite 0 para sair e deixa a data nula: ")
        while True:
            data_pgmto = str(input())
            
            if data_pgmto == '0':
                return None
            
            # variaveis para visualizacao em tempo real
            # data1 = data_pgmto[:4]  
            # data2 = data_pgmto[4:5]  
            # data3 = data_pgmto[5:7] 
            # data4 = data_pgmto[7:8]    
            # data5 = data_pgmto[8:10]
            
            # verifica se a data foi preenchida com a quantidade certa de chars
            if len(data_pgmto) > 10 or len(data_pgmto) < 10:
                print('Data digitada incorretamente: você esqueceu algum dado, ou inseriu dados de mais')
                continue
            
            # verifica se a data esta digitada corretamente
            if data_pgmto[:4].isdigit():
                if data_pgmto[4:5] == '-':
                    if data_pgmto[5:7].isdigit():
                        if data_pgmto[7:8] == '-':
                            if data_pgmto[8:10].isdigit():
                                
                                # verifica se a data tem números corretos
                                if int(data_pgmto[:4]) < 3000:
                                    if int(data_pgmto[5:7]) <= 12 and int(data_pgmto[5:7]) >= 1:
                                        
                                        # se for fevereiro:
                                        if int(data_pgmto[5:7]) == 2:
                                            # ano bissexto
                                            if int(data_pgmto[:4]) % 400 == 0:
                                                if int(data_pgmto[8:10]) <= 29 and int(data_pgmto[8:10]) >= 1:
                                                    pass
                                                else:
                                                    print('Data digitada incorretamente: o ano inserido é bissexto, e fevereiro não deve ter mais de 29 dias.')
                                                    continue
                                            
                                            # ano não bissexto
                                            elif int(data_pgmto[8:10]) <= 28 and int(data_pgmto[8:10]) >= 1:
                                                pass
                                            
                                            else:
                                                print('Data digitada incorretamente: fevereiro não deve ter mais de 28 dias.')
                                                continue
                                        
                                        # se for abril, junho, setembro ou novembro
                                        if int(data_pgmto[5:7]) == 4 or int(data_pgmto[5:7]) == 6 or int(data_pgmto[5:7]) == 9 or int(data_pgmto[5:7]) == 11:
                                            if int(data_pgmto[8:10]) <= 30 and int(data_pgmto[8:10]) >= 1:
                                                pass
                                            else:
                                                print('Data digitada incorretamente: meses 04, 06, 09 e 11 não possuem mais que 30 dias.')
                                                continue       
                                        # outros meses do ano
                                        else:
                                            if int(data_pgmto[8:10]) <= 31 and int(data_pgmto[8:10]) >= 1:
                                                pass
                                            else:
                                                print('Data digitada incorretamente: os meses do ano não possuem mais que 31 dias.')
                                                continue
                                            
                                    else:
                                        print('Data digitada incorretamente: um ano não possui mais que 12 meses.')   
                                        continue
                                else:
                                    print('Data digitada incorretamente: o ano não deve exceder o número 2999.')
                                    continue                                
                            else:
                                print('Data digitada incorretamente: dias devem ser compostos de apenas números.')
                                continue
                        else:
                            print("Data digitada incorretamente: para separar os anos dos meses e dias use um traço ('-').")
                            continue
                    else:
                        print("Data digitada incorretamente: usa apenas números para inserir o mês).")
                        continue
                else:
                    print("Data digitada incorretamente: para separar os anos dos meses e dias use um traço ('-').")
                    continue
            else:
                print("Data digitada use apenas números para informar o ano.")
                continue
                                
            # verifica se a data é maior que a data atual
            if data_pgmto <= date.today().strftime('%Y-%m-%d'):
                return data_pgmto
            else:
                print('A data de pagamento deve ser anterior ou igual a data atual')
                continue

    def set_data_recebimento(self, data_pgmto:str):
        self.data_recebimento = data_pgmto

    def get_data_recebimento(self) -> str:
        return self.data_recebimento

# -------
# prazo do recebimento
    def input_data_recebimento_esperado():
        print("Digite o prazo para o recebimento no formato 'AAAA-MM-DD' ou digite 0 para sair: ")
        while True:
            data_pgmto = str(input())
            
            if data_pgmto == '0':
                return
            
            # variaveis para visualizacao em tempo real
            # data1 = data_pgmto[:4]  
            # data2 = data_pgmto[4:5]  
            # data3 = data_pgmto[5:7] 
            # data4 = data_pgmto[7:8]    
            # data5 = data_pgmto[8:10]
            
            # verifica se a data foi preenchida com a quantidade certa de chars
            if len(data_pgmto) > 10 or len(data_pgmto) < 10:
                print('Data digitada incorretamente: você esqueceu algum dado, ou inseriu dados de mais')
                continue
            
            # verifica se a data esta digitada corretamente
            if data_pgmto[:4].isdigit():
                if data_pgmto[4:5] == '-':
                    if data_pgmto[5:7].isdigit():
                        if data_pgmto[7:8] == '-':
                            if data_pgmto[8:10].isdigit():
                                
                                # verifica se a data tem números corretos
                                if int(data_pgmto[:4]) < 3000:
                                    if int(data_pgmto[5:7]) <= 12 and int(data_pgmto[5:7]) >= 1:
                                        
                                        # se for fevereiro:
                                        if int(data_pgmto[5:7]) == 2:
                                            # ano bissexto
                                            if int(data_pgmto[:4]) % 400 == 0:
                                                if int(data_pgmto[8:10]) <= 29 and int(data_pgmto[8:10]) >= 1:
                                                    pass
                                                else:
                                                    print('Data digitada incorretamente: o ano inserido é bissexto, e fevereiro não deve ter mais de 29 dias.')
                                                    continue
                                            
                                            # ano não bissexto
                                            elif int(data_pgmto[8:10]) <= 28 and int(data_pgmto[8:10]) >= 1:
                                                pass
                                            
                                            else:
                                                print('Data digitada incorretamente: fevereiro não deve ter mais de 28 dias.')
                                                continue
                                        
                                        # se for abril, junho, setembro ou novembro
                                        if int(data_pgmto[5:7]) == 4 or int(data_pgmto[5:7]) == 6 or int(data_pgmto[5:7]) == 9 or int(data_pgmto[5:7]) == 11:
                                            if int(data_pgmto[8:10]) <= 30 and int(data_pgmto[8:10]) >= 1:
                                                pass
                                            else:
                                                print('Data digitada incorretamente: meses 04, 06, 09 e 11 não possuem mais que 30 dias.')
                                                continue       
                                        # outros meses do ano
                                        else:
                                            if int(data_pgmto[8:10]) <= 31 and int(data_pgmto[8:10]) >= 1:
                                                pass
                                            else:
                                                print('Data digitada incorretamente: os meses do ano não possuem mais que 31 dias.')
                                                continue
                                            
                                    else:
                                        print('Data digitada incorretamente: um ano não possui mais que 12 meses.')   
                                        continue
                                else:
                                    print('Data digitada incorretamente: o ano não deve exceder o número 2999.')
                                    continue                                
                            else:
                                print('Data digitada incorretamente: dias devem ser compostos de apenas números.')
                                continue
                        else:
                            print("Data digitada incorretamente: para separar os anos dos meses e dias use um traço ('-').")
                            continue
                    else:
                        print("Data digitada incorretamente: usa apenas números para inserir o mês).")
                        continue
                else:
                    print("Data digitada incorretamente: para separar os anos dos meses e dias use um traço ('-').")
                    continue
            else:
                print("Data digitada use apenas números para informar o ano.")
                continue
                       
            return data_pgmto

    def set_data_recebimento_esperado(self, data_recebimento_esperado:str):
        self.data_recebimento_esperado = data_recebimento_esperado
        
    def get_data_recebimento_esperado(self):
        return self.data_recebimento_esperado
