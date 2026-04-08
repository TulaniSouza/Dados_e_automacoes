# lista_compras.py

print("--- Minha Lista de Compras Inteligente ---")
print("Digite o nome do item para adicionar ou 'sair' para finalizar.\n")

# Criamos uma lista vazia
lista = []

while True:
    item = input("Item: ").strip() # .strip() remove espaços extras acidentais
    
    # Condição de saída
    if item.lower() == 'sair':
        break
    
    # Adicionando o item à lista
    if item: # Verifica se o usuário não digitou algo vazio
        lista.append(item)
        print(f"'{item}' adicionado!")
    else:
        print("Por favor, digite um nome válido.")

# Exibição da lista final
print("\n" + "="*20)
print("SUA LISTA FINAL:")

# Verificamos se a lista não está vazia antes de mostrar
if not lista:
    print("A lista está vazia.")
else:
    # O loop 'for' percorre cada item da lista
    for i, produto in enumerate(lista, 1):
        print(f"{i}. {produto}")

print("="*20)
print("Boas compras!")