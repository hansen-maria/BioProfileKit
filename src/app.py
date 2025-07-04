#! usr/bin/env Python3

import pyximport

from utils.file_reader import read_file

pyximport.install()

from jinja2 import Environment, FileSystemLoader
from qc_eda.basic.numerical_data import overview,column_overview
from pathlib import Path



def main():
    file = "../test_data/iedb.tsv"
    df = read_file(file)
    general = overview(df, file)
    dups = df[df.duplicated(keep=False)]
    #ToDo: Pagination
    test_html = dups.to_html(classes="table table-hover table-responsive nowrap", border="0", table_id="dup_table")

    for i in df.columns:
        print(column_overview(df, i))
    Path("renders").mkdir(parents=True, exist_ok=True)

    env = Environment(loader=FileSystemLoader('templates'))
    landing_template = env.get_template('LandingPage.jinja')
    numeric_template = env.get_template('numeric_overview.jinja')

    with open("renders/index.html", 'w') as output:
        print(landing_template.render(), file = output)

    with open("renders/numeric_data.html", "w") as output:
        print(numeric_template.render(general=general, dups=test_html), file = output)


if __name__ == '__main__':
    main()
