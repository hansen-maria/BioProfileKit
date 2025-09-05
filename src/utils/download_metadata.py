import io
import zipfile
from pathlib import Path
import pandas as pd
import requests
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
    else:
        print(f"{download_text} file already exists. Skipping download.")


def get_gene_ontology():
    url = "http://current.geneontology.org/ontology/go-basic.obo"
    obo_file = Path("go-basic.obo")
    download_file(url, obo_file, "GO Metadata")

    print("Loading GO DAG File...")
    go_dag = GODag(str(obo_file))
    print(go_dag.version)
    data = list()
    for go_id in go_dag.keys():
        term = go_dag[go_id]
        namespace = getattr(term, "namespace", "")
        data.append([go_id, term.name, namespace])

    df = pd.DataFrame(data, columns=["GO_ID", "Name", "Namespace"])

    print(df)


def get_clusters_of_orthologous_groups():
    url: str = "https://ftp.ncbi.nlm.nih.gov/pub/COG/COG2024/data/cog-24.def.tab"
    cog_file = Path("cog-24.def.tab")
    download_file(url, cog_file, "COG Metadata")

    print("Loading COG Tab File...")
    cog_df = pd.read_csv(
        cog_file,
        sep="\t",
        names=[
            "COG ID",
            "COG functional category",
            "COG name",
            "Gene name associated with the COG",
            "Functional pathway associated with the COG",
            "PubMed ID, associated with the COG",
            "PDB ID of the structure associated with the COG"
        ]
    )
    print(cog_df)


def get_tax_ids():
    url: str = "https://ftp.ncbi.nih.gov/pub/taxonomy/taxcat.zip"
    tax_file = Path("categories.dmp")
    taget_path = Path("./")
    download_zip_archive(url, str(tax_file), taget_path.joinpath(tax_file), "Tax ID Metadata")

    print("Loading Tax ID File...")
    tax_df = pd.read_csv(
        tax_file,
        sep="\t",
        names=[
            "top-level",
            "species-level",
            "taxid"
        ]
    )
    print(tax_df)


get_gene_ontology()
get_clusters_of_orthologous_groups()
get_tax_ids()
