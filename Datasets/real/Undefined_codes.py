Code 1:
numbers = [1, 2, 3, 4, 5]
squares = []
total = 0  
for num in numbers:
    total += num  
    squares.append(total ** 2)  
print(squares)
   
========================================
Code 2:
words = ["python", "code", "parallel"]
upper_words = []
count = 0  
for word in words:
    count += len(word)  
    upper_words.append(f"{word.upper()}_{count}") 
print(upper_words)

========================================
Code 3:
numbers = [10, 15, 20, 25, 30]
odd_numbers = []
sum_odds = 0  
for num in numbers:
    if num % 2 != 0:
        sum_odds += num  
        odd_numbers.append(sum_odds)  
print(odd_numbers)
  
========================================
Code 4:
import hashlib

strings = ["hello", "world", "parallel"]
hashes = []
prev_hash = ""  
for s in strings:
    combined = s + prev_hash 
    prev_hash = hashlib.md5(combined.encode()).hexdigest()
    hashes.append(prev_hash)  
print(hashes)
   
========================================
Code 5:
size = 3
identity_matrix = []
prev_row = [] 
for i in range(size):
    row = []
    for j in range(size):
        val = 1 if i == j else prev_row[j] * 0  
        row.append(val)
    prev_row = row
    identity_matrix.append(row)  
print(identity_matrix)
   
========================================
Code 6:
sentences = ["Hello world", "Parallel computing", "Python is great"]
word_counts = []
total_words = 0  
for sentence in sentences:
    total_words += len(sentence.split())  
    word_counts.append(total_words)  
print(word_counts)
  
========================================
Code 7:
import math

angles = [0, 30, 45, 60, 90]
sines = []
phase = 0  
for angle in angles:
    phase += angle  
    sines.append(math.sin(math.radians(phase)))  
print(sines)
    
========================================
Code 8:
urls = ["https://google.com", "https://github.com", "https://python.org"]
domains = []
last_domain = ""  
for url in urls:
    domain = url.split("//")[1].split("/")[0]
    domain = f"{last_domain}_{domain}" if last_domain else domain  
    last_domain = domain
    domains.append(domain)  
print(domains)
   
========================================
Code 9:
import math

numbers = [5, 7, 10]
factorials = []
last_fact = 1  
for n in numbers:
    last_fact *= math.factorial(n)  
    factorials.append(last_fact)  
print(factorials)
  
========================================
Code 10:
pixels = [(120, 80, 200), (255, 255, 255), (0, 0, 0)]
grayscale = []
prev_avg = 0 
for pixel in pixels:
    avg = sum(pixel) // 3
    avg = (avg + prev_avg) // 2 
    prev_avg = avg
    grayscale.append(avg)  
print(grayscale)
   
========================================
Code 11:
numeros = [1, 2, 3, 4, 5]
somas = []
acumulado = 0
for n in numeros:
    acumulado += n
    somas.append(acumulado)
print("Exemplo 1 - Soma acumulada:", somas)

========================================
Code 12:
numeros = [1, 2, 3, 4]
produtos = []
acumulado = 1
for n in numeros:
    acumulado *= n
    produtos.append(acumulado)
print("Exemplo 2 - Produto acumulado:", produtos) 
    
========================================
Code 13:   
fibonacci = [0, 1]
for i in range(8):
    proximo = fibonacci[-1] + fibonacci[-2]
    fibonacci.append(proximo)
print("Exemplo 3 - Sequência de Fibonacci:", fibonacci)
    
========================================
Code 14:
valores = [10, 20, 30, 40]
media_parcial = []
soma = 0
for i in range(len(valores)):
    soma += valores[i]
    media = soma / (i + 1)
    media_parcial.append(media)
print("Exemplo 4 - Média acumulada:", media_parcial)
    
========================================
Code 15:
sequencia = [1]
for i in range(1, 6):
    sequencia.append(sequencia[i-1] * 2 + 1)
print("Exemplo 5 - Sequência dependente:", sequencia)

========================================
Code 16: 
valores = [10, 13, 15, 14, 20]
diferencas = [0]
for i in range(1, len(valores)):
    diferenca = valores[i] - valores[i-1]
    diferencas.append(diferenca)
print("Exemplo 6 - Diferenças entre vizinhos:", diferencas)

========================================
Code 17:
movimentos = [100, -30, -20, 50, -10]
saldos = []
saldo = 0
for valor in movimentos:
    saldo += valor
    saldos.append(saldo)
print("Exemplo 7 - Saldos ao longo do tempo:", saldos)
    
========================================
Code 18:
leituras = [1, 1, 2, 2, 3, 2, 2, 1]
mudancas = []
for i in range(1, len(leituras)):
    if leituras[i] != leituras[i - 1]:
        mudancas.append((i, leituras[i]))
print("Exemplo 8 - Mudanças detectadas:", mudancas)
    
========================================
Code 19:
valores = [1, 2, 2, 3, 1, 4, 2]
vistos = set()
filtrado = []
for v in valores:
    if v not in vistos:
        filtrado.append(v)
        vistos.add(v)
print("Exemplo 9 - Sem duplicatas:", filtrado)

========================================
Code 20:
letras = ["a", "b", "c", "d"]
resultado = ""
etapas = []
for letra in letras:
    resultado += letra
    etapas.append(resultado)
print("Exemplo 10 - Construção passo a passo:", etapas)

========================================
Code 21:
def fatorial_cumulativo():
    resultado = 1
    valores = []
    for i in range(1, 10):
        resultado *= i
        valores.append(resultado)
    return valores

========================================
Code 22:
def fibonacci():
    fib = [0, 1]
    for i in range(2, 15):
        fib.append(fib[i-1] + fib[i-2])
    return fib

========================================
Code 23:
def soma_acumulativa():
    numeros = [5, 2, 8, 1, 9, 3]
    total = 0
    resultado = []
    for num in numeros:
        total += num
        resultado.append(total)
    return resultado

========================================
Code 24:
def string_crescente():
    texto = ""
    caracteres = ['a', 'b', 'c', 'd', 'e']
    for char in caracteres:
        texto += char
    return texto

========================================
Code 25:
def multiplicacao_aninhada():
    produto = 1
    fatores = [1, 2, 3, 4, 5]
    for num in fatores:
        produto *= num
    return produto

