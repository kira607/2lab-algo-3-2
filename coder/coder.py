from collections import Counter

from .tree import ShanonFanoTree


class ShanonFanoCoder:
    def __init__(self):
        self.string = None

        self.tree = None
        self.codes_table = None

        self.code_sep = None
        self.code = None

        self.string_size = None
        self.code_size = None
        self.wrapping_coefficient = None

    def encode(self, string: str):
        counter_table = Counter(string)

        self.string = string

        self.tree = ShanonFanoTree.from_counter_table(counter_table)
        self.codes_table = self.tree.get_codes_table()

        self.code_sep = tuple(self.codes_table[c] for c in string)
        self.code = ''.join(self.code_sep)

        self._count_sizes()
        return self

    def decode(self, code, decoder):
        self._load_decoder(decoder)
        self._load_code(code)

        inv_table = dict((v, k) for k, v in self.codes_table.items())

        self.string = ''.join(inv_table[i] for i in self.code_sep)

        self._count_sizes()
        return self

    def _load_decoder(self, decoder):
        if isinstance(decoder, dict):
            self.tree = ShanonFanoTree.from_codes_table(decoder)
            self.codes_table = decoder
        elif isinstance(decoder, ShanonFanoTree):
            self.tree = decoder
            self.codes_table = decoder.get_codes_table()
    
    def _load_code(self, code):
        if isinstance(code, str):
            self.code_sep = self.tree.separate(code)
            self.code = code
        elif isinstance(code, list):
            self.code_sep == code
            self.code = ''.join(self.code_sep)

    def _count_sizes(self):
        self.string_size = len(self.string) * 8
        self.code_size = len(self.code)
        self.wrapping_coefficient = self.string_size / self.code_size
