Code 1:
def gerar_nomes_arquivos(n):
    arquivos = []
    tamanhoMax = 100
    for i in range(tamanhoMax):
        nome = f"relatorio_{i:03d}.pdf"
        arquivos.append(nome)
    return arquivos

========================================
Code 2:
import math

def calcular_valores_sensores(n):
    leituras = []
    for i in range(50):
        valor = round(math.sin(i * 0.1) * 100, 2)
        leituras.append(valor)
    return leituras

========================================
Code 3:
def gerar_cores(n):
    cores = []
    for i in range(50):
        r = (i * 37) % 256
        g = (i * 73) % 256
        b = (i * 113) % 256
        cores.append((r, g, b))
    return cores

========================================
Code 4:
def construir_linhas_csv(n):
    linhas = []
    tamanhoMax = 1000
    for i in range(tamanhoMax):
        linha = f"{i},Usuario_{i},usuario{i}@exemplo.com"
        linhas.append(linha)
    return linhas

========================================
Code 5:
import random

def simular_respostas(n):
    respostas = []
    for i in range(50):
        tempo = random.randint(80, 300)  # tempo entre 80ms e 300ms
        respostas.append(tempo)
    return respostas

========================================
Code 6:
import random
import string

def gerar_senhas(n):
    senhas = []
    for i in range(50):
        tamanho = random.randint(8, 12)
        caracteres = string.ascii_letters + string.digits + "!@#$%"
        senha = ''.join(random.choice(caracteres) for _ in range(tamanho))
        senhas.append(senha)
    return senhas

========================================
Code 7:
import random

def simular_temperaturas(50):
    temperaturas = []
    for i in range(n):
        temp = round(random.uniform(15.0, 35.0), 1)
        temperaturas.append(temp)
    return temperaturas
   
========================================
Code 8:
import uuid

def gerar_transacoes(n):
    transacoes = []
    for i in range(50):
        transacao_id = str(uuid.uuid4())
        transacoes.append(transacao_id)
    return transacoes

========================================
Code 9:
def gerar_miniaturas(n):
    miniaturas = []
    for i in range(50):
        resolucao = f"160x120-{i}"
        miniaturas.append(resolucao)
    return miniaturas

========================================         
Code 10:
import random

def gerar_coordenadas(n):
    coordenadas = []
    for i in range(n):
        lat = round(random.uniform(-90.0, 90.0), 6)
        lon = round(random.uniform(-180.0, 180.0), 6)
        coordenadas.append((lat, lon))
    return coordenadas

========================================
Code 11:
import random
import string
import math

def gerar_nomes_imagens(n):
    imagens = []
    for i in range(n):
        nome = f"imagem_{i:04d}.png"
        imagens.append(nome)
    return imagens

========================================
Code 12:
def gerar_numeros_aleatorios(n):
    numeros = []
    for i in range(n):
        numeros.append(random.randint(1, 100))
    return numeros    
    
========================================
Code 13:   
def converter_para_binario(n):
    binarios = []
    for i in range(n):
        binarios.append(bin(i)[2:])
    return binarios   
    
========================================
Code 14:
def gerar_combinacoes_rgb(n):
    cores = []
    for i in range(n):
        r = (i * 5) % 256
        g = (i * 10) % 256
        b = (i * 15) % 256
        cores.append((r, g, b))
    return cores  
    
========================================
Code 15:
def calcular_quadrados(n):
    quadrados = []
    for i in range(n):
        quadrados.append(i ** 2)
    return quadrados

========================================
Code 16: 
def gerar_codigos(n):
    codigos = []
    for i in range(n):
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        codigos.append(codigo)
    return codigos

========================================
Code 17:
def calcular_angulo_em_graus(n):
    angulos = []
    for i in range(n):
        rad = i * 0.1
        grau = round(math.degrees(rad), 2)
        angulos.append(grau)
    return angulos   
    
========================================
Code 18:
def gerar_datas_ficticias(n):
    datas = []
    for i in range(n):
        dia = (i % 30) + 1
        mes = (i % 12) + 1
        ano = 2023
        datas.append(f"{dia:02d}/{mes:02d}/{ano}")
    return datas
    
========================================
Code 19:
def criar_frases(n):
    frases = []
    for i in range(n):
        frases.append(f"Este é o item número {i}.")
    return frases  

========================================
Code 20:
def gerar_booleanos(n):
    valores = []
    for i in range(n):
        valores.append(i % 2 == 0)
    return valores 

========================================
Code 21:
def calcular_quadrados():
    numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    quadrados = []
    for num in numeros:
        quadrados.append(num ** 2)
    return quadrados

========================================
Code 22:
def calcular_quadrados_e_cubos():
    resultados = []
    for i in range(1, 11):  
        quadrado = i ** 2
        cubo = i ** 3
        resultados.append((quadrado, cubo))
    return resultados

