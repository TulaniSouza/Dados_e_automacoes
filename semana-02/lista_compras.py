

print("--- Minha Lista de Compras Inteligente ---")
print("Digite o nome do item para adicionar ou 'sair' para finalizar.\n")

lista = []

while True:
    item = input("Item: ").strip() 
    
    if item.lower() == 'sair':
        break
    
    if item: # Verifica se o usuário não digitou algo vazio
        lista.append(item)
        print(f"'{item}' adicionado!")
    else:
        print("Por favor, digite um nome válido.")

print("\n" + "="*20)
print("SUA LISTA FINAL:")

if not lista:
    print("A lista está vazia.")
else:
    for i, produto in enumerate(lista, 1):
        print(f"{i}. {produto}")
print("="*20)
print("Boas compras!")