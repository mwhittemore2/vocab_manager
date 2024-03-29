from ...models import Book, Page, PageContent

def add_page(batch, page_content, page_number, upload_info):
    """
    Adds the database representation of a page to the next batch 
    to be inserted into the database.

    Parameters
    ----------
    batch: list
        The batch to be inserted
    page_content: PageContent
        The content of the page to be added
    page_number: int
        The number of the page to be added
    upload_info: func
        The document resource creator
    """
    user = upload_info["user"]
    resource = upload_info["resource"]
    doc = upload_info["doc"]
    page = Page(
                email=user,
                resource=resource(doc, page_number),
                content=page_content
               )
    batch.append(page)

def check_line_start(line_breaks, char_count):
    """
    Determines whether the current word is the start
    of a line.

    line_breaks: dict
        The words split across a line in the current page
    
    char_count: int
        The number of characters examined so far in the
        current line
    
    Returns
    -------
    bool
        True if the current word starts a line, False otherwise
    """
    if len(line_breaks["start"]) == 0:
        return True
    
    if len(line_breaks["end"]) == 0:
        return False
    
    can_process = not (line_breaks["start"][-1] == line_breaks["end"][-1])
    can_process = can_process and (char_count == 0)
    return can_process

def get_next_page_pointer(words, page):
    """
    Finds the position of the first word in the page
    immediately following the current one.

    Parameters
    ----------
    words: list
        The words in the next page
    
    page: int
        The number of the next page
    
    Returns
    -------
    dict
        Pointer to the start of the next page
    """
    line = len(words) - 1
    if(line < 0):
        empty_pointer = {}
        return empty_pointer
    
    pos = len(words[line]) - 1
    next_pointer = {
        "line": line,
        "page": page,
        "pos": max(0, pos)
    }
    return next_pointer

def get_page_content(words, page, prev_state):
    """
    Builds the database representation of the content of the
    page to be saved.

    Parameters
    ----------
    words: list
        The words in the next page (to build next-page pointer)
    
    page: int
        The number of the page to be saved
    
    prev_state: dict
        The content of the page to be saved
    
    Returns
    -------
    PageContent
        The database representation of the content of the page
    """
    prev_line_breaks = prev_state["line_breaks"]
    prev_words = prev_state["words"]
    next_page = page + 1
    next_page_pointer = get_next_page_pointer(words, next_page)
    prev_line_breaks["pageBoundaries"]["next"] = next_page_pointer
    page_content = PageContent(words=prev_words, breaks=prev_line_breaks)
    return page_content

def get_prev_page_pointer(words, line_breaks):
    """
    Finds the start position of the last word in the page 
    immediately preceding the current one.

    Parameters
    ----------
    words: list
        The words in the previous page
    line_breaks:
        The words split across a line in the previous page
    
    Returns
    -------
    dict
        Pointer to the last word of the previous page
    """
    if not ("end" in line_breaks):
        empty_pointer = {}
        return empty_pointer
    
    if len(line_breaks["end"]) == 0:
        empty_pointer = {}
        return empty_pointer

    last_line_break = line_breaks["end"][-1]
    last_word = line_breaks["tokens"][last_line_break]
    indicies = last_word["positions"][0]
    page, line, pos = indicies
    if(pos <= 0):
        if line > 0:
            line = line - 1
            pos = len(words[line]) - 1
    else:
        pos = pos - 1
    prev_pointer = {
        "line": line,
        "page": page,
        "pos": pos
    }
    return prev_pointer

def process_line_end(token, curr_boundary, line_info, line_breaks):
    """
    Updates line breaks dictionary to save data about a split token that
    overlaps with the end of a line.

    Parameters
    ----------
    token: dict
        The token that overlaps with the end of the line
    
    curr_boundary: dict
        The most recent line boundary reached in the page
    
    line_info: list
        The context of the line within the current page
    
    line_breaks: dict
        The words split across a line in the current page
    
    Returns
    -------
    dict
        The next boundary to be processed
    """
    line_num, page_num, new_page, num_words, line_size = line_info
    new_boundary = {}
    curr_pos = curr_boundary["pos"]

    #Word overflows onto next line
    if "break" in token:
        left_token = [page_num, line_num, num_words - 1]
        right_token = []
        if (line_num + 1) < new_page:
            right_token = [page_num, line_num + 1, 0]
            line_breaks["end"].append(curr_pos)
            line_breaks["start"].append(curr_pos)
            new_boundary["pos"] = curr_pos + 1
        else:
            right_token = [page_num + 1, 0, 0]
            line_breaks["end"].append(curr_pos)
            new_boundary = {
                "pos": 1,
                "start": [0]
            }
        
        to_append = {
            "fulltext": token["break"],
            "positions": [left_token, right_token]
        }
        line_breaks["tokens"].append(to_append)
        
        if (line_num + 1) >= new_page:
            new_boundary["tokens"] = [to_append]
    
    #Word ends at line cutoff point
    else:
        line_breaks["end"].append(curr_pos)
        
        if token["size"] == line_size:
            line_breaks["start"].append(curr_pos)
        
        to_append = {
            "fulltext": token["text"],
            "positions": [[page_num, line_num, max(0, num_words - 1)]]
        }
        line_breaks["tokens"].append(to_append)

        if (line_num + 1) < new_page:
            new_boundary["pos"] = curr_pos + 1
        else:
            new_boundary["pos"] = 0
    
    return new_boundary

