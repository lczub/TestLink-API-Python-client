#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2018-2021 Luiko Czub, TestLink-API-Python-client developers
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

# TestCases for Testlink API clients whatArgs calls
# - TestlinkAPIClient, TestlinkAPIGeneric
# 

import pytest
import re

def test_whatArgs_noArgs(api_client):
    response = api_client.whatArgs('sayHello')
    assert re.match('sayHello().*', response)
    
def test_whatArgs_onlyOptionalArgs(api_client):
    response = api_client.whatArgs('getTestCaseKeywords')
    assert re.match(r'getTestCaseKeywords\(\[.*=<.*>\].*\).*',
                    response)
     
def test_whatArgs_OptionalAndPositionalArgs(api_client):
    response = api_client.whatArgs('createBuild')
    assert re.match(r'createBuild\(<.*>.*\).*', response)
 
def test_whatArgs_MandatoryArgs(api_client):
    response = api_client.whatArgs('uploadExecutionAttachment')
    assert re.match(r'uploadExecutionAttachment\(<attachmentfile>, <.*>.*\).*',
                    response)
 
def test_whatArgs_unknownMethods(api_client):
    response = api_client.whatArgs('apiUnknown')
    assert re.match(r"callServerWithPosArgs\('apiUnknown', \[apiArg=<apiArg>\]\)", 
                    response)

test_data_apiCall_descriptions_equal_all = [
    ('getTestCasesForTestSuite', ['getkeywords=<getkeywords>']),
    ('reportTCResult', ['user=<user>', 'execduration=<execduration>', 
                        'timestamp=<timestamp>', 'steps=<steps>', 
                        "[{'step_number' : 6,"]),
    ('getLastExecutionResult', ['options=<options>','getBugs']),
    ('getTestCasesForTestPlan', ['<testplanid>,', 
                        'buildid=<buildid>', 'platformid=<platformid>', 
                        'testcaseid=<testcaseid>', 'keywordid=<keywordid>', 
                        'keywords=<keywords>', 'executed=<executed>',
                        'assignedto=<assignedto>', 'executestatus=<executestatus>',
                        'executiontype=<executiontype>', 'getstepinfo=<getstepinfo>',
                        'details=<details>', 'customfields=<customfields>', 
                        'keywordid - keywords']),
    ('createTestCase', ['<testcasename>,', '<testsuiteid>,', '<testprojectid>,', 
                        '<authorlogin>,', '<summary>,', #'<steps>,', 
                        'preconditions=<preconditions>', 
                        'importance=<importance>', 
                        'executiontype=<executiontype>', 'order=<order>', 
                        'internalid=<internalid>', 
                        'checkduplicatedname=<checkduplicatedname>', 
                        'actiononduplicatedname=<actiononduplicatedname>', 
                        'status=<status>', 
                        'estimatedexecduration=<estimatedexecduration>']),
    ('createTestPlan', ['prefix=<prefix>', 'testprojectname=<testprojectname>']),
    ('getTestSuite',['<testsuitename>', '<prefix>']),
    ('updateTestSuite',['<testsuiteid>,', 'testprojectid=<testprojectid>', 
                        'prefix=<prefix>', 'parentid=<parentid>', 
                        'testsuitename=<testsuitename>', 'details=<details>', 
                        'order=<order>']),
    ('createBuild',['<testplanid>,', '<buildname>,', 'active=<active>', 
                    'copytestersfrombuild=<copytestersfrombuild>']),
    ('addTestCaseToTestPlan',['<testprojectid>,', '<testplanid>,', 
                              '<testcaseexternalid>,', '<version>,', 
                              'platformid=<platformid>', 
                              'executionorder=<executionorder>', 
                              'urgency=<urgency>', 'overwrite=<overwrite>']),
    ('createTestProject',['<testprojectname>,', '<testcaseprefix>,', 
                          'notes=<notes>', 'active=<active>', 
                          'public=<public>', 'options=<options>', 
                          'itsname=<itsname>', 'itsenabled=<itsenabled>']),
    ('getIssueTrackerSystem',['<itsname>,']),
    ('getExecutionSet',['<testplanid>,', 'testcaseid=<testcaseid>', 
                        'testcaseexternalid=<testcaseexternalid>', 
                        'buildid=<buildid>', 'buildname=<buildname>', 
                        'platformid=<platformid>', 
                        'platformname=<platformname>', 'options=<options>']),
    ('getRequirements',['<testprojectid>,', 'testplanid=<testplanid>', 
                        'platformid=<platformid>']),
    ('getReqCoverage',['<testprojectid>,', '<requirementdocid>,']),
    ('setTestCaseTestSuite',['<testcaseexternalid>,', '<testsuiteid>,']),
    ('getTestSuiteAttachments',['<testsuiteid>,']),
    ('getAllExecutionsResults',['<testplanid>,','testcaseid=<testcaseid>', 
                        'testcaseexternalid=<testcaseexternalid>', 
                        'platformid=<platformid>', 'buildid=<buildid>',
                        'options=<options>']),
    ('getTestCaseAttachments',['version=<version>', 
                               'testcaseexternalid=<testcaseexternalid>']),
    ('uploadTestCaseAttachment',['<testcaseid>,', '<version>,', 
                               'title=<title>', 'description=<description>',
                               'filename=<filename>', 'filetype=<filetype>',
                               'content=<content>']),
    ('createPlatform',['<testprojectname>,', '<platformname>,', 'notes=<notes>', 
                       'platformondesign=<platformondesign>', 
                       'platformonexecution=<platformonexecution>']),
    ('closeBuild', ['<buildid>']),
    ('createUser', ['<login>', '<firstname>', '<lastname>', '<email>', 
                    'password=<password>']),
    ('setUserRoleOnProject', ['<userid>', '<rolename>', '<testprojectid>'])
    ]

@pytest.mark.parametrize("apiCall, descriptions", 
                         test_data_apiCall_descriptions_equal_all)     
def test_whatArgs_apiCall_descriptions_equal_all(api_client, apiCall, descriptions):
    argsDescription = api_client.whatArgs(apiCall)
    for parts in descriptions:
        assert parts in argsDescription
 
test_data_apiCall_descriptions_only_generic = [
    ('createTestCase', ['<steps>,']),
    ('createBuild',['buildnotes=<buildnotes>']),
    ('getTestCaseAttachments',['testcaseid=<testcaseid>'])
    ]
@pytest.mark.parametrize("apiCall, descriptions", 
                         test_data_apiCall_descriptions_only_generic)     
def test_whatArgs_apiCall_descriptions_only_generic(api_generic_client, apiCall, descriptions):
    argsDescription = api_generic_client.whatArgs(apiCall)
    for parts in descriptions:
        assert parts in argsDescription

test_data_apiCall_descriptions_only_general = [
    ('createTestCase', ['steps=<steps>']),
    ('createBuild',['<buildnotes>,']),
    ('getTestCaseAttachments',['<testcaseid>,'])
    ]
@pytest.mark.parametrize("apiCall, descriptions", 
                         test_data_apiCall_descriptions_only_general)     
def test_whatArgs_apiCall_descriptions_only_general(api_general_client, apiCall, descriptions):
    argsDescription = api_general_client.whatArgs(apiCall)
    for parts in descriptions:
        assert parts in argsDescription
         
        