========================================
Code 26:
def busca_em_profundidade(grafo={'A':['B','C'], 'B':['D'], 'C':[], 'D':[]}):
    visitados = set()
    pilha = ['A']
    resultado = []
    while pilha:
        vertice = pilha.pop()
        if vertice not in visitados:
            visitados.add(vertice)
            resultado.append(vertice)
            pilha.extend(grafo[vertice])
    return resultado

========================================
Code 27:
def bubble_sort():
    arr = [5, 3, 8, 6, 7, 2]
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

========================================
Code 28:
def gerador_congruencial():
    seed = 5
    resultados = []
    for _ in range(10):
        seed = (8121 * seed + 28411) % 134456
        resultados.append(seed)
    return resultados

========================================
Code 29:
def caminho_grafo():
    grafo = {0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}
    caminho = [0]
    atual = 0
    while grafo[atual]:
        proximo = grafo[atual].pop()
        caminho.append(proximo)
        atual = proximo
    return caminho

========================================
Code 30:
def fatorial_recursivo(n=5):
    if n == 0:
        return 1
    else:
        return n * fatorial_recursivo(n-1)

========================================
Code 31:
def simulacao_juros():
    capital = 1000
    juros = []
    for _ in range(10):
        capital *= 1.05
        juros.append(round(capital, 2))
    return juros

========================================
Code 32:
def torre_hanoi(n=3):
    movimentos = []
    def mover(de, para):
        movimentos.append(f"{de}→{para}")
    def resolver(n, origem, destino, auxiliar):
        if n > 0:
            resolver(n-1, origem, auxiliar, destino)
            mover(origem, destino)
            resolver(n-1, auxiliar, destino, origem)
    resolver(n, 'A', 'C', 'B')
    return movimentos

========================================
Code 33:
def integracao_numerica():
    def f(x): return x**2
    a, b = 0, 2
    n = 100
    h = (b - a) / n
    integral = 0
    for i in range(n):
        x = a + i*h
        integral += f(x) * h
    return integral

========================================
Code 34:
def newton_raphson(f=lambda x: x**2-2, df=lambda x: 2*x, x0=2, iteracoes=5):
    x = x0
    aproximacoes = []
    for _ in range(iteracoes):
        x = x - f(x)/df(x)
        aproximacoes.append(x)
    return aproximacoes

========================================
Code 35:
def markov_chain():
    matriz = [[0.9, 0.1], [0.5, 0.5]]
    estado = [1, 0]
    historico = []
    for _ in range(10):
        novo_estado = [0, 0]
        for i in range(2):
            for j in range(2):
                novo_estado[j] += estado[i] * matriz[i][j]
        estado = novo_estado
        historico.append(estado.copy())
    return historico

========================================
Code 36:
def runge_kutta(f=lambda t, y: t + y, t0=0, y0=1, h=0.1, passos=5):
    t, y = t0, y0
    resultados = []
    for _ in range(passos):
        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h/2, y + k2/2)
        k4 = h * f(t + h, y + k3)
        y += (k1 + 2*k2 + 2*k3 + k4)/6
        t += h
        resultados.append(y)
    return resultados

========================================
Code 37:
def lfsr():
    registrador = 0b1001
    saida = []
    for _ in range(15):
        bit = (registrador ^ (registrador >> 1)) & 1
        registrador = (registrador >> 1) | (bit << 3)
        saida.append(registrador)
    return saida

========================================
Code 38:
def caminho_critico():
    atividades = {
        'A': {'duracao': 2, 'dependencias': []},
        'B': {'duracao': 3, 'dependencias': ['A']},
        'C': {'duracao': 1, 'dependencias': ['B']}
    }
    tempos = {}
    for atv in ['A', 'B', 'C']:
        if not atividades[atv]['dependencias']:
            tempos[atv] = atividades[atv]['duracao']
        else:
            tempos[atv] = max(tempos[dep] for dep in atividades[atv]['dependencias']) + atividades[atv]['duracao']
    return tempos

========================================
Code 39:
def gauss_seidel(A=[[4,1],[1,3]], b=[1,2], iteracoes=5):
    n = len(b)
    x = [0] * n
    for _ in range(iteracoes):
        for i in range(n):
            soma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - soma) / A[i][i]
    return x

========================================
Code 40:
def backpropagation():
    pesos = [0.5, -0.3]
    entrada = 0.7
    alvo = 1.0
    historico = []
    for _ in range(10):
        sa��da = entrada * pesos[0] + pesos[1]
        erro = alvo - sa��da
        pesos[0] += 0.1 * erro * entrada
        pesos[1] += 0.1 * erro
        historico.append(pesos.copy())
    return historico

========================================
Code 41:
def fechamento_transitivo(grafo={'A':['B'],'B':['C'],'C':[]}):
    fechamento = {k: set(v) for k, v in grafo.items()}
    for k in grafo:
        for i in grafo:
            if k in fechamento[i]:
                fechamento[i].update(fechamento[k])
    return fechamento

========================================
Code 42:
def simulacao_epidemia():
    saudaveis = 990
    infectados = 10
    recuperados = 0
    historico = []
    for _ in range(20):
        novos_infectados = min(0.0003 * saudaveis * infectados, saudaveis)
        novos_recuperados = 0.1 * infectados
        saudaveis -= novos_infectados
        infectados += novos_infectados - novos_recuperados
        recuperados += novos_recuperados
        historico.append((saudaveis, infectados, recuperados))
    return historico

========================================
Code 43:
def hash_encadeado():
    from hashlib import sha256
    texto = "dado inicial"
    hashes = []
    for _ in range(5):
        texto = sha256(texto.encode()).hexdigest()
        hashes.append(texto)
    return hashes

========================================
Code 44:
def monte_carlo_dependente():
    import random
    pontos = [(random.random(), random.random()) for _ in range(1000)]
    dentro = 0
    resultados = []
    for x, y in pontos:
        if x**2 + y**2 <= 1:
            dentro += 1
        pi_estimado = 4 * dentro / (len(resultados)+1)
        resultados.append(pi_estimado)
    return resultados[-10:]

========================================
Code 45:
def compressao_rle():
    texto = "AAABBBCCCDDDD"
    comprimido = []
    count = 1
    for i in range(1, len(texto)):
        if texto[i] == texto[i-1]:
            count += 1
        else:
            comprimido.append((texto[i-1], count))
            count = 1
    comprimido.append((texto[-1], count))
    return comprimido

