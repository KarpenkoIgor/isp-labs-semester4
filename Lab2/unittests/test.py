import unittest
import Examples


class TestFunction(unittest.TestCase):

    def test_json_diff_str(self):
        dumped = Examples.json_seria.dumps(Examples.difference)
        loaded = Examples.json_seria.loads(dumped)
        self.assertEqual(loaded(3, 45), Examples.difference(3, 45))
        self.assertEqual(loaded(14.2, 33.5), Examples.difference(14.2, 33.5))
        self.assertNotEqual(loaded(30, 4), Examples.difference(31, 25))
        self.assertRaises(TypeError, lambda: loaded("json", "error"))

    def test_json_diff_file(self):
        Examples.json_seria.dump(Examples.difference)
        loaded = Examples.json_seria.load()
        self.assertEqual(loaded(3, -5), Examples.difference(3, -5))
        self.assertEqual(loaded(12.1, 2.6), Examples.difference(12.1, 2.6))
        self.assertNotEqual(loaded(10, 8), Examples.difference(1, 5))
        self.assertRaises(TypeError, lambda: loaded("json", "error"))

    def test_pickle_diff_str(self):
        dumped = Examples.pickle_seria.dumps(Examples.difference)
        loaded = Examples.pickle_seria.loads(dumped)
        self.assertEqual(loaded(2, 8), Examples.difference(2, 8))
        self.assertEqual(loaded(17.2, 13.5), Examples.difference(17.2, 13.5))
        self.assertNotEqual(loaded(10, 8), Examples.difference(1, 5))
        self.assertRaises(TypeError, lambda: loaded("pickle", "error"))

    def test_pickle_diff_file(self):
        Examples.pickle_seria.dump(Examples.difference)
        loaded = Examples.pickle_seria.load()
        self.assertEqual(loaded(16, -5), Examples.difference(16, -5))
        self.assertEqual(loaded(11, 2.6), Examples.difference(11, 2.6))
        self.assertNotEqual(loaded(10, 8), Examples.difference(1, 5))
        self.assertRaises(TypeError, lambda: loaded("pickle", "error"))

    def test_toml_diff_str(self):
        dumped = Examples.toml_seria.dumps(Examples.difference)
        loaded = Examples.toml_seria.loads(dumped)
        self.assertEqual(loaded(2, 8), Examples.difference(2, 8))
        self.assertEqual(loaded(1.2, 13.5), Examples.difference(1.2, 13.5))
        self.assertNotEqual(loaded(1, 8), Examples.difference(71, 5))
        self.assertRaises(TypeError, lambda: loaded("toml", "error"))

    def test_toml_diff_file(self):
        Examples.toml_seria.dump(Examples.difference)
        loaded = Examples.toml_seria.load()
        self.assertEqual(loaded(-12, 11), Examples.difference(-12, 11))
        self.assertEqual(loaded(1.2, 6.6), Examples.difference(1.2, 6.6))
        self.assertNotEqual(loaded(1, 8), Examples.difference(1, 0))
        self.assertRaises(TypeError, lambda: loaded("toml", "error"))

    def test_yaml_diff_str(self):
        dumped = Examples.yaml_seria.dumps(Examples.difference)
        loaded = Examples.yaml_seria.loads(dumped)
        self.assertEqual(loaded(2, 8), Examples.difference(2, 8))
        self.assertEqual(loaded(13.2, 13), Examples.difference(13.2, 13))
        self.assertNotEqual(loaded(10, 8), Examples.difference(1.6, 5))
        self.assertRaises(TypeError, lambda: loaded("yaml", "error"))

    def test_yaml_diff_file(self):
        Examples.yaml_seria.dump(Examples.difference)
        loaded = Examples.yaml_seria.load()
        self.assertEqual(loaded(16, -5), Examples.difference(16, -5))
        self.assertEqual(loaded(11, 2.6), Examples.difference(11, 2.6))
        self.assertNotEqual(loaded(10, 8), Examples.difference(1, 5))
        self.assertRaises(TypeError, lambda: loaded("yaml", "error"))


