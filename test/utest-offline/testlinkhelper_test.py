#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012-2019 Luiko Czub, TestLink-API-Python-client developers
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

# TestCases for TestLinkHelper
# this test works WITHOUT an online TestLink Server
# no calls are send to a TestLink Server

import pytest, sys
IS_PY3 = sys.version_info[0] > 2

class DummyTestLinkAPI(object):
    """ Dummy for Simulation TestLinkAPICLient. 
    Used for init() tests with TestLinkHelper.connect(api_class)
    """
    
    def __init__(self, server_url, devKey, **args):
        self.server = server_url
        self.devKey = devKey
        self.args   = args

ENVNAMES = ('TESTLINK_API_PYTHON_SERVER_URL', 'TESTLINK_API_PYTHON_DEVKEY', 
            'http_proxy')
EXPECTED_DEFAULTS = ('http://localhost/testlink/lib/api/xmlrpc.php', '42',
                     '')

def setEnviron(monkeypatch, envname, envvalue ):
    """ manipulates environment variable ENVNAME to emulate setting ENVVALUE. 
        tests must use pytest fixture monkeypatch """
    if envvalue is None:
        monkeypatch.delenv(envname, False)
    else:
        monkeypatch.setenv(envname, envvalue)


test_data_init_envs = [
    ((None, None, None), 
     EXPECTED_DEFAULTS ),
    (('SERVER-URL-1', None, None), 
     ('SERVER-URL-1', EXPECTED_DEFAULTS[1], EXPECTED_DEFAULTS[2])),
    ((None, 'DEVKEY-2', None),
     (EXPECTED_DEFAULTS[0], 'DEVKEY-2', EXPECTED_DEFAULTS[2])),
    (('SERVER-URL-3', 'DEVKEY-3', None), 
     ('SERVER-URL-3', 'DEVKEY-3', EXPECTED_DEFAULTS[2])),
    ((None, None, 'Proxy-4'),
     (EXPECTED_DEFAULTS[0], EXPECTED_DEFAULTS[1], 'Proxy-4')),
    (('SERVER-URL-5', 'DEVKEY-5', 'Proxy-5'),
     ('SERVER-URL-5', 'DEVKEY-5', 'Proxy-5'))
    ]

@pytest.mark.parametrize("env_values, expectations", test_data_init_envs)
def test_init_env(api_helper_class, monkeypatch, env_values, expectations ):
    """ init TestLinkHelper with environment variables """
    # set TestLinkHelper related environment variables
    setEnviron(monkeypatch, ENVNAMES[0], env_values[0])
    setEnviron(monkeypatch, ENVNAMES[1], env_values[1])
    setEnviron(monkeypatch, ENVNAMES[2], env_values[2])
    # init helper without params
    a_helper = api_helper_class()
    assert expectations == (a_helper._server_url, a_helper._devkey, 
                            a_helper._proxy)
         

test_data_init_params = [
    (('SERVER-URL-11', None, None), 
     ('SERVER-URL-11', EXPECTED_DEFAULTS[1], EXPECTED_DEFAULTS[2])), 
    ((None, 'DEVKEY-12', None),
     (EXPECTED_DEFAULTS[0], 'DEVKEY-12', EXPECTED_DEFAULTS[2])),
    (('SERVER-URL-13', 'DEVKEY-13', None),
     ('SERVER-URL-13', 'DEVKEY-13', EXPECTED_DEFAULTS[2])),
    ((None, None, 'Proxy-14'),
     (EXPECTED_DEFAULTS[0], EXPECTED_DEFAULTS[1],'Proxy-14')),
    (('SERVER-URL-15', 'DEVKEY-15', 'Proxy-15'),
     ('SERVER-URL-15', 'DEVKEY-15', 'Proxy-15'))
    ]

@pytest.mark.parametrize("param_values, expectations", test_data_init_params)
def test_init_params(api_helper_class, monkeypatch, param_values, expectations):
    """ init TestLinkHelper with parameter and no env variables """
    # unset TestLinkHelper related environment variables
    setEnviron(monkeypatch, ENVNAMES[0], None)
    setEnviron(monkeypatch, ENVNAMES[1], None)
    setEnviron(monkeypatch, ENVNAMES[2], None)
    # init helper with params
    a_helper = api_helper_class(*param_values)
    assert expectations == (a_helper._server_url, a_helper._devkey, 
                            a_helper._proxy)
 
def test_init_env_params(api_helper_class, monkeypatch):
    """ init TestLinkHelper with mixed method parameter and env variables """
    # set TestLinkHelper related environment variables
    setEnviron(monkeypatch, ENVNAMES[0], 'SERVER-URL-21')
    setEnviron(monkeypatch, ENVNAMES[1], 'DEVKEY-21')
    setEnviron(monkeypatch, ENVNAMES[2], 'PROXY-21')
    # init helper with method params
    a_helper = api_helper_class('SERVER-URL-22', 'DEVKEY-22', 'PROXY-22')
    # the method params have a high priority than the environment variables
    assert 'SERVER-URL-22' == a_helper._server_url
    assert 'DEVKEY-22' == a_helper._devkey
    assert 'PROXY-22' == a_helper._proxy
     