========================================
Code 23:
def verificar_primos():
    candidatos = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    primos = []
    for num in candidatos:
        is_primo = True
        for i in range(2, int(num**0.5)+1):
            if num % i == 0:
                is_primo = False
                break
        primos.append(is_primo)
    return primos

========================================
Code 24:
def calcular_fatoriais():
    fatoriais = [1]
    for i in range(1, 10):
        fatoriais.append(fatoriais[i-1] * i)
    return fatoriais

========================================
Code 25:
def converter_para_binario():
    numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    binarios = []
    for num in numeros:
        binarios.append(bin(num)[2:])
    return binarios

========================================
Code 26:
def gerar_cores_hex():
    import random
    cores = []
    for _ in range(10):
        cores.append(f"#{random.randint(0, 0xFFFFFF):06x}")
    return cores

========================================
Code 27:
def simular_lancamentos_dados():
    import random
    resultados = []
    for _ in range(20):
        resultados.append(random.randint(1, 6))
    return resultados

========================================
Code 28:
def calcular_raizes_quadradas():
    import math
    numeros = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    raizes = []
    for num in numeros:
        raizes.append(math.sqrt(num))
    return raizes

========================================
Code 29:
def gerar_emails():
    dominio = "exemplo.com"
    usuarios = ["joao", "maria", "pedro", "ana"]
    emails = []
    for usuario in usuarios:
        emails.append(f"{usuario}@{dominio}")
    return emails

========================================
Code 30:
def criar_matriz_identidade():
    tamanho = 4
    matriz = []
    for i in range(tamanho):
        linha = [0] * tamanho
        linha[i] = 1
        matriz.append(linha)
    return matriz

========================================
Code 31:
def calcular_potencias():
    base = 2
    expoentes = [0, 1, 2, 3, 4, 5]
    potencias = []
    for exp in expoentes:
        potencias.append(base ** exp)
    return potencias

========================================
Code 32:
def gerar_coordenadas_aleatorias():
    import random
    coordenadas = []
    for _ in range(5):
        coordenadas.append((random.random(), random.random()))
    return coordenadas

========================================
Code 33:
def criar_dicionario_numeros():
    chaves = ['a', 'b', 'c', 'd']
    valores = [1, 2, 3, 4]
    dicionario = {}
    for chave, valor in zip(chaves, valores):
        dicionario[chave] = valor
    return dicionario

========================================
Code 34:
def simular_temperaturas():
    import random
    temperaturas = []
    for _ in range(24):
        temperaturas.append(round(random.gauss(25, 5), 1))
    return temperaturas

========================================
Code 35:
def calcular_senos():
    import math
    angulos = [0, 30, 45, 60, 90]
    senos = []
    for ang in angulos:
        rad = math.radians(ang)
        senos.append(round(math.sin(rad), 4))
    return senos

========================================
Code 36:
def gerar_hashes():
    import hashlib
    textos = ["senha1", "segredo", "123456"]
    hashes = []
    for texto in textos:
        hashes.append(hashlib.md5(texto.encode()).hexdigest())
    return hashes

========================================
Code 37:
def criar_lista_palavras():
    import random
    import string
    palavras = []
    for _ in range(5):
        palavra = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
        palavras.append(palavra)
    return palavras

========================================
Code 38:
def calcular_medias_isoladas():
    dados = [10, 20, 30, 40, 50]
    medias = []
    for num in dados:
        medias.append(num / 2) 
    return medias

========================================
Code 39:
def verificar_palindromos():
    palavras = ["ovo", "python", "reviver", "casa"]
    resultados = []
    for palavra in palavras:
        resultados.append(palavra == palavra[::-1])
    return resultados

========================================
Code 40:
def gerar_progressao_aritmetica():
    a1 = 5
    r = 3
    termos = []
    for i in range(10):
        termos.append(a1 + i * r)
    return termos

========================================
Code 41:
def calcular_distancia_origem():
    import math
    pontos = [(1,1), (2,2), (3,4), (5,5)]
    distancias = []
    for (x, y) in pontos:
        distancias.append(round(math.sqrt(x**2 + y**2), 2))
    return distancias

========================================
Code 42:
def criar_sequencia_alternada():
    sequencia = []
    for i in range(10):
        sequencia.append((-1)**i)
    return sequencia

========================================
Code 43:
def gerar_nomes_aleatorios():
    import random
    nomes = []
    primeiros = ["Ana", "João", "Maria", "Pedro"]
    sobrenomes = ["Silva", "Santos", "Oliveira", "Souza"]
    for _ in range(5):
        nomes.append(f"{random.choice(primeiros)} {random.choice(sobrenomes)}")
    return nomes

========================================
Code 44:
def calcular_dobro_e_triplo():
    numeros = [1, 2, 3, 4, 5]
    resultados = []
    for num in numeros:
        resultados.append((num*2, num*3))  
    return resultados

