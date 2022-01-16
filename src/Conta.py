from Padroes import executa_query
from Padroes import clear
from Despesa import Despesa
from Padroes import tipo_contas
from Receita import Receita
from datetime import date

class Conta:
    receitas = []
    receitas_list = None
    despesas = []
    despesas_list = None
    saldo = 0.0
    instituicao = ''
    tipo = ''
    id = None
    
    def __init__(self, id:int = 0, instituicao:str = '', tipo:str = '', saldo:float = 0):
        self.id = id
        self.instituicao = instituicao
        self.tipo = tipo
        self.saldo = saldo

# ---------------------------------
# métodos para despesas e receitas
    def load_despesas(self) -> None:
        self.despesas_list = executa_query(f"select DESPESAS.ID, VALOR, DATA_PAGAMENTO_ESPERADO, DESPESAS.TIPO, DESPESAS.DATA_PAGAMENTO from DESPESAS join CONTAS on CONTAS.ID = {self.id} and CONTAS.ID = DESPESAS.ID_CONTA")
 
        self.despesas.clear()

        for despesa in self.despesas_list:
            self.despesas.append(Despesa(despesa[0], despesa[1], despesa[2], despesa[3], despesa[4]))
    
    def load_receitas(self) -> None:
        self.receitas_list = executa_query(f"select RECEITAS.ID, VALOR, RECEITAS.DATA_RECEBIMENTO_PREVISTO, RECEITAS.TIPO, RECEITAS.DESCRICAO, RECEITAS.DATA_RECEBIMENTO from RECEITAS join CONTAS on CONTAS.ID = {self.id} and CONTAS.ID = RECEITAS.ID_CONTA")
 
        self.receitas.clear()

        for receita in self.receitas_list:
            self.receitas.append(Receita(receita[0], receita[1], receita[2], receita[3], receita[4], receita[5]))

    def filtro_despesas(self, filtro:str):
        valido = True
        
        # filtrar por prazo decrescente
        if filtro == 'a':
            self.despesas.clear()
            self.despesas_list.sort(key=lambda x:x[2])
            
            for despesa in self.despesas_list:
                self.despesas.append(Despesa(despesa[0], despesa[1], despesa[2], despesa[3]))
         
        # filtrar por prazo crescente       
        elif filtro == 'b':
            self.despesas.clear()
            self.despesas_list.sort(key=lambda x:x[2], reverse = True)
            
            for despesa in self.despesas_list:
                self.despesas.append(Despesa(despesa[0], despesa[1], despesa[2], despesa[3]))
                
        # filtrar por valor decrescente       
        elif filtro == 'c':
            self.despesas.clear()
            self.despesas_list.sort(key=lambda x:x[0])
            
            for despesa in self.despesas_list:
                self.despesas.append(Despesa(despesa[0], despesa[1], despesa[2], despesa[3]))
                
        # filtrar por valor decrescente       
        elif filtro == 'd':
            self.despesas.clear()
            self.despesas_list.sort(key=lambda x:x[0], reverse = True)
            
            for despesa in self.despesas_list:
                self.despesas.append(Despesa(despesa[0], despesa[1], despesa[2], despesa[3]))
        
        # filtrar por tipo crescente       
        elif filtro == 'e':
            self.despesas.clear()
            self.despesas_list.sort(key=lambda x:x[3])
            
            for despesa in self.despesas_list:
                self.despesas.append(Despesa(despesa[0], despesa[1], despesa[2], despesa[3]))
                
        # filtrar por tipo crescente       
        elif filtro == 'f':
            self.despesas.clear()
            self.despesas_list.sort(key=lambda x:x[3], reverse = True)
            
            for despesa in self.despesas_list:
                self.despesas.append(Despesa(despesa[0], despesa[1], despesa[2], despesa[3]))
                
        else:
            valido = False
            
        return valido

    def filtro_receitas(self, filtro:str):
        valido = True
        
        # filtrar por prazo decrescente
        if filtro == 'a':
            self.receitas.clear()
            self.receitas_list.sort(key=lambda x:x[2])
            
            for receita in self.receitas_list:
                self.receitas.append(Receita(receita[0], receita[1], receita[2], receita[3], receita[4], receita[5]))
         
        # filtrar por prazo crescente       
        elif filtro == 'b':
            self.receitas.clear()
            self.receitas_list.sort(key=lambda x:x[2], reverse = True)
            
            for receita in self.receitas_list:
                self.receitas.append(Receita(receita[0], receita[1], receita[2], receita[3], receita[4], receita[5]))
                
        # filtrar por valor crescente       
        elif filtro == 'c':
            self.receitas.clear()
            self.receitas_list.sort(key=lambda x:x[1])
            
            for receita in self.receitas_list:
                self.receitas.append(Receita(receita[0], receita[1], receita[2], receita[3], receita[4], receita[5]))
                
        # filtrar por valor decrescente       
        elif filtro == 'd':
            self.receitas.clear()
            self.receitas_list.sort(key=lambda x:x[1], reverse = True)
            
            for receita in self.receitas_list:
                self.receitas.append(Receita(receita[0], receita[1], receita[2], receita[3], receita[4], receita[5]))
        
        # filtrar por tipo crescente       
        elif filtro == 'e':
            self.receitas.clear()
            self.receitas_list.sort(key=lambda x:x[3])
            
            for receita in self.receitas_list:
                self.receitas.append(Receita(receita[0], receita[1], receita[2], receita[3], receita[4], receita[5]))
                
        # filtrar por tipo crescente       
        elif filtro == 'f':
            self.receitas.clear()
            self.receitas_list.sort(key=lambda x:x[3], reverse = True)
            
            for receita in self.receitas_list:
                self.receitas.append(Receita(receita[0], receita[1], receita[2], receita[3], receita[4], receita[5]))
                
        else:
            valido = False
            
        return valido
