#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2018 Luiko Czub, TestLink-API-Python-client developers
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
    assert re.match('getTestCaseKeywords\(\[.*=<.*>\].*\).*',
                    response)
     
def test_whatArgs_OptionalAndPositionalArgs(api_client):
    response = api_client.whatArgs('createBuild')
    assert re.match('createBuild\(<.*>.*\).*', response)
 
def test_whatArgs_MandatoryArgs(api_client):
    response = api_client.whatArgs('uploadExecutionAttachment')
    assert re.match('uploadExecutionAttachment\(<attachmentfile>, <.*>.*\).*',
                    response)
 
def test_whatArgs_unknownMethods(api_client):
    response = api_client.whatArgs('apiUnknown')
    assert re.match("callServerWithPosArgs\('apiUnknown', \[apiArg=<apiArg>\]\)", 
                    response)

test_data_apiCall_descriptions_equal_all = [
    ('getTestCasesForTestSuite', ['getkeywords=<getkeywords>']),
    ('reportTCResult', ['user=<user>', 'execduration=<execduration>', 
                        'timestamp=<timestamp>', 'steps=<steps>', 
                        "[{'step_number' : 6,"]),
    ('getLastExecutionResult', ['options=<options>','getBugs']),
    ('getTestCasesForTestPlan', ['buildid=<buildid>', 'platformid=<platformid>', 
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
    ('getTestSuiteAttachments',['<testsuiteid>,'])
    ]

@pytest.mark.parametrize("apiCall, descriptions", 
                         test_data_apiCall_descriptions_equal_all)     
def test_whatArgs_apiCall_descriptions_equal_all(api_client, apiCall, descriptions):
    argsDescription = api_client.whatArgs(apiCall)
    for parts in descriptions:
        assert parts in argsDescription
 
test_data_apiCall_descriptions_only_generic = [
    ('createTestCase', ['<steps>,']),
    ('createBuild',['buildnotes=<buildnotes>'])
    ]
@pytest.mark.parametrize("apiCall, descriptions", 
                         test_data_apiCall_descriptions_only_generic)     
def test_whatArgs_apiCall_descriptions_only_generic(api_generic_client, apiCall, descriptions):
    argsDescription = api_generic_client.whatArgs(apiCall)
    for parts in descriptions:
        assert parts in argsDescription

test_data_apiCall_descriptions_only_general = [
    ('createTestCase', ['steps=<steps>']),
    ('createBuild',['<buildnotes>,'])
    ]
@pytest.mark.parametrize("apiCall, descriptions", 
                         test_data_apiCall_descriptions_only_general)     
def test_whatArgs_apiCall_descriptions_only_general(api_general_client, apiCall, descriptions):
    argsDescription = api_general_client.whatArgs(apiCall)
    for parts in descriptions:
        assert parts in argsDescription
         
# 
# def test_whatArgs_createTestPlan(api_client):
#     argsDescription = api_client.whatArgs('createTestPlan')
#     self.assertIn('prefix=<prefix>', argsDescription)
#     self.assertIn('testprojectname=<testprojectname>', argsDescription)
# 
# def test_whatArgs_getTestSuite(api_client):
#     argsDescription = api_client.whatArgs('getTestSuite')
#     self.assertIn('<testsuitename>, <prefix>', argsDescription)
#     
# def test_whatArgs_updateTestSuite(api_client):
#     argsDescription = api_client.whatArgs('updateTestSuite')
#     self.assertIn('<testsuiteid>,', argsDescription)
#     self.assertIn('testprojectid=<testprojectid>', argsDescription)
#     self.assertIn('prefix=<prefix>', argsDescription)
#     self.assertIn('parentid=<parentid>', argsDescription)
#     self.assertIn('testsuitename=<testsuitename>', argsDescription)
#     self.assertIn('details=<details>', argsDescription)
#     self.assertIn('order=<order>', argsDescription)
# 
# def test_whatArgs_createBuild(api_client):
#     argsDescription = api_client.whatArgs('createBuild')
#     self.assertIn('<testplanid>,', argsDescription)
#     self.assertIn('<buildname>,', argsDescription)
#     self.assertIn('buildnotes=<buildnotes>', argsDescription)
#     self.assertIn('active=<active>', argsDescription)
#     self.assertIn('open=<open>', argsDescription)
#     self.assertIn('releasedate=<releasedate>', argsDescription)
#     self.assertIn('copytestersfrombuild=<copytestersfrombuild>', argsDescription)
# 
# def test_whatArgs_addTestCaseToTestPlan(api_client):
#     argsDescription = api_client.whatArgs('addTestCaseToTestPlan')
#     self.assertIn('<testprojectid>,', argsDescription)
#     self.assertIn('<testplanid>,', argsDescription)
#     self.assertIn('<testcaseexternalid>,', argsDescription)
#     self.assertIn('<version>,', argsDescription)
#     self.assertIn('platformid=<platformid>', argsDescription)
#     self.assertIn('executionorder=<executionorder>', argsDescription)
#     self.assertIn('urgency=<urgency>', argsDescription)
#     self.assertIn('overwrite=<overwrite>', argsDescription)
#            
# def test_whatArgs_createTestProject(api_client):
#     argsDescription = api_client.whatArgs('createTestProject')
#     self.assertIn('<testprojectname>,', argsDescription)
#     self.assertIn('<testcaseprefix>,', argsDescription)
#     self.assertIn('notes=<notes>', argsDescription)
#     self.assertIn('active=<active>', argsDescription)
#     self.assertIn('public=<public>', argsDescription)
#     self.assertIn('options=<options>', argsDescription)
#     self.assertIn('itsname=<itsname>', argsDescription)
#     self.assertIn('itsenabled=<itsenabled>', argsDescription)
# 
# def test_whatArgs_getIssueTrackerSystem(api_client):
#     argsDescription = api_client.whatArgs('getIssueTrackerSystem')
#     self.assertIn('<itsname>,', argsDescription)
# 
# def test_whatArgs_getExecutionSet(api_client):
#     argsDescription = api_client.whatArgs('getExecutionSet')
#     self.assertIn('<testplanid>,', argsDescription)
#     self.assertIn('testcaseid=<testcaseid>', argsDescription)
#     self.assertIn('testcaseexternalid=<testcaseexternalid>', argsDescription)
#     self.assertIn('buildid=<buildid>', argsDescription)
#     self.assertIn('buildname=<buildname>', argsDescription)
#     self.assertIn('platformid=<platformid>', argsDescription)
#     self.assertIn('platformname=<platformname>', argsDescription)
#     self.assertIn('options=<options>', argsDescription)
#     
# def test_whatArgs_getRequirements(api_client):
#     argsDescription = api_client.whatArgs('getRequirements')
#     self.assertIn('<testprojectid>,', argsDescription)
#     self.assertIn('testplanid=<testplanid>', argsDescription)
#     self.assertIn('platformid=<platformid>', argsDescription)
#     
# def test_whatArgs_getReqCoverage(api_client):
#     argsDescription = api_client.whatArgs('getReqCoverage')
#     self.assertIn('<testprojectid>,', argsDescription)
#     self.assertIn('<requirementdocid>,', argsDescription)
# 
# def test_whatArgs_setTestCaseTestSuite(api_client):
#     argsDescription = api_client.whatArgs('setTestCaseTestSuite')
#     self.assertIn('<testcaseexternalid>,', argsDescription)
#     self.assertIn('<testsuiteid>,', argsDescription)
#     
# def test_whatArgs_getTestSuiteAttachments(api_client):
#     argsDescription = api_client.whatArgs('getTestSuiteAttachments')
#     self.assertIn('<testsuiteid>,', argsDescription)

        