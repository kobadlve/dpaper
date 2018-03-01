# This is a test script.

from dbx_client import (
    DBXClient
)
import inquirer


def main():
    c = DBXClient()
    c.get_folders()

    questions = [
        inquirer.List('name',
                      message='Select folder',
                      choices=list(c.folders.keys()),
                      ),
    ]

    answer = inquirer.prompt(questions)
    folder_name = answer['name']
    c.get_docs_with_folder_name(folder_name)

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


if __name__ == '__main__':
    main()
