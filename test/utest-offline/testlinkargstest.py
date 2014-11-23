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
# from testlink.testlinkapigeneric import testlinkargs
from testlink import testlinkargs
import sys
if sys.version_info[0] < 3:
    if sys.version_info[1] < 7:
        import unittest2 as unittest
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp



class testlinkargsTestCase(unittest.TestCase):
    """ TestCases for module testlinkargs """
    
    def setUp(self):
        """ backup TestLinkHelper related environment variables """
        
        # module under test
        self.mut = testlinkargs
        # reset the args cache
        self.mut._resetRegister()
        # api simulation
        self.api = self 

    def tearDown(self):
        # reset the args cache
        self.mut._resetRegister()

    def test__resetRegister(self):
        self.mut._apiMethodsArgs['BigBird'] = 'not a Small Bird'
        self.assertIsNotNone(self.mut._apiMethodsArgs.get('BigBird'))
        self.mut._resetRegister()
        self.assertIsNone(self.mut._apiMethodsArgs.get('BigBird'))

    def test_registerMethod(self):
        self.mut.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                ['quad','tre'], ['cinque'])
        a_def = self.mut._apiMethodsArgs['DummyMethod']
        self.assertEqual((['Uno', 'due', 'tre'], ['Uno', 'due', 'tre', 'quad'],
                          ['cinque']), a_def )

    def test_registerMethod_noArgs(self):
        self.mut.registerMethod('DummyMethod')
        a_def = self.mut._apiMethodsArgs['DummyMethod']
        self.assertEqual(([], [], []), a_def )
        
    def test_registerMethod_onlyArgsOptional(self):
        self.mut.registerMethod('DummyMethod', apiArgsOptional=['quad','tre'])
        a_def = self.mut._apiMethodsArgs['DummyMethod']
        self.assertEqual(([], ['quad','tre'], []), a_def )
        
    def test_registerMethod_onlyArgsPositional(self):
        self.mut.registerMethod('DummyMethod', ['Uno', 'due', 'tre'])
        a_def = self.mut._apiMethodsArgs['DummyMethod']
        self.assertEqual((['Uno', 'due', 'tre'], ['Uno', 'due', 'tre'], []), 
                         a_def )
        
    def test_getMethodsWithPositionalArgs(self):
        self.mut.registerMethod('Method_3pos_0opt', ['Uno', 'due', 'tre']) 
        self.mut.registerMethod('Method_0pos_2opt', [], ['Uno', 'due'])        
        self.mut.registerMethod('Method_1pos_2opt',  ['Uno'], ['due', 'tre']) 
        a_def = self.mut.getMethodsWithPositionalArgs()
        self.assertEqual({'Method_3pos_0opt' : ['Uno', 'due', 'tre'],
                          'Method_1pos_2opt' : ['Uno']}, 
                         a_def )
        
    def test_registerMethod_ErrorAlreadyDefined(self):
        self.mut.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                ['quad','tre'], ['cinque'])
        with self.assertRaisesRegexp(testlinkargs.TLArgError, 
                                     'DummyMethod already registered'):
            self.mut.registerMethod('DummyMethod')
            
    def test_registerArgOptional(self):
        self.mut.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                ['quad','tre'], ['cinque'])
        self.mut.registerArgOptional('DummyMethod', 'sei')
        a_def = self.mut._apiMethodsArgs['DummyMethod']
        self.assertEqual((['Uno', 'due', 'tre'], 
                          ['Uno', 'due', 'tre', 'quad', 'sei'],
                          ['cinque']), a_def )

    def test_registerArgOptional_ErrorUnknownMethod(self):
        with self.assertRaisesRegexp(testlinkargs.TLArgError, 
                                     'DummyMethod not registered'):
            self.mut.registerArgOptional('DummyMethod', 'sei')

    def test_registerArgNonApi(self):
        self.mut.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                ['quad','tre'], ['cinque'])
        self.mut.registerArgNonApi('DummyMethod', 'sei')
        a_def = self.mut._apiMethodsArgs['DummyMethod']
        self.assertEqual((['Uno', 'due', 'tre'], 
                          ['Uno', 'due', 'tre', 'quad'],
                          ['cinque', 'sei']), a_def )
        
    def test_getArgsForMethod_onlyOptionalArgs(self):
        self.mut.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                ['quad','tre'])
        response = self.mut.getArgsForMethod('DummyMethod')
        self.assertEqual(response, (['Uno', 'due', 'tre', 'quad'], []) )
        
    def test_getArgsForMethod_OptionalAndPositionalArgs(self):
        self.mut.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                ['quad','tre']) 
        response = self.mut.getArgsForMethod('DummyMethod', ['Uno', 'quad'])
        self.assertEqual(response, (['due', 'tre'], []) )

    def test_getArgsForMethod_nonApiArgs(self):
        self.mut.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                ['quad','tre'], ['cinque'])
        response = self.mut.getArgsForMethod('DummyMethod', 
                                             ['Uno', 'due', 'tre'])
        self.assertEqual(response,  (['quad'], ['cinque']) )

    def test_getArgsForMethod_unknownMethods(self):
        with self.assertRaisesRegexp(testlinkargs.TLArgError, 
                                     'unknownMethod not registered'):
            self.mut.getArgsForMethod('unknownMethod')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()