# ---------------------------------
# getters, setters, loaders e savers
    def input_conta():
        while True:
            clear()
            
            print('Insira a instituicao da conta: ')
            instituicao = str(input())
            
            print('\nInsira o tipo da conta: ')
            print('[1] Carteira.')
            print('[2] Conta corrente.')
            print('[3] Poupança.')
            print('[4] Outro.')
            
            tipo = ''
            
            while True:
                try:
                    decide_tipo = int(input())
                except ValueError:
                    decide_tipo = 0
                
                if decide_tipo >= 1 and decide_tipo <= 3:
                    tipo = tipo_contas[decide_tipo - 1]
                    break
                elif decide_tipo == 4:
                    print('Insira o tipo:')
                    tipo = str(input())
                    break
                else:
                    return None, None
                
            
            clear()
            print(f"Instituicao: '{instituicao}'.")
            print(f"Tipo: '{tipo}'.")
            print('Confirmar cadastro de conta? [S/N]')
            
            decisao = ''
            
            while True:
                try:
                    decisao = str(input())
                except ValueError:
                    decisao = 0
                
                if decisao.lower() == 's':
                    clear()
                    return instituicao, tipo
                    
                elif decisao.lower() == 'n':
                    continuar_criando_conta = ''
                    print('Continuar com a criação de contas? [S/N]')
                    
                    while True:   
                        decisao = str(input())
                            
                        if decisao.lower() == 's':
                            break
                            
                        elif decisao.lower() == 'n':
                            clear()
                            return None, None
                        
                        else:
                            print("Você digitou uma opção inválida")
                    
                    break
                
                else:
                    print("Você digitou uma opção inválida")

# ---------------
# gerais
    def save(self):
        executa_query(f"insert into CONTAS(INSTITUICAO, SALDO, TIPO) values('{self.instituicao}', 0.0, '{self.tipo}')")
        
    def exclui(self):
        self.load_despesas()
        self.load_receitas()
        
        if self.despesas:
            executa_query(f"delete from DESPESAS where ID_CONTA = {self.id}")  
        
        if self.receitas:
            executa_query(f"delete from RECEITAS where ID_CONTA = {self.id}")  
            
        executa_query(f"delete from CONTAS where ID = {self.id}")
    
    def update(self):
        executa_query(f"update CONTAS set INSTITUICAO = '{self.instituicao}', TIPO = '{self.tipo}' where ID = {self.id}")  

