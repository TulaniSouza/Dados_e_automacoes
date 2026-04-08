import random
import string

print("--- Gerador de Senhas Seguro ---")

# 1. Definindo o tamanho da senha
tamanho = int(input("Digite o comprimento desejado para a senha (ex: 12): "))

# 2. Criando o "pool" de caracteres
# string.ascii_letters contém letras maiúsculas e minúsculas
# string.digits contém números de 0 a 9
# string.punctuation contém símbolos (!, @, #, $, etc.)
caracteres = string.ascii_letters + string.digits + string.punctuation

# 3. Gerando a senha aleatória
# random.choices escolhe caracteres aleatórios da lista e 'join' os junta em uma string
senha = "".join(random.choices(caracteres, k=tamanho))

print("\n-------------------------------")
print(f"Sua nova senha é: {senha}")
print("-------------------------------\n")