def test_createArgparser(api_helper_class):
    """ create TestLinkHelper command line argument parser """
    a_helper = api_helper_class('SERVER-URL-31', 'DEVKEY-31', 'PROXY-31')
    a_parser = a_helper._createArgparser('DESCRIPTION-31')
    assert 'DESCRIPTION-31', a_parser.description
    default_args=a_parser.parse_args('')
    assert 'SERVER-URL-31' == default_args.server_url
    assert 'DEVKEY-31' == default_args.devKey
    assert 'PROXY-31' == default_args.proxy
     
def test_setParamsFromArgs(api_helper_class):
    """ set TestLinkHelper params from command line arguments """
    a_helper = api_helper_class()
    a_helper.setParamsFromArgs(None, ['--server_url', 'SERVER-URL-41', 
                                      '--devKey' , 'DEVKEY-41'])
    assert 'SERVER-URL-41' == a_helper._server_url
    assert 'DEVKEY-41' == a_helper._devkey
     
def test_connect(api_helper_class):
    """ create a TestLink API dummy """
    a_helper = api_helper_class('SERVER-URL-51', 'DEVKEY-51')
    a_tl_api = a_helper.connect(DummyTestLinkAPI)
    assert 'SERVER-URL-51' == a_tl_api.server
    assert 'DEVKEY-51' == a_tl_api.devKey
    assert {} == a_tl_api.args
     
def test_getProxiedTransport_py2(api_helper_class):
    """ create a TestLink Helper with ProxiedTransport - py27 """
    if IS_PY3:
        pytest.skip("py27 specific test")
        
    a_helper = api_helper_class('SERVER-URL-611', 'DEVKEY-611', 'PROXY-611:8080')
                                   #'http://fast.proxy.com.de/')
    a_pt = a_helper._getProxiedTransport()
    assert 'ProxiedTransport' == a_pt.__class__.__name__
    assert 'PROXY-611:8080' == a_pt.proxy
  
def test_getProxiedTransport_py3(api_helper_class):
    """ create a TestLink Helper with ProxiedTransport - py3x """

    if not IS_PY3:
        pytest.skip("py3 specific test")
    
    a_helper = api_helper_class('SERVER-URL-612', 'DEVKEY-612', 'http://PROXY-612:8080')
                                   #'http://fast.proxy.com.de/')
    a_pt = a_helper._getProxiedTransport()
    assert 'ProxiedTransport' == a_pt.__class__.__name__
    assert ('http://proxy-612', 8080) == a_pt.proxy
    
def test_connect_with_proxy2(api_helper_class):
    """ create a TestLink API dummy with ProxiedTransport - py27"""
    if IS_PY3:
        pytest.skip("py27 specific test")

    a_helper = api_helper_class('SERVER-URL-711', 'DEVKEY-711', 'PROXY-711:8080')
    a_tl_api = a_helper.connect(DummyTestLinkAPI)
    assert 'SERVER-URL-711' == a_tl_api.server
    assert 'DEVKEY-711' == a_tl_api.devKey
    assert 'PROXY-711:8080' == a_tl_api.args['transport'].proxy

def test_connect_with_proxy3(api_helper_class):
    """ create a TestLink API dummy with ProxiedTransport - py3x"""
    if not IS_PY3:
        pytest.skip("py3 specific test")
    
    a_helper = api_helper_class('SERVER-URL-712', 'DEVKEY-712', 'https://PROXY-712:8080')
    a_tl_api = a_helper.connect(DummyTestLinkAPI)
    assert 'SERVER-URL-712' == a_tl_api.server
    assert 'DEVKEY-712' == a_tl_api.devKey
    assert ('https://proxy-712', 8080) == a_tl_api.args['transport'].proxy
    
def test_connect_ignoring_proxy_env(api_helper_class, monkeypatch):
    """ create a TestLink API dummy ignoring PROXY env - pullRequest #121 """
    setEnviron(monkeypatch, ENVNAMES[2], 'PROXY-71')
    a_helper = api_helper_class('SERVER-URL-71', 'DEVKEY-71', False)
    a_tl_api = a_helper.connect(DummyTestLinkAPI)
    assert 'SERVER-URL-71' == a_tl_api.server
    assert 'DEVKEY-71' == a_tl_api.devKey
    assert {} == a_tl_api.args
   

def test_connect_with_https_no_context(api_helper_class):
    """ create a TestLink API dummy for https with uncertified context """
    a_helper = api_helper_class('https://SERVER-URL-71', 'DEVKEY-71')
    a_tl_api = a_helper.connect(DummyTestLinkAPI)
    assert 'https://SERVER-URL-71' == a_tl_api.server
    assert 'DEVKEY-71' == a_tl_api.devKey
    a_context = a_tl_api.args['context']
    assert [] == a_context.get_ca_certs()
     
def test_connect_with_https_and_context(api_helper_class):
    """ create a TestLink API dummy for https with special context """
    a_helper = api_helper_class('https://SERVER-URL-71', 'DEVKEY-71')
    a_tl_api = a_helper.connect(DummyTestLinkAPI, context='ssl_context')
    assert 'https://SERVER-URL-71' == a_tl_api.server
    assert 'DEVKEY-71' == a_tl_api.devKey
    assert 'ssl_context' == a_tl_api.args['context']
     