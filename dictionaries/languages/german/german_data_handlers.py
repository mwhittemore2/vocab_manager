import json
import re

from collections import deque

from data_handler import DataHandler

class GermanEntryHandler():
    """
    Parses a single line of raw dictionary data
    and transforms it into dictionary entries for
    inclusion in Elasticsearch.
    """
    def __init__(self):
        """
        Initializes the handler.
        """
        self.initialize_handlers()
        self.pos_pattern = re.compile("({.*?})")
        self.pos_tags = []
        self.replace_pattern = re.compile("((\s)?{.*?})")
    
    def assign_pos_tags(self, pairs):
        """
        Assigns part-of-speech tags to German words.

        Parameters
        ----------
        pairs : list
            A list of German words and their
            English translations.
        
        Returns
        -------
        list
            A list of translation pairs with
            parts-of-speech for the German words
        """
        assigned = []
        default_pos = ["phrase"]

        for pair in pairs:
            tokens = deque()
            tagged = []
            eng = [{"phrase": p} for p in pair[1]]
            for ger in pair[0]:
                tags = self.find_pos_tags(ger)
                if tags:
                    entry = self.remove_pos_tags(ger)
                    tokens.append(entry)
                    while tokens:
                        token = tokens.popleft()
                        entry = {"phrase": token, "pos": tags}
                        tagged.append(entry)
                else:
                    tokens.append(ger)

            while tokens:
                token = tokens.popleft()
                entry = {"phrase": token, "pos": default_pos}
                tagged.append(entry)
                
            assigned.append([tagged, eng])
        
        return assigned

    def find_pos_tags(self, entry):
        """
        Finds the part-of-speech tags, if any,
        in the German raw text entry.

        Parameters
        ----------
        entry : str
            The text entry to parse
        
        Returns
        -------
        list
            The part-of-speech tags
        """
        pos_pattern = self.pos_pattern
        match = pos_pattern.search(entry)
        if not match:
            return []
        
        tags = match.group(0)
        if not tags:
            return []

        tags = tags[1:-1]
        tags = tags.split(",")

        return tags
    
    def get_translation_pairs(self, entry):
        """
        Parses a raw line of text to get
        German words and English translations.

        Parameters
        ----------
        entry : str
            raw line of dictionary text
        
        Returns
        -------
        list
            A list of German words with their
            English translations
        """
        german, english = entry.split(" :: ")
        german = german.split(" | ")
        english = english.split(" | ")
            
        pairs = []
        for pair in zip(german, english):
            ger = pair[0].split("; ")
            eng = pair[1].split("; ")
            pairs.append([ger, eng])
        
        pairs = self.assign_pos_tags(pairs)
        roots = pairs[0]
        translations = []
        
        #Get Elasticsearch entries for base terms
        for ger in roots[0]:
            translation = {}
            translation["base_form"] = ger["phrase"]
            translation["inflected_form"] = ger["phrase"]
            translation["pos"] = ger["pos"]
            translation["definitions"] = [eng["phrase"] for eng in roots[1]]
            wc = len(translation["inflected_form"].split())
            translation["word_count"] = wc
            translations.append(translation) 

        if len(pairs) < 2:
            return translations
        
        #Get Elasticsearch entries for derived terms
        for pair in pairs[1:]:
            if len(pair[0]) == len(roots[0]):
                for ger in enumerate(pair[0]):
                    translation = {}
                    translation["base_form"] = roots[0][ger[0]]["phrase"]
                    translation["inflected_form"] = ger[1]["phrase"]
                    translation["pos"] = roots[0][ger[0]]["pos"]
                    translation["definitions"] = [eng["phrase"] for eng in pair[1]]
                    wc = len(translation["inflected_form"].split())
                    translation["word_count"] = wc
                    translations.append(translation)
            else:
                for ger in pair[0]:
                    translation = {}
                    translation["base_form"] = ger["phrase"]
                    translation["inflected_form"] = ger["phrase"]
                    translation["pos"] = ger["pos"]
                    translation["definitions"] = [eng["phrase"] for eng in pair[1]]
                    wc = len(translation["inflected_form"].split())
                    translation["word_count"] = wc
                    translations.append(translation)
        
        return translations

    def initialize_handlers(self):
        """
        Initializes the handlers for
        different parts-of-speech
        """
        default = GermanDefaultHandler(None)
        pronoun = GermanPronounHandler(default)
        adjective = GermanAdjectiveHandler(pronoun)
        adverb = GermanAdverbHandler(adjective)
        noun = GermanNounHandler(adverb)
        verb = GermanVerbHandler(noun)
        self.handler = verb

    def preprocess(self, entry):
        """
        Removes unnecessary characters from raw text
        before parsing.

        Parameters
        ----------
        entry : str
            The string to be processed
        
        Returns
        -------
        str
            The text line with unnecessary characters removed
        """
        entry = entry.rstrip()
        processed = []
        parens_count = 0
        for i in range(0, len(entry)):
            if entry[i] == "(":
                parens_count +=1
            if entry[i] == ")":
                parens_count += -1
            
            if parens_count > 0:
                if entry[i] == ";":
                    processed.append(",")
                    continue

            processed.append(entry[i])

        processed = "".join(processed)
        return processed

    def process_entry(self, entry):
        """
        Parses a raw text line and converts
        it to German dictionary entries.

        Parameters
        ----------
        entry : str
            The raw text line to process
        
        Returns
        -------
        list
            A list of German dictionary entries
        """
        preprocessed = self.preprocess(entry)
        pairs = self.get_translation_pairs(preprocessed)
        pairs = self.split_by_pos(pairs)
        handler = self.handler
        data = []
        for pair in pairs:
            data += handler.process_entry(pair)
        
        data = [json.dumps(d, ensure_ascii=False) + "\n" for d in data]

        index_cmd = json.dumps({"index":{}}) + "\n"
        to_index = []
        for d in data:
            to_index.append(index_cmd)
            to_index.append(d)

        return to_index

    def remove_pos_tags(self, entry):
        """
        Removes part-of-speech tags from
        a word.

        Parameters
        ----------
        entry : str
            The string to be modified
        
        Returns
        -------
        str
            A string with part-of-speech tags removed
        """
        pattern = self.replace_pattern
        to_replace = ""
        entry = pattern.sub(to_replace, entry)
        return entry
    
    def split_by_pos(self, pairs):
        """
        Makes seperate entries for each part-of-speech
        tag associated with a German word.

        Parameters
        ----------
        pairs : list
            A list of translation pairs
        
        Returns
        -------
        list
            A list of translation pairs with a single
            part-of-speech for each entry
        """
        new_pairs = []
        for pair in pairs:
            tags = pair["pos"]
            for pos_tag in tags:
                new_pair = {}
                new_pair["pos"] = pos_tag
                new_pair["base_form"] = pair["base_form"]
                new_pair["inflected_form"] = pair["inflected_form"]
                new_pair["definitions"] = pair["definitions"]
                new_pair["word_count"] = pair["word_count"]
                new_pairs.append(new_pair)

        return new_pairs 

