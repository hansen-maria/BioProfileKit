#! usr/bin/env Python3

from jinja2 import Environment, FileSystemLoader


def main():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('LandingPage.jinja')
    with open("renders/index.html", 'w') as output:
        print(template.render(landingPageOf='BioProfileKit'), file = output)


if __name__ == '__main__':
    main()
