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

from .testlinkerrors import TLArgError


__doc__ = """ This internal module is used as a 'singleton' to register the 
supported TestLink API methods and there (positional and optional) arguments """


# main hash, where the registered methods and there arguments are stored
# PLEASE never manipulate the entries directly.
#
# definitions structure is
# key(apiMethodeName) = ( [default positional apiArgs], [all apiArgs], 
#                         [other mandatory non api Args] )
# [all apiArgs] includes all positional and optional args without other 
#  mandatory Args
_apiMethodsArgs = {}


def _resetRegister():
    """ clears all entries in _apiMethodsArgs"""
    _apiMethodsArgs.clear()


def _getMethodsArgDefinition(methodName):
    """ returns argument definition for api methodName """
    
    try:
        return _apiMethodsArgs[methodName]
    except KeyError:
        raise TLArgError('apiMethod %s not registered!' % methodName)


def registerMethod(methodName, apiArgsPositional=[], apiArgsOptional=[],
                        otherArgsMandatory=[]):
    """ extend _apiMethodsArgs with a new definition structure for METHODNAME

        definitions structure is
        key(apiMethodeName) = ( [default positional apiArgs], [all apiArgs], 
                                 [other mandatory non api Args] )
       [all apiArgs] includes all positional and optional args without other 
       mandatory Args  """ 
       
    if methodName in _apiMethodsArgs:
        raise TLArgError('apiMethod %s already registered!' % methodName)
    
    allArgs = apiArgsPositional[:]
    for argName in apiArgsOptional:
        if not argName in allArgs:
            allArgs.append(argName)
    _apiMethodsArgs[methodName] = (apiArgsPositional[:], allArgs, 
                                   otherArgsMandatory[:])


def registerArgOptional(methodName, argName):
    """ Update _apiMethodsArgs[methodName] with additional optional argument """ 
       
    allArgs = _getMethodsArgDefinition(methodName)[1]
    if not argName in allArgs:
        allArgs.append(argName)


def registerArgNonApi(methodName, argName):
    """ Update _apiMethodsArgs[methodName] with additional non api argument """ 
       
    nonApiArgs = _getMethodsArgDefinition(methodName)[2]
    if not argName in nonApiArgs:
        nonApiArgs.append(argName)


def getMethodsWithPositionalArgs():
    """ returns a dictionary with method names and there positional args """
    positionalArgNames = {}
    for mname, argdef in list(_apiMethodsArgs.items()):
        # does method MNAME has defined positional arguments?  
        if argdef[0]:
            positionalArgNames[mname] = argdef[0][:]
    return positionalArgNames

# def getApiArgsForMethod(methodName):
#     """ returns list with all api argument name for METHODNAME """
#     return _getMethodsArgDefinition(methodName)[1][:]


def getArgsForMethod(methodName, knownArgNames=[]):
    """ returns for METHODNAME additional arg names as a tuple with two lists 
        a) optional api arguments, not listed in knownArgNames
        b) additional mandatory non api arguments 
        
        raise TLArgError, if METHODNAME is not registered """ 
    
    # argument definitions in _apiMethodsArgs 
    argDef = _getMethodsArgDefinition(methodName)
    
    # find missing optional arg names
    apiArgsAll = argDef[1]
    apiArgs = [x for x in apiArgsAll if x not in knownArgNames]
    
    # other mandatory arg names
    manArgs = argDef[2][:]
    
    return (apiArgs, manArgs)