class TestLambda(unittest.TestCase):

    def test_json_composite_str(self):
        dumped = Examples.json_seria.dumps(Examples.composite)
        loaded = Examples.json_seria.loads(dumped)
        self.assertEqual(loaded(2), Examples.composite(2))
        self.assertEqual(loaded([1, 2, "check"]), Examples.composite([1, 2, "check"]))
        self.assertNotEqual(loaded(3), Examples.composite(1))
        self.assertEqual(loaded("yes"), "yesyesyesyes")

    def test_json_composite_file(self):
        Examples.json_seria.dump(Examples.composite)
        loaded = Examples.json_seria.load()
        self.assertEqual(loaded(2), Examples.composite(2))
        self.assertEqual(loaded([1, 2, "check"]), Examples.composite([1, 2, "check"]))
        self.assertNotEqual(loaded(3), Examples.composite(1))
        self.assertEqual(loaded("yes"), "yesyesyesyes")

    def test_pickle_composite_str(self):
        dumped = Examples.json_seria.dumps(Examples.composite)
        loaded = Examples.json_seria.loads(dumped)
        self.assertEqual(loaded(2), Examples.composite(2))
        self.assertEqual(loaded([1, 2, "check"]), Examples.composite([1, 2, "check"]))
        self.assertNotEqual(loaded(3), Examples.composite(1))
        self.assertEqual(loaded("yes"), "yesyesyesyes")

    def test_pickle_composite_file(self):
        Examples.json_seria.dump(Examples.composite)
        loaded = Examples.json_seria.load()
        self.assertEqual(loaded(2), Examples.composite(2))
        self.assertEqual(loaded([1, 2, "check"]), Examples.composite([1, 2, "check"]))
        self.assertNotEqual(loaded(3), Examples.composite(1))
        self.assertEqual(loaded("yes"), Examples.composite("yes"))

    def test_toml_composite_str(self):
        dumped = Examples.json_seria.dumps(Examples.composite)
        loaded = Examples.json_seria.loads(dumped)
        self.assertEqual(loaded(2), Examples.composite(2))
        self.assertEqual(loaded(17.2), Examples.composite(17.2))
        self.assertNotEqual(loaded(3), Examples.composite(1))
        self.assertEqual(loaded("str"), Examples.composite("str"))

    def test_toml_composite_file(self):
        Examples.json_seria.dump(Examples.composite)
        loaded = Examples.json_seria.load()
        self.assertEqual(loaded(2), Examples.composite(2))
        self.assertEqual(loaded([1, 2, "check"]), Examples.composite([1, 2, "check"]))
        self.assertNotEqual(loaded(3), Examples.composite(1))
        self.assertEqual(loaded("val"), Examples.composite("val"))

    def test_yaml_composite_str(self):
        dumped = Examples.json_seria.dumps(Examples.composite)
        loaded = Examples.json_seria.loads(dumped)
        self.assertEqual(loaded(2), Examples.composite(2))
        self.assertEqual(loaded([1, 2, "check"]), Examples.composite([1, 2, "check"]))
        self.assertNotEqual(loaded(3), Examples.composite(1))
        self.assertEqual(loaded("c"), Examples.composite("c"))

    def test_yaml_composite_file(self):
        Examples.json_seria.dump(Examples.composite)
        loaded = Examples.json_seria.load()
        self.assertEqual(loaded(2), Examples.composite(2))
        self.assertEqual(loaded([1, 2, "check"]), Examples.composite([1, 2, "check"]))
        self.assertNotEqual(loaded(3), Examples.composite(1))
        self.assertEqual(loaded("1"), Examples.composite("1"))


class TestObject(unittest.TestCase):

    def test_json_person_str(self):
        dumped = Examples.json_seria.dumps(Examples.person)
        loaded = Examples.json_seria.loads(dumped)
        self.assertEqual(loaded.base(loaded), Examples.person.base())
        self.assertEqual(loaded.coefficient, Examples.person.coefficient)
        self.assertEqual(loaded.name, Examples.person.name)
        self.assertEqual(loaded.samples, Examples.person.samples)

    def test_json_person_file(self):
        Examples.json_seria.dump(Examples.person)
        loaded = Examples.json_seria.load()
        self.assertEqual(loaded.base(loaded), Examples.person.base())
        self.assertEqual(loaded.coefficient, Examples.person.coefficient)
        self.assertEqual(loaded.name, Examples.person.name)
        self.assertEqual(loaded.samples, Examples.person.samples)

    def test_pickle_person_str(self):
        dumped = Examples.pickle_seria.dumps(Examples.person)
        loaded = Examples.pickle_seria.loads(dumped)
        self.assertEqual(loaded.base(), Examples.person.base())
        self.assertEqual(loaded.coefficient, Examples.person.coefficient)
        self.assertEqual(loaded.name, Examples.person.name)
        self.assertEqual(loaded.samples, Examples.person.samples)

    def test_pickle_person_file(self):
        Examples.pickle_seria.dump(Examples.person)
        loaded = Examples.pickle_seria.load()
        self.assertEqual(loaded.base(), Examples.person.base())
        self.assertEqual(loaded.coefficient, Examples.person.coefficient)
        self.assertEqual(loaded.name, Examples.person.name)
        self.assertEqual(loaded.samples, Examples.person.samples)

    def test_toml_person_str(self):
        dumped = Examples.toml_seria.dumps(Examples.person)
        loaded = Examples.toml_seria.loads(dumped)
        self.assertEqual(loaded.base(loaded), Examples.person.base())
        self.assertEqual(loaded.coefficient, Examples.person.coefficient)
        self.assertEqual(loaded.name, Examples.person.name)
        self.assertEqual(loaded.samples, Examples.person.samples)

    def test_toml_person_file(self):
        Examples.toml_seria.dump(Examples.person)
        loaded = Examples.toml_seria.load()
        self.assertEqual(loaded.base(loaded), Examples.person.base())
        self.assertEqual(loaded.coefficient, Examples.person.coefficient)
        self.assertEqual(loaded.name, Examples.person.name)
        self.assertEqual(loaded.samples, Examples.person.samples)

    def test_yaml_person_str(self):
        dumped = Examples.yaml_seria.dumps(Examples.person)
        loaded = Examples.yaml_seria.loads(dumped)
        self.assertEqual(loaded.base(loaded), Examples.person.base())
        self.assertEqual(loaded.coefficient, Examples.person.coefficient)
        self.assertEqual(loaded.name, Examples.person.name)
        self.assertEqual(loaded.samples, Examples.person.samples)

    def test_yaml_person_file(self):
        Examples.yaml_seria.dump(Examples.person)
        loaded = Examples.yaml_seria.load()
        self.assertEqual(loaded.base(loaded), Examples.person.base())
        self.assertEqual(loaded.coefficient, Examples.person.coefficient)
        self.assertEqual(loaded.name, Examples.person.name)
        self.assertEqual(loaded.samples, Examples.person.samples)


