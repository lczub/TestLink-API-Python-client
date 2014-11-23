#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013-2014 Luiko Czub, TestLink-API-Python-client developers
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# ------------------------------------------------------------------------

# this test works WITHOUT an online TestLink Server
# no calls are send to a TestLink Server

import unittest
from testlink.testlinkerrors import TLResponseError
from testlink.testlinkargs import registerMethod, getArgsForMethod
from testlink.testlinkdecorators import decoApiCallAddAttachment,\
decoApiCallAddDevKey, decoApiCallWithoutArgs, \
decoMakerApiCallReplaceTLResponseError, decoMakerApiCallWithArgs 

import sys
if sys.version_info[0] < 3:
    if sys.version_info[1] < 7:
        import unittest2 as unittest
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp


class testlinkdecoratorsTestCase(unittest.TestCase):
    """ TestCases for decorators, used by TestlinkAPIGeneric for build 
        TestLink API methodsServer.  """
        
    devKey = '007'
    def setUp(self):
        self.api = self
        
    def _getAttachmentArgs(self, attachmentfile):
        # simulation of TestlinkAPIGeneric._getAttachmentArgs()
        # needed in test_decoApiCallAddAttachment
        return {'filename': 'name %s' % attachmentfile,
                'filetype': 'type %s' % attachmentfile,
                'content' : 'content %s' % attachmentfile}

