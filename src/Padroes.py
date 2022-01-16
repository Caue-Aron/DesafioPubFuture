# funções auxiliares e configurações extras
import errno
from typing import Any
import mysql
import mysql.connector as conexao
import os

# ---------------------------------
# armazenamento de tipos (contas, despesas e receitas)
tipo_contas = ['Carteira', 'Conta corrente', 'Poupança']
tipo_despesas = ['Alimentação', 'Educação', 'Lazer', 'Moradia', 'Roupa', 'Saúde', 'Transporte']
tipo_receitas = ['Salário', 'Presente', 'Prêmio']

host = ""
user = ""
password = ""
database = ""


def executa_query(sql:str):
    
    try:
        banco = mysql.connector.connect(
                    host = host,
                    user = user,
                    password = password,
                    database = database
                )
    except mysql.connector.Error as e:
        print('Não foi possível se conectar com o banco de dados.\n')
        print(e.msg)
        quit()
    
    cursor = banco.cursor()
    
    try:
        cursor.execute(sql)
    except mysql.connector.Error as e:
        print(e.msg)
        quit()
    
    resultados = cursor.fetchall()
    banco.commit()
        
    cursor.close()
    banco.close()
    
    return resultados

# ---------------------------------
# limpar tela
def clear():
    os.system('cls')