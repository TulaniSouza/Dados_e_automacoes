import json
import os


def load_interaction(interaction_path):
    with open(interaction_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def replay(interaction):
    # TODO: implementar reprodução usando prompt_version e policy version
    print('Reprodução de decisão ainda não implementada.')
    print('Interaction payload:')
    print(json.dumps(interaction, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Reproduz uma decisão de agente a partir de um registro de interação.')
    parser.add_argument('interaction_path', help='Caminho para o JSON de interação armazenado')
    args = parser.parse_args()

    interaction = load_interaction(args.interaction_path)
    replay(interaction)