========================================
Code 45:
def converter_para_fahrenheit():
    temperaturas_c = [0, 10, 20, 30, 40]
    fahrenheit = []
    for tc in temperaturas_c:
        fahrenheit.append(round((tc * 9/5) + 32, 1))
    return fahrenheit

========================================
Code 46:
def gerar_permutacoes():
    import random
    lista_original = [1, 2, 3]
    permutacoes = []
    for _ in range(3):
        copia = lista_original.copy()
        random.shuffle(copia)
        permutacoes.append(copia)
    return permutacoes

========================================
Code 47:
def calcular_velocidade_media():
    distancias = [100, 200, 150, 300]
    tempos = [2, 4, 3, 5]
    velocidades = []
    for d, t in zip(distancias, tempos):
        velocidades.append(round(d / t, 2))
    return velocidades

========================================
Code 48:
def criar_arquivos_temporarios():
    import tempfile
    arquivos = []
    for _ in range(3):
        arquivos.append(tempfile.NamedTemporaryFile(delete=False).name)
    return arquivos

========================================
Code 49:
def simular_crescimento_populacional():
    populacoes = []
    taxas = [0.01, 0.02, 0.03]
    pop_inicial = 1000
    anos = 5
    for taxa in taxas:
        pop = pop_inicial
        for _ in range(anos):
            pop *= (1 + taxa)
        populacoes.append(round(pop))
    return populacoes

========================================
Code 50:
def gerar_uuid():
    import uuid
    uuids = []
    for _ in range(5):
        uuids.append(str(uuid.uuid4()))
    return uuids

========================================
Code 51:
def converter_para_grayscale():
    import numpy as np
    imagem = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    gray = np.zeros((100, 100))
    for i in range(100):
        r, g, b = imagem[i, 50] 
        gray[i, 50] = 0.2989*r + 0.5870*g + 0.1140*b
    return gray

========================================
Code 52:
def calcular_estatisticas():
    dados = [2.3, 4.5, 1.2, 6.7, 3.4]
    stats = []
    for valor in dados:
        stats.append((valor, valor**2, valor**0.5))  
    return stats

========================================
Code 53:
def contar_caracteres():
    textos = ["Python", "Paralelismo", "Processamento"]
    contagens = []
    for texto in textos:
        contagens.append((texto, len(texto)))
    return contagens

========================================
Code 54:
def simular_dados():
    import random
    resultados = []
    for _ in range(1000):
        resultados.append(random.randint(1, 6))
    return sum(resultados)/len(resultados)  

========================================
Code 55:
def gerar_senhas():
    import random
    import string
    senhas = []
    for _ in range(5):
        senha = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        senhas.append(senha)
    return senhas 

========================================
Code 56:
def converter_temperaturas():
    temps_c = [0, 10, 20, 30, 40]
    temps_f = []
    for tc in temps_c:
        temps_f.append(tc * 9/5 + 32)
    return temps_f

========================================
Code 57:
def calcular_areas():
    import math
    raios = [1, 2, 3, 4, 5]
    areas = []
    for r in raios:
        areas.append(math.pi * r**2)
    return areas

========================================
Code 58:
def processar_compras():
    itens = [("maçã", 2.5), ("leite", 3.0), ("pão", 4.2)]
    totais = []
    for item, preco in itens:
        totais.append((item, preco * 1.1))  
    return totais

========================================
Code 59:
def calcular_cubos():
    numeros = [1, 2, 3, 4, 5]
    resultados = []
    for num in numeros:
        resultados.append((num, num ** 3, num ** (1/3))) 
    return resultados

========================================
Code 60:
def validar_emails():
    emails = ["user@exemplo.com", "invalido", "outro@site.com"]
    validos = []
    for email in emails:
        validos.append(("@" in email and "." in email.split("@")[1]))
    return validos

========================================
Code 61:
def calcular_fatoriais():
    from math import factorial
    numeros = [1, 2, 3, 4, 5, 6]
    return [(n, factorial(n)) for n in numeros]

========================================
Code 62:
def converter_para_hexadecimal():
    valores = [10, 15, 20, 255, 100]
    return [(val, hex(val)) for val in valores]

========================================
Code 63:
def verificar_primos():
    numeros = [2, 3, 4, 5, 7, 11, 13, 15]
    return [(num, num > 1 and all(num % i != 0 for i in [2, 3, 5, 7])) for num in numeros]

========================================
Code 64:
def calcular_area_circulos():
    raios = [1.0, 2.5, 3.0, 5.0]
    return [(r, 3.14159 * r ** 2) for r in raios]

========================================
Code 65:
def processar_strings():
    palavras = ["Python", "Código", "Exemplo", "Dados"]
    return [(p, p.upper(), p.lower(), len(p)) for p in palavras]

