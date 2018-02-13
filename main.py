import dropbox
from pygments.lexers import PythonLexer
from prompt_toolkit import prompt
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.contrib.completers import WordCompleter
from tqdm import tqdm
import os

access_token = os.environ["DROPBOX_TOKEN"]
export_format = dropbox.paper.ExportFormat('markdown')

# Dropbox client
dbx = dropbox.Dropbox(access_token)
# All document list
docs_list = dbx.paper_docs_list()
# { folder_name: [doc_id]}
folders = {}
# { doc_id: doc_info }
docs = {}
print("Get documents")
i = 0
for id in tqdm(docs_list.doc_ids):
    i += 1
    if i > 10:
        break
    try:
        folder = dbx.paper_docs_get_folder_info(id).folders[0]
        if folder.name in folders:
            folders[folder.name].append(id)
        else:
            folders[folder.name] = [id]
        docs[id] = dbx.paper_docs_download(id, export_format)
    except Exception as e:
        pass

completer = WordCompleter(list(folders.keys()))
selected_folder = prompt('Select Folder: ',
                         completer=completer,
                         lexer=PygmentsLexer(PythonLexer))

selected_docs_ids = folders[selected_folder]
titles = []
for id in selected_docs_ids:
    titles.append(docs[id][0].title)

completer = WordCompleter(titles)
selected_title = prompt('Select Doc: ',
                         completer=completer,
                         lexer=PygmentsLexer(PythonLexer))
