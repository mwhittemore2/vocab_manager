from collections import deque

class Tokenizer():
    """
    Tokenizes text from a user-specified language so 
    that it will render properly in a browser.
    """
    def __init__(self, language):
        """
        Initializes the tokenizer.

        Parameters
        ----------
        language : str
            The language to be tokenized
        """
        self.language = language

    def convert(self, line):
        """
        Transforms text into corresponding tokens
        with intermediate whitespace.

        Parameters
        ----------
        line : str
            The text to be tokenized
        
        Returns
        -------
        list
            A collection of tokens
        """
        tokens = self.language.tokenize(line)
        whitespace = self.language.whitespace()
        whitespace = {"text": whitespace, "size": len(whitespace)}
        new_tokens = deque([])
        for token in tokens:
            token = {"text": token, "size": len(token)}
            new_tokens.append(token)
            if not self.language.is_punctuation(token["text"]):
                new_tokens.append(whitespace)
        return new_tokens

    def split_token(self, token, pos):
        """
        Separates a token into two at the user-specified position.

        Parameters
        ----------
        token : Token
            The token to be separated
        pos: int
            The character position at which to perform the separation
        
        Returns
        -------
        list
            A collection of the two separated tokens
        """
        text = token["text"]
        t1 = text[0:pos]
        t2 = text[pos:]
        separator = self.language.separator()
        
        tokens = []
        if "break" in token:
            t1 = {"text": t1 + separator, "size": len(t1), "break": token["break"]}
            tokens.append(t1)
            t2 = {"text": t2, "size": len(t2), "break": token["break"]}
            tokens.append(t2)
        else:
            t1 = {"text": t1 + separator, "size": len(t1), "break": text}
            tokens.append(t1)
            t2 = {"text": t2, "size": len(t2), "break": text}
            tokens.append(t2)
        
        return tokens

    def tokenize(self, line, line_size, offset=0):
        """
        Tokenizes text according to the user-specified
        line length.

        Parameters
        ----------
        line : str
            The text to be tokenized
        line_size : int
            The character position at which to insert a line break
        offset : int
            The position at which to start counting characters
        """
        tokens = self.convert(line)
        char_count = offset
        while tokens:
            token = tokens.popleft()
            if char_count + token["size"] > line_size:
                cutoff = line_size - char_count
                new_tokens = self.split_token(token, cutoff)
                tokens.appendleft(new_tokens[1])
                char_count = 0
                yield new_tokens[0]
            else:
                char_count = char_count + token["size"]
                yield token