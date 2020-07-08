from ...models import Book, Page, PageContent

class DocumentUploader():
    """
    Uploads a user-specified document.
    """
    def __init__(self, params):
        """
        Initializes the document upload mechanism.

        Parameters
        ----------
        params : dict
            Configurations for the document upload procedure
        """
        self.params = params

    def cleanup(self, doc):
        """
        Removes a document for the database.

        Parameters
        ----------
        doc : dict
            The document to be deleted
        """
        to_delete = Page.objects(
                                 email=self.params["email"],
                                 resource__title=doc["title"],
                                 resource__author=doc["author"]
                                )
        if to_delete.first():
            try: 
                to_delete.delete()
            except Exception as e:
                error_msg = "Couldn't delete existing document"
                raise Exception(error_msg)
    
    def insert_batch(self, batch, doc):
        """
        Inserts a batch of pages into the database.

        Parameters
        ----------
        batch : list
            The pages to be inserted
        doc : dict
            The document from which the pages are derived
        """
        try:
            Page.objects.insert(batch)
        except Exception as e:
            error_msg = "Couldn't insert page batch"
            self.cleanup(doc)
            raise Exception(error_msg)

    def upload(self, doc):
        """
        Saves the document to the database.

        Parameters
        ----------
        doc : dict
            The document to be saved
        """
        user = self.params["email"]
        new_page = int(self.params["new_page"])
        line_size = int(self.params["line_size"])
        batch_size = int(self.params["batch_size"])
        tokenizer = self.params["tokenizer"]
        resource = self.params["resource"]
        
        #Remove existing document
        self.cleanup(doc)

        #Process each line in document
        line_num = 1
        line_str = "1"
        page_num = 1
        lines = {line_str:[]}
        line_breaks = {"start":{}, "end":{}}
        batch = []
        char_count = 0
        for line in doc["file"]:
            #blank new line
            if line == "\n":
                char_count = 0
                line_num += 1
                line_str = str(line_num)
                lines[line_str] = []
                continue

            tokenized = tokenizer.tokenize(line, line_size)
            for token in tokenized:
                #Check if token continues onto next line
                if token["size"] + char_count >= line_size:
                    lines[line_str].append(token["text"])
                    if "break" in token:
                        line_breaks["end"][line_str] = token["break"]
                        line_breaks["start"][str(line_num+1)] = token["break"]
                    char_count = 0
                    if line_num < new_page:
                        line_num += 1
                        line_str = str(line_num)
                        lines[line_str] = []
                    else:
                        line_num += 1
                else:
                    lines[line_str].append(token["text"])
                    char_count += token["size"]
                
                #Save current page and start new one
                if line_num > new_page:
                    page_content = PageContent(lines=lines, breaks=line_breaks)
                    page = Page(
                                email=user,
                                resource=resource(doc, page_num),
                                content=page_content
                                )
                    batch.append(page)
                    page_num += 1
                    line_num = 1
                    line_str = "1"
                    lines = {line_str:[]}
                    line_breaks = {"start":{}, "end":{}}
                
                #Insert pages into database if there are enough
                if len(batch) >= batch_size:
                    self.insert_batch(batch, doc)
                    batch = []
        
        #Load last page
        page_content = PageContent(lines=lines, breaks=line_breaks)
        page = Page(
                        email=user,
                        resource=resource(doc, page_num),
                        content=page_content    
                        )
        batch.append(page)
            
        #Insert final batch
        self.insert_batch(batch, doc)