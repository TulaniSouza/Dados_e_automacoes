import argparse
import json
import os


def load_golden_set(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate(golden, results):
    total = len(golden)
    correct = 0
    details = []

    for item in golden:
        interaction_id = item.get('interaction_id')
        expected = item.get('expected_decision')
        actual = results.get(interaction_id, {}).get('decision')
        match = expected == actual
        if match:
            correct += 1
        details.append({
            'interaction_id': interaction_id,
            'expected': expected,
            'actual': actual,
            'match': match
        })

    accuracy = correct / total if total else 0
    return {
        'total': total,
        'correct': correct,
        'accuracy': accuracy,
        'details': details
    }


def main(golden_path, results_path):
    golden = load_golden_set(golden_path)
    results = load_golden_set(results_path)
    results_by_id = {item['interaction_id']: item for item in results}
    summary = evaluate(golden, results_by_id)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Avalia um golden set contra resultados de agente.')
    parser.add_argument('golden_path', help='Caminho para o golden set JSON')
    parser.add_argument('results_path', help='Caminho para resultados de agente JSON')
    args = parser.parse_args()
    main(args.golden_path, args.results_path)
