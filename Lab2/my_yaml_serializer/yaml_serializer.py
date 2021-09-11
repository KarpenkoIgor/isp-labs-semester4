import inspect
import builtins
from additional.additional import convert, deconvert


class Yaml:
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

    def to_str(self, obj, name='', tab = ''):
        if isinstance(obj, (int, float, str, bool, type(None))):
            return self.to_str_primitive(obj, name, tab)
        if isinstance(obj, (list, tuple, set)):
            return self.to_str_collection(obj, name, tab)
        if isinstance(obj, dict):
            return self.to_str_dict(obj, name, tab)

    def to_str_primitive(self, obj, name, tab):
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
            res += f'{obj}'
        return res

    def to_str_collection(self, obj, name, tab):
        res = ''
        if len(name):
            res += f'{name}:\n'
        res += tab + '- '+ f"'__{type(obj).__name__}__'"+ '\n'
        for x in obj:
            if isinstance(x, str):
                res += tab + '- '+ f"'{self.to_str(x)}'" + '\n'
            else:
                res += tab + '- '+ self.to_str(x) + '\n'
        return res

    def to_str_dict(self, obj, name, tab):
        res = ''
        if len(name):
            res += f'{name}:'
            if obj == {}:
                res += ' {}\n'
                return res 
            res += '\n'
            tab += '  '
        for k, v in obj.items():
            res += tab + self.to_str(v, self.to_str(str(k)), tab)
            if res[-1] != '\n':
                res += '\n'    
        return res

    def from_str(self, s, tab=''):
        if self.pos >= len(s):
            return
        elif s[self.pos] in self.nums:
            return self.from_str_num(s)
        elif s[self.pos:self.pos+4] == 'null':
            return self.from_str_null(s)
        elif s[self.pos:self.pos+4] == 'true':
            return self.from_str_true(s)
        elif s[self.pos:self.pos+5] == 'false':
            return self.from_str_false(s)
        elif s[self.pos] == '[' or s[self.pos+len(tab)] == '-':
            return self.from_str_collection(s, tab)
        elif s[self.pos+len(tab):self.pos+len(tab)+2] == '  ' or s[self.pos] =='{':
            return self.from_str_dict(s, '  ')
        elif self.pos == 0:
            return self.from_str_dict(s, tab)
        else:
            return self.from_str_str(s)

    def from_str_str(self, s):
        res = ""
        opened = False
        while self.pos < len(s) and s[self.pos] not in(':', '\n') or opened:
            if s[self.pos] == "'":
                if opened:
                    opened = False
                else:
                    opened = True
                self.pos += 1
                continue
            res += s[self.pos]
            self.pos += 1        
        self.pos += 1
        return res

    def from_str_num(self, s):
        s_pos = self.pos
        while self.pos < len(s) and (s[self.pos] in self.nums or s[self.pos] == '.'):
            self.pos += 1
        num = s[s_pos:self.pos]
        self.pos += 1
        return float(num) if '.' in str(num) else int(num)
    
    def from_str_null(self, s):
        self.pos += 5
        return None
    
    def from_str_true(self, s):
        self.pos += 5
        return True
    
    def from_str_false(self, s):
        self.pos += 6
        return False

    def from_str_collection(self, s, tab):
        res = []
        self.pos += len(tab)
        self.pos += 2
        s_type = self.from_str_str(s)
        if tab + '-' != s[self.pos:self.pos + len(tab) + 1]:
            if s_type == '__tuple__':
                return tuple(res)
            elif s_type == '__set__':
                return set(res)
            return res
        self.pos += len(tab)
        while self.pos < len(s):
            self.pos += 2
            v = self.from_str(s)
            res.append(v)
            if tab + '-' != s[self.pos:self.pos + len(tab) + 1]:
                break
            self.pos += len(tab)
        if s_type == '__tuple__':
            return tuple(res)
        elif s_type == '__set__':
            return set(res)
        return res

    def from_str_dict(self, s, tab):
        res = {}
        if s[self.pos] == '{':
            self.pos += 3
            return res
        while self.pos < len(s):
            new_tab = ''
            while s[self.pos] == ' ':
                new_tab += ' '
                self.pos += 1
            if len(new_tab) >= len(tab):
                tab = new_tab
                k = self.from_str_str(s)
                if self.pos >= len(s):
                    return k
                if s[self.pos] == ' ':
                    self.pos += 1
                    v = self.from_str(s, new_tab)
                else:
                    self.pos += 1
                    v = self.from_str(s, new_tab)
            elif len(new_tab) < len(tab):
                self.pos -= len(new_tab)
                return res
            res[k] = v
        return res