========================================
Code 66:
def classificar_temperaturas():
    temps = [20.5, 15.0, 30.2, 10.7, 25.0]
    return [(t, "Frio" if t < 15 else "Ameno" if t < 25 else "Quente") for t in temps]

========================================
Code 67:
def calcular_descontos():
    precos = [100.0, 50.0, 200.0, 75.0]
    return [(p, p * 0.1 if p > 100 else p * 0.05, p * 0.9 if p > 100 else p * 0.95) for p in precos]

========================================
Code 68:
def calcular_fibonacci_posicoes():
    posicoes = [5, 7, 10]
    phi = (1 + 5**0.5) / 2
    return [(n, int((phi**n - (-phi)**-n) / 5**0.5)) for n in posicoes]

========================================
Code 69:
def analisar_senhas():
    senhas = ["senha123", "123456", "Segura@2023", "admin"]
    return [(s, len(s) * (1 + (s.lower() != s) + (not s.isalnum()))) for s in senhas]

========================================
Code 70:
def converter_temperaturas():
    celsius = [0.0, 25.0, 37.0, 100.0]
    return [(c, c * 9/5 + 32, c + 273.15) for c in celsius]

========================================
Code 71:
def calcular_imc():
    dados = [(70, 1.75), (85, 1.80), (60, 1.65)]
    return [(p, a, p / a**2) for p, a in dados]

========================================
Code 72:
def verificar_palindromos():
    palavras = ["radar", "python", "ovo", "casa"]
    return [(p, p == p[::-1]) for p in palavras]

========================================
Code 73:
def calcular_juros_compostos():
    investimentos = [(1000, 0.05, 5), (5000, 0.07, 10), (2000, 0.03, 3)]
    return [(p, t, a, p * (1 + t)**a) for p, t, a in investimentos]

========================================
Code 74:
def processar_dados_sensor():
    leituras = [23.5, 24.0, 22.8, 25.1, 21.9]
    return [(l, (l - 20) / 10) for l in leituras]

========================================
Code 75:
def classificar_produtos():
    produtos = [("Notebook", 2500), ("Celular", 1200), ("Tablet", 800)]
    return [(n, p, "Premium" if p > 2000 else "Intermediário" if p > 1000 else "Básico") for n, p in produtos]

========================================
Code 76:
def calcular_velocidade_media():
    dados = [(100, 2), (150, 3), (200, 4)]
    return [(d, t, d/t) for d, t in dados]

========================================
Code 77:
def extrair_dominios():
    emails = ["user@gmail.com", "admin@empresa.com", "contato@site.org"]
    return [(e, e.split('@')[1]) for e in emails]

========================================
Code 78:
def calcular_consumo_energia():
    dispositivos = [("Geladeira", 50, 24), ("TV", 100, 5), ("Lâmpada", 15, 10)]
    return [(n, p * h / 1000) for n, p, h in dispositivos]

========================================
Code 79:
def converter_moedas():
    valores = [100.0, 250.0, 50.0]
    taxa = 5.20
    return [(v, v / taxa) for v in valores]

========================================
Code 80:
def analisar_textos():
    textos = ["Python é poderoso", "Data Science", "Machine Learning"]
    return [(t, len(t.split()), len(t), len([c for c in t.lower() if c in 'aeiouáéíóúãõâêîôû'])) for t in textos]

========================================
Code 81:
def calcular_media_notas():
    alunos = [("João", [8.5, 7.0, 9.0]), ("Maria", [9.0, 9.5, 8.5])]
    return [(n, sum(notas)/len(notas)) for n, notas in alunos]

========================================
Code 82:
def verificar_estoque():
    produtos = [("Caneta", 50), ("Caderno", 20), ("Borracha", 100)]
    return [(n, "OK" if q >= 30 else "Repor") for n, q in produtos]

========================================
Code 83:
def calcular_distancia_pontos():
    pontos = [((0, 0), (3, 4)), ((1, 1), (4, 5)), ((2, 3), (5, 7))]
    return [(p1, p2, ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5) for p1, p2 in pontos]

========================================
Code 84:
def processar_logs():
    logs = ["ERRO: Falha no sistema", "INFO: Usuário logado", "ERRO: Arquivo não encontrado"]
    return [(l, l.split(':')[0]) for l in logs]

========================================
Code 85:
def calcular_volumes():
    dados = [("Cubo", 3), ("Esfera", 2), ("Cilindro", 5)]
    return [(n, 3**3 if n == "Cubo" else (4/3)*3.14159*2**3 if n == "Esfera" else 3.14159*5**2*5) for n, v in dados]

========================================
Code 86:
def classificar_idades():
    idades = [12, 25, 7, 19, 30, 5]
    return [(i, "Criança" if i < 13 else "Adolescente" if i < 20 else "Adulto" if i < 60 else "Idoso") for i in idades]

