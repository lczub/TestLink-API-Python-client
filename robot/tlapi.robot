#  Copyright 2014-2019 Luiko Czub
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

*** Settings ***
Documentation     Smoke tests for Library TestlinkAPILibrary
...               
...               TestlinkAPILibrary is a wrapper for calling 
...               Testlink XMLRPC api methods  via *Testlink-API-Python-client*
...               classes _TestlinkAPIClient_ and _TestlinkAPIGeneric_. 
Force Tags        api
Default Tags      general
Library           TestlinkAPILibrary
Library           Collections

*** Variables ***

*** Test Cases ***
Init Api Class TestLinkAPIClient
    ${tlapi_client}=    Create Api Client    TestlinkAPIClient
    ${method_args}=    Call Method    ${tlapi_client}    whatArgs    repeat
    Should Contain    ${method_args}    Repeats a message back
    Should Be Equal As Strings    ${tlapi_client.__class__.__name__}    TestlinkAPIClient

Init Api Class TestlinkAPIGeneric
    ${tlapi_client}=    Create Api Client    TestlinkAPIGeneric
    ${method_args}=    Call Method    ${tlapi_client}    whatArgs    repeat
    Should Contain    ${method_args}    Repeats a message back
    Should Be Equal As Strings    ${tlapi_client.__class__.__name__}    TestlinkAPIGeneric

Call Api Method without arguments
    ${response}=    Call Api Method    sayHello
    Should Be Equal As Strings    ${response}    Hello!

Call Api Method with mandatory argument
    ${response}=    Call Api Method    repeat    Hugo
    Should Be Equal As Strings    ${response}    You said: Hugo

Call Api Method with optional arguments
    [Tags]    devexample
    @{response1}=    Call Api Method    getTestCaseIDByName    TESTCASE_B
    Should Not Be Empty    ${response1}
    @{response2}=    Call Api Method    getTestCaseIDByName    TESTCASE_B    testprojectname=PROJECT_API_GENERIC-10
    Should Not Be Empty    ${response2}
