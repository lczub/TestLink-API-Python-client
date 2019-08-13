#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013-2019 Luiko Czub, TestLink-API-Python-client developers
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

import pytest
# from testlink.testlinkapigeneric import testlinkargs
from testlink import testlinkargs

@pytest.fixture()
def args_register():
    """ reset singelton testlinkargs before and after the test """
    testlinkargs._resetRegister()
    yield testlinkargs
    testlinkargs._resetRegister()

def test__resetRegister(args_register):
    args_register._apiMethodsArgs['BigBird'] = 'not a Small Bird'
    assert None != args_register._apiMethodsArgs.get('BigBird')
    args_register._resetRegister()
    assert None == args_register._apiMethodsArgs.get('BigBird')


def test_registerMethod(args_register):
    args_register.registerMethod('DummyMethod', ['Uno', 'due', 'tre'], 
                                 ['quad','tre'], ['cinque'])
    a_def = args_register._apiMethodsArgs['DummyMethod']
    assert a_def == (['Uno', 'due', 'tre'], ['Uno', 'due', 'tre', 'quad'], 
                     ['cinque'])
 
def test_registerMethod_noArgs(args_register):
    args_register.registerMethod('DummyMethod')
    a_def = args_register._apiMethodsArgs['DummyMethod']
    assert a_def == ([], [], [])
     
def test_registerMethod_onlyArgsOptional(args_register):
    args_register.registerMethod('DummyMethod', apiArgsOptional=['quad','tre'])
    a_def = args_register._apiMethodsArgs['DummyMethod']
    assert a_def == ([], ['quad','tre'], [])
     
def test_registerMethod_onlyArgsPositional(args_register):
    args_register.registerMethod('DummyMethod', ['Uno', 'due', 'tre'])
    a_def = args_register._apiMethodsArgs['DummyMethod']
    assert a_def == (['Uno', 'due', 'tre'], ['Uno', 'due', 'tre'], []) 
     
def test_getMethodsWithPositionalArgs(args_register):
    args_register.registerMethod('Method_3pos_0opt', ['Uno', 'due', 'tre']) 
    args_register.registerMethod('Method_0pos_2opt', [], ['Uno', 'due'])        
    args_register.registerMethod('Method_1pos_2opt',  ['Uno'], ['due', 'tre']) 
    a_def = args_register.getMethodsWithPositionalArgs()
    assert a_def == {'Method_3pos_0opt' : ['Uno', 'due', 'tre'],
                     'Method_1pos_2opt' : ['Uno']}
     
def test_registerMethod_ErrorAlreadyDefined(args_register):
    args_register.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                 ['quad','tre'], ['cinque'])
    with pytest.raises(testlinkargs.TLArgError,
                       match='DummyMethod already registered'):
        args_register.registerMethod('DummyMethod')
         
def test_registerArgOptional(args_register):
    args_register.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                 ['quad','tre'], ['cinque'])
    args_register.registerArgOptional('DummyMethod', 'sei')
    a_def = args_register._apiMethodsArgs['DummyMethod']
    assert a_def  == (['Uno', 'due', 'tre'],
                      ['Uno', 'due', 'tre', 'quad', 'sei'], ['cinque'])
 
def test_registerArgOptional_ErrorUnknownMethod(args_register):
    with pytest.raises(testlinkargs.TLArgError, 
                       match='DummyMethod not registered'):
        args_register.registerArgOptional('DummyMethod', 'sei')
 
def test_registerArgNonApi(args_register):
    args_register.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],
                                 ['quad','tre'], ['cinque'])
    args_register.registerArgNonApi('DummyMethod', 'sei')
    a_def = args_register._apiMethodsArgs['DummyMethod']
    assert a_def  == (['Uno', 'due', 'tre'], ['Uno', 'due', 'tre', 'quad'],
                      ['cinque', 'sei'])
     
def test_getArgsForMethod_onlyOptionalArgs(args_register):
    args_register.registerMethod('DummyMethod', ['Uno', 'due', 'tre'], 
                                 ['quad','tre'])
    response = args_register.getArgsForMethod('DummyMethod')
    assert  response == (['Uno', 'due', 'tre', 'quad'], [])
     
def test_getArgsForMethod_OptionalAndPositionalArgs(args_register):
    args_register.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                 ['quad','tre']) 
    response = args_register.getArgsForMethod('DummyMethod', ['Uno', 'quad'])
    assert  response == (['due', 'tre'], [])
 
def test_getArgsForMethod_nonApiArgs(args_register):
    args_register.registerMethod('DummyMethod', ['Uno', 'due', 'tre'],  
                                 ['quad','tre'], ['cinque'])
    response = args_register.getArgsForMethod('DummyMethod', 
                                              ['Uno', 'due', 'tre'])
    assert  response == (['quad'], ['cinque']) 
 
def test_getArgsForMethod_unknownMethods(args_register):
    with pytest.raises(testlinkargs.TLArgError, 
                       match='unknownMethod not registered'):
        args_register.getArgsForMethod('unknownMethod')
        