========================================
Code 87:
def calcular_potencia_eletrica():
    dados = [(110, 10), (220, 5), (110, 15)]
    return [(v, a, v * a) for v, a in dados]

========================================
Code 88:
def extrair_metadados_arquivos():
    arquivos = ["relatorio.pdf", "imagem.jpg", "planilha.xlsx"]
    return [(a.split('.')[0], a.split('.')[1], a.split('.')[1].upper()) for a in arquivos]

========================================
Code 89:
def calcular_combustivel_viagem():
    viagens = [(300, 12), (150, 10), (450, 15)]
    return [(d, c, d/c) for d, c in viagens]

========================================
Code 90:
def gerar_hashes_simples():
    strings = ["senha", "123456", "secreto"]
    return [(s, sum(ord(c) for c in s) % 1000) for s in strings]


========================================
Code 91:
def calcular_quadrados_perfeitos():
    numeros = [4, 9, 16, 25, 36]
    return [(n, int(n**0.5)) for n in numeros]

========================================
Code 92:
def verificar_anagramas():
    palavras = ["amor", "roma", "casa", "saco"]
    referencia = "amor"
    return [(p, sorted(p) == sorted(referencia)) for p in palavras]

========================================
Code 93:
def converter_para_binario():
    valores = [5, 10, 15, 20]
    return [(v, bin(v)) for v in valores]

========================================
Code 94:
def calcular_dias_para_natal():
    from datetime import date
    datas = [date(2023, 12, 20), date(2023, 12, 24), date(2023, 12, 31)]
    natal = date(2023, 12, 25)
    return [(d, (natal - d).days) for d in datas]

========================================
Code 95:
def classificar_numeros():
    numeros = [10, 20, 30, 40]
    return [(n, "Par" if n % 2 == 0 else "Ímpar", "Múltiplo de 10" if n % 10 == 0 else "") for n in numeros]

========================================
Code 96:
def extrair_vogais():
    palavras = ["python", "programação", "dados"]
    return [(p, [c for c in p if c in 'aeiou']) for p in palavras]

========================================
Code 97:
def calcular_volume_esferas():
    raios = [1.0, 2.0, 3.0]
    return [(r, (4/3) * 3.14159 * r**3) for r in raios]

========================================
Code 98:
def gerar_codigos():
    produtos = ["Mouse", "Teclado", "Monitor"]
    return [(p, f"{p[:3].upper()}-{len(p)}") for p in produtos]

========================================
Code 99:
def verificar_extensoes():
    arquivos = ["foto.jpg", "relatorio.pdf", "planilha.xlsx"]
    return [(a, a.split('.')[-1]) for a in arquivos]

========================================
Code 100:
def calcular_desvio_padrao():
    amostras = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return [(a, sum(a)/len(a)) for a in amostras]

========================================
Code 101:
def calcular_raizes_quadradas():
    numeros = [4, 9, 16, 25, 36]
    resultados = []
    for num in numeros:
        resultados.append((num, num**0.5))
    return resultados

========================================
Code 102:
def converter_fahrenheit_celsius():
    temperaturas = [32, 68, 95, 104]
    conversoes = []
    for temp in temperaturas:
        conversoes.append((temp, (temp - 32) * 5/9))
    return conversoes

========================================
Code 103:
def contar_vogais():
    palavras = ["Python", "Programação", "Dados"]
    contagens = []
    for palavra in palavras:
        vogais = sum(1 for letra in palavra.lower() if letra in 'aeiou')
        contagens.append((palavra, vogais))
    return contagens

========================================
Code 104:
def calcular_imc():
    dados = [(70, 1.75), (85, 1.80), (60, 1.65)]
    resultados = []
    for peso, altura in dados:
        resultados.append((peso, altura, peso/(altura**2)))
    return resultados

========================================
Code 105:
def verificar_palindromos():
    strings = ["radar", "python", "ovo", "casa"]
    resultados = []
    for s in strings:
        resultados.append((s, s == s[::-1]))
    return resultados

========================================
Code 106:
def calcular_juros_simples():
    investimentos = [(1000, 0.05, 2), (2000, 0.07, 3)]
    resultados = []
    for principal, taxa, tempo in investimentos:
        resultados.append((principal, principal*taxa*tempo))
    return resultados

========================================
Code 107:
def gerar_hashes_md5():
    import hashlib
    textos = ["senha123", "dados456", "info789"]
    hashes = []
    for texto in textos:
        hashes.append((texto, hashlib.md5(texto.encode()).hexdigest()))
    return hashes

========================================
Code 108:
def calcular_areas_circulos():
    import math
    raios = [1.0, 2.5, 3.0, 5.0]
    areas = []
    for r in raios:
        areas.append((r, math.pi*r**2))
    return areas

========================================
Code 109:
def classificar_numeros():
    numeros = [1, 2, 3, 4, 5, 6]
    classificacoes = []
    for num in numeros:
        classificacoes.append((num, "par" if num%2==0 else "ímpar"))
    return classificacoes