def process_line_start(token, curr_boundary, line_info, line_breaks):
    """
    Updates line breaks dictionary to save data about a split token that
    overlaps with the beginning of a line.

    Parameters
    ----------
    token: dict
        The token that overlaps with the start of the line
    
    curr_boundary: dict
        The most recent line boundary reached in the page
    
    line_info: list
        The context of the line within the current page
    
    line_breaks: dict
        The words split across a line in the current page
    
    Returns
    -------
    dict
        The next boundary to be processed
    """
    line_num, page_num, new_page, line_size = line_info
    new_boundary = {}
    curr_pos = curr_boundary["pos"]
    
    line_breaks["start"].append(curr_pos)
    to_append = {
        "fulltext": token["text"],  
        "positions": [[page_num, line_num, 0]]
    }
    line_breaks["tokens"].append(to_append)

    if token["size"] == line_size:
        line_breaks["end"].append(curr_pos)
        if (line_num + 1) >= new_page:
            new_boundary["pos"] = 0
            return new_boundary
    
    new_boundary["pos"] = curr_pos + 1
    return new_boundary

def reset_line_breaks(curr_boundary={}):
    """
    Builds a fresh line breaks dictionary while keeping any 
    information provided concerning line boundaries.

    Parameters
    ----------
    curr_boundary: dict
        Line boundaries to be preserved

    Returns
    -------
    dict
        The newly initialized line breaks dictionary 
    """
    start = []
    end = []
    tokens = []
    if "end" in curr_boundary:
        end = curr_boundary["end"]
    if "start" in curr_boundary:
        start = curr_boundary["start"]
    if "tokens" in curr_boundary:
        tokens = curr_boundary["tokens"]
    
    line_breaks = {
        "end": end,
        "pageBoundaries": {},
        "start": start,
        "tokens": tokens
    }
    return line_breaks

def reset_prev_state():
    """
    Initializes a dictionary to hold information
    about previously examined pages.

    Returns
    -------
    dict
        The dictionary to hold previous page data
    """
    prev_state = {
        "line_breaks": reset_line_breaks(),
        "words": [[]]
    }
    return prev_state

def update_prev_state(words, line_breaks, prev_state):
    """
    Modifies a dictionary containing information about a previous 
    page to store information about the currently supplied page.

    Parameters
    ----------
    words: list
        The words in the current page
    line_breaks: dict
        The words split across a line in the current page
    """
    prev_page_pointer = get_prev_page_pointer(prev_state["words"], prev_state["line_breaks"])
    prev_state["line_breaks"] = line_breaks
    prev_state["words"] = words
    prev_state["line_breaks"]["pageBoundaries"] = {
        "previous": prev_page_pointer
    }

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
        early_cutoff = int(self.params["early_cutoff"])
        batch_size = int(self.params["batch_size"])
        tokenizer = self.params["tokenizer"]
        resource = self.params["resource"]
        upload_info = {"user": user, "resource": resource, "doc": doc}
        
        #Remove current document from database, if it exists
        self.cleanup(doc)

        #Process each line in document
        line_num = 0
        page_num = 1
        words = [[]]
        line_breaks = reset_line_breaks()
        prev_state = reset_prev_state()
        batch = []
        can_add_page = False
        char_count = 0
        curr_boundary = {
            "pos": 0
        }
        for line in doc["file"]:
            #Convert from bytes to unicode if necessary
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            #Blank new line
            if line == "\n":
                #Insert empty Line
                line_num += 1
                words.append([])

                #Start new line for text
                char_count = 0
                line_num += 1
                words.append([])
                continue

            tokenized = tokenizer.tokenize(line, line_size, offset=char_count, padding=early_cutoff)
            for token in tokenized:
                #Check if token continues onto next line
                if token["size"] + char_count >= line_size:
                    words[line_num].append(token["text"])
                    line_info = [line_num, page_num, new_page, len(words[line_num]), line_size]
                    curr_boundary = process_line_end(token, curr_boundary, line_info, line_breaks)
                    char_count = 0
                    if (line_num + 1) < new_page:
                        line_num += 1
                        words.append([])
                    else:
                        line_num += 1
                else:
                    if check_line_start(line_breaks, char_count):
                        line_info = [line_num, page_num, new_page, line_size]
                        curr_boundary = process_line_start(token, curr_boundary, line_info, line_breaks)
                    words[line_num].append(token["text"])
                    char_count += token["size"]
                
                #Add page to upload batch
                if can_add_page:
                    can_get_next_pointer = (len(words[0]) > 1) or (len(words) > 1)
                    if can_get_next_pointer:
                        prev_page = page_num - 1
                        page_content = get_page_content(words, prev_page, prev_state)
                        add_page(batch, page_content, prev_page, upload_info)
                        can_add_page = False
                
                #Start new page
                if (line_num + 1) > new_page:
                    can_add_page = True
                    update_prev_state(words, line_breaks, prev_state)
                    page_num += 1
                    line_num = 0
                    words = [[]]
                    line_breaks = reset_line_breaks(curr_boundary)
                
                #Insert page batch into database
                if len(batch) >= batch_size:
                    self.insert_batch(batch, doc)
                    batch = []
        
        #Load last page
        prev_page = page_num - 1
        if len(words) > 0:
            update_prev_state(words, line_breaks, prev_state)
            blank_page = []
            page_content = get_page_content(blank_page, page_num, prev_state)
            add_page(batch, page_content, page_num, upload_info)
        else:
            page_content = get_page_content(words, prev_page, prev_state)
            add_page(batch, page_content, prev_page, upload_info)

        #Insert final batch
        self.insert_batch(batch, doc)