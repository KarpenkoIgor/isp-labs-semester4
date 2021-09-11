import inspect
import builtins
from additional.additional import convert, deconvert

class Toml():
    def __init__(self):
        self.pos = 0
        self.nums = [str(i) for i in range(10)]
        self.depth = 0

    def dumps(self, obj):
        r = convert(obj)
        return self.to_str(r)

    def dump(self, obj, fp):
        with open(fp, 'w+') as f:
            f.write(self.dumps(obj))

    def loads(self, s):
        self.pos = 0
        self.depth = 0
        r = self.from_str(s)
        return deconvert(r)

    def load(self, fp):
        with open(fp, 'r') as f:
            return self.loads(f.read())

    def to_str(self, obj, name='', path=''):
        if isinstance(obj, (int, float, str, bool, type(None))):
            return self.to_str_primitive(obj, name)
        if isinstance(obj, (list, tuple, set)):
            return self.to_str_collection(obj, name)
        if isinstance(obj, dict):
            return self.to_str_dict(obj, name, path)

    def to_str_primitive(self, obj, name):
        res = ''
        if  name != '':
            res += f'{name} = '        
        if obj is None:
            res += 'null'
        elif isinstance(obj, bool):
            res += 'true' if obj else 'false'
        elif isinstance(obj, (int, float)):
            res += str(obj)
        elif isinstance(obj, str):
            if name == '':
                res += f'{obj}'
            else:
                res += f'"{obj}"'
        return res

    def to_str_collection(self, obj, name):
        res = ''
        if len(name):                    
            res += f'{name} = '
        res += '[ ' + f'"__{type(obj).__name__}__", '    
        for x in obj:
            if isinstance(x, str): 
                res += ' '+ f'"{self.to_str(x)}"' + ','
            else:
                res += ' '+ self.to_str(x) + ','
        res += ']\n'
        return res

    def to_str_dict(self, obj, name, path):
        res = ''
        if len(name):
            if path == '':
                path += name
            else:
                path += '.' + name
            if res[-2:] == '\n\n':
                res += f'[{path}]\n'
            else:
                res += f'\n[{path}]\n'
            if obj == {}:
                return res 

        for k, v in obj.items():
            if res[-2:] == '\n\n' and path != '':
                res += f'[{path}]\n'
            new_res = self.to_str(v, self.to_str(str(k)), path)
            res += new_res
            if res[-1] != '\n':
                res += '\n'
        if res[-2:] != '\n\n':
            res += '\n'
        return res

    def from_str(self, s, curr_dict={}):
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
        elif s[self.pos] == '[':
            return self.from_str_collection(s)
        elif s[self.pos] == ']' or s[self.pos] =='.':
            return self.from_str_dict(s, curr_dict)
        elif self.pos == 0:
            return self.from_str_dict(s, curr_dict)
        else:
            return self.from_str_str(s)

    def from_str_str(self, s):
        res = ""
        opened = False
        while self.pos < len(s) and s[self.pos] not in ('\n', ',', ' ') or opened:
            if s[self.pos] == '"':
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

    def from_str_collection(self, s):
        res = []
        self.pos += 2
        s_type = self.from_str_str(s)
        self.pos += 1
        while self.pos < len(s) and s[self.pos] != ']':
            self.pos += 1
            v = self.from_str(s)
            res.append(v)
        self.pos += 2
        if s_type == '__tuple__':
            return tuple(res)
        elif s_type == '__set__':
            return set(res)
        return res

    def from_str_dictname(self, s):
        res = ""
        while self.pos < len(s) and s[self.pos] not in (']', '.'):
            res += s[self.pos]
            self.pos += 1    
        return res

    def from_str_dict(self, s, curr_dict):
        res = {}
        if curr_dict != {}:
            res = curr_dict        
        if s[self.pos] == ']':
            self.pos += 2        
        if s[self.pos] == '\n':
            self.depth -= 1
            return res
        if s[self.pos] == '.':
            self.pos += 1
            k = self.from_str_dictname(s)
            v = res.get(k)
            self.depth += 1
            if v is None:
                v = self.from_str(s)
            else:
                v = self.from_str_dict(s, v)
            res[k] = v
        while self.pos < len(s):   
            if s[self.pos] == '\n':
                if self.depth != 0:
                    self.depth -= 1
                    return res
                self.pos += 1
                if self.pos >= len(s):
                    return res
                if s[self.pos] == '[':
                    self.pos += 1
                    k = self.from_str_dictname(s)
                    v = res.get(k)
                    self.depth += 1
                    if v is None:
                        v = self.from_str(s)
                    else:
                        v = self.from_str_dict(s, v)
                else: 
                    continue
            else:    
                k = self.from_str_str(s)  
                if self.pos >= len(s):
                    return k
                self.pos += 2
                v = self.from_str(s) 
            res[k] = v
        return res