# ---------------
# gui
    def acessa(self):
        clear()
        print(f"Instituição: {self.instituicao}.")
        print(f"Tipo: {self.tipo}.")
        print(f"Saldo: {self.saldo}.\n")
        
        print('Pressione qualquer outra tecla para voltar.')
        
        print("[1] Acessar receitas.")
        print("[2] Acessar despesas.")
        print("[3] Cadastrar receita.")
        print("[4] Cadastrar despesa.")
        print('[5] Editar conta.')
        
        while True:
            try:
                decisao = int(input())
            except ValueError:
                decisao = -1
                
            if decisao == 1:
                self.load_receitas()
                self.acessa_receitas()
                
                clear() 
                print('Pressione qualquer outra tecla para sair.')                
                print(f"Instituição: {self.instituicao}.")
                print(f"Tipo: {self.tipo}.")
                print(f"Saldo: {self.saldo}.\n")
                
                print("[1] Acessar receitas.")
                print("[2] Acessar despesas.")
                print("[3] Cadastrar receita.")
                print("[4] Cadastrar despesa.")
                
            elif decisao == 2:
                self.load_despesas()
                self.acessa_despesas()
                
                clear() 
                print('Pressione qualquer outra tecla para sair.')                
                print(f"Instituição: {self.instituicao}.")
                print(f"Tipo: {self.tipo}.")
                print(f"Saldo: {self.saldo}.\n")
                
                print("[1] Acessar receitas.")
                print("[2] Acessar despesas.")
                print("[3] Cadastrar receita.")
                print("[4] Cadastrar despesa.")
             
            elif decisao == 3:
                novo_saldo = self.cadastra_receita()
                
                if novo_saldo:
                    self.saldo = self.saldo + novo_saldo
                
                clear()        
                print('Pressione qualquer outra tecla para sair.')        
                print(f"Instituição: {self.instituicao}.")
                print(f"Tipo: {self.tipo}.")
                print(f"Saldo: {self.saldo}.\n")
                
                print("[1] Acessar receitas.")
                print("[2] Acessar despesas.")
                print("[3] Cadastrar receita.")
                print("[4] Cadastrar despesa.")
              
            elif decisao == 4:
                self.cadastra_despesa() 
                
                clear()        
                print('Pressione qualquer outra tecla para sair.')        
                print(f"Instituição: {self.instituicao}.")
                print(f"Tipo: {self.tipo}.")
                print(f"Saldo: {self.saldo}.\n")
                
                print("[1] Acessar receitas.")
                print("[2] Acessar despesas.")
                print("[3] Cadastrar receita.")
                print("[4] Cadastrar despesa.")
             
            elif decisao == 5:
                self.instituicao, self.tipo = Conta.input_conta()
                self.update()
                break

            else: return
            
    def acessa_receitas(self):
        if not self.receitas:
            clear()
            print('Essa conta não possui Receitas. \nPressione 1 para cadastrar uma nova receita ou qualquer tecla para voltar')
            
            while True:
                try:
                    decisao = int(input())
                except ValueError:
                    decisao = -1
                    
                if decisao == 1:
                    self.cadastra_receita()
                    return
                else:
                    return
        
        self.menu_receitas()
        
        while True:
            decisao = input()
            
            if decisao.isdigit():
                
                decisao = int(decisao)
                if decisao == 0:
                    clear()
                    return
                    
                elif (decisao > len(self.receitas)) or (decisao < 0):
                    print('Digite uma opção válida.')
                
                else:
                    novo_saldo = self.receitas[decisao - 1].acessa(self.id)
                    
                    if isinstance(novo_saldo, (float)):
                        self.set_saldo(novo_saldo + self.get_saldo())
                        self.update_saldo()
                        self.load_receitas()
                        self.menu_receitas()
                    else:
                        return
                    
                    
            elif isinstance(decisao, str):
                filtro_correto = self.filtro_receitas(decisao.lower())
                
                if not filtro_correto:
                    print('Opção inválida.')
                    continue
                
                self.menu_receitas()
      
    def acessa_despesas(self):
        if not self.despesas:
            clear()
            print('Essa conta não possui despesas. \nPressione 1 para cadastrar uma nova despesa ou qualquer tecla para voltar')
            
            while True:
                try:
                    decisao = int(input())
                except ValueError:
                    decisao = -1
                    
                if decisao == 1:
                    self.cadastra_despesa()
                    return
                else:
                    return
        
        self.menu_despesas()
        
        while True:
            decisao = input()
            
            if decisao.isdigit():
                
                decisao = int(decisao)
                if decisao == 0:
                    clear()
                    return
                    
                elif (decisao > len(self.despesas)) or (decisao < 0):
                    print('Opção inválida.')
                
                else:
                    novo_saldo = self.despesas[decisao - 1].acessa(self.saldo, self.id)
                    
                    if isinstance(novo_saldo, (int, float)):
                        self.set_saldo(novo_saldo)
                        self.update_saldo()
                            
                    self.menu_despesas()
                    
            elif isinstance(decisao, str):
                filtro_correto = self.filtro_despesas(decisao.lower())
                
                if not filtro_correto:
                    print('Opção inválida.')
                    continue
                
                self.menu_despesas()
    
    def cadastra_receita(self):
        clear()
        
        valor = 0.0
        tipo = ''
        data_recebimento_esperado = ''
        descricao = ''
        
        
        print('Digite 0 para retornar para a tela da conta')
        
        valor, data_recebimento_esperado, tipo, descricao = Receita.input_receita()
        if not valor and not data_recebimento_esperado and not tipo and not descricao:
            return
        
        clear()
        print(f'Valor: {valor}')
        print(f'Tipo: {tipo}')
        print(f'Prazo para recebimento: {data_recebimento_esperado}')
        print(f'Descrição: {descricao}')
        print('\nConfirmar receita? [S/N]')
        
        while True:
            try:
                decisao = str(input())
            except ValueError:
                decisao = -1
                
            if decisao.lower() == 's':
                executa_query(f"insert into RECEITAS(VALOR, DATA_RECEBIMENTO_PREVISTO, TIPO, DESCRICAO, ID_CONTA) values({valor}, '{data_recebimento_esperado}', '{tipo}', '{descricao}', {self.id})")
                print('Receita criada com sucesso! Pressione qualquer tecla para continuar.')
                
                return
                
            elif decisao.lower() == 'n':
                clear()
                return
                         
    def cadastra_despesa(self):
        clear()
        
        valor = 0.0
        tipo = ''
        data_pgmto = ''
        
        
        print('Digite 0 para retornar para a tela da conta')
        
        valor, data_pgmto_prazo, tipo = Despesa.input_despesa()
        if not valor and not data_pgmto_prazo and not tipo:
            return
        
        clear()
        print(f'Valor: {valor}')
        print(f'Tipo: {tipo}')
        print(f'Prazo para pagamento: {data_pgmto_prazo}')
        print('\nConfirmar despesa? [S/N]')
        
        while True:
            try:
                decisao = str(input())
            except ValueError:
                decisao = -1
                
            if decisao.lower() == 's':
                executa_query(f"insert into DESPESAS(VALOR, DATA_PAGAMENTO_ESPERADO, TIPO, ID_CONTA) values({valor}, '{data_pgmto_prazo}', '{tipo}', {self.id})")
                print('Despesa criada com sucesso! Pressione qualquer tecla para continuar.')
                input()
                clear()
                return
                
            elif decisao.lower() == 'n':
                clear()
                return
     
    def menu_receitas(self):
        clear()
        print('Selecione a despesa correspondente para ver opções ou pressione 0 para sair\n')
        print("Filtros disponíveis:")
        print("\t'A': filtrar por prazo (mais recente)")
        print("\t'B': filtrar por prazo (menos recente)")
        print("\t'C': filtrar por valor (decrescente)")
        print("\t'D': filtrar por valor (crescente)")
        print("\t'E': filtrar por Tipo (alfabético)")
        print("\t'F': filtrar por Tipo (alfabético decrescente)")
        print("\t'G': filtrar por Descricao (alfabético)")
        print("\t'H': filtrar por Descricao (alfabético decrescente)\n")

        print('    |Tipo\t|Data prevista do recebimento\t|Valor\t|Situação\t\t\t\t|Descricao')
        count = 1
        for receita in self.receitas:
            print(f"[{count}] |{receita.get_tipo()}\t|{receita.get_data_recebimento_esperado()}\t\t\t|{receita.get_valor()}\t|{receita.get_situacao()}\t|{receita.get_descricao()}")
            count = count + 1
     
    def menu_despesas(self):
        clear()
        print('Selecione a despesa correspondente para ver opções ou pressione 0 para sair\n')
        print("Filtros disponíveis:")
        print("\t'A': filtrar por prazo (mais recente)")
        print("\t'B': filtrar por prazo (menos recente)")
        print("\t'C': filtrar por valor (decrescente)")
        print("\t'D': filtrar por valor (crescente)")
        print("\t'E': filtrar por Tipo (alfabético)")
        print("\t'F': filtrar por Tipo (alfabético decrescente)\n")

        print('    |Tipo\t\t|Data prevista do pagamento\t|Valor\t\t|Situação')
        count = 1
        for despesa in self.despesas:
            
            if despesa.get_tipo() != 'Alimentação':
                print(f"[{count}] |{despesa.get_tipo()}\t\t|{despesa.get_data_pgmto_esperado()}\t\t\t|{despesa.get_valor()}\t\t|{despesa.get_situacao()}")
            
            else: 
                print(f"[{count}] |{despesa.get_tipo()}\t|{despesa.get_data_pgmto_esperado()}\t\t\t|{despesa.get_valor()}\t\t|{despesa.get_situacao()}")
            
            count = count + 1
                 
# ---------------
# saldo
    def set_saldo(self, saldo) -> None:
        self.saldo = saldo

    def get_saldo(self) -> float:
        return self.saldo

    def update_saldo(self)  -> None:
        executa_query(f"update CONTAS set SALDO = {self.saldo} where ID = {self.id}")

# ---------------
# instituicao
    def set_instituicao(self, instituicao) -> None:
        self.instituicao = instituicao
        
    def get_instituicao(self) -> str:
        return self.instituicao