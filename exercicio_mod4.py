def modulo4(numeros):
    grupos = {0: [], 1: [], 2: [], 3: []}

    for n in numeros:
        resto = n % 4
        grupos[resto].append(n)

    print("= Grupos por resto (mod 4) =")
    for resto, nums in grupos.items():
        print(f"  Resto {resto}: {nums}")

    print()
    print(f"Elemento neutro da adição módulo 4: 0")
    print()

    inversos = {0: 0, 1: 3, 2: 2, 3: 1}

    for n in numeros:
        r = n % 4
        inv = inversos[r]
        print(f"Número: {n} (mod 4 = {r}) | Inverso aditivo mod 4: {inv}")


numeros = [0, 1, 2, 3, 4, 5, 6, 7]
modulo4(numeros)
