# funções auxiliares e configurações extras
from typing import Any
import mysql.connector as conexao
import os

# ---------------------------------
# armazenamento de tipos (contas, despesas e receitas)
tipo_contas = ['Carteira', 'Conta corrente', 'Poupança']
tipo_despesas = ['Alimentação', 'Educação', 'Lazer', 'Moradia', 'Roupa', 'Saúde', 'Transporte']
tipo_receitas = ['Salário', 'Presente', 'Prêmio']

def executa_query(sql:str):
    banco = conexao.connect(
                host = "127.0.0.1",
                user = "root",
                password = "ca150703",
                database = "desafio"
            )
    
    cursor = banco.cursor()
    cursor.execute(sql)
    
    resultados = cursor.fetchall()
    banco.commit()
        
    cursor.close()
    banco.close()
    
    return resultados

# ---------------------------------
# limpar tela
def clear():
    os.system('cls')