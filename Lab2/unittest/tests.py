import unittest
from factory.factory import Factory
import test_source


class SerializeTester(unittest.TestCase):
#---------JSON---------
    def test_json_int(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.int_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)
        
    def test_json_float(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.float_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_str(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.str_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_boolean(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.boolean_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_none(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.none_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_list(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.list_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_tuple(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.tuple_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_set(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.set_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_json_dict(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.dict_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj['Name'], new_obj['Name'])

    def test_json_lambda(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_json_simple_func(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.simple_func
        self.s.dump(old_obj, 'test.json')
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_json_cmplx_func(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.cmplx_func
        old_obj_2 = test_source.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        new_obj_2 = self.s.loads(self.s.dumps(old_obj_2))
        self.assertEqual(old_obj(4), new_obj(4))
        self.assertEqual(old_obj_2(4), new_obj_2(4))

    def test_json_simple_class_obj(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.SimpleClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.say_kuku(), new_obj.say_kuku(new_obj))
        self.assertEqual(old_obj.word, new_obj.word)

    def test_json_cmplx_class_obj(self):
        self.s = Factory.create_serializer('.json')
        old_obj = test_source.ComplexClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.simple_class.word, new_obj.simple_class.word)
        self.assertEqual(old_obj.func_with_glob(), new_obj.func_with_glob(new_obj))
        self.assertEqual(old_obj.const, new_obj.const)
        self.assertEqual(old_obj.simple_class.say_kuku(), new_obj.simple_class.say_kuku(new_obj.simple_class))

#---------YAML---------
    def test_yaml_int(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.int_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_float(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.float_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_str(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.str_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_boolean(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.boolean_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_none(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.none_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_list(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.list_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_tuple(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.tuple_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_set(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.set_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_lambda(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_yaml_simple_func(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.simple_func
        self.s.dump(old_obj, 'test.yaml')
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_yaml_cmplx_func(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.cmplx_func
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_yaml_simple_class_obj(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.SimpleClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.say_kuku(), new_obj.say_kuku(new_obj))
        self.assertEqual(old_obj.word, new_obj.word)

    def test_yaml_dict(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.dict_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_yaml_cmplx_class_obj(self):
        self.s = Factory.create_serializer('.yaml')
        old_obj = test_source.ComplexClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.simple_class.word, new_obj.simple_class.word)
        self.assertEqual(old_obj.func_with_glob(), new_obj.func_with_glob(new_obj))
        self.assertEqual(old_obj.const, new_obj.const)
        self.assertEqual(old_obj.simple_class.say_kuku(), new_obj.simple_class.say_kuku(new_obj.simple_class))
    
#---------TOML---------
    def test_toml_int(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.int_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_float(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.float_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_str(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.str_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_boolean(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.boolean_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_none(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.none_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_list(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.list_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_tuple(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.tuple_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_set(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.set_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_toml_dict(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.dict_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj['Name'], new_obj['Name'])

    def test_toml_lambda(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_toml_simple_func(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.simple_func
        self.s.dump(old_obj, 'test.toml')
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_toml_cmplx_func(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.cmplx_func
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_toml_simple_class_obj(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.SimpleClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.say_kuku(), new_obj.say_kuku(new_obj))
        self.assertEqual(old_obj.word, new_obj.word)

    def test_toml_cmplx_class_obj(self):
        self.s = Factory.create_serializer('.toml')
        old_obj = test_source.ComplexClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.simple_class.word, new_obj.simple_class.word)
        self.assertEqual(old_obj.func_with_glob(), new_obj.func_with_glob(new_obj))
        self.assertEqual(old_obj.const, new_obj.const)
        self.assertEqual(old_obj.simple_class.say_kuku(), new_obj.simple_class.say_kuku(new_obj.simple_class))

#---------PICKLE---------
    def test_pickle_int(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.int_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_float(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.float_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_str(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.str_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_boolean(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.boolean_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_none(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.none_glob
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_list(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.list_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_tuple(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.tuple_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_set(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.set_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)
        
    def test_pickle_dict(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.dict_1
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj, new_obj)

    def test_pickle_lambda(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.simple_lambda
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(5), new_obj(5))

    def test_pickle_cmplx_func(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.cmplx_func
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj(4), new_obj(4))

    def test_pickle_simple_class_obj(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.SimpleClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.say_kuku(), new_obj.say_kuku(new_obj))
        self.assertEqual(old_obj.word, new_obj.word)

    def test_pickle_cmplx_class_obj(self):
        self.s = Factory.create_serializer('.pickle')
        old_obj = test_source.ComplexClass()
        new_obj = self.s.loads(self.s.dumps(old_obj))
        self.assertEqual(old_obj.simple_class.word, new_obj.simple_class.word)
        self.assertEqual(old_obj.func_with_glob(), new_obj.func_with_glob(new_obj))
        self.assertEqual(old_obj.const, new_obj.const)
        self.assertEqual(old_obj.simple_class.say_kuku(), new_obj.simple_class.say_kuku(new_obj.simple_class))

if __name__ == '__main__':
    unittest.main()