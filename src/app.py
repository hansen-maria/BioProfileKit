#! usr/bin/env Python3
import os
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader
from termcolor import colored

from qc_eda.basic.numerical_data import overview, column_overview, numeric_columns
from qc_eda.biological.biological_data import dna_rna_columns
from utils.file_reader import read_file

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option("-i", "--input", type=click.Path(exists=True, resolve_path=True), required=True,
              help="Input file as .tsv, .csv or .json", )
def cli(input: str):
    input_path = Path(input)
    print(colored(f'Reading file {input_path.name}', 'green'))

    df = read_file(input_path)
    general = overview(df, input_path.name)
    dups = df[df.duplicated(keep=False)]
    dups = dups.reset_index()
    duplicates_table = dups.to_html(classes="table table-hover table-responsive nowrap", border="0", table_id="dup_table",
                             index=False)
    print(colored(f'Analyse {len(df.columns)} columns', 'blue'))

    column_overviews = [column_overview(df, col) for col in df.columns]
    for i in column_overviews:
        if i.sequence == 'dna':
            bio = dna_rna_columns(df[i.name])
            print(bio)
    print(colored(f'Analyse {len(df.select_dtypes(include='number').columns)} numeric columns ', 'blue'))

    numeric_overviews = [numeric_columns(df, col) for col in df.select_dtypes(include='number').columns]

    Path("renders").mkdir(parents=True, exist_ok=True)

    landing_template = env.get_template('LandingPage.jinja')
    numeric_template = env.get_template('numeric_overview.jinja')
    columns = env.get_template('columns.jinja')

    print(colored('Writing report …', 'green'))
    with open("renders/index.html", 'w') as output:
        print(landing_template.render(), file=output)

    with open("renders/numeric_data.html", "w") as output:
        print(numeric_template.render(general=general, dups=duplicates_table), file=output)

    with open("renders/columns.html", "w") as output:
        print(columns.render(columns=column_overviews, overview=numeric_overviews), file=output)
