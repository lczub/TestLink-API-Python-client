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
#
# TestCases for decorators, used by TestlinkAPIGeneric building 
# TestLink API methods. 

import pytest

from testlink.testlinkerrors import TLResponseError
from testlink.testlinkargs import registerMethod, getArgsForMethod
from testlink.testlinkdecorators import decoApiCallAddAttachment,\
decoApiCallAddDevKey, decoApiCallWithoutArgs, \
decoMakerApiCallReplaceTLResponseError, decoMakerApiCallWithArgs, \
decoMakerApiCallChangePosToOptArg


class dummy_api_testlinkdecorator(object):
    """ class simulating testlink api client with required attributes for 
        testlinkdecorators_test """
         
    devKey = '007'
         
    def _getAttachmentArgs(self, attachmentfile):
        # simulation of TestlinkAPIGeneric._getAttachmentArgs()
        # needed in test_decoApiCallAddAttachment
        return {'filename': 'name %s' % attachmentfile,
                'filetype': 'type %s' % attachmentfile,
                'content' : 'content %s' % attachmentfile}

@pytest.fixture()
def dummy_api():
    """ simulates testlink api client with required attributes devKey and 
        _getAttachmentArgs
    """
    return dummy_api_testlinkdecorator()

def test_noWrapperName_decoApiCallWithoutArgs():
    " decorator test: original function name should be unchanged "
    
    @decoApiCallWithoutArgs
    def orig_funcname1(a_api):
        "orig doc string1"
        return 'noArgs'
    
    assert 'orig_funcname1' == orig_funcname1.__name__
    assert 'orig doc string1' == orig_funcname1.__doc__
    assert 'testlinkdecorators_test' in orig_funcname1.__module__

def test_decoApiCallWithArgs():
    " decorator test: positional and optional arguments should be registered "
     
    from testlink.testlinkargs import getMethodsWithPositionalArgs
    @decoMakerApiCallWithArgs(['Uno', 'due', 'tre'], ['quad'])
    def DummyMethod(a_api):
        "a dummy api method with 3 positional args and 1 optional arg"
        pass
     
    posArgs = getMethodsWithPositionalArgs()
    assert ['Uno', 'due', 'tre'] == posArgs['DummyMethod']

def test_noWrapperName_decoApiCallWithArgs():
    " decorator test: original function name should be unchanged "
     
    @decoMakerApiCallWithArgs()
    def orig_funcname2(a_api):
        "orig doc string2"
        return 'noArgs'
     
    assert 'orig_funcname2' == orig_funcname2.__name__
    assert 'orig doc string2' == orig_funcname2.__doc__
    assert 'testlinkdecorators_test' in orig_funcname2.__module__

def test_decoApiCallAddDevKey(dummy_api):
    " decorator test: argsOptional should be extended with devKey"
     
    registerMethod('a_func')
    @decoApiCallAddDevKey
    def a_func(a_api, *argsPositional, **argsOptional):
        return argsPositional, argsOptional
     
    # check method argument definition
    allArgs = getArgsForMethod('a_func')
    assert (['devKey'], []) == allArgs
    # check call arguments
    response = a_func(dummy_api)
    assert {'devKey' : dummy_api.devKey} == response[1]

def test_noWrapperName_decoApiCallAddDevKey():
    " decorator test: original function name should be unchanged "
     
    registerMethod('orig_funcname3')
    @decoApiCallAddDevKey
    def orig_funcname3(a_api, *argsPositional, **argsOptional):
        "orig doc string3"
        return argsPositional, argsOptional
     
    assert 'orig_funcname3' == orig_funcname3.__name__
    assert 'orig doc string3' == orig_funcname3.__doc__
    assert 'testlinkdecorators_test' in orig_funcname3.__module__
     
def test_decoApiCallReplaceTLResponseError_NoCodeError():
    " decorator test: TLResponseError (code=None) should be handled "
     
    @decoMakerApiCallReplaceTLResponseError()
    def a_func(a_api, *argsPositional, **argsOptional):
        raise TLResponseError('DummyMethod', 
                            argsOptional, 'Empty Response! ')

    response = a_func('dummy_api')
    assert [] == response
     
def test_decoApiCallReplaceTLResponseError_CodeError():
    " decorator test: TLResponseError (code=777) should be raised "
     
    @decoMakerApiCallReplaceTLResponseError()
    def a_func(a_api, *argsPositional, **argsOptional):
        raise TLResponseError('DummyMethod', 
                            argsOptional, 'Empty Response! ', 777)

    with pytest.raises(TLResponseError, match='777.*Empty'):
        a_func('dummy_api')
     
def test_decoApiCallReplaceTLResponseError_CodeErrorOk():
    " decorator test: TLResponseError (code=777) should be handled "
     
    @decoMakerApiCallReplaceTLResponseError(777)
    def a_func(a_api, *argsPositional, **argsOptional):
        raise TLResponseError('DummyMethod', 
                            argsOptional, 'Empty Response! ', 777)

    response = a_func('dummy_api')
    assert [] == response

def test_decoApiCallReplaceTLResponseError_NoError():
    " decorator test: response without TLResponseError should be passed "
     
    @decoMakerApiCallReplaceTLResponseError(777)
    def a_func(a_api, *argsPositional, **argsOptional):
        return argsOptional

    response = a_func('dummy_api', name='BigBird')
    assert {'name' : 'BigBird'} == response

