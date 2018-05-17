#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013-2018 Luiko Czub, TestLink-API-Python-client developers
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

from functools import wraps
from .testlinkargs import registerMethod, registerArgOptional, registerArgNonApi
from .testlinkerrors import TLResponseError

__doc__ = """ This internal module defines the decorator functions, which are 
used to generate the TestLink API methods in a generic way 

Method definitions should be build either with 
@decoMakerApiCallWithArgs(argNamesPositional, argNamesOptional)
   for calling a server method with arguments 
   - argNamesPositional = list default positional args
   - argNamesOptional   = list additional optional args
   to check the server response, if it includes TestLink Error Codes or 
   an empty result (which raise a TLResponseError) 
or   
@decoApiCallWithoutArgs
   for calling server methods without arguments
   to check the server response, if it includes TestLink Error Codes or 
   an empty result (which raise a TLResponseError)
 
Additional behavior could be added with
   
@decoApiCallAddDevKey
   - to expand the parameter list with devKey key/value pair
     before calling the server method
@decoMakerApiCallReplaceTLResponseError(replaceCode)
   - to catch an TLResponseError after calling the server method and with an 
     empty list
     - replaceCode : TestLink Error Code, which should be handled 
                     default is None for "Empty Results"
@decoApiCallAddAttachment:
    - to add an mandatory argument 'attachmentfile'
      - attachmentfile is a python file descriptor pointing to the file 
    - to expand parameter list with key/value pairs
         'filename', 'filetype', 'content'
      from 'attachmentfile' before calling the server method
@decoMakerApiCallChangePosToOptArg(argPos, argName):
    - to change the positional argument ARGPOS into an optional argument ARGNAME. 
    - used for example in createTestPlan to support TL 1.9.13 and 1.9.14
      argument definitions
      - with TL 1.9.13 'testprojectname' was mandatory and expected as argPos 2
      - with TL 1.9.14 'testproject' is optional, cause new argument 'prefix'
        could be used as alternative      
"""



# decorators for generic api calls
# see http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python

def decoApiCallWithoutArgs(methodAPI):
    """ Decorator for calling server methods without arguments """ 
    
    # register methods without positional and optional arguments 
    registerMethod(methodAPI.__name__)
 
    @wraps(methodAPI)  
    def wrapperWithoutArgs(self):
        return self.callServerWithPosArgs(methodAPI.__name__)
    return wrapperWithoutArgs

def decoMakerApiCallWithArgs(argNamesPositional=[], argNamesOptional=[]):
    """ creates a decorator for calling a server method with arguments

     argNamesPositional defines a list of positional arguments, which should be
     registered in the global apiMethodsArgNames for the server method
     argNamesOptional defines a list of optional arguments, which should be
     registered in the global apiMethodsArgNames for the server method
     
     """

    def decoApiCallWithArgs(methodAPI):
        """ Decorator for calling a server method with arguments """
        
        # register methods positional and optional arguments 
        registerMethod(methodAPI.__name__, argNamesPositional, argNamesOptional)
        # define the method server call           
        @wraps(methodAPI)  
        def wrapperWithArgs(self, *argsPositional, **argsOptional):
            return self.callServerWithPosArgs(methodAPI.__name__, 
                                              *argsPositional, **argsOptional)
        return wrapperWithArgs
    return decoApiCallWithArgs

def decoApiCallAddDevKey(methodAPI):
    """ Decorator to expand parameter list with devKey"""
    # register additional optional argument devKey 
    registerArgOptional(methodAPI.__name__, 'devKey')
    @wraps(methodAPI)  
    def wrapperAddDevKey(self, *argsPositional, **argsOptional):
        if not ('devKey' in argsOptional):
            argsOptional['devKey'] = self.devKey
        return methodAPI(self, *argsPositional, **argsOptional)
    return wrapperAddDevKey

def decoMakerApiCallReplaceTLResponseError(replaceCode=None, replaceValue=[]):
    """ creates a decorator, which replace an TLResponseError with a new value

     Default (replaceCode=None) handles the cause 'Empty Result'
     - ok for getProjectTestPlans, getBuildsForTestPlan, which returns just ''
     Problems are getTestPlanByName, getFirstLevelTestSuitesForTestProject
     - they do not return just '', they returns the error message
        3041: Test plan (noPlatform) has no platforms linked
        7008: Test Project (noSuite) is empty
      could be handled with replaceCode=3041 / replaceCode=7008
      
     Default (replaceValue=[]) new return value is an empty list
     - could be changed to other things like {}       

     """  
    # for understanding, what we are doing here please read
    # # see http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python
    # - Passing arguments to the decorator
    
    def decoApiCallReplaceTLResponseError(methodAPI):
        """ Decorator to replace an TLResponseError with an empty list """
        @wraps(methodAPI)  
        def wrapperReplaceTLResponseError(self, *argsPositional, **argsOptional):
            response = None
            try:
                response = methodAPI(self, *argsPositional, **argsOptional)
            except TLResponseError as tl_err:
                if tl_err.code == replaceCode:
                    # empty result (response == '') -> code == None
                    # special case NoPlatform -> code == 3041
                    response = replaceValue
                else:
                    # seems to be another response failure - we forward it
                    raise  
            return response
        return wrapperReplaceTLResponseError
    return decoApiCallReplaceTLResponseError

def decoApiCallAddAttachment(methodAPI):
    """ Decorator to expand parameter list with devKey and attachmentfile
        attachmentfile  is a python file descriptor pointing to the file
    """  
    registerArgOptional(methodAPI.__name__, 'devKey')
    registerArgNonApi(methodAPI.__name__, 'attachmentfile')
    @wraps(methodAPI)  
    def wrapperAddAttachment(self, attachmentfile, *argsPositional, **argsOptional):
        if not ('devKey' in argsOptional):
            argsOptional['devKey'] = self.devKey
        argsAttachment = self._getAttachmentArgs(attachmentfile)
        # add additional key/value pairs from argsOptional 
        # although overwrites filename, filetype, content with user definition
        # if they exist
        argsAttachment.update(argsOptional)
        return methodAPI(self, *argsPositional, **argsAttachment)
    return wrapperAddAttachment

def decoMakerApiCallChangePosToOptArg(argPos, argName):
    """ creates a decorator, which change the positional argument ARGPOS into
        an optional argument ARGNAME. 
        
        argPos=1 is the first positional arg
     """  
    # for understanding, what we are doing here please read
    # # see http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python
    # - Passing arguments to the decorator
    
    def decoApiCallChangePosToOptArg(methodAPI):
        """ Decorator to change a positional argument into an optional ARGNAME """
        @wraps(methodAPI)  
        def wrapperChangePosToOptArg(self, *argsPositional, **argsOptional):
            argsPositionalChanged = list(argsPositional)
            if (argPos > 0) and (len(argsPositional) >= argPos):
                argValue = argsPositionalChanged.pop(argPos - 1)
                argsOptional[argName] = argValue
            return methodAPI(self, *argsPositionalChanged, **argsOptional)
        return wrapperChangePosToOptArg
    return decoApiCallChangePosToOptArg