class TestClass(unittest.TestCase):

    def test_json_scholarship_str(self):
        dumped = Examples.json_seria.dumps(Examples.Scholarship)
        loaded = Examples.json_seria.loads(dumped)
        parsed_obj = loaded("Anton")
        fig_obj = Examples.Scholarship("Lesha")
        self.assertEqual(parsed_obj.base(), fig_obj.base())
        self.assertEqual(parsed_obj.coefficient, fig_obj.coefficient)
        parsed_obj.coefficient = 1.6
        fig_obj.coefficient = 1.6
        self.assertEqual(parsed_obj.base(), fig_obj.base())

    def test_json_scholarship_file(self):
        Examples.json_seria.dump(Examples.Scholarship)
        loaded = Examples.json_seria.load()
        parsed_obj = loaded("Anton")
        fig_obj = Examples.Scholarship("Lesha")
        self.assertEqual(parsed_obj.base(), fig_obj.base())
        self.assertEqual(parsed_obj.coefficient, fig_obj.coefficient)
        parsed_obj.coefficient = 1.6
        fig_obj.coefficient = 1.6
        self.assertEqual(parsed_obj.base(), fig_obj.base())

    def test_pickle_scholarship_str(self):
        dumped = Examples.pickle_seria.dumps(Examples.Scholarship)
        loaded = Examples.pickle_seria.loads(dumped)
        parsed_obj = loaded("Anton")
        fig_obj = Examples.Scholarship("Lesha")
        self.assertEqual(parsed_obj.base(), fig_obj.base())
        self.assertEqual(parsed_obj.coefficient, fig_obj.coefficient)
        parsed_obj.coefficient = 1.6
        fig_obj.coefficient = 1.6
        self.assertEqual(parsed_obj.base(), fig_obj.base())

    def test_pickle_scholarship_file(self):
        Examples.pickle_seria.dump(Examples.Scholarship)
        loaded = Examples.pickle_seria.load()
        parsed_obj = loaded("Anton")
        fig_obj = Examples.Scholarship("Lesha")
        self.assertEqual(parsed_obj.base(), fig_obj.base())
        self.assertEqual(parsed_obj.coefficient, fig_obj.coefficient)
        parsed_obj.coefficient = 1.6
        fig_obj.coefficient = 1.6
        self.assertEqual(parsed_obj.base(), fig_obj.base())

    def test_toml_scholarship_str(self):
        dumped = Examples.toml_seria.dumps(Examples.Scholarship)
        loaded = Examples.toml_seria.loads(dumped)
        parsed_obj = loaded("Anton")
        fig_obj = Examples.Scholarship("Lesha")
        self.assertEqual(parsed_obj.base(), fig_obj.base())
        self.assertEqual(parsed_obj.coefficient, fig_obj.coefficient)
        parsed_obj.coefficient = 1.6
        fig_obj.coefficient = 1.6
        self.assertEqual(parsed_obj.base(), fig_obj.base())

    def test_toml_scholarship_file(self):
        Examples.toml_seria.dump(Examples.Scholarship)
        loaded = Examples.toml_seria.load()
        parsed_obj = loaded("Anton")
        fig_obj = Examples.Scholarship("Lesha")
        self.assertEqual(parsed_obj.base(), fig_obj.base())
        self.assertEqual(parsed_obj.coefficient, fig_obj.coefficient)
        parsed_obj.coefficient = 1.6
        fig_obj.coefficient = 1.6
        self.assertEqual(parsed_obj.base(), fig_obj.base())

    def test_yaml_scholarship_str(self):
        dumped = Examples.yaml_seria.dumps(Examples.Scholarship)
        loaded = Examples.yaml_seria.loads(dumped)
        parsed_obj = loaded("Anton")
        fig_obj = Examples.Scholarship("Lesha")
        self.assertEqual(parsed_obj.base(), fig_obj.base())
        self.assertEqual(parsed_obj.coefficient, fig_obj.coefficient)
        parsed_obj.coefficient = 1.6
        fig_obj.coefficient = 1.6
        self.assertEqual(parsed_obj.base(), fig_obj.base())

    def test_yaml_scholarship_file(self):
        Examples.yaml_seria.dump(Examples.Scholarship)
        loaded = Examples.yaml_seria.load()
        parsed_obj = loaded("Anton")
        fig_obj = Examples.Scholarship("Lesha")
        self.assertEqual(parsed_obj.base(), fig_obj.base())
        self.assertEqual(parsed_obj.coefficient, fig_obj.coefficient)
        parsed_obj.coefficient = 1.6
        fig_obj.coefficient = 1.6
        self.assertEqual(parsed_obj.base(), fig_obj.base())