========================================
Code 46:
def gerador_mandelbrot():
    resultados = []
    for y in range(-10, 11):
        linha = []
        for x in range(-20, 21):
            c = complex(x/10, y/10)
            z = 0
            for _ in range(20):
                z = z**2 + c
            linha.append(abs(z))
        resultados.append(linha)
    return resultados

========================================
Code 47:
def criptografia_fluxo():
    chave = 0b1011
    texto = [0b0101, 0b1100, 0b0011]
    cifrado = []
    for byte in texto:
        cifrado.append(byte ^ chave)
        chave = (chave << 1) | (chave >> 3) & 0b1111
    return cifrado

========================================
Code 48:
def simulacao_bolsa():
    import random
    preco = 100.0
    historico = []
    for _ in range(30):
        variacao = (random.random() - 0.5) * 0.1 * preco
        preco += variacao
        historico.append(preco)
    return historico

========================================
Code 49:
def automato_celular():
    celulas = [0, 1, 0, 1, 0, 1, 0, 1]
    historico = []
    for _ in range(5):
        novas_celulas = []
        for i in range(len(celulas)):
            vizinhos = celulas[(i-1)%len(celulas)], celulas[(i+1)%len(celulas)]
            novas_celulas.append(1 if sum(vizinhos) == 1 else 0)
        celulas = novas_celulas
        historico.append(celulas.copy())
    return historico

========================================
Code 50:
def difusao_calor():
    temperatura = [20]*10
    temperatura[4] = 100
    historico = []
    for _ in range(10):
        nova_temp = temperatura.copy()
        for i in range(1, len(temperatura)-1):
            nova_temp[i] = 0.5 * (temperatura[i-1] + temperatura[i+1])
        temperatura = nova_temp
        historico.append(temperatura.copy())
    return historico

========================================
Code 51:
def fibonacci():
    n = 10  
    fib = [0, 1]
    for i in range(2, n+1):
        fib.append(fib[i-1] + fib[i-2])  
    return fib[n]

========================================
Code 52:
def bubble_sort():
    arr = [5, 3, 8, 6, 7, 2]
    n = len(arr)
    for i in range(n-1):  
        if arr[i] > arr[i+1]:
            arr[i], arr[i+1] = arr[i+1], arr[i]  
    return arr  

========================================
Code 53:
def juros_compostos():
    capital = 1000
    taxa = 0.05
    historico = [capital]
    for _ in range(5): 
        capital *= (1 + taxa)  
        historico.append(round(capital, 2))
    return historico

========================================
Code 54:
def prefix_sum():
    arr = [3, 1, 4, 1, 5]
    prefix = [arr[0]]
    for i in range(1, len(arr)):
        prefix.append(prefix[i-1] + arr[i])  
    return prefix

========================================
Code 55:
def sir_model():
    S, I, R = 990, 10, 0
    beta, gamma = 0.0003, 0.1
    historico = [(S, I, R)]
    for _ in range(10): 
        novos_infectados = min(beta * S * I, S)
        novos_recuperados = gamma * I
        S -= novos_infectados
        I += novos_infectados - novos_recuperados
        R += novos_recuperados
        historico.append((S, I, R))
    return historico

========================================
Code 56:
def gerador_congruencial():
    seed = 5
    resultados = [seed]
    for _ in range(5):
        seed = (8121 * seed + 28411) % 134456  
        resultados.append(seed)
    return resultados

========================================
Code 57:
def calcular_fatorial():
    n = 5
    fatorial = 1
    for i in range(1, n+1):
        fatorial *= i  
    return fatorial

========================================
Code 58:
def markov_chain():
    import numpy as np
    transicao = [[0.9, 0.1], [0.5, 0.5]]
    estado = [1, 0]
    historico = [estado.copy()]
    for _ in range(3):  # 3 passos
        estado = np.dot(estado, transicao)  
        historico.append([round(x, 2) for x in estado])
    return historico

========================================
Code 59:
import math

dias = 10
distancia_anterior = 100000
aceleracao_base = 1.01
dia = 1

print("Distância acumulada por dia (em km):")

for _ in range(dias):
    nova_distancia = distancia_anterior * aceleracao_base * math.log(dia + 1)
    print(f"Dia {dia}: {nova_distancia:,.2f} km")
    distancia_anterior = nova_distancia
    dia += 1

========================================
Code 60:
def runge_kutta():
    def f(t, y): return t + y  
    t, y, h = 0, 1, 0.1
    solucao = [(t, y)]
    for _ in range(3):  
        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h/2, y + k2/2)
        k4 = h * f(t + h, y + k3)
        y += (k1 + 2*k2 + 2*k3 + k4)/6  
        t += h
        solucao.append((round(t,1), round(y,4)))
    return solucao

========================================
Code 61:
def calcular_fatoriais():
    numeros = [1, 2, 3, 4, 5, 6]
    resultados = []
    fat = 1
    for n in numeros:
        fat *= n
        resultados.append((n, fat))
    return resultados

========================================
Code 62:
def converter_para_hexadecimal():
    valores = [10, 15, 20, 255, 100]
    hexadecimais = []
    ultimo = 0
    for val in valores:
        ultimo = val + ultimo % 100
        hexadecimais.append((ultimo, hex(ultimo)))
    return hexadecimais

========================================
Code 63:
def verificar_primos():
    numeros = [2, 3, 4, 5, 7, 11, 13, 15]
    primos = []
    ultimo_primo = None
    for num in numeros:
        primo = num > 1
        for i in range(2, int(num**0.5)+1):
            if num % i == 0:
                primo = False
                break
        if primo:
            ultimo_primo = num
        primos.append((num, primo, ultimo_primo))
    return primos

========================================
Code 64:
def calcular_area_circulos():
    raios = [1.0, 2.5, 3.0, 5.0]
    areas = []
    soma = 0
    for r in raios:
        soma += r
        areas.append((soma, 3.14159 * soma ** 2))
    return areas

========================================
Code 65:
def processar_strings():
    palavras = ["Python", "Código", "Exemplo", "Dados"]
    processadas = []
    concat = ""
    for palavra in palavras:
        concat += palavra[0]
        processadas.append((concat, palavra.upper(), palavra.lower(), len(concat)))
    return processadas

========================================
Code 66:
def classificar_temperaturas():
    temps = [20.5, 15.0, 30.2, 10.7, 25.0]
    classificacoes = []
    media = 0
    for i, temp in enumerate(temps):
        media = (media * i + temp) / (i + 1)
        classificacao = "Frio" if temp < media else "Quente"
        classificacoes.append((temp, media, classificacao))
    return classificacoes

