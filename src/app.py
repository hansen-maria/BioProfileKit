#! usr/bin/env Python3
import os
import shutil
from pathlib import Path

import click
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from termcolor import colored
from importlib_resources import files
from qc_eda.basic.numerical_data import overview, column_overview, numeric_columns, categorical_columns
from qc_eda.biological.biological_data import dna_rna_columns, protein_columns
from qc_eda.biological.measurement_data import measurement_columns
from utils.file_reader import read_file
from qc_eda.basic.general import correlation_heatmap, missing_matrix, boxplot

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
TEMPLATE_DIR = files("templates").joinpath()
STATIC_DIR = files("static").joinpath()
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=True)


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option("-i", "--input", type=click.Path(exists=True, resolve_path=True), required=True,
              help="Input file as .tsv, .csv or .json", )
def cli(input: str):
    input_path = Path(input)
    print(colored(f'Reading file {input_path.name}', 'green'))

    df = read_file(input_path)
    general = overview(df, input_path.name)
    correlation_heatmap(df)
    missing_matrix(df)
    boxplot(df)
    dups = df[df.duplicated(keep=False)]
    dups = dups.reset_index()
    duplicates_table = dups.to_html(classes="table table-hover table-responsive nowrap", border="0",
                                    table_id="dup_table",
                                    index=False)
    print(colored(f'Analyse {len(df.columns)} columns', 'blue'))

    column_overviews = [column_overview(df, col) for col in df.columns]

    for col_overview in column_overviews:
        if hasattr(col_overview, "top_10") and isinstance(col_overview.top_10, pd.Series):
            col_overview.top_10_items = list(col_overview.top_10.items())  # Needed for jinja2
        if col_overview.sequence == 'dna':
            print(colored(f'Analyzing DNA/RNA sequences in column: {col_overview.name}', 'cyan'))
            bio_data = dna_rna_columns(df[col_overview.name])
            col_overview.dna_rna_data = bio_data
        elif col_overview.sequence == 'protein':
            print(colored(f'Analyzing protein sequences in column: {col_overview.name}', 'cyan'))
            bio_data = protein_columns(df[col_overview.name])
            col_overview.protein_data = bio_data
        else:
            col_overview.dna_rna_data = None
            col_overview.protein_data = None

        if col_overview.sequence == 'None':
            measurement_data = measurement_columns(col_overview, df)
            if measurement_data:
                print(colored(f'Analyzing lab measurements in column: {col_overview.name}', 'cyan'))
                col_overview.measurement_data = measurement_data
            else:
                col_overview.measurement_data = None
        else:
            col_overview.measurement_data = None

    print(colored(f'Analyse {len(df.select_dtypes(include="number").columns)} numeric columns ', 'blue'))

    numeric_overviews = [numeric_columns(df, col) for col in df.select_dtypes(include='number').columns]

    cat_columns = [col for col in df.select_dtypes(include=['object', 'bool', 'int64', 'float64']).columns if
                   any(i.sequence == 'None' for i in column_overviews if i.name == col)]
    print(colored(f'Analyse {len(cat_columns)} object columns ', 'blue'))
    categorical_overviews = [categorical_columns(df, col) for col in cat_columns]

    Path("renders").mkdir(parents=True, exist_ok=True)

    #print(STATIC_DIR)
    shutil.copytree(str(STATIC_DIR), "renders/static/", dirs_exist_ok=True)

    landing_template = env.get_template('LandingPage.jinja')
    numeric_template = env.get_template('numeric_overview.jinja')
    columns = env.get_template('columns.jinja')

    print(colored('Writing report …', 'green'))
    with open("renders/index.html", 'w', encoding="utf-8") as output:
        print(landing_template.render(), file=output)

    with open("renders/numeric_data.html", "w",encoding="utf-8") as output:
        print(numeric_template.render(general=general, dups=duplicates_table), file=output)

    with open("renders/columns.html", "w",encoding="utf-8") as output:
        print(columns.render(columns=column_overviews, overview=numeric_overviews, categorical=categorical_overviews),
              file=output)