class TestHardFunction(unittest.TestCase):

    def test_json_calc_str(self):
        dumped = Examples.json_seria.dumps(Examples.calculate)
        loaded = Examples.json_seria.loads(dumped)
        self.assertEqual(loaded(1.2), Examples.calculate(1.2))
        self.assertEqual(loaded(0.2), Examples.calculate(0.2))
        self.assertRaises(TypeError, lambda: loaded("1.2"))

    def test_json_calc_file(self):
        Examples.json_seria.dump(Examples.calculate)
        loaded = Examples.json_seria.load()
        self.assertEqual(loaded(1.2), Examples.calculate(1.2))
        self.assertEqual(loaded(0.2), Examples.calculate(0.2))
        self.assertRaises(TypeError, lambda: loaded("1.2"))

    def test_pickle_calc_str(self):
        dumped = Examples.pickle_seria.dumps(Examples.calculate)
        loaded = Examples.pickle_seria.loads(dumped)
        self.assertEqual(loaded(1.2), Examples.calculate(1.2))
        self.assertEqual(loaded(0.2), Examples.calculate(0.2))
        self.assertRaises(TypeError, lambda: loaded("1.2"))

    def test_pickle_calc_file(self):
        Examples.pickle_seria.dump(Examples.calculate)
        loaded = Examples.pickle_seria.load()
        self.assertEqual(loaded(1.2), Examples.calculate(1.2))
        self.assertEqual(loaded(0.2), Examples.calculate(0.2))
        self.assertRaises(TypeError, lambda: loaded("1.2"))

    def test_toml_calc_str(self):
        dumped = Examples.toml_seria.dumps(Examples.calculate)
        loaded = Examples.toml_seria.loads(dumped)
        self.assertEqual(loaded(1.2), Examples.calculate(1.2))
        self.assertEqual(loaded(0.2), Examples.calculate(0.2))
        self.assertRaises(TypeError, lambda: loaded("1.2"))

    def test_toml_calc_file(self):
        Examples.toml_seria.dump(Examples.calculate)
        loaded = Examples.toml_seria.load()
        self.assertEqual(loaded(1.2), Examples.calculate(1.2))
        self.assertEqual(loaded(0.2), Examples.calculate(0.2))
        self.assertRaises(TypeError, lambda: loaded("1.2"))

    def test_yaml_calc_str(self):
        dumped = Examples.yaml_seria.dumps(Examples.calculate)
        loaded = Examples.yaml_seria.loads(dumped)
        self.assertEqual(loaded(1.2), Examples.calculate(1.2))
        self.assertEqual(loaded(0.2), Examples.calculate(0.2))
        self.assertRaises(TypeError, lambda: loaded("1.2"))

    def test_yaml_calc_file(self):
        Examples.yaml_seria.dump(Examples.calculate)
        loaded = Examples.yaml_seria.load()
        self.assertEqual(loaded(1.2), Examples.calculate(1.2))
        self.assertEqual(loaded(0.2), Examples.calculate(0.2))
        self.assertRaises(TypeError, lambda: loaded("1.2"))
