# ─── NÍVEL 1: BÁSICO ───────────────────────────────────


def fatorial(n):
    """Calcula n! (fatorial) sem recursão."""
    pass


def fibonacci(quantidade):
    """Gera os primeiros N números de Fibonacci."""
    pass


def eh_palindromo(texto):
    """Verifica se uma string é um palíndromo."""
    pass


# ─── NÍVEL 2: INTERMEDIÁRIO ────────────────────────────


def frequencia_caracteres(frase):
    """Conta quantas vezes cada caractere aparece na frase."""
    pass


def crivo_eratostenes(n):
    """Encontra todos os primos até n usando o Crivo de Eratóstenes."""
    pass


def jogar_velha():
    """Jogo da velha no terminal com verificação de vitória."""
    pass


# ─── NÍVEL 3: DESAFIO ──────────────────────────────────


def decimal_para_binario(n):
    """Converte decimal para binário sem usar bin()."""
    pass


def inverter_lista(lista):
    """Inverte uma lista sem usar slice [::-1] nem reverse()."""
    pass


def matriz_espiral(matriz):
    """Percorre matriz em ordem espiral.
    Ex: [[1,2,3],[4,5,6],[7,8,9]] -> [1,2,3,6,9,8,7,4,5]
    """
    pass


# ─── TESTES BÁSICOS (descomente conforme for fazendo) ───

if __name__ == "__main__":

    # Nível 1
    # print(fatorial(5))              # esperado: 120
    # print(fibonacci(10))            # esperado: [0,1,1,2,3,5,8,13,21,34]
    # print(eh_palindromo("asa"))     # esperado: True
    # print(eh_palindromo("casa"))    # esperado: False

    # Nível 2
    # print(frequencia_caracteres("ola"))  # esperado: {'o':1, 'l':1, 'a':1}
    # print(crivo_eratostenes(20))         # esperado: [2,3,5,7,11,13,17,19]

    # Nível 3
    # print(decimal_para_binario(13))  # esperado: 1101
    # print(inverter_lista([1,2,3]))   # esperado: [3,2,1]
    # print(matriz_espiral([[1,2,3],[4,5,6],[7,8,9]]))
    # esperado: [1,2,3,6,9,8,7,4,5]



# teste basic ()

def namo(adeva):
	adeva=int(input("escreva um numero: \n"))
	
