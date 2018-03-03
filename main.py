# This is a test script.

from dbx_client import (
    DBXClient
)
import inquirer
import click


@click.group()
def main():
    pass


@main.command()
def interactive():
    c = DBXClient()
    c.get_folders()

    # Select folder.
    questions = [
        inquirer.List('name',
                      message='Select folder',
                      choices=list(c.folders.keys()),
                      ),
    ]

    answer = inquirer.prompt(questions)
    folder_name = answer['name']
    c.get_docs_with_folder_name(folder_name)

    # Select document.
    questions = [
        inquirer.List('name',
                      message='Select doc',
                      choices=c.get_doc_titles_with_folder_name(folder_name),
                      ),
    ]

    answer = inquirer.prompt(questions)
    title = answer['name']
    doc = c.get_doc_with_title(title)

    print(doc.title)
    print(doc.data)


@main.command()
def list():
    pass


@main.command()
def cat():
    pass


@main.command()
def downlaod():
    pass


if __name__ == '__main__':
    main()
