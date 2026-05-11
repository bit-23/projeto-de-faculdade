import matplotlib.pyplot as plt

# Valores de x
x = [100, 140, 160, 200]

# Valores acumulados F(x)
F = [0.21, 0.45, 0.52, 1.00]

# Criando gráfico em escada
plt.step(x, F, where='post')

# Título e nomes dos eixos
plt.title('Função de Distribuição Acumulada')
plt.xlabel('x (ms)')
plt.ylabel('F(x)')

# Limites dos eixos
plt.ylim(0, 1.1)

# Grade
plt.grid(True)

# Mostrar gráfico
plt.show()