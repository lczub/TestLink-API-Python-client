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

# this test requires an online TestLink Server, which connection parameters
# are defined in environment variables
#     TESTLINK_API_PYTHON_SERVER_URL and TESTLINK_API_PYTHON_DEVKEY

import pytest
from testlink import testlinkerrors

def test_callServer_noArgs(api_client):
    """ test _callServer() - calling method with no args """
    
    assert 'Hello!' == api_client._callServer('sayHello')

def test_callServer_withArgs(api_client):
    """ test _callServer() - calling method with args """
    
    assert 'You said: some arg' == api_client._callServer('repeat', {'str': 'some arg'})

def test_callServer_ProtocolError(api_client_class, api_helper_class):
    """ test _callServer() - Server raises ProtocollError """
     
    server_url = api_helper_class()._server_url
    bad_server_url = server_url.split('xmlrpc.php')[0] 
    api_client = api_helper_class(bad_server_url).connect(api_client_class)

    with pytest.raises(testlinkerrors.TLConnectionError, 
                       match='ProtocolError'):
        api_client._callServer('sayHello')

def test_callServer_socketError(api_client_class, api_helper_class):
    """ test _callServer() - Server raises a socket Error (getaddrinfo failed) """
     
    bad_server_url = 'http://111.222.333.4/testlink/lib/api/xmlrpc.php' 
    api_client = api_helper_class(bad_server_url).connect(api_client_class)

    with pytest.raises(testlinkerrors.TLConnectionError, 
                       match='getaddrinfo failed'):
        api_client._callServer('sayHello')

def test_callServer_FaultError(api_client):
    """ test _callServer() - Server raises Fault Error """
     
    with pytest.raises(testlinkerrors.TLAPIError):
        api_client._callServer('sayGoodBye')

