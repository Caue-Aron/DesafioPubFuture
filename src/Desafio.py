from Conta import Conta
from Padroes import clear
from Padroes import tipo_contas
from Padroes import executa_query
import Padroes


# função para se conectar ao banco de dados e para iniciar a tela
# do programa
class Main:
    
    contas = []
    contas_list = []
    
    def iniciar(self):
        clear()
        self.set_banco()
        
        clear()
        self.tela_inicial()

# ---------------------------------
# telas de gui
    def tela_inicial(self):
        clear()
        
        decisao = None
        
        while True:
            self.carrega_contas()
            print('Pressione qualquer outra tecla para sair.')  
            print('[1] Acessar conta.')
            print('[2] Cadastrar conta.')
            print('[3] Remover conta.')
            print('[4] Transferir saldo entre contas.')
            
            try:
                decisao = int(input())
            except ValueError:
                decisao = 0
                
            if decisao == 1: 
                if self.contas:
                    self.tela_de_contas()
                else:
                    clear()
                    print('Você não tem contas cadastradas. Pressione qualquer tecla para continuar.')
                    input()
                    clear()
                
            elif decisao == 2:
                self.tela_de_cadastro_de_contas()
            
            elif  decisao == 3:
                if self.contas:
                    self.tela_remove_conta()
                else:
                    clear()
                    print('Você não tem contas cadastradas. Pressione qualquer tecla para continuar.')
                    input()
                    clear()
                    
            elif  decisao == 4:
                if len(self.contas) > 1:
                    self.transferir_dados_entre_contas()
                else:
                    clear()
                    print('Você precisa de duas ou mais contas para efetuar uma transferência. Pressione qualquer tecla para continuar.')
                    input()
                    clear()
                
            else:
                return
    
    def filtro(self, filtro:str):
        valido = True
        
        if filtro == 'a':
            self.contas.clear()
            self.contas_list.sort(key=lambda x:x[1])
            
            for conta in self.contas_list:
                self.contas.append(Conta(conta[0], conta[1], conta[2]))
                
        elif filtro == 'b':
            self.contas.clear()
            self.contas_list.sort(key=lambda x:x[1], reverse = True)
            
            for conta in self.contas_list:
                self.contas.append(Conta(conta[0], conta[1], conta[2]))
        
        else:
            valido = False
            
        return valido
            
    def tela_de_contas(self):
        
        self.menu_contas()
        
        while True:
            decisao = input()
            
            if decisao.isdigit():
                
                decisao = int(decisao)
                
                if decisao == 0:
                    clear()
                    return
                    
                elif (decisao > len(self.contas)) or (decisao < 0):
                    print('Opção inválida.')
                
                else:
                    self.contas[decisao - 1].acessa()
                    self.menu_contas()
                    
            elif isinstance(decisao, str):
                
                if decisao.lower() == 't':
                    self.transferir_dados_entre_contas()
                    
                else:
                    filtro_correto = self.filtro(decisao.lower())
                    
                    if not filtro_correto:
                        print('Opção inválida.')
                        continue
                        
                self.menu_contas()

    def tela_de_cadastro_de_contas(self):
        print('Pressione qualquer outra tecla para sair.')
        instituicao, tipo = Conta.input_conta()
        
        if instituicao and tipo:
            self.contas.append(Conta(instituicao = instituicao, tipo = tipo))
            self.contas[-1].save()
        
    def tela_remove_conta(self):        
        clear()
        print('Selecione a conta que você deseja excluir, ou pressione 0 para sair: ')
        
        count = 1
        for contas in self.contas:
            print(f"[{count}] {contas.get_instituicao()}")
            count = count + 1
        
        while True:
            try:
                decisao = int(input())
            except ValueError:
                decisao = -1
                
            if decisao == 0:
                clear()
                return
                
            elif (decisao > len(self.contas)) or (decisao < 0):
                print('Você digitou uma opção inválida.')
            
            else:
                self.contas[decisao - 1].exclui()
                clear()
                return

    def menu_contas(self):
        clear()
        print('Selecione sua conta digitando o número correspondente ou pressione 0 para volta\n')
        print('Filtros disponíveis (digitar a letra correspondente): ')
        print('\tA: filtro por ordem alfabética (crescente).')
        print('\tB: filtro por ordem alfabética (decrescente).')
        
        count = 1
        print('\n    |Instituicao')
        for conta in self.contas:
            print(f"[{count}] |{conta.get_instituicao()}")
            count = count + 1

    def set_banco(self):        
        print('Insira o TCP: ')
        host = str(input())
        
        print('Insira o usuario: ') 
        user = str(input())
        
        print('Insira a senha: ')
        senha = str(input())
        
        print('Insira a database: ')
        database = str(input())
        
        Padroes.host = host
        Padroes.user = user
        Padroes.password = senha
        Padroes.database = database
                    
        