#     def tearDown(self):
#         pass

    def test_noWrapperName_decoApiCallWithoutArgs(self):
        " decorator test: original function name should be unchanged "
        
        @decoApiCallWithoutArgs
        def orig_funcname1(a_api):
            "orig doc string"
            return 'noArgs'
        
        self.assertEqual('orig_funcname1', orig_funcname1.__name__)
        self.assertEqual('orig doc string', orig_funcname1.__doc__)
        self.assertEqual('testlinkdecoratorstest', orig_funcname1.__module__)

    def test_decoApiCallWithArgs(self):
        " decorator test: positional and optional arguments should be registered "
        
        from testlink.testlinkargs import getMethodsWithPositionalArgs
        @decoMakerApiCallWithArgs(['Uno', 'due', 'tre'], ['quad'])
        def DummyMethod(a_api):
            "a dummy api method with 3 positional args and 1 optional arg"
            pass
        
        posArgs = getMethodsWithPositionalArgs()
        self.assertEqual(['Uno', 'due', 'tre'], posArgs['DummyMethod'])

    def test_noWrapperName_decoApiCallWithArgs(self):
        " decorator test: original function name should be unchanged "
        
        @decoMakerApiCallWithArgs()
        def orig_funcname2(a_api):
            "orig doc string"
            return 'noArgs'
        
        self.assertEqual('orig_funcname2', orig_funcname2.__name__)
        self.assertEqual('orig doc string', orig_funcname2.__doc__)
        self.assertEqual('testlinkdecoratorstest', orig_funcname2.__module__)

    def test_decoApiCallAddDevKey(self):
        " decorator test: argsOptional should be extended with devKey"
        
        registerMethod('a_func')
        @decoApiCallAddDevKey
        def a_func(a_api, *argsPositional, **argsOptional):
            return argsPositional, argsOptional
        
        # check method argument definition
        allArgs = getArgsForMethod('a_func')
        self.assertEqual((['devKey'], []), allArgs)
        # check call arguments
        response = a_func(self.api)
        self.assertEqual({'devKey' : self.api.devKey}, response[1])

    def test_noWrapperName_decoApiCallAddDevKey(self):
        " decorator test: original function name should be unchanged "
        
        registerMethod('orig_funcname3')
        @decoApiCallAddDevKey
        def orig_funcname3(a_api, *argsPositional, **argsOptional):
            "orig doc string"
            return argsPositional, argsOptional
        
        self.assertEqual('orig_funcname3', orig_funcname3.__name__)
        self.assertEqual('orig doc string', orig_funcname3.__doc__)
        self.assertEqual('testlinkdecoratorstest', orig_funcname3.__module__)
        
    def test_decoApiCallReplaceTLResponseError_NoCodeError(self):
        " decorator test: TLResponseError (code=None) should be handled "
        
        @decoMakerApiCallReplaceTLResponseError()
        def a_func(a_api, *argsPositional, **argsOptional):
            raise TLResponseError('DummyMethod', 
                                argsOptional, 'Empty Response! ')

        response = a_func(self.api)
        self.assertEqual([], response)
        
    def test_decoApiCallReplaceTLResponseError_CodeError(self):
        " decorator test: TLResponseError (code=777) should be raised "
        
        @decoMakerApiCallReplaceTLResponseError()
        def a_func(a_api, *argsPositional, **argsOptional):
            raise TLResponseError('DummyMethod', 
                                argsOptional, 'Empty Response! ', 777)

        with self.assertRaisesRegexp(TLResponseError, '777.*Empty'):
            a_func(self.api)
        
    def test_decoApiCallReplaceTLResponseError_CodeErrorOk(self):
        " decorator test: TLResponseError (code=777) should be handled "
        
        @decoMakerApiCallReplaceTLResponseError(777)
        def a_func(a_api, *argsPositional, **argsOptional):
            raise TLResponseError('DummyMethod', 
                                argsOptional, 'Empty Response! ', 777)

        response = a_func(self.api)
        self.assertEqual([], response)

    def test_decoApiCallReplaceTLResponseError_NoError(self):
        " decorator test: response without TLResponseError should be passed "
        
        @decoMakerApiCallReplaceTLResponseError(777)
        def a_func(a_api, *argsPositional, **argsOptional):
            return argsOptional

        response = a_func(self.api, name='BigBird')
        self.assertEqual({'name' : 'BigBird'}, response)

    def test_decoApiCallReplaceTLResponseError_replaceValue(self):
        " decorator test: TLResponseError should be replaced with {}"
        
        @decoMakerApiCallReplaceTLResponseError(replaceValue={})
        def a_func(a_api, *argsPositional, **argsOptional):
            raise TLResponseError('DummyMethod', 
                                argsOptional, 'Empty Response! ')

        response = a_func(self.api)
        self.assertEqual({}, response)

    def test_noWrapperName_decoApiCallReplaceTLResponseError(self):
        " decorator test: original function name should be unchanged "
        
        @decoMakerApiCallReplaceTLResponseError()
        def orig_funcname4(a_api, *argsPositional, **argsOptional):
            "orig doc string"
            return argsPositional, argsOptional
        
        self.assertEqual('orig_funcname4', orig_funcname4.__name__)
        self.assertEqual('orig doc string', orig_funcname4.__doc__)
        self.assertEqual('testlinkdecoratorstest', orig_funcname4.__module__)
        
    def test_decoApiCallAddAttachment(self):
        " decorator test: argsOptional should be extended attachment file infos"
        
        registerMethod('func_addAttachment')
        @decoApiCallAddAttachment
        def func_addAttachment(a_api, *argsPositional, **argsOptional):
            return argsPositional, argsOptional
        
        # check method argument definition
        allArgs = getArgsForMethod('func_addAttachment')
        self.assertEqual((['devKey'], ['attachmentfile']), allArgs)
        # check call arguments
        response = func_addAttachment(self.api, 'a_file')
        self.assertEqual({'devKey' : self.api.devKey, 'filename': 'name a_file',
                    'filetype': 'type a_file', 'content' : 'content a_file'}, 
                         response[1])
        
    def test_noWrapperName_decoApiCallAddAttachment(self):
        " decorator test: original function name should be unchanged "
        
        registerMethod('orig_funcname5')
        @decoApiCallAddAttachment
        def orig_funcname5(a_api):
            "orig doc string"
            return 'noArgs'
        
        self.assertEqual('orig_funcname5', orig_funcname5.__name__)
        self.assertEqual('orig doc string', orig_funcname5.__doc__)
        self.assertEqual('testlinkdecoratorstest', orig_funcname5.__module__)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()