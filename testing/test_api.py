import json
import datetime

from base64 import b64encode
from http import HTTPStatus

from app.models import Book, Page, PageContent, VocabEntry
from testing.test_base import BaseTest

class APITest(BaseTest):
    """
    Contains logic for running any test that interacts with
    the REST APIS.
    """
    __test__ = False

    def get_headers(self, username, password):
        """
        Creates headers to be sent in every JSON request.

        Parameters
        ----------
        username : str
            The name of the user
        password : str
            The user's password for accessing the REST APIs
        
        Returns
        -------
        dict
            The headers of the JSON request
        """
        credentials = b64encode((username + ":" + password).encode('utf-8'))
        credentials = credentials.decode('utf-8')
        headers = {}
        headers["Authorization"] = 'Basic ' + credentials
        headers["Accept"] = 'application/json'
        headers["Content-Type"] = 'application/json'
        return headers 

class DocumentRetrievalTest(APITest):
    """
    A collection of tests for validating the document_retrieval
    REST API.
    """
    __test__ = True

    def setUp(self):
        """
        Loads sample data before every test.
        """
        super().setUp()

        #Load sample data
        #content_kant = "Erfahrung ist ohne Zweifel das erste Produkt..."
        kant_dict = {
            "words": [
                ["Erfahrung ist", "ohne Zwei-"],
                ["fel", "das erste Produkt..."]
            ],
            "breaks": {
                "start": [0],
                "end": [0],
                "tokens": {
                    "fulltext": "Zweifel",
                    "positions": [[1,0,1],[1,1,0]]
                }
            }
        }
        content_kant = PageContent(words=kant_dict["words"], breaks=kant_dict["breaks"])
        #content_hegel = "Das Wissen, welches zuerst oder unmittlebar..."
        hegel_dict = {
            "words": [
                ["Das Wissen, ", "welches ", "zu-"],
                ["erst ", "oder unmittelbar..."]
            ],
            "breaks": {
                "start": [0],
                "end": [0],
                "tokens": {
                    "fulltext": "zuerst",
                    "positions": [[1,0,2],[1,1,0]]
                }
            }
        }
        content_hegel = PageContent(words=hegel_dict["words"], breaks=hegel_dict["breaks"])
        book1 = Book(
                     title="Kritik der reinen Vernunft",
                     author="Immanuel Kant",
                     language="german",
                     page_number=1,
                     publisher="Johann Friedrich Hartknoch"
                     )
        book2 = Book(
                     title="Phänomenologie des Geistes",
                     author="Georg Wilhelm Friedrich Hegel",
                     language="german",
                     page_number=1,
                     publisher="Joseph Anton Goebhardt"
                     )
        page1 = Page(
                     email=self.username,
                     resource=book1,
                     content=content_kant
                     )
        page2 = Page(
                     email=self.username,
                     resource=book2,
                     content=content_hegel
                     )
        page1.save()
        page2.save()

        self.kant = {"book": book1, "content": kant_dict, "page": page1}
        self.hegel = {"book": book2, "content": hegel_dict, "page": page2}

    def test_fetch_page(self):
        """
        Tests the single page service provided by document_retrieval.
        """
        #Get page to fetch
        query = {}
        query["title"] = self.kant["book"].title
        query["author"] = self.kant["book"].author
        query["page"] = 1
        query = json.dumps(query, ensure_ascii=False)
        
        #Make API call to fetch page
        response = self.client.post(
                                    '/api/v1/document_retrieval/page',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["title"], self.kant["book"].title)
        self.assertEqual(json_response["author"], self.kant["book"].author)
        self.assertEqual(int(json_response["page"]), 1)
        self.assertEqual(json_response["content"], self.kant["content"])

    def test_list_docs(self):
        """
        Tests the list_docs service provided by document_retrieval.
        """
        #Documents for testing
        kant = {}
        kant["title"] = self.kant["book"].title
        kant["author"] = self.kant["book"].author
        hegel = {}
        hegel["title"] = self.hegel["book"].title
        hegel["author"] = self.hegel["book"].author

        #Make API call to list a user's documents
        response = self.client.get(
                                   '/api/v1/document_retrieval/doc_list',
                                   headers=self.get_headers(self.username, self.password)
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn(kant, json_response["works"])
        self.assertIn(hegel, json_response["works"])
            
    def test_no_page(self):
        """
        Tests that the fetch_page service handles requests
        for non-existent user resources correctly.
        """
        #Search for non-existent page
        query = {}
        query["title"] = self.kant["book"].title
        query["author"] = self.kant["book"].author
        query["page"] = 10
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to fetch page
        response = self.client.post(
                                    '/api/v1/document_retrieval/page',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)
    
    def test_no_docs(self):
        """
        Tests that the list_docs service handles requests for
        non-existent user resources correctly.
        """
        #Delete all docs
        Page.objects().delete()

        #Make API call to list a user's documents
        response = self.client.get(
                                   '/api/v1/document_retrieval/doc_list',
                                   headers=self.get_headers(self.username, self.password)
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)
    
    def test_page_range(self):
        """
        Tests the page range service provided by document_retrieval.
        """
        #Load new page
        book_kant = Book(
                         title="Kritik der reinen Vernunft",
                         author="Immanuel Kant",
                         language="german",
                         page_number=2,
                         publisher="Johann Friedrich Hartknoch"
                        )
        new_dict = {
            "words": [
                ["Wenn aber gleich ", "alle unsere Erken-"],
                ["ntniss ", "mit der Erfahrung anhebt..."]
            ],
            "breaks": {
                "start": [0],
                "end": [0],
                "tokens": {
                    "fulltext": "Erkenntniss",
                    "positions": [[1,0,1],[1,1,0]]
                }
            }
        }
        new_content = PageContent(words=new_dict["words"], breaks=new_dict["breaks"])
        new_page = Page(
                        email=self.username,
                        resource=book_kant,
                        content=new_content
                       )
        new_page.save()

        #Specify page range
        query = {}
        query["title"] = self.kant["book"].title
        query["author"] = self.kant["book"].author
        query["start"] = 1
        query["end"] = 5
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to fetch page
        response = self.client.post(
                                    '/api/v1/document_retrieval/page_range',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )
        
        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["title"], self.kant["book"].title)
        self.assertEqual(json_response["author"], self.kant["book"].author)
        self.assertEqual(int(json_response["startPage"]), 1)
        self.assertEqual(len(json_response["content"]), 2)
        self.assertEqual(json_response["content"][0], self.kant["content"])
        self.assertEqual(json_response["content"][1], new_dict)