# -------------------------------
# funções de banco
    def carrega_contas(self):
        self.contas.clear()
        self.contas_list = executa_query('select ID, INSTITUICAO, TIPO, SALDO from CONTAS')
        
        for conta in self.contas_list:
            self.contas.append(Conta(conta[0], conta[1], conta[2], conta[3]))

# -------------------------------
# funções entre contas
    def transferir_dados_entre_contas(self):
        clear()
        print('Selecione a conta da qual você quer transferir (retirar) saldo ou pressione 0 para voltar: ')
        
        count = 1
        print('\n    |Instituicao')
        for conta in self.contas:
            print(f"[{count}] |{conta.get_instituicao()}")
            count = count + 1
            
        while True:
            try:
                conta_1 = int(input())
            except ValueError:
                conta_1 = -1
        
            if conta_1 == 0:
                clear()
                break
                
            elif (conta_1 > len(self.contas)) or (conta_1 < 0):
                print('Opção inválida.')
                
            else:
                conta_1 = conta_1 - 1
                clear()
                print('Selecione a conta que receberá o saldo.')
                
                count = 1
                print('\n    |Instituicao')
                for conta in self.contas:
                    print(f"[{count}] |{conta.get_instituicao()}")
                    count = count + 1
                    
                while True:
                    try:
                        conta_2 = int(input())
                    except ValueError:
                        conta_2 = -1
                
                    if conta_2 == 0:
                        clear()
                        break
                        
                    elif (conta_2 > len(self.contas)) or (conta_2 < 0):
                        print('Opção inválida.')
                        
                    else:
                        conta_2 = conta_2 - 1
                        clear()
                        print(f"Fazer transferência da conta {self.contas[conta_1].get_instituicao()} para a {self.contas[conta_2].get_instituicao()}? [S/N]")
                        while True:
                            try:
                                decisao = str(input())
                            except ValueError:
                                decisao = -1
                                
                            if decisao.lower() == 's':
                                print("\nSaldos:")
                                print(f"{self.contas[conta_1].get_instituicao()}: {self.contas[conta_1].get_saldo()}")
                                print(f"{self.contas[conta_2].get_instituicao()}: {self.contas[conta_2].get_saldo()}\n")
                                
                                print('Quanto você deseja transferir?')
                                print('Aperte 0 para sair.')
                                while True:
                                    try:
                                        valor = float(input())
                                    except ValueError:
                                        valor = -1 
                                                                                        
                                    if valor == 0:
                                        break
                                    
                                    elif valor < 0:
                                        print('Os valores não podem ser negativos ou letras')
                                        
                                    else:
                                        if self.contas[conta_1].get_saldo() >= valor:
                                            self.contas[conta_2].set_saldo(valor + self.contas[conta_2].get_saldo())
                                            self.contas[conta_2].update_saldo()
                                            
                                            self.contas[conta_1].set_saldo(self.contas[conta_1].get_saldo() - valor)
                                            self.contas[conta_1].update_saldo()
                                            
                                            clear()
                                            print('Transferência feita com sucesso! Pressione qualquer tecla para continuar')
                                            input()
                                            
                                            break
                                        else:
                                            print('Digite um valor menor do que o saldo que será transferido')
                                
                                break
                      
                            elif decisao.lower() == 'n':
                                clear()
                                break
                            
                            else:
                                print('Digite uma opção válida')
                        break            
                break

main = Main()
main.iniciar()