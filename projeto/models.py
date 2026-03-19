import mysql.connector
from mysql.connector import Error

def conectar():
    """ Estabelece a conexão com o banco de dados MySQL """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1:3306',          # ou o IP do servidor
            database='faculdade',  # nome do seu banco de dados
            user='root',               # seu usuário do MySQL
            password='h8x1e0k7'    # sua senha do MySQL
        )
        if connection.is_connected():
            print("Conectado ao MySQL com sucesso")
            
            # Criando um cursor para executar comandos
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("Você está conectado ao banco de dados: ", record)

    except Error as e:
        print("Erro ao conectar ao MySQL", e)
    
    finally:
        # Fechando a conexão
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexão MySQL foi encerrada")

if __name__ == "__main__":
    conectar()
