import json
import datetime

from base64 import b64encode
from http import HTTPStatus

from app.models import Book, Page, VocabEntry
from testing.test_base import BaseTest

class APITest(BaseTest):
    __test__ = False

    def get_headers(self, username, password):
        credentials = b64encode((username + ":" + password).encode('utf-8'))
        credentials = credentials.decode('utf-8')
        headers = {}
        headers["Authorization"] = 'Basic ' + credentials
        headers["Accept"] = 'application/json'
        headers["Content-Type"] = 'application/json'
        return headers 

class DocumentRetrievalTest(APITest):
    __test__ = True

    def setUp(self):
        super().setUp()

        #Load sample data
        content_kant = "Erfahrung ist ohne Zweifel das erste Produkt..."
        content_hegel = "Das Wissen, welches zuerst oder unmittlebar..."
        book1 = Book(title="Kritik der reinen Vernunft",
                     author="Immanuel Kant",
                     language="german",
                     page_number=1,
                     publisher="Johann Friedrich Hartknoch"
                     )
        book2 = Book(title="Phänomenologie des Geistes",
                     author="Georg Wilhelm Friedrich Hegel",
                     language="german",
                     page_number=1,
                     publisher="Joseph Anton Goebhardt"
                     )
        page1 = Page(email=self.username,
                     resource=book1,
                     content=content_kant
                     )
        page2 = Page(email=self.username,
                     resource=book2,
                     content=content_hegel
                     )
        page1.save()
        page2.save()

        self.kant = {"book": book1, "page": page1}
        self.hegel = {"book": book2, "page": page2}

    def test_fetch_page(self):
        #Get page to fetch
        query = {}
        query["title"] = self.kant["book"].title
        query["author"] = self.kant["book"].author
        query["page"] = 1
        query = json.dumps(query, ensure_ascii=False)
        
        #Make API call to fetch page
        response = self.client.get(
            '/api/v1/document_retrieval/fetch_page',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response["title"], self.kant["book"].title)
        self.assertEqual(json_response["author"], self.kant["book"].author)
        self.assertEqual(int(json_response["page"]), 1)
        self.assertEqual(json_response["content"], self.kant["page"].content)

    def test_list_docs(self):
        #Documents for testing
        kant = {}
        kant["title"] = self.kant["book"].title
        kant["author"] = self.kant["book"].author
        hegel = {}
        hegel["title"] = self.hegel["book"].title
        hegel["author"] = self.hegel["book"].author

        #Make API call to list a user's documents
        response = self.client.get(
            '/api/v1/document_retrieval/list_docs',
            headers=self.get_headers(self.username, self.password)
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn(kant, json_response["docs"])
        self.assertIn(hegel, json_response["docs"])
            
    def test_no_page(self):
        #Search for non-existent page
        query = {}
        query["title"] = self.kant["book"].title
        query["author"] = self.kant["book"].author
        query["page"] = 10
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to fetch page
        response = self.client.get(
            '/api/v1/document_retrieval/fetch_page',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)
    
    def test_no_docs(self):
        #Delete all docs
        Page.objects().delete()

        #Make API call to list a user's documents
        response = self.client.get(
            '/api/v1/document_retrieval/list_docs',
            headers=self.get_headers(self.username, self.password)
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)


class APISecurityTest(APITest):
    __test__ = True

    def test_bad_password(self):
        bad_password = "wrong_password"

        #Make API call to list a user's documents
        response = self.client.get(
            '/api/v1/document_retrieval/list_docs',
            headers=self.get_headers(self.username, bad_password)
        )

    def test_bad_user(self):
        #Make API call to list documents
        response = self.client.get(
            '/api/v1/document_retrieval/list_docs',
            headers=self.get_headers('','')
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED.value)

    def test_no_user(self):
        #Make API call to list documents
        response = self.client.get(
            '/api/v1/document_retrieval/list_docs'
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED.value)

    def test_token(self):
        #Make API call to get token
        response = self.client.post(
            '/api/v1/tokens',
            headers=self.get_headers(self.username, self.password)
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']
        
        #Make API call with the token
        response = self.client.get(
            '/api/v1/document_retrieval/list_docs',
            headers=self.get_headers(token,'')
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

class TranslationTest(APITest):
    __test__ = True

    def test_inflected(self):
        #Get word to translate
        query = {}
        query["page"] = 1
        query["query"] = "Mitarbeiterinnen"
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to translate word
        response = self.client.get(
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
        #Get phrase to translate
        query = {}
        query["page"] = 1
        query["query"] = "lieferbare Bücher"
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to translate phrase
        response = self.client.get(
            '/api/v1/translation/german',
            headers=self.get_headers(self.username, self.password),
            data=query        
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        json_response = json.loads(response.get_data(as_text=True))
        translation = json_response["translations"][0]["definition"]
        self.assertEqual(translation, "books in print")

    def test_no_translation(self):
        #Get random word that will return no matches
        query = {}
        query["page"] = 1
        query["query"] = "fsdgdfsgdfgf"
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to translate word
        response = self.client.get(
            '/api/v1/translation/german',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_no_page(self):
        #Look for page that will have no results
        query = {}
        query["page"] = 1000
        query["query"] = "Mitarbeiterinnen"
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to translate word
        response = self.client.get(
            '/api/v1/translation/german',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

class VocabularyAcquisitionTest(APITest):
    __test__ = True

    def setUp(self):
        super().setUp()

        #Initialize resource objects
        title = "Kritik der reinen Vernunft"
        author = "Immanuel Kant"
        publisher = "Johann Friedrich Hartknoch"
        self.book1 = Book(title=title,
                          author=author,
                          language="german",
                          page_number=1,
                          publisher=publisher
                          )
        self.book2 = Book(title=title,
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
        vocab = VocabEntry(email=self.username,
                           vocab_text=word,
                           language="german",
                           pos=pos,
                           resource=self.book1,
                           definitions=definitions,
                           timestamp=datetime.datetime.now()
                           )
        vocab.save()
        vocab = VocabEntry(email=self.username,
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
        vocab = VocabEntry(email=self.username,
                           vocab_text=word,
                           language="german",
                           pos=pos,
                           resource=self.book1,
                           definitions=definitions,
                           timestamp=datetime.datetime.now()
                           )
        vocab.save() 

    def test_add_vocab_item(self):
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
            '/api/v1/vocab_acquisition/add_vocab_entry/german',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.CREATED.value)
        vocab_item = VocabEntry.objects(vocab_text=vocab_info["text"]).first()
        self.assertIsNotNone(vocab_item)

    def test_multi_lookup(self):
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
        response = self.client.get(
            '/api/v1/vocab_acquisition/lookup_vocab_entries/german',
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
        hegel = Book(title=title,
                     author=author,
                     language="german",
                     page_number=1,
                     publisher=publisher
                     )
        word = "Geist"
        definitions = ["Spirit"]
        pos = "noun_masculine"
        vocab = VocabEntry(email=self.username,
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
        response = self.client.get(
            '/api/v1/vocab_acquisition/lookup_vocab_entries/german',
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
        #Initialize data
        query = {}
        query["vocab_text"] = "Erfahrung"
        query = json.dumps(query, ensure_ascii=False)

        #Make API cal to delete words
        response = self.client.delete(
            '/api/v1/vocab_acquisition/remove_vocab_entry/german',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT.value)
        entries = VocabEntry.objects(vocab_text="Erfahrung")
        self.assertIsNone(entries.first())
    
    def test_no_lookup(self):
        #Word that's not in user's vocabulary
        query = {}
        query["vocab_text"] = "Mensch"
        query["title"] = self.book1.title
        query["author"] = self.book1.author
        query["page"] = 1
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to look up word
        response = self.client.get(
            '/api/v1/vocab_acquisition/lookup_vocab_entry/german',
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
        response = self.client.get(
            '/api/v1/vocab_acquisition/lookup_vocab_entries/german',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_no_removal(self):
        #Word that's not in user's vocabulary
        query = {"vocab_text": "Mensch"}
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to delete word
        response = self.client.delete(
            '/api/v1/vocab_acquisition/remove_vocab_entry/german',
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
            '/api/v1/vocab_acquisition/remove_vocab_entry/german',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_single_lookup(self):
        #Initialize data
        vocab_text = "Erfahrung"
        query = {}
        query["page"] = self.book1.page_number
        query["title"] = self.book1.title
        query["author"] = self.book1.author
        query["vocab_text"] = vocab_text
        query = json.dumps(query, ensure_ascii=False)

        #Make API call to look up single word
        response = self.client.get(
            '/api/v1/vocab_acquisition/lookup_vocab_entry/german',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        vocab_entry = VocabEntry.objects(vocab_text=vocab_text,
                                         resource=self.book1
                                         ).first()
        self.assertIsNotNone(vocab_entry)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(self.book1.author, json_response["vocab_item"]["author"])
        self.assertEqual(self.book1.title, json_response["vocab_item"]["title"])
        self.assertEqual(vocab_text, json_response["vocab_item"]["vocab_text"])

    def test_single_removal(self):
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
            '/api/v1/vocab_acquisition/remove_vocab_entry/german',
            headers=self.get_headers(self.username, self.password),
            data=query
        )

        #Process response
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT.value)
        vocab_entry = VocabEntry.objects(vocab_text=vocab_text,
                                         resource=self.book1
                                         ).first()
        self.assertIsNone(vocab_entry)
        vocab_entry = VocabEntry.objects(vocab_text=vocab_text,
                                         resource=self.book2
                                         ).first()
        self.assertIsNotNone(vocab_entry)