========================================
Code 67:
def calcular_descontos():
    precos = [100.0, 50.0, 200.0, 75.0]
    descontos = []
    total = 0
    for preco in precos:
        total += preco
        desconto = preco * 0.1 if total > 300 else preco * 0.05
        descontos.append((total, desconto, preco - desconto))
    return descontos

========================================
Code 68:
def gerar_sequencia_fibonacci():
    n = 10
    sequencia = []
    a, b = 0, 1
    for _ in range(n):
        sequencia.append(a)
        a, b = b, a + b
    return sequencia

========================================
Code 69:
def analisar_senhas():
    senhas = ["senha123", "123456", "Segura@2023", "admin"]
    forcas = []
    padrao = ""
    for senha in senhas:
        padrao += senha[0]
        comprimento = len(padrao)
        tem_maiuscula = any(c.isupper() for c in padrao)
        tem_especial = any(not c.isalnum() for c in padrao)
        forcas.append((padrao, comprimento * (1 + tem_maiuscula + tem_especial)))
    return forcas

========================================
Code 70:
def converter_temperaturas():
    celsius = [0.0, 25.0, 37.0, 100.0]
    conversoes = []
    offset = 0
    for temp in celsius:
        offset += temp/10
        fahrenheit = (temp * 9/5) + 32 + offset
        kelvin = temp + 273.15 + offset
        conversoes.append((temp, fahrenheit, kelvin))
    return conversoes

========================================
Code 71:
def calcular_imc():
    dados = [(70, 1.75), (85, 1.80), (60, 1.65)]
    resultados = []
    imc_anterior = 0
    for peso, altura in dados:
        imc = peso / (altura ** 2) + imc_anterior/10
        imc_anterior = imc
        resultados.append((peso, altura, imc))
    return resultados

========================================
Code 72:
def verificar_palindromos():
    palavras = ["radar", "python", "ovo", "casa"]
    resultados = []
    ultimo_palindromo = ""
    for palavra in palavras:
        if palavra == palavra[::-1]:
            ultimo_palindromo = palavra
        resultados.append((palavra, palavra == palavra[::-1], ultimo_palindromo))
    return resultados

========================================
Code 73:
def calcular_juros_compostos():
    investimentos = [(1000, 0.05, 5), (5000, 0.07, 10), (2000, 0.03, 3)]
    resultados = []
    montante_acumulado = 0
    for principal, taxa, anos in investimentos:
        montante = principal * (1 + taxa) ** anos + montante_acumulado
        montante_acumulado += montante
        resultados.append((principal, taxa, anos, montante))
    return resultados

========================================
Code 74:
def processar_dados_sensor():
    leituras = [23.5, 24.0, 22.8, 25.1, 21.9]
    processados = []
    media = leituras[0]
    for leitura in leituras:
        media = (media + leitura) / 2
        processados.append((leitura, media))
    return processados

========================================
Code 75:
def classificar_produtos():
    produtos = [("Notebook", 2500), ("Celular", 1200), ("Tablet", 800)]
    classificacoes = []
    total = 0
    for nome, preco in produtos:
        total += preco
        categoria = "Premium" if preco > total/len(classificacoes+[1]) else "Básico"
        classificacoes.append((nome, preco, categoria))
    return classificacoes

========================================
Code 76:
def calcular_velocidade_media():
    dados = [(100, 2), (150, 3), (200, 4)]
    velocidades = []
    tempo_total = 0
    for distancia, tempo in dados:
        tempo_total += tempo
        velocidades.append((distancia, tempo_total, distancia/tempo_total))
    return velocidades

========================================
Code 77:
def extrair_dominios():
    emails = ["user@gmail.com", "admin@empresa.com", "contato@site.org"]
    dominios = []
    prefixo = ""
    for email in emails:
        prefixo += email.split('@')[0][0]
        dominio = prefixo + email.split('@')[1]
        dominios.append((email, dominio))
    return dominios

========================================
Code 78:
def calcular_consumo_energia():
    dispositivos = [("Geladeira", 50, 24), ("TV", 100, 5), ("Lâmpada", 15, 10)]
    consumos = []
    total = 0
    for nome, potencia, horas in dispositivos:
        total += potencia * horas
        consumos.append((nome, total))
    return consumos

========================================
Code 79:
def converter_moedas():
    valores = [100.0, 250.0, 50.0]
    conversoes = []
    acumulado = 0
    for valor in valores:
        acumulado += valor
        conversoes.append((acumulado, acumulado / 5.20))
    return conversoes

========================================
Code 80:
def analisar_textos():
    textos = ["Python é poderoso", "Data Science", "Machine Learning"]
    analises = []
    todas_palavras = []
    for texto in textos:
        palavras = texto.split()
        todas_palavras.extend(palavras)
        analises.append((texto, len(todas_palavras), sum(len(p) for p in todas_palavras)))
    return analises

========================================
Code 81:
def calcular_media_notas():
    alunos = [("João", [8.5, 7.0, 9.0]), ("Maria", [9.0, 9.5, 8.5])]
    medias = []
    media_geral = 0
    for i, (nome, notas) in enumerate(alunos):
        media = sum(notas)/len(notas)
        media_geral = (media_geral * i + media) / (i + 1)
        medias.append((nome, media, media_geral))
    return medias

========================================
Code 82:
def verificar_estoque():
    produtos = [("Caneta", 50), ("Caderno", 20), ("Borracha", 100)]
    status = []
    minimo = float('inf')
    for nome, quantidade in produtos:
        minimo = min(minimo, quantidade)
        status.append((nome, "OK" if quantidade > minimo else "Repor"))
    return status

========================================
Code 83:
def calcular_distancia_pontos():
    pontos = [((0, 0), (3, 4)), ((1, 1), (4, 5)), ((2, 3), (5, 7))]
    distancias = []
    distancia_total = 0
    for p1, p2 in pontos:
        distancia = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5
        distancia_total += distancia
        distancias.append((p1, p2, distancia_total))
    return distancias

========================================
Code 84:
def processar_logs():
    logs = ["ERRO: Falha no sistema", "INFO: Usuário logado", "ERRO: Arquivo não encontrado"]
    contagens = []
    erros = 0
    for log in logs:
        if log.startswith("ERRO"):
            erros += 1
        contagens.append((log, erros))
    return contagens