========================================
Code 110:
def extrair_dominios():
    emails = ["user@exemplo.com", "admin@empresa.org", "contato@site.net"]
    dominios = []
    for email in emails:
        dominios.append((email, email.split('@')[1]))
    return dominios

========================================
Code 111:
def calcular_fatoriais():
    from math import factorial
    numeros = [1, 2, 3, 4, 5]
    resultados = []
    for n in numeros:
        resultados.append((n, factorial(n)))  
    return resultados

========================================
Code 112:
def converter_para_binario():
    numeros = [10, 15, 20, 25]
    binarios = []
    for num in numeros:
        binarios.append((num, bin(num)))
    return binarios

========================================
Code 113:
def calcular_volume_esferas():
    import math
    raios = [1.0, 2.0, 3.0]
    volumes = []
    for r in raios:
        volumes.append((r, (4/3)*math.pi*r**3))
    return volumes

========================================
Code 114:
def verificar_primos():
    numeros = [2, 3, 4, 5, 7, 11, 13, 15]
    resultados = []
    for num in numeros:
        if num < 2:
            resultados.append((num, False))
            continue
        primo = all(num % i != 0 for i in range(2, int(num**0.5) + 1))
        resultados.append((num, primo))
    return resultados

========================================
Code 115:
def processar_strings():
    strings = ["Python", "Código", "Exemplo"]
    processadas = []
    for s in strings:
        processadas.append((s, s.upper(), s.lower(), len(s)))
    return processadas

========================================
Code 116:
def calcular_descontos():
    produtos = [("Notebook", 2500), ("Celular", 1200), ("Tablet", 800)]
    descontos = []
    for nome, preco in produtos:
        desconto = preco*0.1 if preco>2000 else preco*0.05
        descontos.append((nome, preco, desconto))
    return descontos

========================================
Code 117:
def gerar_codigos():
    produtos = ["Mouse", "Teclado", "Monitor"]
    codigos = []
    for i, produto in enumerate(produtos, 1001):
        codigos.append((produto, f"COD-{i}"))
    return codigos

========================================
Code 118:
def calcular_velocidades():
    dados = [(100, 2), (150, 3), (200, 4)]
    velocidades = []
    for distancia, tempo in dados:
        velocidades.append((distancia, tempo, distancia/tempo))
    return velocidades

========================================
Code 119:
def analisar_textos():
    textos = ["Python é poderoso", "Data Science", "Machine Learning"]
    analises = []
    for texto in textos:
        palavras = texto.split()
        vogais = sum(1 for letra in texto.lower() if letra in 'aeiou')
        analises.append((texto, len(palavras), vogais))
    return analises

========================================
Code 120:
def converter_para_hexadecimal():
    numeros = [10, 15, 20, 255]
    hexadecimais = []
    for num in numeros:
        hexadecimais.append((num, hex(num)))
    return hexadecimais

========================================
Code 121:
def calcular_consumo_energia():
    dispositivos = [("Geladeira", 50, 24), ("TV", 100, 5), ("Lâmpada", 15, 10)]
    consumos = []
    for nome, potencia, horas in dispositivos:
        consumos.append((nome, potencia*horas/1000))
    return consumos

========================================
Code 122:
def verificar_anagramas():
    pares = [("amor", "roma"), ("casa", "saco"), ("pato", "topa")]
    resultados = []
    for a, b in pares:
        resultados.append((a, b, sorted(a)==sorted(b)))
    return resultados

========================================
Code 123:
def calcular_distancia_pontos():
    pontos = [((0,0), (3,4)), ((1,1), (4,5)), ((2,3), (5,7))]
    distancias = []
    for (x1,y1), (x2,y2) in pontos:
        distancia = ((x2-x1)**2 + (y2-y1)**2)**0.5
        distancias.append(((x1,y1), (x2,y2), distancia))
    return distancias

========================================
Code 124:
def processar_logs():
    logs = ["ERRO: Sistema falhou", "INFO: Usuário logado", "ERRO: Arquivo não encontrado"]
    contagens = []
    for log in logs:
        contagens.append((log, log.split(':')[0]))
    return contagens

========================================
Code 125:
def classificar_idades():
    idades = [12, 25, 7, 19, 30, 5]
    categorias = []
    for idade in idades:
        categoria = "Criança" if idade<13 else "Adolescente" if idade<20 else "Adulto"
        categorias.append((idade, categoria))
    return categorias

========================================
Code 126:
def calcular_potencia_eletrica():
    dados = [(110, 10), (220, 5), (110, 15)]
    potencias = []
    for tensao, corrente in dados:
        potencias.append((tensao, corrente, tensao*corrente))
    return potencias

