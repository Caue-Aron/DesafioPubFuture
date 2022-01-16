from Padroes import executa_query
from datetime import date
from Padroes import clear
from Padroes import tipo_despesas

class Despesa:
    valor = 0.0
    data_pgmto = None
    data_pgmto_esperado = ''
    tipo = ""
    id = None

    def __init__(self, id:int, valor:float, data_pgmto_esperado:str, tipo:str, data_pgmto:str = None) -> None:
        self.set_Despesa(id, valor, data_pgmto_esperado, tipo, data_pgmto)
    
    def set_Despesa(self, id:int, valor:float, data_pgmto_esperado:str, tipo:str, data_pgmto:str) -> None:
        self.id = id
        self.valor = valor
        self.data_pgmto_esperado = data_pgmto_esperado
        self.tipo = tipo
        self.data_pgmto = data_pgmto
        
# ---------------------------------------
# gui
    def acessa(self, saldo:float, conta_id:int):
        
        
        while True:
            clear()
            print('O que você deseja fazer? Pressione qualquer outra tecla para sair\n')
            
            if not self.data_pgmto:
                print('[1] Pagar despesa.')
            else:
                print(f'Essa despesa já foi paga em {self.data_pgmto}.\nDigite novamente: ')
            
            print('[2] Editar despesa.')
            print('[3] Deletar despesa.')
            
            try:
                decisao = int(input())
            except ValueError:
                decisao = -1

            if decisao == 1:
                if not self.data_pgmto:
                    clear()
                    print('Deseja pagar a despesa? [S/N]')
                    
                    while True:
                        try:
                            decisao = str(input())
                        except ValueError:
                            decisao = -1
                            
                        if decisao == 'S' or decisao == 's':
                            if saldo >= self.valor:
                                self.data_pgmto = str(date.today().strftime('%Y-%m-%d'))
                                executa_query(f"update DESPESAS set	DATA_PAGAMENTO = '{self.data_pgmto}' where ID = {self.id}")
                                clear()
                                print('Despesa paga com sucesso! Pressione qualquer tecla para continuar')
                                input()
                                return saldo - self.valor
                            
                            else:
                                print('Você não tem saldo suficiente. Pressione qualquer tecla para continuar.')
                                input()
                                clear()
                                break
                                    
                        elif decisao == 'N' or decisao == 'n':
                            clear()
                            break
                        
                        else:
                            print('Digite uma opção válida.')

                else:
                    break
                
            if decisao == 2:                
                valor, data_pgmto_esperado, tipo = Despesa.input_despesa()
                data_pgmto = Despesa.input_data_pgmto()
                
                if valor and data_pgmto_esperado and tipo and data_pgmto:
                    executa_query(f"update DESPESAS set VALOR = {valor}, DATA_PAGAMENTO_ESPERADO = '{data_pgmto_esperado}', DATA_PAGAMENTO = '{data_pgmto}', TIPO = '{tipo}' where ID = {self.id}")
                    self.set_Despesa(self.id, valor, data_pgmto_esperado, tipo, data_pgmto)
                               
            elif decisao == 3:
                print('Deseja mesmo deletar essa despesa? [S/N]')
                while True:
                    try:
                        decisao = str(input())
                    except ValueError:
                        decisao = -1
                        
                    if decisao.lower() == 's':
                        sql = f"delete from DESPESAS where ID_CONTA = {conta_id} and ID = {self.id}"
                        executa_query(sql)
                        clear()
                        print('Despesa excluída com sucesso! Pressione qualquer tecla para continuar.')
                        input()
                        return 'a'
                        
                    elif decisao.lower() == 'n':
                        clear()
                        break
                    
                    else:
                        print('Digite uma opção válida')

            else:
                return

# ---------------------------------------
# getters, setters e
# loaders e savers para o banco
# método load traz o valor do banco para programa
# e save leva o valor do programa para o banco
# -------
    def get_situacao(self):
        if self.data_pgmto == None and str(self.data_pgmto_esperado) > date.today().strftime('%Y-%m-%d'):
            return f'Despesa esperando pagamento (vence em {self.data_pgmto_esperado})'       
              
        elif str(self.data_pgmto_esperado) < date.today().strftime('%Y-%m-%d'):
            if self.data_pgmto:
                return f'Despesa vencida (paga em {self.data_pgmto})'
            else:
                return 'Despesa vencida'

        elif self.data_pgmto:
            return f'Despesa paga em {self.data_pgmto}'
            
    def input_despesa():
        valor = Despesa.input_valor()
        if not valor:
            return None, None, None

        tipo = Despesa.input_tipo()
        if not tipo:
            return None, None, None
        
        data_pgmto_prazo = Despesa.input_data_pgmto_esperado()
        if not data_pgmto_prazo:
            return None, None, None

        return valor, data_pgmto_prazo, tipo

# ---------
# valor
    def input_valor():
        valor = 0
        print('Digite o valor da despesa: ')
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
        
        print('Selecione o tipo da despesa')
        print('[1] Alimentação.')
        print('[2] Educação.')
        print('[3] Lazer.')
        print('[4] Moradia.')
        print('[5] Roupa.')
        print('[6] Saúde.')
        print('[7] Transporte.')
        print('[8] Outro.')
        
        while True:   
            try:
                decisao = int(input())
            except ValueError:
                decisao = -1
                
            if decisao == 0:
                return
                
            elif decisao >= 1 and decisao <= 7:
                tipo = tipo_despesas[decisao - 1]
                break
            
            elif decisao == 8:
                print('Digite o tipo da despesa: ')
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
# data do pagamento
    def input_data_pgmto():
        print("Digite a data do pagamento no formato 'AAAA-MM-DD' ou digite 0 para sair e deixa a data nula: ")
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

    def set_data_pgmto(self, data_pgmto:str):
        self.data_pgmto = data_pgmto

    def get_data_pgmto(self) -> str:
        return self.data_pgmto

# -------
# prazo do pagamento
    def input_data_pgmto_esperado():
        print("Digite o prazo para o pagamento no formato 'AAAA-MM-DD' ou digite 0 para sair: ")
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

    def set_data_pgmto_esperado(self, data_pgmto_esperado:str):
        self.data_pgmto_esperado = data_pgmto_esperado
