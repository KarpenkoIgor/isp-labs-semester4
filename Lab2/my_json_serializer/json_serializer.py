import inspect
import builtins
from additional.additional import convert, deconvert


class Json:
    def __init__(self):
        self.pos = 0
        self.nums = [str(i) for i in range(10)]

    def dumps(self, obj):
        return self.to_str(convert(obj))

    def dump(self, obj, fp):
        with open(fp, 'w+') as f:
            f.write(self.dumps(obj))

    def loads(self, s):
        self.pos = 0
        return deconvert(self.from_str(s))

    def load(self, fp):
        with open(fp, 'r') as f:
            return self.loads(f.read())

    def to_str(self, obj, name=''):
        if isinstance(obj, (int, float, str, bool, type(None))):
            return self.to_str_primitive(obj, name)
        if isinstance(obj, (list, tuple, set)):
            return self.to_str_collection(obj, name)
        if isinstance(obj, dict):
            return self.to_str_dict(obj, name)
        return self.to_str_class_obj(obj, name)

    def to_str_primitive(self, obj, name):
        res = ''
        if  name != '':
            res += f'{name}: '        
        if obj is None:
            res += 'null'
        elif isinstance(obj, bool):
            res += 'true' if obj else 'false'
        elif isinstance(obj, (int, float)):
            res += str(obj)
        elif isinstance(obj, str):
            res += f'"{obj}"'
        return res

    def to_str_collection(self, obj, name):
        res = ''
        if len(name):
            res += f'{name}: '
        res += '[' + f'"__{type(obj).__name__}__", '
        for x in obj:
            res += self.to_str(x) + ', '
        if len(res) > 2 and res[-2] == ',':
            res = res[:-2]
        res += ']'
        return res

    def to_str_dict(self, obj, name):
        res = ''
        if len(name):
            res += f'{name}: '
        res += '{'
        for k, v in obj.items():
            res += self.to_str(v, self.to_str(str(k))) + ', '        
        if len(res) > 2 and res[-2] == ',':
            res = res[:-2]
            self.pos -= 2
        res += '}'
        self.pos += 2
        return res

    def from_str(self, s):
        if self.pos >= len(s):
            return
        if s[self.pos] in self.nums:
            return self.from_str_num(s)
        elif s[self.pos:self.pos+4] == 'null':
            return self.from_str_null(s)
        elif s[self.pos:self.pos+4] == 'true':
            return self.from_str_true(s)
        elif s[self.pos:self.pos+5] == 'false':
            return self.from_str_false(s)
        if s[self.pos] == '"':
            return self.from_str_str(s)
        if s[self.pos] == '[':
            return self.from_str_collection(s)
        if s[self.pos] == '{':
            return self.from_str_dict(s)

    def from_str_str(self, s):
        res = ""
        self.pos += 1
        if s[self.pos] == '"':
            self.pos += 1
        while self.pos < len(s) and s[self.pos] not in ('"', "'"):
            res += s[self.pos]
            self.pos += 1        
        self.pos += 1
        return res

    def from_str_num(self, s):
        s_pos = self.pos
        while self.pos < len(s) and (s[self.pos] in self.nums or s[self.pos] == '.'):
            self.pos += 1
        num = s[s_pos:self.pos]

        return float(num) if '.' in str(num) else int(num)
    
    def from_str_null(self, s):
        self.pos += 4
        return None
    
    def from_str_true(self, s):
        self.pos += 4
        return True
    
    def from_str_false(self, s):
        self.pos += 5
        return False

    def from_str_collection(self, s):
        res = []
        self.pos += 1
        s_type = self.from_str_str(s)
        while self.pos < len(s) and s[self.pos] not in (']', '}', ')'):
            if s[self.pos] == ' ' or s[self.pos] == ',':
                self.pos += 1
                continue
            v = self.from_str(s)
            res.append(v)
            if self.pos < len(s) and s[self.pos] in (']', '}', ')'):
                break
            self.pos += 1
        self.pos += 1
        if s_type == '__tuple__':
            return tuple(res)
        elif s_type == '__set__':
            return set(res)
        return res

    def from_str_dict(self, s):
        res = {}
        self.pos += 1
        while self.pos < len(s) and s[self.pos] != '}':
            while s[self.pos] in (' ', ','):
                self.pos += 1
                continue            
            k = self.from_str_str(s)
            self.pos = s.find(':', self.pos)+2
            v = self.from_str(s)
            res[k] = v
        self.pos += 1
        return res