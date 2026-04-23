import random
import string

print("--- Gerador de Senhas Seguro ---")

tamanho = int(input("Digite o comprimento desejado para a senha (ex: 12): "))

caracteres = string.ascii_letters + string.digits + string.punctuation


senha = "".join(random.choices(caracteres, k=tamanho))

print("\n-------------------------------")
print(f"Sua nova senha é: {senha}")
print("-------------------------------\n")