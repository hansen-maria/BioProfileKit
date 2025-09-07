import io
import os
import pathlib
import zipfile
from pathlib import Path
import pandas as pd
import requests
from goatools.base import download_go_basic_obo
from goatools.obo_parser import GODag

def download_file(url: str, file_path: Path, download_text: str):
    if not file_path.exists():
        print(f"Begin download of {download_text} file. This may take a while...")
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Fehler abfangen
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("\tDownload completed!")
    else:
        print(f"{download_text} file already exists. Skipping download.")


def download_zip_archive(url: str, zip_file_name: str, file_path: Path, download_text: str):
    if not file_path.exists():
        print(f"Begin download of {download_text} archive. This may take a while...")
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            buffer = io.BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    buffer.write(chunk)
            buffer.seek(0)

            with zipfile.ZipFile(buffer) as zf:
                with zf.open(zip_file_name) as source_file, open(file_path, "wb") as target:
                    for chunk in iter(lambda: source_file.read(8192), b""):
                        target.write(chunk)

        print("\tDownload completed!")
        #zip_path.unlink()
    else:
        print(f"{download_text} file already exists. Skipping download.")


def get_gene_ontology():
    obo_path = download_go_basic_obo()
    go_dag = GODag(obo_path)
    print(go_dag.version)
    data = list()
    for go_id in go_dag.keys():
        term = go_dag[go_id]
        namespace = getattr(term, "namespace", "")
        data.append([go_id, term.name, namespace])

    df = pd.DataFrame(data, columns=["GO_ID", "Name", "Namespace"])
    if Path(obo_path).is_file():
        pathlib.Path(obo_path).unlink(missing_ok=True)
        print(f"Removed {obo_path}")


def get_clusters_of_orthologous_groups():
    url: str = "https://ftp.ncbi.nlm.nih.gov/pub/COG/COG2024/data/cog-24.def.tab"
    fields = ["COG ID", "Functional Category", "COG name"]
    response = requests.get(url)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text), sep="\t", skipinitialspace=True,usecols=[0,1,2], names=fields)
        print(df)
    else:
        print(f"Error: {response.status_code}")


def get_tax_ids():
    url: str = "https://ftp.ncbi.nih.gov/pub/taxonomy/taxdmp.zip"
    tax_file = Path("names.dmp")
    target_path = Path("./")
    download_zip_archive(url, str(tax_file), target_path.joinpath(tax_file), "Tax ID Metadata")

    print("Loading Tax ID File...")
    df = pd.read_csv(tax_file, sep="|\t", header=None, engine='python')
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df = df[[0, 1]].dropna()
    df.columns = ["TaxID", "Name"]
    df = df.groupby("TaxID")["Name"].apply(lambda x: "; ".join(sorted(set(x)))).reset_index()
    print(df)



get_gene_ontology()
#get_clusters_of_orthologous_groups()
#get_tax_ids()
