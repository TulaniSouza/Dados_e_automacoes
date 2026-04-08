#Seja bemv-vindo ao meu repositório Kensei!
print("Olá, Kensei!")
print("Espero que gostem deste repositório\n")

# Perguntando o nome do usuário
nome = input("Qual seu nome?")
print("Olá, ",nome,"!")
idade = input("Qual é a sua idade?")
print(f"Idade: {idade} ótima idade para aprender!")
altura = float(input("Qual é a sua altura?"))
print(f"Altura: {altura} que legal, cabe na vaga!")
estudante_input= input ("Você é estudante de cibersegurança? (sim/não): ").lower()
if estudante_input == "não" or estudante_input == "nao":
    print("Ah, puxa... seríamos ótimos colegas de trabalho! Mas também tem muita coisa legal por aí.")
else: print("Que ótimo! Bem-vindo à comunidade Kensei! Vamos aprender muito juntos!")