========================================
Code 85:
def calcular_volumes():
    dados = [("Cubo", 3), ("Esfera", 2), ("Cilindro", 5)]
    volumes = []
    fator = 1
    for nome, valor in dados:
        if nome == "Cubo":
            volume = valor ** 3 * fator
        elif nome == "Esfera":
            volume = (4/3) * 3.14159 * valor ** 3 * fator
        else:
            volume = 3.14159 * valor ** 2 * 5 * fator
        fator = volume % 10
        volumes.append((nome, volume))
    return volumes

========================================
Code 86:
def classificar_idades():
    idades = [12, 25, 7, 19, 30, 5]
    categorias = []
    ultima_categoria = ""
    for idade in idades:
        if idade < 13:
            categoria = "Criança"
        elif idade < 20:
            categoria = "Adolescente"
        elif idade < 60:
            categoria = "Adulto"
        else:
            categoria = "Idoso"
        if categoria == ultima_categoria:
            categoria += " (repetido)"
        ultima_categoria = categoria
        categorias.append((idade, categoria))
    return categorias

========================================
Code 87:
def calcular_potencia_eletrica():
    dados = [(110, 10), (220, 5), (110, 15)]
    potencias = []
    total_corrente = 0
    for tensao, corrente in dados:
        total_corrente += corrente
        potencias.append((tensao, total_corrente, tensao * total_corrente))
    return potencias

========================================
Code 88:
def extrair_metadados_arquivos():
    arquivos = ["relatorio.pdf", "imagem.jpg", "planilha.xlsx"]
    metadados = []
    extensoes = set()
    for arquivo in arquivos:
        nome, extensao = arquivo.split('.')
        extensoes.add(extensao)
        metadados.append((nome, extensao, len(extensoes)))
    return metadados

========================================
Code 89:
def calcular_combustivel_viagem():
    viagens = [(300, 12), (150, 10), (450, 15)]
    consumos = []
    combustivel_total = 0
    for distancia, consumo_medio in viagens:
        combustivel_total += distancia / consumo_medio
        consumos.append((distancia, consumo_medio, combustivel_total))
    return consumos

========================================
Code 90:
def gerar_hashes_simples():
    strings = ["senha", "123456", "secreto"]
    hashes = []
    hash_anterior = 0
    for s in strings:
        hash_val = (hash_anterior + sum(ord(c) for c in s)) % 1000
        hash_anterior = hash_val
        hashes.append((s, hash_val))
    return hashes


========================================
Code 91:
def calcular_soma_ponderada():
    valores = [10, 20, 30]
    pesos = [0.5, 1.5, 2.0]
    total = 0
    resultados = []
    for i in range(len(valores)):
        total += valores[i] * pesos[i]
        resultados.append((valores[i], pesos[i], total))
    return resultados

========================================
Code 92:
def gerar_sequencia_geometrica():
    a = 2
    r = 3
    n = 5
    sequencia = []
    for i in range(n):
        sequencia.append(a)
        a *= r
    return sequencia

========================================
Code 93:
def construir_triangulo_pascal():
    linhas = 5
    triangulo = []
    linha_anterior = []
    for i in range(linhas):
        linha = [1] if i == 0 else [1] + [linha_anterior[j] + linha_anterior[j+1] for j in range(i-1)] + [1]
        triangulo.append(linha)
        linha_anterior = linha
    return triangulo

========================================
Code 94:
def calcular_media_movel_ponderada_dependente():
    valores = [10, 20, 30, 40, 50]
    medias = []
    acumulada = 0
    for i in range(2, len(valores)):
        acumulada += (valores[i-2] * 0.2 + valores[i-1] * 0.3 + valores[i] * 0.5)
        medias.append((i, acumulada))
    return medias

========================================
Code 95:
def codificar_diff_sequencial_dependente():
    valores = [100, 105, 107, 110, 115]
    diffs = [valores[0]]
    acumulado = valores[0]
    for i in range(1, len(valores)):
        diferenca = valores[i] - acumulado
        diffs.append(diferenca)
        acumulado += diferenca  
    return diffs

========================================
Code 96:
def simular_investimento_acoes():
    precos = [50, 52, 51, 53, 55]
    saldo = 1000
    historico = []
    for p in precos:
        saldo *= (p / precos[precos.index(p)-1]) if precos.index(p) > 0 else 1
        historico.append((p, saldo))
    return historico

========================================
Code 97:
def calcular_maximo_local():
    valores = [10, 12, 15, 13, 18, 20, 17]
    maximos = []
    max_atual = valores[0]
    for v in valores:
        max_atual = max(max_atual, v)
        maximos.append(max_atual)
    return maximos

========================================
Code 98:
def processar_buffer():
    buffer = []
    dados = [1, 2, 3, 4, 5, 6, 7, 8]
    for i in range(len(dados)):
        buffer.append(dados[i])
        if len(buffer) > 3:
            buffer.pop(0)
    return buffer

