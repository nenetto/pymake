import unittest

class TestCommonFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_pymake_var(self):
        from pymake.utils.common_functions import get_pymake_var
        self.assertEqual(get_pymake_var('project-name'), 'pymake')

    def test_pymake_var_error(self):
        from pymake.utils.common_functions import get_pymake_var

        with self.assertRaises(SystemExit) as cm:
            get_pymake_var('non-exist')

        self.assertEqual(cm.exception.code, 1)

    def test_replace_vars(self):
        from pymake.utils.common_functions import replace_vars

        text = '{project-name} is a text with two {vars}'
        replacement = {'{project-name}': 'TEST1',
                       '{vars}': 'TEST2'}
        expected = 'TEST1 is a text with two TEST2'

        self.assertEqual(expected, replace_vars(text, replacement))

    def test_merge_dicts_replacement(self):
        from pymake.utils.common_functions import merge_dicts

        dict1 = {'test1': 'A',
                 'test2': 'AA'}

        dict2 = {'test1': 'B',
                 'test2': 'BB',
                 'testB': 'ADD'}

        dictexpected = {'test1': 'B',
                        'test2': 'BB',
                        'testB': 'ADD'}

        self.assertEqual(dictexpected, merge_dicts(dict1, dict2))
        self.assertEqual(dictexpected, merge_dicts(dict1, dict2, replacement=True))
        self.assertEqual(dictexpected, merge_dicts(dict1, dict2, True))

    def test_merge_dicts_no_replacement(self):
        from pymake.utils.common_functions import merge_dicts

        dict1 = {'test1': 'A',
                 'test2': 'AA'}

        dict2 = {'test1': 'B',
                 'test2': 'BB',
                 'testB': 'ADD'}

        dictexpected = {'test1': 'A',
                        'test2': 'AA',
                        'testB': 'ADD'}

        self.assertEqual(dictexpected, merge_dicts(dict1, dict2, replacement=False))

    def test_applymodifier(self):
        from pymake.utils.common_functions import applymodifier
        text = 'PROJECT NAME 2'
        expected = 'project_name_2'

        self.assertEqual(expected, applymodifier(text, 'lower_no_spaces'))


