import os
import unittest

import yaml

from app.content_management.lib.resources import create_book
from app.content_management.lib.upload import DocumentUploader
from app.models import Page
from testing.test_base import BaseTest

class DocumentManagementTest(BaseTest):
    """
    Verifies that documents are uploaded and
    parsed correctly.
    """
    __test__ = True
    __language__ = "german"

    def init_documents(self, language):
        """
        Sets up documents to be used in test suite.

        Parameters
        ----------
        language : str
            The language the test documents are written in
        """
        doc_dir = self.app.config["TEST_DOCUMENT_UPLOAD"]["doc_location"]
        metadata_file = self.app.config["TEST_DOCUMENT_UPLOAD"]["doc_metadata"]
        
        #Load metadata describing test documents from yaml file
        metadata_file = os.path.join(doc_dir, metadata_file)
        with open(metadata_file, 'r') as m_data:
            try:
                self.metadata = yaml.safe_load(m_data)
            except Exception as e:
                print("Error loading DocumentManagementTest metadata.")
                print(e)
                raise Exception("Couldn't load metadata file " + metadata_file)

        #Save documents
        self.doc = {}
        to_read = []
        documents = os.scandir(doc_dir)
        for document in documents:
            doc_name = document.name
            if len(doc_name) > 4:
                if doc_name[-4:] == ".txt":
                    to_read.append(doc_name)
        for document in to_read:
            with open(os.path.join(doc_dir, document), 'r') as d:
                try:
                    self.doc[document] = {}
                    self.doc[document]["file"] = d.readlines()
                    self.doc[document]["title"] = self.metadata[document]["title"]
                    self.doc[document]["author"] = self.metadata[document]["author"]
                    self.doc[document]["language"] = self.__language__
                except Exception as e:
                    print("Error reading test document in DocumentManagementTest.")
                    print(e)
                    raise Exception("Couldn't load test document " + document)
        
    def init_uploader(self, language):
        """
        Sets up the DocumentUpload object to be tested
        in the test suite.

        Parameters
        ----------
        language : str
            The language the test documents are written in
        """

        params = {}
        params["email"] = self.username
        params["new_page"] = self.app.config["TEST_DOCUMENT_UPLOAD"]["page_limit"]
        params["line_size"] = self.app.config["TEST_DOCUMENT_UPLOAD"]["line_size"]
        params["early_cutoff"] = 0
        params["batch_size"] = self.app.config["TEST_DOCUMENT_UPLOAD"]["batch_size"]
        params["tokenizer"] = self.app.config["TOKENIZER"].select(language)
        params["resource"] = create_book
        self.params = params
        self.doc_uploader = DocumentUploader(params)

    def setUp(self):
        """
        Initializes the infrastructure for running
        a unit test.
        """

        super().setUp()
        language = self.__language__
        self.init_documents(language)
        self.init_uploader(language)
    
    def test_blank_line(self):
        """
        Tests that a document with a blank line
        is processed correctly.
        """

        #Upload document
        document = self.doc[self.metadata["blank_line"]]
        self.doc_uploader.upload(document)

        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )
        
        has_page = True
        page = pages.first()
        if not page:
            has_page = False

        self.assertTrue(has_page)

        #Check first page
        content = page.content
        self.assertEqual(len(content.words), 3)
        self.assertEqual(len(content.words[1]), 0)
        first_line = ["Habe", " ", "Mut"]
        self.assertEqual(content.words[0][0:3], first_line)
        last_line = ["zuwissen", " "]
        self.assertEqual(content.words[2][0:2], last_line)

    def test_cleanup(self):
        """
        Tests that a document can be successfully deleted.
        """

        #Upload document
        document = self.doc[self.metadata["cleanup"]]
        self.doc_uploader.upload(document)

        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                             )
        
        has_pages = True
        if not pages.first():
            has_pages = False
        
        self.assertTrue(has_pages)

        #Remove document
        self.doc_uploader.cleanup(document)
        
        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )
        
        has_pages = False
        if pages.first():
            has_pages = True
        
        self.assertFalse(has_pages)

    def test_line_break(self):
        """
        Tests that a word which has to be split across
        two lines is processed correctly.
        """
        
        #Upload document
        document = self.doc[self.metadata["line_break"]]
        self.doc_uploader.upload(document)

        page = Page.objects(
                            email=self.username,
                            resource__title=document["title"],
                            resource__author=document["author"],
                            resource__page_number=1
                           )
        
        page = page.first()
        has_page = True
        if not page:
            has_page = False
        
        self.assertTrue(has_page)
        
        #Check for line breaks
        content = page.content
        self.assertEqual(content.breaks["tokens"][1]["fulltext"], "ist")
        self.assertEqual(content.breaks["start"][1], 1)
        self.assertEqual(content.breaks["end"][0], 1)
    
    def test_load_multi_page(self):
        """
        Tests that more than one page can be saved
        properly.
        """

        #Upload document
        document = self.doc[self.metadata["load_multi_page"]]
        self.doc_uploader.upload(document)

        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )
        
        #Get page count
        count = 0
        for page in pages:
            count += 1
        
        has_correct_count = (count == 4)
        self.assertTrue(has_correct_count) 

    def test_load_single_page(self):
        """
        Tests that a single page can be loaded properly.
        """

        #Upload document
        document = self.doc[self.metadata["load_single_page"]]
        self.doc_uploader.upload(document)

        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )
        
        #Get page count
        count = 0
        for page in pages:
            count += 1
        
        has_correct_count = (count == 1)
        self.assertTrue(has_correct_count)
    
    def test_next_page_pointer(self):
        """
        Tests that the JSON representation of a page of text
        contains the proper pointer to the first word of the
        next page.
        """

        #Upload document
        document = self.doc[self.metadata["page_boundaries"]]
        self.doc_uploader.upload(document)

        #Get pages
        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )
        pages.order_by('resource__page_number')
        
        test_data = []
        for page in pages:
            test_data.append(page)
        
        has_pages = (len(test_data) == 2)
        self.assertTrue(has_pages)

        #Test empty pointer
        content = test_data[1].content
        page_boundaries = content["breaks"]["pageBoundaries"]
        empty_pointer = {}
        self.assertEqual(page_boundaries["next"], empty_pointer)

        #Test regular pointer
        content = test_data[0].content
        page_boundaries = content["breaks"]["pageBoundaries"]
        test_pointer = {
            "line": 0,
            "page": 2,
            "pos": 1
        }
        self.assertEqual(page_boundaries["next"], test_pointer)
    
    def test_no_line_break(self):
        """
        Tests that a word isn't split across two lines
        if it isn't necessary.
        """

        #Upload document
        document = self.doc[self.metadata["no_line_break"]]
        self.doc_uploader.upload(document)

        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )

        has_page = True
        page = pages.first()
        if not page:
            has_page = False

        self.assertTrue(has_page)

        #Check for line break
        content = page.content
        self.assertEqual(content.breaks["end"][0], 1)
        self.assertEqual(content.breaks["tokens"][1]["fulltext"], "Welt")
        self.assertEqual(content.breaks["start"][1], 2)
        self.assertEqual(content.breaks["tokens"][2]["fulltext"], " ")

    def test_page_content_multi_line(self):
        """
        Tests that a page with multiple lines
        is processed correctly.
        """

        #Upload document
        document = self.doc[self.metadata["page_content_multi_line"]]
        self.doc_uploader.upload(document)

        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )
        
        has_page = True
        page = pages.first()
        if not page:
            has_page = False
        
        self.assertTrue(has_page)

        content = page.content
        #Check first line
        self.assertGreaterEqual(len(content.words), 1)
        self.assertLessEqual(3, len(content.words[0]))
        self.assertEqual(content.words[0][2], "Welt")
        self.assertGreaterEqual(len(content.breaks["end"]), 1)
        self.assertEqual(content.breaks["end"][0], 1)
        self.assertEqual(content.breaks["tokens"][1]["fulltext"], "ist")

        #Check second line
        self.assertGreaterEqual(len(content.words), 2)
        self.assertLessEqual(3, len(content.words[1]))
        self.assertEqual(content.words[1][2], "meine")
        self.assertEqual(content.breaks["start"][1], 1)
    
    def test_page_content_single_line(self):
        """
        Tests that a page with a single line
        is processed correctly.
        """

        #Upload document
        document = self.doc[self.metadata["page_content_single_line"]]
        self.doc_uploader.upload(document)

        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )
        
        has_page = True
        page = pages.first()
        if not page:
            has_page = False
        
        self.assertTrue(has_page)

        #Check for single line
        content = page.content
        self.assertEqual(len(content.words), 2)
        self.assertEqual(len(content.words[1]), 0)
        self.assertLessEqual(3, len(content.words[0]))
        self.assertEqual(content.words[0][2], "Welt")
    
    def test_prev_page_pointer(self):
        """
        Tests that the JSON representation of a page of text
        contains the proper pointer to the last word of the
        previous page.
        """

        #Upload document
        document = self.doc[self.metadata["page_boundaries"]]
        self.doc_uploader.upload(document)

        #Get pages
        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )
        pages.order_by('resource__page_number')
        
        test_data = []
        for page in pages:
            test_data.append(page)
        
        has_pages = (len(test_data) == 2)
        self.assertTrue(has_pages)

        #Test empty pointer
        content = test_data[0].content
        page_boundaries = content["breaks"]["pageBoundaries"]
        empty_pointer = {}
        self.assertEqual(page_boundaries["previous"], empty_pointer)

        #Test regular pointer
        content = test_data[1].content
        page_boundaries = content["breaks"]["pageBoundaries"]
        test_pointer = {
            "line": 2,
            "page": 1,
            "pos": 3
        }
        self.assertEqual(page_boundaries["previous"], test_pointer)
    
    def test_token_offset(self):
        """
        Tests the tokenizer when starting from
        a non-zero offset.
        """
        #Upload document
        document = self.doc[self.metadata["offset"]]
        self.doc_uploader.upload(document)

        #Get pages
        pages = Page.objects(
                             email=self.username,
                             resource__title=document["title"],
                             resource__author=document["author"]
                            )
        
        test_data = []
        for page in pages:
            test_data.append(page)
        
        has_page = (len(test_data) == 1)
        self.assertTrue(has_page)

        #Check offsets are processed correctly
        content = test_data[0].content
        expected = [
            ['Habe', ' ', 'Mut', ' ', 'z-'],
            ['u', ' ', 'wissen', ' ']
        ]
        self.assertEqual(content["words"], expected)