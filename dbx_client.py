import dropbox
from tqdm import tqdm
import os


class Doc(object):
    """ Doc class
    """

    def __init__(self, doc_id: str, title: str, data: str):
        self.doc_id = doc_id
        self.title = title
        self.data = data


class Folder(object):
    """ Folder class

    Attributes:
        ids: doc ids in folder.
    """

    def __init__(self, name=str, ids=[str]):
        self.name = name
        self.doc_ids = ids


class DBXClient(object):
    """ API Helper.
    Need to set DROPBOX_TOKEN.

    Attributes:
        None
    """

    def __init__(self):
        """Initialize."""
        self.access_token = os.environ["DROPBOX_TOKEN"]
        self.export_format = dropbox.paper.ExportFormat('markdown')
        self.dbx = dropbox.Dropbox(self.access_token)
        self.docs_list = self.dbx.paper_docs_list()

    def get_folders(self):
        """Get Folders."""
        # {'folder_name': [doc_id]}
        folders = {}
        for doc_id in tqdm(self.docs_list.doc_ids):
            try:
                folder = self.dbx.paper_docs_get_folder_info(doc_id).folders[0]
                if folder.name in folders:
                    folders[folder.name].append(doc_id)
                else:
                    folders[folder.name] = [doc_id]
            except:
                pass
        self.folders = folders

    def get_docs_with_folder_name(self, name):
        """Get docs."""
        self.docs = []
        for doc_id in tqdm(self.folders[name]):
            self.docs.append(self.download_doc(doc_id))

    def get_doc_titles_with_folder_name(self, name) -> [str]:
        """Get doc title."""
        titles = []
        for doc in self.docs:
            titles.append(doc.title)
        return titles

    def get_doc_with_title(self, title) -> Doc:
        for doc in self.docs:
            if title == doc.title:
                return doc

    def download_doc(self, doc_id: int) -> Doc:
        """Download doc."""
        (result, response) = self.dbx.paper_docs_download(doc_id, self.export_format)
        data = response.content.decode()
        return Doc(doc_id, result.title, data)
