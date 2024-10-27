import os
import sys

try:
    from tqdm.contrib import tenumerate
except ImportError:
    tenumerate = enumerate

orjson_loads = None
ujson_loads = None
rapidjson_loads = None
simplejson_loads = None
json_loads = None
try:
    from orjson import loads as orjson_loads
except ImportError:
    try:
        from ujson import loads as ujson_loads
    except ImportError:
        try:
            from rapidjson import loads as rapidjson_loads
        except ImportError:
            try:
                from simplejson import loads as simplejson_loads
            except ImportError:
                from json import loads as json_loads

def jsonload(data):
    if orjson_loads:
        return orjson_loads(data.encode())
    elif ujson_loads:
        return ujson_loads(data)
    elif rapidjson_loads:
        return rapidjson_loads(data)
    elif simplejson_loads:
        return simplejson_loads(data)
    elif json_loads:
        return json_loads(data)

def isinvalid(word):
    if len(word) > 1:
        word = word[0].lower() + word[1:]
    return not set(word) <= set("abcdefghijklmnopqrstuvwxyz-")

class WordExtractor:
    def __init__(self, filename: str, datatype: str, chunks: int):
        self.path = os.path.splitext(filename)[0]
        self.file = open(filename, 'r', encoding='utf-8')
        self.type = datatype
        self.filter_word_only = False

        self.newlines = 0
        if chunks < 1:
            self.newlines = None
            return
        while True:
            c = self.file.read(chunks)
            if not c:
                break
            self.newlines += c.count('\n')
        self.file.seek(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

    def generate_json(self):
        with open(f"{self.path}-{self.type}.json", "w", encoding='utf-8') as f:
            f.write('[')

            for elem in tenumerate(self.file, total=self.newlines):
                if self.type not in elem[1]:
                    continue

                data = jsonload(elem[1])
                if data["pos"] != self.type:
                    continue

                if self.filter_word_only and isinvalid(data['word']):
                    continue
                word = data["word"].replace('"', '\\"').lower()
                f.write(f'"{word}",')

            f.seek(f.seek(0, os.SEEK_END) - 1)
            f.write(']')

    def generate_txt(self):
        with open(f"{self.path}-{self.type}.txt", "w", encoding='utf-8') as f:
            for elem in tenumerate(self.file, total=self.newlines):
                if self.type not in elem[1]:
                    continue

                data = jsonload(elem[1])
                if data["pos"] != self.type:
                    continue

                if self.filter_word_only and isinvalid(data['word']):
                    continue
                f.write(data["word"].lower() + '\n')

def list_wordtypes(filename: str):
    types = []
    for l in open(filename, 'r', encoding='utf-8'):
        d = jsonload(l)
        if d['pos'] not in types:
            types.append(d['pos'])
    return types

if __name__ == "__main__":
    if len(sys.argv) < 3:
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            print("Listing of word types under selected file, please wait...")
            print("\t- " + "\n\t- ".join(list_wordtypes(sys.argv[1])))
            sys.exit(0)
        print(f"USAGE: {os.path.basename(__file__)} <input file> <word type> [output types]")
        print("WHERE:")
        print("\t- Input file should be in JSONL format UTF8")
        print("\t- Word type should be noun, adv, adj, verb, etc...")
        print("\t- Output type should be JSON or TXT")
        print("\t- There might be multiple output types")
        print(f"\nTIP: List word types by running {os.path.basename(__file__)} <input file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print("ERROR: Inexistant input file")
        sys.exit(1)
    datatype = sys.argv[2]

    generate_json = "json" in "".join(sys.argv[2:]).lower()
    generate_txt = "txt" in "".join(sys.argv[2:]).lower()

    print('Counting elements by chunks of 4096 characters...')
    with WordExtractor(input_file, datatype, 4096) as extractor:
        extractor.filter_word_only = True
        if generate_json:
            print("Generating JSON output...")
            extractor.generate_json()
        if generate_txt:
            print("Generating TXT output...")
            extractor.generate_txt()
