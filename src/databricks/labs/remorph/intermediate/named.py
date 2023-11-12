import re

# Code ported from https://github.com/databricks/databricks-sdk-go/blob/main/openapi/code/named.go

reserved_words = [
    "break", "default", "func", "interface", "select", "case", "defer", "go",
    "map", "struct", "chan", "else", "goto", "switch", "const", "fallthrough",
    "if", "range", "type", "continue", "for", "import", "return", "var",
    "append", "bool", "byte", "iota", "len", "make", "new", "package",
]


class Named:
    def __init__(self, name: str):
        self._name = name
        self._singular_transforms = [
            self._regex_transform("(s|ss|sh|ch|x|z)es$", "\\1"),
            self._regex_transform("([bcdfghjklmnpqrstvwxz])ies$", "\\1y"),
            self._regex_transform("([a-z])s$", "\\1"),
        ]
        self._singular_exceptions = {"dbfs": "dbfs",
                                     "warehouses": "warehouse",
                                     "databricks": "databricks"}

    @property
    def name(self) -> str:
        return self._name

    def is_name_reserved(self) -> bool:
        return self.camel_name() in reserved_words

    def is_name_plural(self) -> bool:
        if not self._name:
            return False
        return self._name[-1] == 's'

    def singular(self) -> 'Named':
        if not self.is_name_plural():
            return self

        exception = self._singular_exceptions.get(self._name.lower())
        if exception:
            return Named(exception)

        for transform in self._singular_transforms:
            after = transform(self._name)
            if after != self._name:
                return Named(after)

        return self

    def pascal_name(self) -> str:
        return ''.join(word.capitalize() for word in self._split_ascii())

    def title_name(self) -> str:
        return ' '.join(self._split_ascii()).title()

    def camel_name(self) -> str:
        if self._name == "_":
            return "_"
        cc = self.pascal_name()
        return cc[0].lower() + cc[1:]

    def snake_name(self) -> str:
        if self._name == "_":
            return "_"
        return '_'.join(self._split_ascii())

    def constant_name(self) -> str:
        return self.snake_name().upper()

    def kebab_name(self) -> str:
        return '-'.join(self._split_ascii())

    def abbr_name(self) -> str:
        return ''.join(word[0] for word in self._split_ascii())

    @staticmethod
    def _regex_transform(pattern, replace):
        search = re.compile(pattern)

        def transform(src):
            return search.sub(replace, src)

        return transform

    @staticmethod
    def _search(name, cond, direction, i):
        name_len = len(name)
        incr = 1 if direction else -1
        while 0 <= i < name_len:
            if name[i].isalpha():
                return cond(name[i])
            i += incr
        return False

    def _check_cond_at_nearest_letters(self, name, cond, i):
        r = name[i]
        if r.isalpha():
            return cond(r)
        return self._search(name, cond, True, i) and self._search(name, cond, False, i)

    def _split_ascii(self):
        current = []
        name = self._name
        name_len = len(name)
        is_prev_upper = is_current_upper = is_next_lower = is_next_upper = is_not_last_char = False

        for i in range(name_len):
            r = name[i]
            if r == '$':
                continue

            is_current_upper = self._check_cond_at_nearest_letters(name, str.isupper, i)
            r = r.lower()
            is_not_last_char = i + 1 < name_len

            if is_not_last_char:
                is_next_lower = self._check_cond_at_nearest_letters(name, str.islower, i + 1)
                is_next_upper = self._check_cond_at_nearest_letters(name, str.isupper, i + 1)

            split, before, after = False, False, True

            if is_prev_upper and is_current_upper and is_next_lower and is_not_last_char:
                split, before, after = True, False, True

            if not is_current_upper and is_next_upper:
                split, before, after = True, True, False

            if not r.isalnum():
                split, before, after = True, False, False

            if before:
                current.append(r)

            if split and current:
                yield ''.join(current)
                current = []

            if after:
                current.append(r)

            is_prev_upper = is_current_upper

        if current:
            yield ''.join(current)