========================================
Code 99:
def gerar_senha_sequencial():
    caracteres = ['a', 'b', 'c', '1', '2']
    senha = ''
    for i in range(5):
        senha += caracteres[(ord(senha[-1]) % len(caracteres)] if senha else caracteres[0]
    return senha

========================================
Code 100:
def calcular_derivada_dependente():
    valores = [0, 3, 6, 9, 12]
    derivadas = []
    ultima_derivada = 0
    for i in range(1, len(valores)):
        derivada = (valores[i] - valores[i-1]) + ultima_derivada
        derivadas.append(derivada)
        ultima_derivada = derivada
    return derivadas

========================================
Code 101:
def calcular_soma_acumulativa():
    numeros = [5, 3, 8, 2, 7]
    soma = 0
    resultados = []
    for num in numeros:
        soma += num
        resultados.append((num, soma))
    return resultados

========================================
Code 102:
def gerar_sequencia_fibonacci():
    n = 10
    sequencia = []
    a, b = 0, 1
    for _ in range(n):
        sequencia.append(a)
        a, b = b, a + b
    return sequencia

========================================
Code 103:
def calcular_media_movel_dependente():
    valores = [10, 12, 15, 13, 18, 20]
    media_movel = [valores[0]]
    for i in range(1, len(valores)):
        media = (valores[i] + media_movel[i-1]) / 2  
        media_movel.append(media)
    return media_movel

========================================
Code 104:
def codificar_rle():
    texto = "AAABBBCCDAA"
    codificado = []
    count = 1
    for i in range(1, len(texto)):
        if texto[i] == texto[i-1]:
            count += 1
        else:
            codificado.append((texto[i-1], count))
            count = 1
    codificado.append((texto[-1], count))
    return codificado

========================================
Code 105:
def processar_transacoes():
    saldo = 1000
    transacoes = [200, -50, 300, -100]
    historico = []
    for valor in transacoes:
        saldo += valor
        historico.append((valor, saldo))
    return historico

========================================
Code 106:
def construir_triangulo_pascal():
    linhas = 5
    triangulo = []
    linha_anterior = []
    for i in range(linhas):
        linha = [1] if i == 0 else [1] + [linha_anterior[j] + linha_anterior[j+1] for j in range(i-1)] + [1]
        triangulo.append(linha)
        linha_anterior = linha
    return triangulo

========================================
Code 107:
def simular_juros_compostos():
    capital = 1000
    taxa = 0.05
    resultados = []
    for mes in range(1, 13):
        capital *= (1 + taxa)
        resultados.append((mes, capital))
    return resultados

========================================
Code 108:
def codificar_diff():
    valores = [100, 105, 107, 110, 115]
    diffs = [valores[0]]
    for i in range(1, len(valores)):
        diffs.append(valores[i] - valores[i-1])
    return diffs

========================================
Code 109:
def calcular_maximo_local():
    valores = [10, 12, 15, 13, 18, 20, 17]
    max_atual = valores[0]
    maximos = []
    for v in valores:
        max_atual = max(max_atual, v)
        maximos.append(max_atual)
    return maximos

========================================
Code 110:
def gerar_senha_sequencial():
    caracteres = ['a', 'b', 'c', '1', '2']
    senha = caracteres[0]
    for i in range(1, 5):
        senha += caracteres[(ord(senha[-1]) % len(caracteres)]
    return senha

========================================
Code 111:
def calcular_prefix_sum():
    dados = [3, 1, 7, 0, 4, 1, 6]
    prefix_sum = [dados[0]]
    for i in range(1, len(dados)):
        prefix_sum.append(prefix_sum[i-1] + dados[i])
    return prefix_sum

========================================
Code 112:
def simular_cadeia_markov():
    import random
    estados = ['A', 'B', 'C']
    transicoes = {'A': {'A':0.1, 'B':0.6, 'C':0.3},
                 'B': {'A':0.5, 'B':0.2, 'C':0.3},
                 'C': {'A':0.4, 'B':0.1, 'C':0.5}}
    estado_atual = 'A'
    sequencia = [estado_atual]
    for _ in range(10):
        prob = random.random()
        acumulado = 0
        for prox_estado, p in transicoes[estado_atual].items():
            acumulado += p
            if prob <= acumulado:
                estado_atual = prox_estado
                break
        sequencia.append(estado_atual)
    return sequencia

========================================
Code 113:
def processar_buffer_circular():
    buffer = []
    dados = [1, 2, 3, 4, 5, 6, 7, 8]
    for i in range(len(dados)):
        buffer.append(dados[i])
        if len(buffer) > 3:
            buffer.pop(0)
    return buffer

========================================
Code 114:
def calcular_derivada_numerica_dependente():
    valores = [0, 3, 6, 9, 12]
    derivadas = []
    acumulado = 0
    for i in range(1, len(valores)):
        acumulado += valores[i] - valores[i-1]  
        derivadas.append(acumulado)
    return derivadas

========================================
Code 115:
def simular_fila_atendimento():
    tempo_chegada = [1, 3, 5, 7]
    tempo_servico = [2, 4, 1, 3]
    tempo_saida = []
    for i in range(len(tempo_chegada)):
        inicio = max(tempo_chegada[i], tempo_saida[i-1] if i > 0 else 0)
        tempo_saida.append(inicio + tempo_servico[i])
    return tempo_saida

========================================
Code 116:
def gerar_sequencia_collatz():
    n = 10
    sequencia = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        sequencia.append(n)
    return sequencia

========================================
Code 117:
def calcular_serie_temporal():
    valores = [10, 12, 11, 13, 15]
    suavizados = [valores[0]]
    alpha = 0.3
    for i in range(1, len(valores)):
        novo_valor = alpha * valores[i] + (1 - alpha) * suavizados[i-1]
        suavizados.append(novo_valor)
    return suavizados

========================================
Code 118:
def verificar_balanceamento_dependente():
    expressoes = ["(a+b)", "(x*(y+z))", "(()))"]
    resultados = []
    contador = 0  
    for exp in expressoes:
        balanceado = True
        for char in exp:
            if char == '(':
                contador += 1
            elif char == ')':
                contador -= 1
            if contador < 0:
                balanceado = False
                break
        resultados.append((exp, balanceado and contador == 0))
    return resultados

========================================
Code 119:
def simular_contador_estados():
    estados = [True, False, True, True, False]
    contagem = 0
    historico = []
    for estado in estados:
        contagem = contagem + 1 if estado else max(0, contagem - 1)
        historico.append(contagem)
    return historico

========================================
Code 120:
def calcular_diferenca_anterior_dependente():
    valores = [10, 15, 13, 18, 22]
    diffs = []
    ultima_diff = 0
    for i in range(len(valores)):
        diff = valores[i] - (valores[i-1] if i > 0 else 0) + ultima_diff
        diffs.append(diff)
        ultima_diff = diff
    return diffs

========================================
Code 121:
def processar_stack_operacoes():
    stack = []
    operacoes = [('push', 5), ('push', 3), ('pop', None), ('push', 7)]
    resultados = []
    for op, val in operacoes:
        if op == 'push':
            stack.append(val)
        elif op == 'pop':
            stack.pop()
        resultados.append(list(stack))
    return resultados

========================================
Code 122:
def gerar_sequencia_mandelbrot():
    c = complex(0.3, 0.5)
    z = 0
    sequencia = []
    for _ in range(10):
        z = z**2 + c
        sequencia.append(z)
    return sequencia

========================================
Code 123:
def calcular_raiz_quadrada_newton():
    num = 25
    estimativa = num / 2
    historico = []
    for _ in range(5):
        estimativa = (estimativa + num / estimativa) / 2
        historico.append(estimativa)
    return historico

========================================
Code 124:
def codificar_lzw():
    texto = "ABABABAB"
    dicionario = {chr(i): i for i in range(256)}
    proximo_codigo = 256
    codificacao = []
    w = ""
    for c in texto:
        wc = w + c
        if wc in dicionario:
            w = wc
        else:
            codificacao.append(dicionario[w])
            dicionario[wc] = proximo_codigo
            proximo_codigo += 1
            w = c
    if w:
        codificacao.append(dicionario[w])
    return codificacao

========================================
Code 125:
def simular_autômato_finito():
    estados = {'A': {'0':'A', '1':'B'},
              'B': {'0':'C', '1':'B'},
              'C': {'0':'A', '1':'B'}}
    estado_atual = 'A'
    entrada = "011001"
    caminho = [estado_atual]
    for simbolo in entrada:
        estado_atual = estados[estado_atual][simbolo]
        caminho.append(estado_atual)
    return caminho

========================================
Code 126:
def calcular_histograma_cumulativo():
    dados = [1, 3, 2, 4, 1, 3, 2]
    histograma = {}
    cumulativo = {}
    soma = 0
    for val in dados:
        histograma[val] = histograma.get(val, 0) + 1
        soma += val
        cumulativo[val] = cumulativo.get(val, 0) + soma
    return cumulativo

========================================
Code 127:
def simular_investimento_acoes():
    precos = [50, 52, 51, 53, 55]
    saldo = 1000
    historico = []
    for i in range(len(precos)):
        if i > 0:
            saldo *= (precos[i] / precos[i-1])
        historico.append((precos[i], saldo))
    return historico

========================================
Code 128:
def verificar_intervalos_sobrepostos():
    intervalos = [(1,3), (2,5), (4,6), (7,9)]
    resultados = []
    fim_anterior = float('-inf')
    for inicio, fim in intervalos:
        resultados.append((inicio > fim_anterior, inicio, fim))
        fim_anterior = fim
    return resultados

========================================
Code 129:
def gerar_hash_incremental():
    texto = "python"
    hash_val = 0
    for i, char in enumerate(texto):
        hash_val = (hash_val * 31 + ord(char)) % 1000
    return hash_val

========================================
Code 130:
import math

def calcular_entropia_shannon_dependente():
    texto = "aabbbccde"
    entropia = 0
    total = len(texto)
    for i, c in enumerate(set(texto), start=1):
        p = texto.count(c) / total
        entropia = (entropia + (-p * math.log2(p))) / i 
    return entropia

========================================
Code 131:
def calcular_soma_ponderada():
    valores = [10, 20, 30]
    pesos = [0.5, 1.5, 2.0]
    total = 0
    resultados = []
    for i in range(len(valores)):
        total += valores[i] * pesos[i]
        resultados.append((valores[i], pesos[i], total))
    return resultados

========================================
Code 132:
def gerar_sequencia_geometrica():
    a = 2
    r = 3
    sequencia = []
    for _ in range(5):
        sequencia.append(a)
        a *= r
    return sequencia

========================================
Code 133:
def calcular_saldo_contabil():
    transacoes = [100, -50, 200, -30]
    saldo = 500
    historico = []
    for t in transacoes:
        saldo += t
        historico.append((t, saldo))
    return historico
 
========================================
Code 134:
def construir_sequencia_triangular_dependente():
    sequencia = []
    acumulado = 0
    for n in range(1, 6):
        acumulado += n
        sequencia.append(acumulado)
    return sequencia

========================================
Code 135:
def calcular_juros_sobre_juros():
    capital = 1000
    resultados = []
    for mes in range(1, 6):
        capital *= 1.1
        resultados.append((mes, capital))
    return resultados

========================================
Code 136:
def simular_rendimento_fundo():
    aportes = [100, 200, 150]
    rendimento = 0.05
    saldo = 0
    historico = []
    for aporte in aportes:
        saldo = (saldo + aporte) * (1 + rendimento)
        historico.append((aporte, saldo))
    return historico
  
========================================
Code 137:
def gerar_codigo_incremental():
    produtos = ["mouse", "teclado", "monitor"]
    codigos = []
    ultimo_cod = 1000
    for p in produtos:
        ultimo_cod += 1
        codigos.append((p, f"COD{ultimo_cod}"))
    return codigos
 
========================================
Code 138:
def calcular_media_ponderada_acumulada():
    valores = [10, 20, 30]
    pesos = [1, 2, 3]
    soma_ponderada = 0
    soma_pesos = 0
    resultados = []
    for v, p in zip(valores, pesos):
        soma_ponderada += v * p
        soma_pesos += p
        resultados.append((v, p, soma_ponderada/soma_pesos))
    return resultados
  
========================================
Code 139:
def simular_emprestimo():
    principal = 10000
    taxa = 0.01
    pagamentos = []
    for mes in range(1, 4):
        juros = principal * taxa
        principal -= 3000
        pagamentos.append((mes, juros, principal))
    return pagamentos
      
========================================
Code 140:
def gerar_sequencia_padrao():
    seq = [1]
    for _ in range(5):
        seq.append(seq[-1] * 2 + 1)
    return seq    

========================================
Code 141:
def calcular_soma_exponencial():
    numeros = [1, 2, 3, 4]
    soma = 0
    resultados = []
    for n in numeros:
        soma += 2**n
        resultados.append((n, soma))
    return resultados

========================================
Code 142:
def gerar_sequencia_fatorial():
    sequencia = []
    fat = 1
    for n in range(1, 6):
        fat *= n
        sequencia.append((n, fat))
    return sequencia

========================================
Code 143:
def calcular_media_movel_ponderada():
    valores = [10, 12, 15, 18, 20]
    medias = []
    for i in range(2, len(valores)):
        media = (valores[i-2]*0.2 + valores[i-1]*0.3 + valores[i]*0.5)
        medias.append(media)
    return medias

========================================
Code 144:
def simular_crescimento_populacional():
    populacao = 1000
    taxa = 0.1
    historico = []
    for ano in range(1, 6):
        populacao *= (1 + taxa)
        historico.append((ano, populacao))
    return historico

========================================
Code 145:
def codificar_sequencia_diferencial():
    valores = [5, 8, 12, 15, 20]
    diffs = [valores[0]]
    for i in range(1, len(valores)):
        diffs.append(valores[i] - valores[i-1])
    return diffs

========================================
Code 146:
def calcular_saldo_investimento():
    aportes = [1000, 500, 800]
    rendimento = 0.08
    saldo = 0
    historico = []
    for aporte in aportes:
        saldo = (saldo + aporte) * (1 + rendimento)
        historico.append((aporte, saldo))
    return historico

========================================
Code 147:
def gerar_codigo_sequencial():
    produtos = ["Tablet", "Smartphone", "Laptop"]
    codigos = []
    ultimo = 1000
    for produto in produtos:
        ultimo += 5
        codigos.append((produto, f"DEV{ultimo}"))
    return codigos

========================================
Code 148:
def calcular_razao_acumulada():
    numeros = [2, 4, 6, 8]
    razao = 1
    resultados = []
    for n in numeros:
        razao *= n
        resultados.append((n, razao))
    return resultados

========================================
Code 149:
def simular_amortizacao_emprestimo():
    principal = 20000
    taxa = 0.015
    pagamentos = []
    for mes in range(1, 7):
        juros = principal * taxa
        principal -= 3500
        pagamentos.append((mes, juros, principal))
    return pagamentos

========================================
Code 150:
def gerar_sequencia_recursiva():
    seq = [2]
    for _ in range(6):
        seq.append(seq[-1] * 3 - 1)
    return seq

========================================
Code 151:
def calcular_variancia_accumulada():
    valores = [10, 15, 20, 25]
    media_accum = valores[0]
    variancias = []
    for i in range(1, len(valores)):
        media_accum = (media_accum + valores[i]) / 2
        variancias.append(media_accum)
    return variancias

========================================
Code 152:
def processar_buffer_fifo():
    buffer = []
    dados = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(len(dados)):
        buffer.append(dados[i])
        if len(buffer) > 4:
            buffer = buffer[1:]
    return buffer

========================================
Code 153:
def calcular_juros_compostos_continuos():
    capital = 5000
    taxa = 0.07
    resultados = []
    for ano in range(1, 6):
        capital *= (1 + taxa)**ano
        resultados.append((ano, capital))
    return resultados

========================================
Code 154:
def gerar_senha_cumulativa():
    caracteres = ['a', 'b', 'c', '1', '2', '3']
    senha = caracteres[0]
    for i in range(1, 6):
        senha += caracteres[(ord(senha[-1]) + i) % len(caracteres)]
    return senha

========================================
Code 155:
def calcular_peso_ponderado_accumulado():
    valores = [10, 20, 30, 40]
    pesos = [1, 2, 3, 4]
    total_ponderado = 0
    resultados = []
    for i in range(len(valores)):
        total_ponderado += valores[i] * pesos[i]
        resultados.append(total_ponderado)
    return resultados

========================================
Code 156:
def simular_cadeia_producao():
    estoque = 100
    demandas = [20, 30, 25, 40]
    historico = []
    for demanda in demandas:
        estoque = max(0, estoque - demanda)
        historico.append((demanda, estoque))
    return historico

========================================
Code 157:
def calcular_derivada_segunda():
    valores = [0, 2, 6, 12, 20]
    derivadas = []
    for i in range(2, len(valores)):
        derivada = valores[i] - 2*valores[i-1] + valores[i-2]
        derivadas.append(derivada)
    return derivadas

========================================
Code 158:
def gerar_checksum():
    dados = [65, 66, 67, 68]
    checksum = 0
    resultados = []
    for byte in dados:
        checksum = (checksum + byte) % 256
        resultados.append((byte, checksum))
    return resultados

========================================
Code 159:
def calcular_media_geometrica_accumulada():
    numeros = [2, 4, 8, 16]
    produto = 1
    resultados = []
    for i, n in enumerate(numeros, 1):
        produto *= n
        resultados.append((n, produto**(1/i)))
    return resultados

========================================
Code 160:
def simular_fila_prioridade():
    processos = [("P1", 5), ("P2", 3), ("P3", 8)]
    tempo_atual = 0
    resultados = []
    for processo, duracao in processos:
        tempo_atual += duracao
        resultados.append((processo, tempo_atual))
    return resultados

========================================
Code 161:
def calcular_integral_numerica():
    valores = [0, 1, 4, 9, 16]
    integral = 0
    resultados = []
    for i in range(1, len(valores)):
        integral += (valores[i] + valores[i-1]) / 2
        resultados.append(integral)
    return resultados

========================================
Code 162:
def gerar_hash_cumulativo():
    texto = "dados"
    hash_val = 0
    resultados = []
    for char in texto:
        hash_val = (hash_val * 31 + ord(char)) % 1000
        resultados.append((char, hash_val))
    return resultados

========================================
Code 163:
def calcular_razao_aurea_sequencial():
    a, b = 1, 1
    sequencia = []
    for _ in range(8):
        a, b = b, a + b
        sequencia.append(b/a)
    return sequencia

========================================
Code 164:
def simular_compostagem_continua():
    material = 1000
    taxa = 0.15
    resultados = []
    for dia in range(1, 8):
        material *= (1 - taxa)
        resultados.append((dia, material))
    return resultados

========================================
Code 165:
def calcular_diferenca_percentual_accumulada():
    valores = [100, 120, 90, 110]
    diff_accum = 0
    resultados = []
    for i in range(1, len(valores)):
        diff = (valores[i] - valores[i-1]) / valores[i-1]
        diff_accum += diff
        resultados.append(diff_accum)
    return resultados

========================================
Code 166:
def gerar_codigo_verificacao():
    numeros = [123, 456, 789]
    codigos = []
    verificador = 0
    for num in numeros:
        verificador = (verificador + num % 10) % 10
        codigos.append((num, verificador))
    return codigos

========================================
Code 167:
def calcular_volatilidade_accumulada():
    precos = [50, 52, 48, 55, 53]
    volatilidade = 0
    resultados = []
    for i in range(1, len(precos)):
        variacao = abs(precos[i] - precos[i-1]) / precos[i-1]
        volatilidade += variacao
        resultados.append(volatilidade)
    return resultados

========================================
Code 168:
def simular_degradacao():
    qualidade = 100
    taxas = [0.1, 0.2, 0.15, 0.25]
    historico = []
    for taxa in taxas:
        qualidade *= (1 - taxa)
        historico.append((taxa, qualidade))
    return historico

========================================
Code 169:
def calcular_correlacao_accumulada():
    x = [1, 2, 3, 4]
    y = [2, 4, 6, 8]
    soma_xy = 0
    resultados = []
    for i in range(len(x)):
        soma_xy += x[i] * y[i]
        resultados.append(soma_xy)
    return resultados

========================================
Code 170:
def gerar_sequencia_logistica():
    x = 0.5
    r = 3.7
    sequencia = []
    for _ in range(10):
        x = r * x * (1 - x)
        sequencia.append(x)
    return sequencia