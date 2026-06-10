import argparse
import hashlib
import json
import os
from datetime import datetime

import pandas as pd
from jsonschema import Draft7Validator, ValidationError

INPUT_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), '..', 'schemas', 'agent_input_schema.json')


def load_schema(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_input(data, schema):
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        raise ValidationError(errors[0].message)


def compute_sha256(path):
    sha = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha.update(chunk)
    return sha.hexdigest()


def main(csv_path, output_path):
    df = pd.read_csv(csv_path)
    data = {
        'source': os.path.basename(csv_path),
        'rows': len(df),
        'schema': list(df.columns),
        'ingested_at': datetime.utcnow().isoformat() + 'Z',
        'sha256': compute_sha256(csv_path)
    }
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, 'dataset_metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'CSV ingestado com sucesso: {data}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingestão e validação de CSV para agente de dados.')
    parser.add_argument('csv_path', help='Caminho do arquivo CSV de entrada')
    parser.add_argument('--output-path', default='data/', help='Pasta de saída para metadados')
    args = parser.parse_args()
    main(args.csv_path, args.output_path)
