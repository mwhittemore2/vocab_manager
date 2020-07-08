from abc import ABC

from nltk.tokenize import word_tokenize

from .standard import Tokenizer

class Language(ABC):
    """
    Representation of a language with tokenization capabilities.
    """
    def __init__(self, language):
        """
        Initializes the language representation.

        Parameters
        ----------
        language : str
            The language to be tokenized
        """
        self.language = language
        self.tokenizer = (lambda s: word_tokenize(s, self.language))
    
    def is_punctuation(self, token):
        """
        Determines if a token is punctuation.

        Parameters
        ----------
        token : str
            The token to be tested
        
        Returns
        -------
        bool
            True is the token is punctuation, False otherwise.
        """
        pass

    def separator(self):
        """
        Punctuation for separating text across lines.
        """
        pass

    def tokenize(self, line):
        """
        Tokenizes a line of text from the user-specified language.

        Parameters
        ----------
        line : str
            The text to be tokenized.
        """
        pass

    def whitespace(self):
        """
        Character(s) for separating two words.
        """
        pass

class StandardLanguage(Language):
    """
    Representation of a standard western European language.
    """

    def __init__(self, language):
        """
        Initializes the language representation.

        Parameters
        ----------
        language : str
            The language to be tokenized
        """
        super().__init__(language)
        self.punctuation = [".","?",","]

    def is_punctuation(self, token):
        """
        Determines if a token is punctuation.

        Parameters
        ----------
        token : str
            The token to be tested
        
        Returns
        -------
        bool
            True if the token is punctuation, False otherwise.
        """
        return token in self.punctuation

    def separator(self):
        """
        Standard punctuation for separating a word across lines.

        Returns
        -------
        str
            The standard punctuation for line breaks
        """  
        return "-"
    
    def tokenize(self, line):
        """
        Tokenizes a line of the in the user-specified language

        Parameters
        ----------
        line : str
            The text to be tokenized
        
        Returns
        -------
        list
            A collection of tokens derived from the text
        """
        return self.tokenizer(line)
    
    def whitespace(self):
        """
        Standard character for separating two words.

        Returns
        -------
        str
            Standard blank space character
        """
        return ' '

class TokenizerMapper():
    """
    Mediator for choosing the correct tokenizer.
    """
    def __init__(self):
        """
        Initializes the mapper.
        """
        self.init_tokenizers()
    
    def init_tokenizers(self):
        """
        Initializes the tokenizers.
        """
        self.tokenizers = {}
        self.tokenizers["english"] = Tokenizer(StandardLanguage("english"))
        self.tokenizers["german"] = Tokenizer(StandardLanguage("german"))
        #Add more languages as they become available
    
    def select(self, language):
        """
        Retrieves the appropriate tokenizer for the
        user-specified language.

        Parameters
        ----------
        language : str
            The language for which to retrieve a tokenizer
        
        Returns
        -------
        Tokenizer
            A tokenizer for the user-specified language
        """
        #Search for desired tokenizer
        if language in self.tokenizers:
            tokenizer = self.tokenizers[language]
            return tokenizer
        
        #Default to English
        tokenizer = self.tokenizers["english"]
        return tokenizer