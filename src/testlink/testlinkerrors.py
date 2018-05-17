#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012-2018 Patrick Dassier, Luiko Czub, TestLink-API-Python-client developers
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

class TestLinkError(Exception):
    """ Basic error 
    Return message pass as argument
    """
#    def __init__(self, msg):
#        self.__msg = msg
#
#    def __str__(self):
#        return self.__msg

class TLConnectionError(TestLinkError):
    """ Connection error 
    - wrong url? - server not reachable? """
    
class TLAPIError(TestLinkError):
    """ API error 
    - wrong method name ? - misssing required args? """
    
class TLArgError(TestLinkError):
    """ Call error 
    - wrong number of mandatory params ? - wrong param type? """    

class TLResponseError(TestLinkError):
    """ Response error 
    - Response is empty or includes error codes """
    
    def __init__(self, methodNameAPI, argsOptional, message, code=None):
        self.methodNameAPI = methodNameAPI
        self.argsOptional  = argsOptional
        self.message       = message
        self.code          = code
        msg = '%s\n%s(%s)' % (message, methodNameAPI, argsOptional)
        if code:
            msg = '%s: %s' % (code, msg)
        return super(TLResponseError, self).__init__(msg)
        
           

        