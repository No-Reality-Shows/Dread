# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 19:21:15 2022

@author: No-Reality-Shows
"""

import Dread.functions

##############################################################################
#general config
##############################################################################

#directory for build configuration files
BUILD_DIRECTORY = ""

##############################################################################
#logger config
##############################################################################

LOGGER_LEVEL = 'INFO'
LOGGER_PROPAGATE = False


##############################################################################
#action dictionary - this is a dictionary of functions and parameters
#linked to specific actions within the rule engine
##############################################################################

ACTION_CONFIG = {'get_time':{'action_function':Dread.functions.get_current_utc_time,
                             'params':'{}'}}

##############################################################################
#evaluation config
##############################################################################

EXTERNAL_MODULES = ['math','re','datetime','Dread']

ALLOWED_BUILTINS = {'ArithmeticError': ArithmeticError,
  'AssertionError': AssertionError,
  'AttributeError': AttributeError,
  'BaseException': BaseException,
  'BlockingIOError': BlockingIOError,
  'BrokenPipeError': BrokenPipeError,
  'BufferError': BufferError,
  'BytesWarning': BytesWarning,
  'ChildProcessError': ChildProcessError,
  'ConnectionAbortedError': ConnectionAbortedError,
  'ConnectionError': ConnectionError,
  'ConnectionRefusedError': ConnectionRefusedError,
  'ConnectionResetError': ConnectionResetError,
  'DeprecationWarning': DeprecationWarning,
  'EOFError': EOFError,
  'Ellipsis': Ellipsis,
  'EnvironmentError': EnvironmentError,
  'Exception': Exception,
  'False': False,
  'FileExistsError': FileExistsError,
  'FileNotFoundError': FileNotFoundError,
  'FloatingPointError': FloatingPointError,
  'FutureWarning': FutureWarning,
  'GeneratorExit': GeneratorExit,
  'IOError': IOError,
  'ImportError': ImportError,
  'ImportWarning': ImportWarning,
  'IndentationError': IndentationError,
  'IndexError': IndexError,
  'InterruptedError': InterruptedError,
  'IsADirectoryError': IsADirectoryError,
  'KeyError': KeyError,
  'KeyboardInterrupt': KeyboardInterrupt,
  'LookupError': LookupError,
  'MemoryError': MemoryError,
  'ModuleNotFoundError': ModuleNotFoundError,
  'NameError': NameError,
  'None': None,
  'NotADirectoryError': NotADirectoryError,
  'NotImplemented': NotImplemented,
  'NotImplementedError': NotImplementedError,
  'OSError': OSError,
  'OverflowError': OverflowError,
  'PendingDeprecationWarning': PendingDeprecationWarning,
  'PermissionError': PermissionError,
  'ProcessLookupError': ProcessLookupError,
  'RecursionError': RecursionError,
  'ReferenceError': ReferenceError,
  'ResourceWarning': ResourceWarning,
  'RuntimeError': RuntimeError,
  'RuntimeWarning': RuntimeWarning,
  'StopAsyncIteration': StopAsyncIteration,
  'StopIteration': StopIteration,
  'SyntaxError': SyntaxError,
  'SyntaxWarning': SyntaxWarning,
  'SystemError': SystemError,
  'SystemExit': SystemExit,
  'TabError': TabError,
  'TimeoutError': TimeoutError,
  'True': True,
  'TypeError': TypeError,
  'UnboundLocalError': UnboundLocalError,
  'UnicodeDecodeError': UnicodeDecodeError,
  'UnicodeEncodeError': UnicodeEncodeError,
  'UnicodeError': UnicodeError,
  'UnicodeTranslateError': UnicodeTranslateError,
  'UnicodeWarning': UnicodeWarning,
  'UserWarning': UserWarning,
  'ValueError': ValueError,
  'Warning': Warning,
  'ZeroDivisionError': ZeroDivisionError,
  'abs': abs,
  'all': all,
  'any': any,
  'ascii': ascii,
  'bin': bin,
  'bool': bool,
  'breakpoint': breakpoint,
  'bytearray': bytearray,
  'bytes': bytes,
  'callable': callable,
  'chr': chr,
  'classmethod': classmethod,
  'compile': compile,
  'complex': complex,
  'copyright': copyright,
  'credits': credits,
  'delattr': delattr,
  'dict': dict,
  'dir': dir,
  'divmod': divmod,
  'enumerate': enumerate,
  'filter': filter,
  'float': float,
  'format': format,
  'frozenset': frozenset,
  'getattr': getattr,
  'globals': globals,
  'hasattr': hasattr,
  'hash': hash,
  'help': help,
  'hex': hex,
  'id': id,
  'input': input,
  'int': int,
  'isinstance': isinstance,
  'issubclass': issubclass,
  'iter': iter,
  'len': len,
  'license': license,
  'list': list,
  'locals': locals,
  'map': map,
  'max': max,
  'memoryview': memoryview,
  'min': min,
  'next': next,
  'object': object,
  'oct': oct,
  'open': open,
  'ord': ord,
  'pow': pow,
  'print': print,
  'property': property,
  'range': range,
  'repr': repr,
  'reversed': reversed,
  'round': round,
  'set': set,
  'setattr': setattr,
  'slice': slice,
  'sorted': sorted,
  'staticmethod': staticmethod,
  'str': str,
  'sum': sum,
  'super': super,
  'tuple': tuple,
  'type': type,
  'vars': vars,
  'zip': zip}

##############################################################################
#template objects
##############################################################################

TEMPLATE_TEST_DATA = {'level1':{'level2':{'string':'test_data', 'integer':1, 'float':1.5}}}

ATTRIBUTE_TEMPLATE = {'name':['example_attribute_str', 'example_attribute_int', 'example_attribute_float'], 'attribute_path':['level1,level2,string', 'level1,level2,integer', 'level1,level2,float'], 'dtype':['str', 'int', 'float'], 'default':['missing', 0, 0]}

EXPRESSION_TEMPLATE = {'name':['example_expression_format_str', 'example_expression_math'], 'expression':["data['example_attribute_str'].upper()", "data['example_attribute_int'] / data['example_attribute_float']"], 'dtype':['str', 'float'], 'default':['MISSING', 0]}

RULESET_TEMPLATE = {'name':['example_rule1','example_rule2'],
                    'score':[100,50],
                    'flag':['example_flag', None],
                    'logic':["data['example_attribute_str'] == 'test_data'",
                             "data['example_expression_math'] < 1"]}

DATA_PIPELINE_TEMPLATE = {'type':['attributes','attributes','attributes','expressions', 'expressions'],'name':['example_attribute_str', 'example_attribute_int', 'example_attribute_float', 'example_expression_format_str', 'example_expression_math']}

LOGIC_PIPELINE_TEMPLATE = {'ruleset':['ruleset_template'], 'action':['get_time'], 'score_override':[''], 'flag_override':[''], 'apply_all':[False]}