def test_decoApiCallReplaceTLResponseError_replaceValue():
    " decorator test: TLResponseError should be replaced with {}"
     
    @decoMakerApiCallReplaceTLResponseError(replaceValue={})
    def a_func(a_api, *argsPositional, **argsOptional):
        raise TLResponseError('DummyMethod', 
                            argsOptional, 'Empty Response! ')

    response = a_func('dummy_api')
    assert {} == response

def test_noWrapperName_decoApiCallReplaceTLResponseError():
    " decorator test: original function name should be unchanged "
     
    @decoMakerApiCallReplaceTLResponseError()
    def orig_funcname4(a_api, *argsPositional, **argsOptional):
        "orig doc string4"
        return argsPositional, argsOptional
     
    assert 'orig_funcname4' == orig_funcname4.__name__
    assert 'orig doc string4' == orig_funcname4.__doc__
    assert 'testlinkdecorators_test' in orig_funcname4.__module__
     
def test_decoApiCallAddAttachment(dummy_api):
    " decorator test: argsOptional should be extended attachment file infos"
     
    registerMethod('func_addAttachment')
    @decoApiCallAddAttachment
    def func_addAttachment(a_api, *argsPositional, **argsOptional):
        return argsPositional, argsOptional
     
    # check method argument definition
    allArgs = getArgsForMethod('func_addAttachment')
    assert (['devKey'], ['attachmentfile']) == allArgs
    # check call arguments
    response = func_addAttachment(dummy_api, 'a_file')
    assert response[1] == {'devKey' : dummy_api.devKey, 
                           'filename': 'name a_file',
                           'filetype': 'type a_file', 
                           'content' : 'content a_file'}
     
def test_noWrapperName_decoApiCallAddAttachment():
    " decorator test: original function name should be unchanged "
     
    registerMethod('orig_funcname5')
    @decoApiCallAddAttachment
    def orig_funcname5(a_api):
        "orig doc string5"
        return 'noArgs'
     
    assert 'orig_funcname5' == orig_funcname5.__name__
    assert 'orig doc string5' == orig_funcname5.__doc__
    assert 'testlinkdecorators_test' in orig_funcname5.__module__
     
def test_noWrapperName_decoApiCallChangePosToOptArg():
    " decorator test: original function name should be unchanged "
     
    @decoMakerApiCallChangePosToOptArg(2, 'optArgName')
    def orig_funcname6(*argsPositional, **argsOptional):
        "orig doc string6"
        return argsPositional, argsOptional
     
    assert 'orig_funcname6' == orig_funcname6.__name__
    assert 'orig doc string6' == orig_funcname6.__doc__
    assert 'testlinkdecorators_test' in orig_funcname6.__module__
     
def test_decoApiCallChangePosToOptArg_posArg2():
    " decorator test:  change  posArg 2"
     
    @decoMakerApiCallChangePosToOptArg(2, 'due')
    def a_func(a_api, *argsPositional, **argsOptional):
        return argsPositional, argsOptional

    #'Uno', 'due', 'tre', 'quad',  'cinque'
    # 2 posArgs 2optArgs -> 1posArg, 3optArg
    (posArgs, optArgs) = a_func('dummy_api', 1, 2, tre = 3, quad = 4 )
    assert (1,) == posArgs
    assert {'due' : 2, 'tre' : 3, 'quad' : 4 } == optArgs

    # 3 posArgs 2optArgs -> 2posArg, 2optArg
    (posArgs, optArgs) = a_func('dummy_api', 1, 2, 3, quad = 4 , due = 5)
    assert (1,3) == posArgs
    assert {'due' : 2, 'quad' : 4 } == optArgs

    # 1 posArgs 2optArgs -> 1posArg, 2optArg
    (posArgs, optArgs) = a_func('dummy_api', 1, due = 2, tre = 3)
    assert (1,) == posArgs
    assert {'due' : 2, 'tre' : 3 } == optArgs

    # 0 posArgs 2optArgs -> 0posArg, 2optArg
    (posArgs, optArgs) = a_func('dummy_api', uno = 1, due = 2)
    assert  () == posArgs
    assert {'uno' : 1, 'due' :2} == optArgs

def test_decoApiCallChangePosToOptArg_posArg3():
    " decorator test:  change  posArg 3"
     
    @decoMakerApiCallChangePosToOptArg(3, 'tre')
    def a_func(a_api, *argsPositional, **argsOptional):
        return argsPositional, argsOptional

    # 3 posArgs 0optArgs -> 2posArg, 1optArg
    (posArgs, optArgs) = a_func('dummy_api', 1, 2, 3 )
    assert (1,2) == posArgs
    assert {'tre' : 3} == optArgs

    # 2 posArgs 0optArgs -> 2posArg, 0optArg
    (posArgs, optArgs) = a_func('dummy_api', 1, 2 )
    assert (1,2) == posArgs
    assert {} == optArgs

def test_decoApiCallChangePosToOptArg_posArgNeg1():
    " decorator test:  change  posArg -1"
     
    @decoMakerApiCallChangePosToOptArg(-1, 'last')
    def a_func(a_api, *argsPositional, **argsOptional):
        return argsPositional, argsOptional

    # 3 posArgs 0optArgs -> 2posArg, 1optArg
    (posArgs, optArgs) = a_func('dummy_api', 1, 2, 3 )
    assert (1,2,3) == posArgs
    assert {} == optArgs

    # 1 posArgs 0optArgs -> 0posArg, 1optArg
    (posArgs, optArgs) = a_func('dummy_api', 1 )
    assert (1,) == posArgs
    assert {} == optArgs
 