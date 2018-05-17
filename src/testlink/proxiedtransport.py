#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2014-2018 Mario Benito, TestLink-API-Python-client developers
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

import sys
IS_PY3 = sys.version_info[0] > 2
if IS_PY3:
    from xmlrpc.client import Transport
    from http.client import HTTPConnection
else:
    from xmlrpclib import Transport
    from httplib import HTTPConnection
    
try:
    import gzip
except ImportError:
    gzip = None #python can be built without zlib/gzip support


class ProxiedTransport(Transport):
    def __init__(self):
        if IS_PY3:
            super(ProxiedTransport, self).__init__()
        else:  
            Transport.__init__(self)
        self.realhost = None
        self.proxy = None

    def set_proxy(self, proxy):
        """Define HTTP proxy (with optional basic auth)

        :param str proxy: Proxy string
        """
        cproxy, auth, x509 = self.get_host_info(proxy)
        self.proxy = cproxy
        if auth:
            auth = [ ('Proxy-Authorization', auth[0][1]) ]
            if self._extra_headers:
                self._extra_headers.extend(auth)
            else:
                self._extra_headers = auth

    def make_connection(self, host):
        """return an existing connection if possible.  This allows HTTP/1.1 keep-alive.

        :param str|(str, {}) host: Host descriptor (URL or (URL, x509 info) tuple)
        :return httplib.HTTPConnection:
        """
        if self._connection and host == self._connection[0]:
            return self._connection[1]

        # create a HTTP connection object from a host descriptor
        chost, auth, x509 = self.get_host_info(host)
        if auth:
            if self._extra_headers:
                self._extra_headers.extend(auth)
            else:
                self._extra_headers = auth
        self.realhost = host
        self._connection = host, HTTPConnection(self.proxy)
        return self._connection[1]

    def send_request(self, connection, handler, request_body):
        """Send request header

        :param httplib.HTTPConnection connection: Connection handle
        :param str handler: Target RPC handler
        :param str request_body:XML-RPC body
        """
        if self.accept_gzip_encoding and gzip:
            connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler), skip_accept_encoding=True)
            connection.putheader("Accept-Encoding", "gzip")
        else:
            connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))

    def send_host(self, connection, host):
        """Send host name

        Note: This function doesn't actually add the "Host"
        header anymore, it is done as part of the connection.putrequest() in
        send_request() above.

        :param httplib.HTTPConnection connection: Connection handle
        :param str host: Host name
        """
        extra_headers = self._extra_headers
        if extra_headers:
            if isinstance(extra_headers, dict()):
                extra_headers = extra_headers.items()
            for key, value in extra_headers:
                connection.putheader(key, value)