class GermanBaseHandler(DataHandler):
    """
    Base class for processing German
    dictionary entries
    """
    def __init__(self, next_handler):
        """
        Initializes the handler.

        Parameters
        ----------
        next_handler : DataHandler
            The next handler to try
        """
        super().__init__(next_handler)
        self.pos_tags = []
        self.initialize_tag_map()

    def get_data(self, data):
        """
        Fetches processed German dictionary entry

        Parameters
        ----------
        data : dict
            The German dictionary entry to process
        
        Returns
        -------
        dict
            A German dictionary entry with an updated
            part-of-speech
        """
        tagged = self.map_tags([data])
        return tagged

    def initialize_tag_map(self):
        """
        Initializes the mapping of part-of-speech
        tags from short to long form.
        """
        self.tag_map = {}

    def map_tags(self, entries):
        """
        Map parts-of-speech from short form
        to long form

        Parameters
        ----------
        entries : list
            A list of German dictionary entries
        
        Returns
        -------
        list
            A list of German dictionary entries with
            updated parts-of-speech
        """
        tag_map = self.tag_map
        default_pos = "phrase"
        for entry in entries:
            pos = entry["pos"]
            if pos in tag_map:
                entry["pos"] = tag_map[pos]
            else:
                entry["pos"] = default_pos

        return entries 

    def process_entry(self, entry):
        """
        Convert German dictionary entry into its final form.

        Parameters
        ----------
        entry : dict
            The dictionary entry to convert
        
        list
            The resulting dictionary entries
        """
        tag = entry["pos"]
        if tag in self.pos_tags:
            return self.get_data(entry)
        
        return self.get_handler().process_entry(entry)