========================================
Code 127:
def extrair_metadados():
    arquivos = ["relatorio.pdf", "imagem.jpg", "planilha.xlsx"]
    metadados = []
    for arquivo in arquivos:
        nome, extensao = arquivo.split('.')
        metadados.append((nome, extensao))
    return metadados

========================================
Code 128:
def calcular_combustivel_viagem():
    viagens = [(300, 12), (150, 10), (450, 15)]
    consumos = []
    for distancia, consumo_medio in viagens:
        consumos.append((distancia, consumo_medio, distancia/consumo_medio))
    return consumos

========================================
Code 129:
def gerar_senhas_aleatorias():
    import random
    import string
    senhas = []
    for _ in range(3):
        tamanho = random.randint(8, 12)
        senha = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(tamanho))
        senhas.append((tamanho, senha))
    return senhas

========================================
Code 130:
def converter_moedas():
    valores = [100.0, 250.0, 50.0]
    conversoes = []
    for valor in valores:
        conversoes.append((valor, valor/5.20))
    return conversoes

========================================
Code 131:
def calcular_quadrados():
    numeros = [1, 2, 3, 4, 5]
    resultados = []
    for n in numeros:
        resultados.append((n, n**2))
    return resultados

========================================
Code 132:
def verificar_palavras_maior_5():
    palavras = ["python", "dados", "algoritmo", "code"]
    resultados = []
    for p in palavras:
        resultados.append((p, len(p) > 5))
    return resultados

========================================
Code 133:
def converter_para_ascii():
    caracteres = ['A', 'b', '1', '@']
    resultados = []
    for c in caracteres:
        resultados.append((c, ord(c)))
    return resultados

========================================
Code 134:
def calcular_area_retangulos():
    dimensoes = [(3,4), (5,5), (2,7)]
    resultados = []
    for l, a in dimensoes:
        resultados.append((l, a, l*a))
    return resultados

========================================
Code 135:
def verificar_divisibilidade_3():
    numeros = [9, 10, 12, 15]
    resultados = []
    for n in numeros:
        resultados.append((n, n%3 == 0))
    return resultados

========================================
Code 136:
def extrair_ultimo_caractere():
    palavras = ["banana", "casa", "dado"]
    resultados = []
    for p in palavras:
        resultados.append((p, p[-1]))
    return resultados

========================================
Code 137:
def calcular_cubos():
    valores = [1, 2, 3, 4]
    resultados = []
    for v in valores:
        resultados.append((v, v**3))
    return resultados

========================================
Code 138:
def verificar_letra_inicial():
    palavras = ["gato", "cachorro", "peixe"]
    resultados = []
    for p in palavras:
        resultados.append((p, p[0].lower() in 'aeiou'))
    return resultados

========================================
Code 139:
def calcular_dobro():
    numeros = [10, 25, 30]
    resultados = []
    for n in numeros:
        resultados.append((n, n*2))
    return resultados

========================================
Code 140:
def contar_caracteres():
    strings = ["hello", "world"]
    resultados = []
    for s in strings:
        resultados.append((s, len(s)))
    return resultados    

========================================
Code 141:
def calcular_raizes_cubicas():
    numeros = [8, 27, 64, 125]
    resultados = []
    for n in numeros:
        resultados.append((n, n**(1/3)))
    return resultados

========================================
Code 142:
def verificar_numeros_primos():
    numeros = [2, 3, 4, 5, 7, 11, 13]
    resultados = []
    for n in numeros:
        primo = n > 1
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                primo = False
                break
        resultados.append((n, primo))
    return resultados

========================================
Code 143:
def converter_para_octal():
    valores = [10, 20, 30, 40]
    resultados = []
    for v in valores:
        resultados.append((v, oct(v)))
    return resultados

========================================
Code 144:
def calcular_perimetro_circulos():
    raios = [1.0, 2.5, 3.0, 5.0]
    resultados = []
    for r in raios:
        resultados.append((r, 2 * 3.14159 * r))
    return resultados

========================================
Code 145:
def verificar_anagramas():
    pares = [("amor", "roma"), ("casa", "saco"), ("pato", "topa")]
    resultados = []
    for a, b in pares:
        resultados.append((a, b, sorted(a) == sorted(b)))
    return resultados

========================================
Code 146:
def calcular_potencia():
    bases = [2, 3, 4]
    expoentes = [3, 2, 5]
    resultados = []
    for base, exp in zip(bases, expoentes):
        resultados.append((base, exp, base**exp))
    return resultados

========================================
Code 147:
def extrair_primeiro_nome():
    nomes = ["João Silva", "Maria Santos", "Pedro Costa"]
    resultados = []
    for nome in nomes:
        resultados.append((nome, nome.split()[0]))
    return resultados

========================================
Code 148:
def verificar_palindromos_numericos():
    numeros = [121, 123, 1331, 456]
    resultados = []
    for n in numeros:
        resultados.append((n, str(n) == str(n)[::-1]))
    return resultados

