import unittest
import json
import tempfile
import pandas as pd
import numpy as np


class TestPrettymessaging(unittest.TestCase):

    def setUp(self):
        from pymake.utils.common.prettymessaging import PrettyMessaging
        self.pm = PrettyMessaging('TEST')

    def tearDown(self):
        pass

    def test_prettymessaging_info(self):
        self.pm.print_info('INFO MESSAGE')
        self.pm.print_info('INFO MESSAGE', padding=1)

    def test_prettymessaging_info_2(self):
        self.pm.print_info_2('INFO2 MESSAGE')
        self.pm.print_info_2('INFO2 MESSAGE', padding=1)

    def test_prettymessaging_error(self):
        self.pm.print_error('ERROR MESSAGE', raise_error=None, padding=0)
        self.pm.print_error('ERROR MESSAGE', raise_error=None, padding=2)
        self.assertRaises(AttributeError, lambda: self.pm.print_error('ERROR MESSAGE',
                                                                      raise_error=AttributeError,
                                                                      padding=0))

    def test_prettymessaging_warning(self):
        self.pm.print_warning('WARNING MESSAGE')
        self.pm.print_warning('WARNING MESSAGE', padding=1)

    def test_prettymessaging_dict(self):
        test_dict = dict()
        self.pm.print_dict(test_dict)

        test_dict['k1'] = 'v1'
        test_dict['k2'] = 2
        self.pm.print_dict(test_dict)

    def test_prettymessaging_separator(self):
        self.pm.print_separator()

    def test_prettymessaging_json(self):
        test_dict = dict()
        test_dict['k1'] = 'v1'
        test_dict['k2'] = 2

        with tempfile.NamedTemporaryFile(mode='w') as fp:
            json.dump(test_dict, fp)
            fp.flush()
            self.pm.print_json(fp.name)

    def test_prettymessaging_info_percentage(self):
        self.pm.print_info_percentage(0.0, msg_pre='pre', msg_post='post', padding=0)
        self.pm.print_info_percentage(35.432, msg_pre='pre', msg_post='post', padding=1)
        self.pm.print_info_percentage(100.0, msg_pre='pre', msg_post='post', padding=2)

    def test_prettymessaging_pandas_df(self):
        df = pd.DataFrame({'A': 1.,
                           'B': pd.Timestamp('20130102'),
                           'C': pd.Series(1, index=list(range(4))),
                           'D': np.array([3] * 4, dtype='int32'),
                           'E': pd.Categorical(["test", "train", "test", "train"]),
                           'F': 'foo'})
        self.pm.print_pandas_df(df)
