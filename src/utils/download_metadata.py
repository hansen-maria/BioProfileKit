import shutil
from pathlib import Path
import pandas as pd
import requests
from goatools.obo_parser import GODag

#shutil.unpack_archive(filename, extract_dir)

# https://ftp.ncbi.nih.gov/pub/taxonomy/taxcat.zip
# https://ftp.ncbi.nlm.nih.gov/pub/COG/COG2024/data/cog-24.def.tab
# https://current.geneontology.org/ontology/go-basic.obo

def get_gene_ontology():

    url = "http://current.geneontology.org/ontology/go-basic.obo"
    obo_file = Path("go-basic.obo")
    if not obo_file.exists():
        print("Begin download of Gene Ontologie Metadata file. This may take a while...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Fehler abfangen
        with open(obo_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download completed!")
    else:
        print("GO Metadata file already exists. Skipping download.")
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

get_gene_ontology()