========================================
Code 149:
def calcular_volume_cubos():
    arestas = [2, 3, 4]
    resultados = []
    for a in arestas:
        resultados.append((a, a**3))
    return resultados

========================================
Code 150:
def converter_temperatura_kelvin():
    celsius = [0, 25, 37, 100]
    resultados = []
    for c in celsius:
        resultados.append((c, c + 273.15))
    return resultados

========================================
Code 151:
def verificar_multiplos_5():
    numeros = [10, 15, 22, 30]
    resultados = []
    for n in numeros:
        resultados.append((n, n % 5 == 0))
    return resultados

========================================
Code 152:
def calcular_comprimento_strings():
    palavras = ["Python", "Programação", "Dados"]
    resultados = []
    for p in palavras:
        resultados.append((p, len(p)))
    return resultados

========================================
Code 153:
def extrair_dominio_email():
    emails = ["user@gmail.com", "admin@empresa.com"]
    resultados = []
    for email in emails:
        resultados.append((email, email.split('@')[1]))
    return resultados

========================================
Code 154:
def verificar_letra_maiuscula():
    strings = ["Python", "java", "C++"]
    resultados = []
    for s in strings:
        resultados.append((s, s[0].isupper()))
    return resultados

========================================
Code 155:
def calcular_area_triangulos():
    bases_alturas = [(6, 8), (5, 12), (3, 4)]
    resultados = []
    for b, h in bases_alturas:
        resultados.append((b, h, 0.5 * b * h))
    return resultados

========================================
Code 156:
def converter_para_binario_8bits():
    numeros = [5, 10, 15, 20]
    resultados = []
    for n in numeros:
        resultados.append((n, bin(n)[2:].zfill(8)))
    return resultados

========================================
Code 157:
def verificar_ano_bissexto():
    anos = [2020, 2021, 2024, 1900]
    resultados = []
    for ano in anos:
        bissexto = (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)
        resultados.append((ano, bissexto))
    return resultados

========================================
Code 158:
def calcular_desconto():
    produtos = [("Notebook", 2500), ("Celular", 1200)]
    resultados = []
    for nome, preco in produtos:
        resultados.append((nome, preco, preco * 0.1))
    return resultados

========================================
Code 159:
def extrair_ultimas_3_letras():
    palavras = ["Python", "Programação", "Algoritmo"]
    resultados = []
    for p in palavras:
        resultados.append((p, p[-3:])))
    return resultados

========================================
Code 160:
def verificar_numero_par():
    numeros = [2, 5, 8, 11]
    resultados = []
    for n in numeros:
        resultados.append((n, n % 2 == 0))
    return resultados

========================================
Code 161:
def calcular_media_simples():
    numeros = [10, 20, 30, 40]
    resultados = []
    for n in numeros:
        resultados.append((n, sum(numeros)/len(numeros)))
    return resultados

========================================
Code 162:
def converter_para_maiusculas():
    palavras = ["python", "dados", "programação"]
    resultados = []
    for p in palavras:
        resultados.append((p, p.upper()))
    return resultados

========================================
Code 163:
def verificar_substring():
    palavras = ["python", "programação", "dados"]
    substring = "pro"
    resultados = []
    for p in palavras:
        resultados.append((p, substring in p))
    return resultados

========================================
Code 164:
def calcular_fatorial():
    from math import factorial
    numeros = [1, 2, 3, 4, 5]
    resultados = []
    for n in numeros:
        resultados.append((n, factorial(n)))
    return resultados

========================================
Code 165:
def extrair_ano_data():
    datas = ["2023-12-25", "2024-01-01", "2022-06-15"]
    resultados = []
    for data in datas:
        resultados.append((data, data.split('-')[0]))
    return resultados

========================================
Code 166:
def verificar_email_valido():
    emails = ["user@exemplo.com", "invalido", "outro@site.com"]
    resultados = []
    for email in emails:
        resultados.append((email, '@' in email and '.' in email.split('@')[1]))
    return resultados

========================================
Code 167:
def calcular_distancia_origem():
    pontos = [(3, 4), (1, 1), (5, 12)]
    resultados = []
    for x, y in pontos:
        resultados.append(((x, y), (x**2 + y**2)**0.5))
    return resultados

========================================
Code 168:
def converter_para_minusculas():
    palavras = ["PYTHON", "DADOS", "PROGRAMAÇÃO"]
    resultados = []
    for p in palavras:
        resultados.append((p, p.lower()))
    return resultados

========================================
Code 169:
def verificar_palavra_vazia():
    strings = ["hello", "", "world", ""]
    resultados = []
    for s in strings:
        resultados.append((s, len(s) == 0))
    return resultados

========================================
Code 170:
def calcular_dobro_quadrado():
    numeros = [2, 3, 4, 5]
    resultados = []
    for n in numeros:
        resultados.append((n, 2 * n**2))
    return resultados