class GermanAdjectiveHandler(GermanBaseHandler):
    """
    Processes German adjectives.
    """
    def initialize_tag_map(self):
        """
        Maps adjectives from short to
        long form
        """
        tag_map = {}
        tag_map["adj"] = "adjective"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map

class GermanAdverbHandler(GermanBaseHandler):
    """
    Processes German adverbs.
    """
    def initialize_tag_map(self):
        """
        Maps adverbs from short to
        long form.
        """
        tag_map = {}
        tag_map["adv"] = "adverb"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map

class GermanDefaultHandler(GermanBaseHandler):
    """
    Processes German dictionary entry when no
    other handlers apply.
    """
    def process_entry(self, entry):
        """
        Fetches the base entry.

        Parameters
        ----------
        entry : dict
            The entry to return
        
        Returns
        -------
        dict
            The dictionary entry
        """
        return [entry]

class GermanNounHandler(GermanBaseHandler):
    """
    Processes German nouns.
    """
    def initialize_tag_map(self):
        """
        Maps nouns from short form
        to long form.
        """
        tag_map = {}
        tag_map["m"] = "noun_masculine"
        tag_map["f"] = "noun_feminine"
        tag_map["n"] = "noun_neuter"
        tag_map["pl"] = "noun_plural"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map

class GermanPronounHandler(GermanBaseHandler):
    """
    Processes German pronouns.
    """
    def initialize_tag_map(self):
        """
        Maps pronouns from short form to
        long form.
        """
        tag_map = {}
        tag_map["ppron"] = "personal_pronoun_singular"
        tag_map["ppron pl"] = "personal_pronoun_plural"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map

class GermanVerbHandler(GermanBaseHandler):
    """
    Processes German verbs.
    """
    def __init__(self, next_handler):
        """
        Initializes German verb handler.

        Parameters
        ----------
        next_handler : DataHandler
            The next handler to try
        """
        super().__init__(next_handler)
        self.max_words = 2

    def get_data(self, entry):
        """
        Transforms German verb data.

        Parameters
        ----------
        entry : dict
            The entry to transform
        
        Returns
        list
            The transformed verb data
        """
        if not self.has_correct_size(entry):
            return []

        return super().get_data(entry)
    
    def has_correct_size(self, entry):
        """
        Filters out verbs that are too long.

        Parameters
        ----------
        entry : dict
            The verb to examine
        
        Returns
        -------
        bool
            True if the verb is short enough, False otherwise
        """
        wc = entry["word_count"]
        same_phrase = entry["inflected_form"] == entry["base_form"]
        if wc > self.max_words and not same_phrase:
            return False
        
        return True
            
    def initialize_tag_map(self):
        """
        Maps verbs from short form to long form.
        """
        tag_map = {}
        tag_map["vt"] = "verb_transitive"
        tag_map["vr"] = "verb_reflexive"
        tag_map["vi"] = "verb_intransitive"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map