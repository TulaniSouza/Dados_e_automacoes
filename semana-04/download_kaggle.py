import shutil
from pathlib import Path
import kagglehub
from kagglehub import KaggleDatasetAdapter


DATA_DIR = Path("data")
INPUTS_DIR = DATA_DIR / "inputs"
OUTPUT_CSV = INPUTS_DIR / "dados.csv"
DATASET_SLUG = "rohitsahoo/sales-forecasting"


def find_csv_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.csv"))


def download_dataset(dataset_slug: str) -> Path:
    print(f"Baixando dataset {dataset_slug} via kagglehub...")
    path = kagglehub.dataset_download(dataset_slug)
    return Path(path).resolve()


def copy_first_csv(source_dir: Path, destination: Path) -> None:
    csv_files = find_csv_files(source_dir)

    if not csv_files:
        raise FileNotFoundError(
            f"Nenhum arquivo CSV encontrado em {source_dir}.\n"
            f"Verifique o conteúdo do dataset baixado."
        )

    chosen_csv = csv_files[0]
    print(f"Arquivo CSV encontrado: {chosen_csv}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(chosen_csv, destination)
    print(f"CSV copiado para: {destination}")


def main() -> None:
    dataset_path = download_dataset(DATASET_SLUG)
    print(f"Dataset baixado em: {dataset_path}")

    try:
        copy_first_csv(dataset_path, OUTPUT_CSV)
    except FileNotFoundError as exc:
        print("Erro:", exc)
        print("Arquivos disponíveis:")
        for item in sorted(dataset_path.rglob("*")):
            print("-", item.relative_to(dataset_path))
        raise


if __name__ == "__main__":
    main()
