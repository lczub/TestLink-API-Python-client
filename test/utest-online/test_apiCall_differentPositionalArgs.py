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

# TestCases for Testlink API calls, where the Api Clients uses different 
# positional arg configurations 
# - TestlinkAPIClient, TestlinkAPIGeneric
# 
#
# this test requires an online TestLink Server, which connection parameters
# are defined in environment variables
#     TESTLINK_API_PYTHON_DEVKEY and TESTLINK_API_PYTHON_DEVKEY
#
# FIME LC 29.10.29: test does not really interacts with test link
#                   only negative test with none existing IDs implemented
#                   ok to check every implemented server call one time but not
#                   to cover all possible responses or argument combinations

import pytest
from testlink.testlinkerrors import TLResponseError

class Test_TestlinkAPIClient_Behaviour():
    ''' Test api call with positional arg configuration TestlinkAPIClient '''
  
    def test_getLastExecutionResult_unknownID(self, api_general_client):
        with pytest.raises(TLResponseError, match='3000.*40000711'):
            api_general_client.getLastExecutionResult(40000711, 40000712)
  
    def test_getTestCaseCustomFieldDesignValue_unknownID(self, api_general_client):
        with pytest.raises(TLResponseError, match='7000.*40000711'):
            api_general_client.getTestCaseCustomFieldDesignValue(
                   'TC-40000712', 1, 40000711, 'a_field', 'a_detail')
  
    def test_getTestCasesForTestSuite_unknownID(self, api_general_client):
        with pytest.raises(TLResponseError, match='8000.*40000711'):
            api_general_client.getTestCasesForTestSuite(40000711, 2, 'a_detail')
  
    def test_createBuild_unknownID(self, api_general_client):
        with pytest.raises(TLResponseError, match='3000.*40000711'):
            api_general_client.createBuild(40000711, 'Build 40000712', 'note 40000713')
  
    def test_createTestCase_unknownID(self, api_general_client):
        with pytest.raises(TLResponseError, match='7000.*40000713'):
            api_general_client.createTestCase('case 40000711', 40000712, 40000713, 
                                               'Big Bird', 'summary 40000714')
  
    def test_reportTCResult_unknownID(self, api_general_client):
        with pytest.raises(TLResponseError, match='5000.*40000711'):
            api_general_client.reportTCResult(40000711, 40000712, 'build 40000713', 'p', 
                                              'note 40000714')
  
    def test_uploadExecutionAttachment_unknownID(self, api_general_client, attachmentFile):
        with pytest.raises(TLResponseError, match='6004.*40000712'):
            api_general_client.uploadExecutionAttachment(attachmentFile, 40000712, 
                        'title 40000713', 'descr. 40000714')

class Test_TestlinkAPIGeneric_Behaviour():
    ''' Test api call with positional arg configuration TestlinkAPIGeneric '''
 
    def test_getLastExecutionResult_unknownID(self, api_generic_client):
        with pytest.raises(TLResponseError, match='3000.*40000711'):
            api_generic_client.getLastExecutionResult(40000711, testcaseid=40000712)
 
    def test_getTestCaseCustomFieldDesignValue_unknownID(self, api_generic_client):
        with pytest.raises(TLResponseError, match='7000.*40000711'):
            api_generic_client.getTestCaseCustomFieldDesignValue(
                   'TC-40000712', 1, 40000711, 'a_field', details='full')
 
    def test_getTestCasesForTestSuite_unknownID(self, api_generic_client):
        with pytest.raises(TLResponseError, match='8000.*40000711'):
            api_generic_client.getTestCasesForTestSuite(40000711)
 
    def test_createBuild_unknownID(self, api_generic_client):
        with pytest.raises(TLResponseError, match='3000.*40000711'):
            api_generic_client.createBuild(40000711, 'Build 40000712', buildnotes='note 40000713')
 
    def test_createTestCase_unknownID(self, api_generic_client):
        tc_steps = []
        with pytest.raises(TLResponseError, match='7000.*40000713'):
            api_generic_client.createTestCase('case 40000711', 40000712, 40000713, 
                                        'Big Bird', 'summary 40000714', tc_steps)
 
    def test_reportTCResult_unknownID(self, api_generic_client):
        with pytest.raises(TLResponseError, match='5000.*40000711'):
            api_generic_client.reportTCResult(40000712, 'p', testcaseid=40000711, 
                                       buildname='build 40000713', notes='note 40000714' )
 
    def test_uploadExecutionAttachment_unknownID(self, api_generic_client, attachmentFile):
        with pytest.raises(TLResponseError, match='6004.*40000712'):
            api_generic_client.uploadExecutionAttachment(attachmentFile, 40000712, 
                        title='title 40000713', description='descr. 40000714')

