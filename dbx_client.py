import dropbox
import os


class DBXClient(object):
    """ API Helper.

    Attributes:
        None
    """

    def __init__(self):
        """Initialize."""
        self.access_token = os.environ["DROPBOX_TOKEN"]
        self.export_format = dropbox.paper.ExportFormat('markdown')
        self.dbx = dropbox.Dropbox(self.access_token)
        self.docs_list = self.dbx.paper_docs_list()

    def get_folder(self):
        """Get Folders."""
        folders = {}
        for doc_id in self.docs_list.doc_ids:
            folder = self.dbx.paper_docs_get_folder_info(doc_id).folders[0]
            if folder.name in folders:
                folders[folder.name].append(doc_id)
            else:
                folders[folder.name] = [doc_id]

    def download_docs(self, doc_id: int) -> str:
        """Download doc."""
        response = self.dbx.paper_docs_download(id, self.export_format)
        doc_str = response.content.decode()
        return doc_str
