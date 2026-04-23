
print("--- Organizador de Nomes (Ordem Alfabética) ---")
print("Digite os nomes um por um. Quando terminar, digite 'fim'.\n")

nomes = []

# 1. Coletando os nomes
while True:
    entrada = input("Digite um nome: ").strip()
    
    if entrada.lower() == 'fim':
        break
    
    if entrada:
        # Usamos .title() para que o nome comece sempre com letra maiúscula
        nomes.append(entrada.title())
    else:
        print("Entrada inválida. Tente novamente.")

# 2. Organizando a lista
# O método .sort() modifica a lista original organizando-a de A a Z
nomes.sort()

# 3. Exibindo o resultado
print("\n" + "="*30)
print(f"Lista Organizada ({len(nomes)} nomes):")
print("="*30)

if not nomes:
    print("Nenhum nome foi inserido.")
else:
    for nome in nomes:
        print(f"• {nome}")

print("="*30)