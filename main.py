from dbx_client import (
    DBXClient
)
import inquirer
import click
from tqdm import tqdm


@click.group()
def main():
    pass


@main.command(help='Interactive mode.')
def i():
    """Interactive mode."""
    c = DBXClient()
    c.get_folders()

    print("end: ", c.folders.keys())
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


@main.command(help='Show list of documents.')
def l():
    """Show list."""
    c = DBXClient()
    docs = {}
    for doc_id in tqdm(c.docs_list.doc_ids):
        doc = c.download_doc(doc_id)
        docs[doc.title] = doc.doc_id
    sorted_docs = sorted(docs.items(), key=lambda x: x[0])
    for doc in sorted_docs:
        print('{}: {}'.format(doc[0], doc[1]))


@main.command(help='Show document data with id.')
@click.argument('doc_id')
def c(doc_id):
    """Show document."""
    c = DBXClient()
    doc = c.download_doc(doc_id)
    print(doc.data)


@main.command(help='Download document with id.')
@click.argument('doc_id')
def d(doc_id):
    """Download document."""
    c = DBXClient()
    doc = c.download_doc(doc_id)
    f = open(doc.title + '.md', 'w')
    f.write(doc.data)
    f.close()


if __name__ == '__main__':
    main()
