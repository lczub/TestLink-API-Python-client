#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2014-2020 Mario Benito, Luiko Czub, TestLink-API-Python-client developers
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
# XMLRPC ProxiedTransport for Py27 as described in 
# https://docs.python.org/2.7/library/xmlrpclib.html#example-of-client-usage
# ------------------------------------------------------------------------

import xmlrpclib, httplib

class ProxiedTransport(xmlrpclib.Transport):
    ''' XMLRPC ProxiedTransport for Py27 as described in 
        https://docs.python.org/2.7/library/xmlrpclib.html#example-of-client-usage 
    '''
    
    def set_proxy(self, proxy):
        self.proxy = proxy

    def make_connection(self, host):
        self.realhost = host
        h = httplib.HTTPConnection(self.proxy)
        return h

    def send_request(self, connection, handler, request_body):
        connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))

    def send_host(self, connection, host):
        connection.putheader('Host', self.realhost)

