# quiz.py

print("--- Bem-vindo ao Quiz de Cibersegurança! ---")
print("Responda apenas com 'sim' ou 'não'.\n")

# Variável para contar os acertos
pontuacao = 0

# Pergunta 1
p1 = input("1. Usar a mesma senha para vários sites é seguro? ").lower()
if p1 == "não" or p1 == "nao":
    print("Correto! O ideal é usar um gerenciador de senhas.")
    pontuacao = pontuacao + 1
else:
    print("Errado. Se um site vazar sua senha, todos os outros estarão em risco.")

# Pergunta 2
p2 = input("2. A autenticação de dois fatores (2FA) aumenta a segurança? ").lower()
if p2 == "sim":
    print("Exato! É uma camada extra de proteção.")
    pontuacao += 1 # Forma abreviada de somar 1
else:
    print("Errado. O 2FA é essencial hoje em dia.")

# Pergunta 3
p3 = input("3. 'Phishing' é um tipo de ataque feito por e-mails ou mensagens falsas? ").lower()
if p3 == "sim":
    print("Certo! Eles tentam pescar seus dados.")
    pontuacao += 1
else:
    print("Errado. Phishing é um dos ataques mais comuns via e-mail.")

# Pergunta 4
p4 = input("4. Antivírus gratuito é suficiente para proteger uma empresa inteira? ").lower()
if p4 == "não" or p4 == "nao":
    print("Correto! Empresas precisam de soluções de endpoint mais robustas.")
    pontuacao += 1
else:
    print("Errado. Proteção corporativa exige muito mais que um antivírus básico.")

# Pergunta 5
p5 = input("5. O cadeado verde no navegador garante que o site é 100% confiável? ").lower()
if p5 == "não" or p5 == "nao":
    print("Excelente! O cadeado indica conexão criptografada, mas o site ainda pode ser golpista.")
    pontuacao += 1
else:
    print("Cuidado! O cadeado garante apenas a criptografia do caminho, não a índole do site.")

# Resultado Final
print("\n" + "="*30)
print(f"Fim do Quiz, Kensei!")
print(f"Você acertou {pontuacao} de 5 perguntas.")

if pontuacao == 5:
    print("Nível: Especialista! Você está pronto para o mercado.")
elif pontuacao >= 3:
    print("Nível: Estudante dedicado. Continue praticando!")
else:
    print("Nível: Iniciante. A cibersegurança é um mar de aprendizado!")
print("="*30)