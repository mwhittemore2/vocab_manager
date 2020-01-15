import json
import re

from collections import deque

from data_handler import DataHandler

class GermanEntryHandler():
    #Break entry into translation pairs here and
    #then assign each entry to the appropriate handler
    def __init__(self):
        self.initialize_handlers()
        self.pos_pattern = re.compile("({.*?})")
        self.pos_tags = []
        self.replace_pattern = re.compile("((\s)?{.*?})")
    
    def assign_pos_tags(self, pairs):
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
        
        #Get Elastic Search entries for base terms
        for ger in roots[0]:
            translation = {}
            translation["base_form"] = ger["phrase"]
            translation["inflected_form"] = ger["phrase"]
            #translation["definitions"] = []
            translation["pos"] = ger["pos"]
            #for eng in roots[1]:
            #    translation["definitions"].append(eng["phrase"])
            translation["definitions"] = [eng["phrase"] for eng in roots[1]]
            wc = len(translation["inflected_form"].split())
            translation["word_count"] = wc
            translations.append(translation) 

        if len(pairs) < 2:
            return translations
        
        #Get Elastic Search entries for derived terms
        for pair in pairs[1:]:
            if len(pair[0]) == len(roots[0]):
                for ger in enumerate(pair[0]):
                    translation = {}
                    translation["base_form"] = roots[0][ger[0]]["phrase"]
                    translation["inflected_form"] = ger[1]["phrase"]
                    #translation["definitions"] = []
                    translation["pos"] = roots[0][ger[0]]["pos"]
                    #for eng in pair[1]:
                    #    translation["definitions"].append(eng["phrase"])
                    translation["definitions"] = [eng["phrase"] for eng in pair[1]]
                    wc = len(translation["inflected_form"].split())
                    translation["word_count"] = wc
                    translations.append(translation)
            else:
                for ger in pair[0]:
                    translation = {}
                    translation["base_form"] = ger["phrase"]
                    translation["inflected_form"] = ger["phrase"]
                    #translation["definitions"] = []
                    translation["pos"] = ger["pos"]
                    #for eng in pair[1]:
                    #    translation["definitions"].append(eng["phrase"])
                    translation["definitions"] = [eng["phrase"] for eng in pair[1]]
                    wc = len(translation["inflected_form"].split())
                    translation["word_count"] = wc
                    translations.append(translation)
        
        return translations

    def initialize_handlers(self):
        default = GermanDefaultHandler(None)
        pronoun = GermanPronounHandler(default)
        adjective = GermanAdjectiveHandler(pronoun)
        adverb = GermanAdverbHandler(adjective)
        noun = GermanNounHandler(adverb)
        verb = GermanVerbHandler(noun)
        self.handler = verb

    def preprocess(self, entry):
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
        pattern = self.replace_pattern
        to_replace = ""
        entry = pattern.sub(to_replace, entry)
        return entry
    
    def split_by_pos(self, pairs):
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
    def __init__(self, next_handler):
        super().__init__(next_handler)
        self.pos_tags = []
        self.initialize_tag_map()

    def get_data(self, data):
        tagged = self.map_tags([data])
        return tagged

    def initialize_tag_map(self):
        self.tag_map = {}

    def map_tags(self, entries):
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
        tag = entry["pos"]
        if tag in self.pos_tags:
            return self.get_data(entry)
        
        return self.get_handler().process_entry(entry)

class GermanAdjectiveHandler(GermanBaseHandler):
    def initialize_tag_map(self):
        tag_map = {}
        tag_map["adj"] = "adjective"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map

class GermanAdverbHandler(GermanBaseHandler):
    def initialize_tag_map(self):
        tag_map = {}
        tag_map["adv"] = "adverb"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map

class GermanDefaultHandler(GermanBaseHandler):
    def process_entry(self, entry):
        return [entry]

class GermanNounHandler(GermanBaseHandler):
    def initialize_tag_map(self):
        tag_map = {}
        tag_map["m"] = "noun_masculine"
        tag_map["f"] = "noun_feminine"
        tag_map["n"] = "noun_neuter"
        tag_map["pl"] = "noun_plural"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map

class GermanPronounHandler(GermanBaseHandler):
    def initialize_tag_map(self):
        tag_map = {}
        tag_map["ppron"] = "personal_pronoun_singular"
        tag_map["ppron pl"] = "personal_pronoun_plural"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map

class GermanVerbHandler(GermanBaseHandler):
    def __init__(self, next_handler):
        super().__init__(next_handler)
        self.max_words = 2

    def get_data(self, entry):
            if not self.has_correct_size(entry):
                return []

            return super().get_data(entry)
    
    def has_correct_size(self, entry):
        #words = entry["inflected_form"].split()
        #wc = len(words)
        wc = entry["word_count"]
        same_phrase = entry["inflected_form"] == entry["base_form"]
        if wc > self.max_words and not same_phrase:
            return False
        
        return True
            
    def initialize_tag_map(self):
        tag_map = {}
        tag_map["vt"] = "verb_transitive"
        tag_map["vr"] = "verb_reflexive"
        tag_map["vi"] = "verb_intransitive"
        self.pos_tags = tag_map.keys()
        self.tag_map = tag_map