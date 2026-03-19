# atividade :  Estruturas Algébricas

# 1- suponha que em sistema de arquivos cada usoario pode ter as seguintes permições.

# {ler,escrever,executar}

# a) considere o conjunto de permissões como elemetos. se a operações for de permissões, qual é o elemento neutro?

# b) A operação de união de permissões é associativa? Explique com exemplo.

# c) Esse sistema de permissões com a operação união forma um semigrupo, monóide ou grupo? Justifique.

def atividade1():
   while True:
      print("Atividade1\n")
      print("1- continuar com programa?\n")
      print("2- sair\n")

      a=int(input("digite ai: \n"))
      if a==1:
         print("ok então")


# 2. Dado o conjunto de todas as strings possíveis (palavras e frases), com a operação de concatenar:

# Verifique se a operação é associativa (faça o teste com palavras reais, exemplo: "Olá", "Mundo", "!").

# b) Existe um elemento neutro? Qual seria?

# c) Essa estrutura forma um semigrupo, monóide ou grupo? Explique.


def atividade2():
   while True:
    print("Atividade2\n")
    print("1- continuar com progrma\n")
    print("2- sair\n")
    
    a=int(input("digite ai: \n"))
    if a==1:
        print("ok, então: \n")
        print("A concatenação é associativa\n")
        print("(Ola+mundo)+!\n")
        n1='ola'
        n2='mundo'
        n3='!'
        nc=n1+n2
        na=nc+n3
        print(na)
        print("ola+(mundo+!)\n")
        nb=n2+n3
        nd=n1+nb
        print(nd) # e uma concatenação associativa
        print("A concatenação é associativa")
        print("elemento neutro")
        ne=n1+""
        nf=""+n2
        print(nf+ne) # tem um elemento neutro
        print("não e um grupo pois não tem como substituir o ola em uma string normal")


    elif a==2:
        print("saindo!\n")
        break

    else:
        print("erro!")
        break

atividade2()