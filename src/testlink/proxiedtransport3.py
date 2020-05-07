#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2020 Luiko Czub, TestLink-API-Python-client developers
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

from http.client import HTTPConnection
from xmlrpc.client import Transport
from urllib.parse import urlparse, urlunparse

class ProxiedTransport(Transport):
    ''' XMLRPC ProxiedTransport for Py37+ as described in 
        https://docs.python.org/3.8/library/xmlrpc.client.html#example-of-client-usage
    '''
    
    def set_proxy(self, host, port=None, headers=None):
        ''' if host includes a port definition (e.g. http://myHost:1111) 
            this will be used instead the optional PORT arg
        '''
        
        u1 = urlparse(host)
        uport  = u1.port
        u2 = u1._replace(netloc=u1.hostname)
        uhost  = urlunparse(u2)

        self.proxy = uhost, uport or port
        self.proxy_headers = headers

    def make_connection(self, host):
        connection = HTTPConnection(*self.proxy)
        connection.set_tunnel(host, headers=self.proxy_headers)
        self._connection = host, connection
        return connection