class APISecurityTest(APITest):
    """
    A collection of tests that validate the REST API security infrastructure.
    """
    __test__ = True

    def test_bad_password(self):
        """
        Test that a user is denied access when an incorrect password is given.
        """
        bad_password = "wrong_password"

        #Make API call to list a user's documents
        response = self.client.get(
                                   '/api/v1/document_retrieval/doc_list',
                                   headers=self.get_headers(self.username, bad_password)
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED.value)

    def test_bad_user(self):
        """
        Test that no credentials in the header lead to denying
        access to the REST APIs.
        """
        #Make API call to list documents
        response = self.client.get(
                                   '/api/v1/document_retrieval/doc_list',
                                   headers=self.get_headers('','')
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED.value)

    def test_no_user(self):
        """
        Test that a REST API request with no known user leads to
        denial of access.
        """
        #Make API call to list documents
        response = self.client.get(
                                   '/api/v1/document_retrieval/doc_list'
                                  )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED.value)

    def test_token(self):
        """
        Test that a user can properly receive an authentication token.
        """
        #Make API call to get token
        response = self.client.post(
                                    '/api/v1/tokens',
                                    headers=self.get_headers(self.username, self.password)
                                    )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))

class TranslationTest(APITest):
    """
    A collection of tests which validate the translation service.
    """
    __test__ = True

    def test_inflected(self):
        """
        Test that a foreign word thats different from a base
        dictionary word returns the right translation.
        """
        #Get word to translate
        query = {}
        query["page"] = 1
        query["query"] = "Mitarbeiterinnen"
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to translate word
        response = self.client.post(
                                    '/api/v1/translation/german',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        translation = json_response["translations"][0]["definition"]
        candidates = ["staffers", "employees", "hires"]
        candidates += ["cooperators", "co-workers", "coworkers"]
        candidates += ["collaborators", "staff members"]
        self.assertIn(translation, candidates)

    def test_multiword(self):
        """
        Test that a search term consisting of multiple words
        is translated correctly.
        """
        #Get phrase to translate
        query = {}
        query["page"] = 1
        query["query"] = "lieferbare Bücher"
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to translate phrase
        response = self.client.post(
                                    '/api/v1/translation/german',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query        
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        translation = json_response["translations"][0]["definition"]
        self.assertEqual(translation, "books in print")

    def test_see_also(self):
        """
        Test that a valid link to the base form of a translation
        is given.
        """
        #Look up term that will have a different base form
        query = {}
        query["page"] = 1
        query["query"] = "Häuser"
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to translate word
        response = self.client.post(
                                    '/api/v1/translation/german',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        translation = json_response["translations"][0]["see_also"]
        self.assertIn("Haus", translation["text"])
        self.assertEqual(translation["pos"], "noun_neuter")

    def test_no_translation(self):
        """
        Test that a word that's not part of a foreign language
        returns no translation.
        """
        #Get random word that will return no matches
        query = {}
        query["page"] = 1
        query["query"] = "fsdgdfsgdfgf"
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to translate word
        response = self.client.post(
                                    '/api/v1/translation/german',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_no_page(self):
        """
        Test that the translation services handles requests
        for non-existent pages gracefully.
        """
        #Look for page that will have no results
        query = {}
        query["page"] = 1000
        query["query"] = "Mitarbeiterinnen"
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to translate word
        response = self.client.post(
                                    '/api/v1/translation/german',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

class VocabularyAcquisitionTest(APITest):
    """
    A collection of tests for validating the vocab_acquisition service.
    """
    __test__ = True

    def setUp(self):
        """
        Loads sample data before each test is run.
        """
        super().setUp()

        #Initialize resource objects
        title = "Kritik der reinen Vernunft"
        author = "Immanuel Kant"
        publisher = "Johann Friedrich Hartknoch"
        self.book1 = Book(
                          title=title,
                          author=author,
                          language="german",
                          page_number=1,
                          publisher=publisher
                          )
        self.book2 = Book(
                          title=title,
                          author=author,
                          language="german",
                          page_number=2,
                          publisher=publisher
                          )
        
        #Possible phrases for later use:
        #phrase1 = "Möglichkeit der Erfahrung"
        #phrase2 = "unserer Erfahrung nach"
        
        #Initialize vocabulary entries
        word = "Erfahrung"
        pos = "noun_feminine"
        definitions = ["Experience"]
        vocab = VocabEntry(
                           email=self.username,
                           vocab_text=word,
                           language="german",
                           pos=pos,
                           resource=self.book1,
                           definitions=definitions,
                           timestamp=datetime.datetime.now()
                           )
        vocab.save()
        vocab = VocabEntry(
                           email=self.username,
                           vocab_text=word,
                           language="german",
                           pos=pos,
                           resource=self.book2,
                           definitions=definitions,
                           timestamp=datetime.datetime.now()
                           )
        vocab.save()
        word = "Möglichkeit"
        definitions = ["Possibility"]
        vocab = VocabEntry(
                           email=self.username,
                           vocab_text=word,
                           language="german",
                           pos=pos,
                           resource=self.book1,
                           definitions=definitions,
                           timestamp=datetime.datetime.now()
                           )
        vocab.save() 

    def test_add_vocab_item(self):
        """
        Tests the add_vocab_entry service.
        """
        #Initialize request data
        vocab_info = {}
        vocab_info["text"] = "Vernunft"
        vocab_info["pos"] = "noun_feminine"
        vocab_info["definitions"] = ["Reason"]

        resource = {}
        resource["title"] = self.book1.title
        resource["author"] = self.book1.author
        resource["page_number"] = self.book1.page_number
        resource["publisher"] = self.book1.publisher
        resource["type"] = "book"
        
        query = {}
        query["vocab_info"] = vocab_info
        query["resource"] = resource
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to add a vocabulary entry
        response = self.client.post(
                                    '/api/v1/vocab_acquisition/german/vocab_entry/addition',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                    )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.CREATED.value)
        vocab_item = VocabEntry.objects(vocab_text=vocab_info["text"]).first()
        self.assertIsNotNone(vocab_item)

    def test_multi_lookup(self):
        """
        Tests the lookup_vocab_entries service.
        """
        #Initialize request data
        query = {}
        query["page"] = 1
        query["queries"] = []
        
        subquery = {}
        subquery["page"] = {"start": 1, "finish": 3}
        subquery["title"] = self.book1.title
        subquery["author"] = self.book1.author
        query["queries"].append(subquery)
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to look up words
        response = self.client.post(
                                    '/api/v1/vocab_acquisition/german/vocab_collection/lookup',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        word = {}
        word["vocab_text"] = "Erfahrung"
        word["title"] = self.book1.title
        word["author"] = self.book1.author
        word["page"] = 2
        self.assertIn(word, json_response["vocab_items"])

        #Lookup word from different authors
        title = "Phänomenologie des Geistes"
        author = "Georg Wilhelm Friedrich Hegel"
        publisher = "Joseph Anton Goebhardt"
        hegel = Book(
                     title=title,
                     author=author,
                     language="german",
                     page_number=1,
                     publisher=publisher
                     )
        word = "Geist"
        definitions = ["Spirit"]
        pos = "noun_masculine"
        vocab = VocabEntry(
                           email=self.username,
                           vocab_text=word,
                           language="german",
                           pos=pos,
                           resource=hegel,
                           definitions=definitions,
                           timestamp=datetime.datetime.now()
                           )
        vocab.save()

        query = {}
        query["page"] = 1
        query["queries"] = []

        subquery_kant = {}
        subquery_kant["page"] = {"start": 1, "finish": 3}
        subquery_kant["title"] = self.book1.title
        subquery_kant["author"] = self.book1.author
        query["queries"].append(subquery_kant)

        subquery_hegel = {}
        subquery_hegel["page"] = {"start":1, "finish": 3}
        subquery_hegel["title"] = hegel.title
        subquery_hegel["author"] = hegel.author
        query["queries"].append(subquery_hegel)
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to look up words
        response = self.client.post(
                                    '/api/v1/vocab_acquisition/german/vocab_collection/lookup',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        word = {}
        word["vocab_text"] = "Erfahrung"
        word["title"] = self.book1.title
        word["author"] = self.book1.author
        word["page"] = 2
        self.assertIn(word, json_response["vocab_items"])
        word = {}
        word["vocab_text"] = "Geist"
        word["title"] = hegel.title
        word["author"] = hegel.author
        word["page"] = 1
        self.assertIn(word, json_response["vocab_items"])

    def test_multi_removal(self):
        """
        Tests that the remove_vocab_entry service can delete
        multiple words from a user's vocabulary.
        """
        #Initialize data
        query = {}
        query["vocab_text"] = "Erfahrung"
        query = json.dumps(query, ensure_ascii=False)

        #Make API cal to delete words
        response = self.client.delete(
                                      '/api/v1/vocab_acquisition/german/vocab_entry',
                                      headers=self.get_headers(self.username, self.password),
                                      data=query
                                     )

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT.value)
        entries = VocabEntry.objects(vocab_text="Erfahrung")
        self.assertIsNone(entries.first())
    
    def test_no_lookup(self):
        """
        Tests that requests for non-existent vocabulary words are
        handled gracefully.
        """
        #Word that's not in user's vocabulary
        query = {}
        query["vocab_text"] = "Mensch"
        query["title"] = self.book1.title
        query["author"] = self.book1.author
        query["page"] = 1
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to look up word
        response = self.client.post(
                                    '/api/v1/vocab_acquisition/german/vocab_entry/lookup',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

        #Title that's not mentioned in user's vocabulary list
        query = {}
        query["page"] = 1
        query["queries"] = [{"title": "Kritik der praktischen Vernunft",
                             "author": self.book1.author}]
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to look up words
        response = self.client.post(
                                    '/api/v1/vocab_acquisition/german/vocab_collection/lookup',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_no_removal(self):
        """
        Tests that a request to remove a non-existent vocabulary
        word is handled gracefully.
        """
        #Word that's not in user's vocabulary
        query = {"vocab_text": "Mensch"}
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to delete word
        response = self.client.delete(
                                      '/api/v1/vocab_acquisition/german/vocab_entry',
                                      headers=self.get_headers(self.username, self.password),
                                      data=query
                                     )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

        #Word not in specified book
        query = {}
        query["vocab_text"] = "Mensch"
        query["query"] = {}
        query["query"]["title"] = self.book1.title
        query["query"]["author"] = self.book1.author
        query["query"]["page"] = 1
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to delete word
        response = self.client.delete(
                                      '/api/v1/vocab_acquisition/german/vocab_entry',
                                      headers=self.get_headers(self.username, self.password),
                                      data=query
                                     )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_single_lookup(self):
        """
        Tests the lookup_vocab_entry service.
        """
        #Initialize data
        vocab_text = "Erfahrung"
        query = {}
        query["page"] = self.book1.page_number
        query["title"] = self.book1.title
        query["author"] = self.book1.author
        query["vocab_text"] = vocab_text
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to look up single word
        response = self.client.post(
                                    '/api/v1/vocab_acquisition/german/vocab_entry/lookup',
                                    headers=self.get_headers(self.username, self.password),
                                    data=query
                                   )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        vocab_entry = VocabEntry.objects(
                                         vocab_text=vocab_text,
                                         resource=self.book1
                                         ).first()
        self.assertIsNotNone(vocab_entry)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(self.book1.author, json_response["vocab_item"]["author"])
        self.assertEqual(self.book1.title, json_response["vocab_item"]["title"])
        self.assertEqual(vocab_text, json_response["vocab_item"]["vocab_text"])

    def test_single_removal(self):
        """
        Tests that the remove_vocab_entry service can successfully delete
        a single vocabulary entry.
        """
        #Initialize data
        vocab_text = "Erfahrung"
        query = {}
        query["vocab_text"] = vocab_text
        query["query"] = {}
        query["query"]["title"] = self.book1.title
        query["query"]["author"] = self.book1.author
        query["query"]["page"] = self.book1.page_number
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to delete single instance
        response = self.client.delete(
                                      '/api/v1/vocab_acquisition/german/vocab_entry',
                                      headers=self.get_headers(self.username, self.password),
                                      data=query
                                      )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT.value)
        vocab_entry = VocabEntry.objects(
                                         vocab_text=vocab_text,
                                         resource=self.book1
                                         ).first()
        self.assertIsNone(vocab_entry)
        vocab_entry = VocabEntry.objects(
                                         vocab_text=vocab_text,
                                         resource=self.book2
                                         ).first()
        self.assertIsNotNone(vocab_entry)