#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013-2021 Luiko Czub, TestLink-API-Python-client developers
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

# TestCases for Testlink API calls, where the Api Clients uses equal 
# positional arg configurations
# - TestlinkAPIClient, TestlinkAPIGeneric
# 
# tests requires an online TestLink Server, which connection parameters
# are defined in environment variables
#     TESTLINK_API_PYTHON_DEVKEY and TESTLINK_API_PYTHON_DEVKEY
#
# FIXME LC 29.10.29: test does not really interacts with test link
#                    only negative test with none existing IDs implemented
#                    ok to check every implemented server call one time but not
#                    to cover all possible responses or argument combinations

import pytest
import re
from testlink.testlinkerrors import TLResponseError

# test_ApiCall_UnknownKey_EqualBehaviour

def test_checkDevKey(api_client):
    assert True == api_client.checkDevKey()
    
def test_checkDevKey_unknownKey(api_client):
    with pytest.raises(TLResponseError, match='2000.*invalid') as excinfo:
        api_client.checkDevKey(devKey='unknownKey')
 
def test_sayHello(api_client):
    assert 'Hello!' == api_client.sayHello()

def test_repeat(api_client):
    assert 'You said: Yellow Submarine' == api_client.repeat('Yellow Submarine')
     
def test_about(api_client):
    assert 'Testlink API' in api_client.about()

def test_doesUserExist_unknownID(api_client):
    with pytest.raises(TLResponseError, match='10000.*Big Bird'):
        api_client.doesUserExist('Big Bird')
      
def test_createTestProject_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7001.*Empty name'):
        api_client.createTestProject(testprojectname='', 
                                             testcaseprefix='P40000711')
 
def test_createTestProject_unknownITS(api_client):
    with pytest.raises(TLResponseError, match='13000.*Unable to find'):
        api_client.createTestProject(testprojectname='aProject', 
                            testcaseprefix='aPrefix', itsname='unknownITS')
 
def test_getProjects(api_client):
    assert None is not api_client.getProjects()
       
def test_createTestPlan_projectname_posArg_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7011.*40000712'):
        api_client.createTestPlan('plan 40000711', 'project 40000712')
 
def test_createTestSuite_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.createTestSuite( 40000711, 'suite 40000712', 'detail 40000713')

# see test_apicall_differentPositionalArgs    
# def test_createTestCase_unknownID(api_client):
#     tc_steps = []
#     with pytest.raises(TLResponseError, match='7000.*40000713'):
#         api_client.createTestCase('case 40000711', 40000712, 40000713, 
#                                     'Big Bird', 'summary 40000714', tc_steps)
 
def test_getBuildsForTestPlan_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getBuildsForTestPlan(40000711)
       
def test_getFirstLevelTestSuitesForTestProject_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.getFirstLevelTestSuitesForTestProject(40000711)
 
def test_getFullPath_unknownID(api_client):
    with pytest.raises(TLResponseError, match='getFullPath.*234'):
        api_client.getFullPath('40000711')
 
# see test_apicall_differentPositionalArgs   
# def test_getLastExecutionResult_unknownID(api_client):
#     with pytest.raises(TLResponseError, match='3000.*40000711'):
#         api_client.getLastExecutionResult(40000711, testcaseid=40000712)
       
def test_getLatestBuildForTestPlan_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getLatestBuildForTestPlan(40000711)
       
def test_getProjectTestPlans_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.getProjectTestPlans(40000711)
       
def test_getProjectPlatforms_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.getProjectPlatforms(40000711)
      
def test_getTestCase_unknownID(api_client):
    with pytest.raises(TLResponseError, match='5000.*40000711'):
        api_client.getTestCase(testcaseid=40000711)
       
def test_getTestCase_unknownExternalID(api_client):
    with pytest.raises(TLResponseError, match='5040.*GPROAPI-40000711'):
        api_client.getTestCase(testcaseexternalid='GPROAPI-40000711')
          
def test_getTestCaseAttachments_unknownID(api_client):
    with pytest.raises(TLResponseError, match='5000.*40000711'):
        api_client.getTestCaseAttachments(testcaseid=40000711)

# see test_apicall_differentPositionalArgs        
# def test_getTestCaseCustomFieldDesignValue_unknownID(api_client):
#     with pytest.raises(TLResponseError, match='7000.*40000711'):
#         api_client.getTestCaseCustomFieldDesignValue(
#                'TC-40000712', 1, 40000711, 'a_field', details='full')
       
def test_getTestCaseIDByName_unknownID(api_client):
    with pytest.raises(TLResponseError, match='5030.*Cannot find'):
        api_client.getTestCaseIDByName('Big Bird')
 
def test_getTestCasesForTestPlan_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getTestCasesForTestPlan(40000711)

# see test_apicall_differentPositionalArgs  
# def test_getTestCasesForTestSuite_unknownID(api_client):
#     with pytest.raises(TLResponseError, match='8000.*40000711'):
#         api_client.getTestCasesForTestSuite(40000711)
 
def test_getTestPlanByName_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7011.*40000711'):
        api_client.getTestPlanByName('project 40000711', 'plan 40000712')
 
def test_getTestPlanPlatforms_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getTestPlanPlatforms(40000711)
 
def test_getTestProjectByName_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7011.*40000711'):
        api_client.getTestProjectByName('project 40000711')
 
def test_getTestSuiteByID_unknownID(api_client):
    with pytest.raises(TLResponseError, match='8000.*40000711'):
        api_client.getTestSuiteByID(40000711)
 
def test_getTestSuitesForTestPlan_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getTestSuitesForTestPlan(40000711)
 
def test_getTestSuitesForTestSuite_unknownID(api_client):
    with pytest.raises(TLResponseError, match='8000.*40000711'):
        api_client.getTestSuitesForTestSuite(40000711)
 
def test_getTotalsForTestPlan_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getTotalsForTestPlan(40000711)
 
# see test_apicall_differentPositionalArgs 
# def test_createBuild_unknownID(api_client):
#     with pytest.raises(TLResponseError, match='3000.*40000711'):
#         api_client.createBuild(40000711, 'Build 40000712', buildnotes='note 40000713')
 
# see test_apicall_differentPositionalArgs 
# def test_reportTCResult_unknownID(api_client):
#     with pytest.raises(TLResponseError, match='5000.*40000711'):
#         api_client.reportTCResult(40000712, 'p', testcaseid=40000711, 
#                                    buildname='build 40000713', notes='note 40000714' )

# see test_apicall_differentPositionalArgs  
# def test_uploadExecutionAttachment_unknownID(api_client, attachmentFile):
#     with pytest.raises(TLResponseError, match='6004.*40000712'):
#         api_client.uploadExecutionAttachment(attachmentFile, 40000712, 
#                     title='title 40000713', description='descr. 40000714')
 
def test_createPlatform_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7011.*40000711'):
        api_client.createPlatform('Project 40000711', 'Platform 40000712', 
                                   notes='note 40000713',
                                   platformondesign=True,
                                   platformonexecution=True)
          
def test_addPlatformToTestPlan_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.addPlatformToTestPlan(40000711, 'Platform 40000712')
          
def test_removePlatformFromTestPlan_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.removePlatformFromTestPlan(40000711, 'Platform 40000712')
          
def test_addTestCaseToTestPlan_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.addTestCaseToTestPlan(40000711, 40000712, 'N-40000713', 1)
          
def test_updateTestCase_unknownID(api_client):
    with pytest.raises(TLResponseError, match='5040.*N-40000711'):
        api_client.updateTestCase('N-40000711', version=1)
      
def test_createTestCaseSteps_unknownID(api_client):
    steps = [{'actions' : "Step action 6 -b added by updateTestCase" , 
              'expected_results' : "Step result 6 - b added", 
              'step_number' : 6, 'execution_type' : 1}]
    with pytest.raises(TLResponseError, match='5040.*N-40000711'):
        api_client.createTestCaseSteps('update', steps, 
                                    testcaseexternalid='N-40000711', version=1)
          
def test_deleteTestCaseSteps_unknownID(api_client):
    steps = [2,8]
    with pytest.raises(TLResponseError, match='5040.*N-40000711'):
        api_client.deleteTestCaseSteps('N-40000711', steps, version=1)
          
def test_uploadRequirementSpecificationAttachment_unknownID(api_client, attachmentFile):
    with pytest.raises(TLResponseError, match='6004.*40000712'):
        api_client.uploadRequirementSpecificationAttachment(attachmentFile, 40000712, 
                    title='title 40000713', description='descr. 40000714')
 
def test_uploadRequirementAttachment_unknownID(api_client, attachmentFile):
    with pytest.raises(TLResponseError, match='6004.*40000712'):
        api_client.uploadRequirementAttachment(attachmentFile, 40000712, 
                    title='title 40000713', description='descr. 40000714')
 
def test_uploadTestProjectAttachment_unknownID(api_client, attachmentFile):
    with pytest.raises(TLResponseError, match='7000.*40000712'):
        api_client.uploadTestProjectAttachment(attachmentFile, 40000712, 
                    title='title 40000713', description='descr. 40000714')
 
def test_uploadTestSuiteAttachment_unknownID(api_client, attachmentFile):
    with pytest.raises(TLResponseError, match='8000.*40000712'):
        api_client.uploadTestSuiteAttachment(attachmentFile, 40000712, 
                    title='title 40000713', description='descr. 40000714')
 
def test_uploadTestCaseAttachment_unknownID(api_client, attachmentFile):
    with pytest.raises(TLResponseError, match='5000.*testcaseid'):
        api_client.uploadTestCaseAttachment(attachmentFile, 40000712, 1,
                    title='title 40000713', description='descr. 40000714')
 
def test_uploadAttachment_unknownID(api_client, attachmentFile):
    with pytest.raises(TLResponseError, match='6004.*Invalid Foreign Key ID'):
        api_client.uploadAttachment(attachmentFile, '0000', 'nodes_hierarchy',
                    title='title 40000713', description='descr. 40000714')
 
def test_testLinkVersion(api_client):
    assert re.match(r'\d*\.\d*\.\d*', api_client.testLinkVersion() )
 
def test_getUserByLogin_unknownKey(api_client):
    with pytest.raises(TLResponseError, match='10000.*User Login'):
        api_client.getUserByLogin('unknownUser')
          
def test_getUserByID_unknownKey(api_client):
     with pytest.raises(TLResponseError, match='NO_USER_BY_ID_LOGIN.*User with DB ID'):
        api_client.getUserByID(40000711)

@pytest.mark.xfail(reason='setTestMode not implemented for python client' )
def test_setTestMode(api_client):
    assert api_client.setTestMode(True)
    assert not api_client.setTestMode(False)
 
def test_deleteExecution_unknownKey(api_client):
    try:
        # case: TL configuration allows deletion of executions
        # response returns Success, even if executionID is unkown
        expected = [{'status': True, 'message': 'Success!', 'id': 40000711, 
                           'operation': 'deleteExecution'}]
        assert expected == api_client.deleteExecution(40000711)
    except TLResponseError as tl_err:
        # case: TL configuration does not allow deletion of executions
        # Expects: 232: Configuration does not allow delete executions
        assert 232 == tl_err.code
 
def test_setTestCaseExecutionType_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000712'):
        api_client.setTestCaseExecutionType('N-40000711', 1, 40000712, 1)
          
def test_assignRequirements_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000712'):
        api_client.assignRequirements('N-40000711', 40000712, 
                    [{'req_spec' : 40000713, 'requirements' : [40000714, 40000717]}, 
                     {'req_spec' : 4723, 'requirements' : [4725]}])
          
def test_getExecCountersByBuild_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getExecCountersByBuild(40000711)
          
def test_getTestCaseCustomFieldExecutionValue_unknownID(api_client):
    with pytest.raises(TLResponseError, match='236.*version/executionid'):
        api_client.getTestCaseCustomFieldExecutionValue(
                        'cf_full', '40000711', 1, '715', '40000713')
          
def test_getTestCaseCustomFieldTestPlanDesignValue_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.getTestCaseCustomFieldTestPlanDesignValue(
                        'cf_full', '40000711', 1, '40000713', '615')
          
def test_updateTestCaseCustomFieldDesignValue_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.updateTestCaseCustomFieldDesignValue(
                        'TC-40000712', 1, 40000711, {'cf_field1' : 'value1',
                                             'cf_field2' : 'value2'})
 
def test_getTestSuiteCustomFieldDesignValue_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.getTestSuiteCustomFieldDesignValue(
                                                'cf_full', 40000711, 40000713) 
          
def test_getTestPlanCustomFieldDesignValue_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.getTestPlanCustomFieldDesignValue(
                                                'cf_full', 40000711, 40000712)             
 
def test_getReqSpecCustomFieldDesignValue_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.getReqSpecCustomFieldDesignValue(
                                                'cf_full', 40000711, 4732)             
 
def test_getRequirementCustomFieldDesignValue_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.getRequirementCustomFieldDesignValue(
                                                'cf_full', 40000711, 4734)  
          
def test_assignTestCaseExecutionTask_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.assignTestCaseExecutionTask('username', 40000711, 'TC-40000712', 
                                        buildname='build 40000713', 
                                        platformname='platform 40000714') 
            
def test_getTestCaseBugs_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getTestCaseBugs(40000711, testcaseexternalid='TC-40000712', 
                                    buildname='build 40000713',
                                    platformname='platform 40000714')                         
 
def test_getTestCaseAssignedTester_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getTestCaseAssignedTester(40000711, 'TC-40000712', 
                                        buildname='build 40000713', 
                                        platformname='platform 40000714') 
            
def test_unassignTestCaseExecutionTask_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.unassignTestCaseExecutionTask(40000711, 'TC-40000712', 
                                    buildname='build 40000713', 
                                    platformname='platform 40000714',
                                    user='username',action='unassignOne') 
  
def test_getProjectKeywords_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.getProjectKeywords(40000711) 
 
def test_getTestCaseKeywords_unknownID(api_client):
    with pytest.raises(TLResponseError, match='5040.*40000712'):
        api_client.getTestCaseKeywords(testcaseid=40000712) 
 
def test_getTestCaseKeywords_unknownID_set(api_client):
    with pytest.raises(TLResponseError, match='5040.*40000712'):
        api_client.getTestCaseKeywords(testcaseid=[40000712, 40000713]) 
 
def test_getTestCaseKeywords_unknownID_external_single(api_client):
    with pytest.raises(TLResponseError, match='5040.*TC-40000712'):
        api_client.getTestCaseKeywords(testcaseexternalid='TC-40000712')
          
def test_getTestCaseKeywords_unknownID_external_set(api_client):
    with pytest.raises(TLResponseError, match='5040.*TC-40000712'):
        api_client.getTestCaseKeywords(testcaseexternalid=['TC-40000712', 'TC-40000713'])
 
def test_deleteTestPlan_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.deleteTestPlan(40000711) 
 
def test_addTestCaseKeywords_unknownID(api_client):
    with pytest.raises(TLResponseError, match='5040.*TC-40000712'):
        api_client.addTestCaseKeywords({'TC-40000712' :  
                                         ['KeyWord01', 'KeyWord03']}) 
 
def test_removeTestCaseKeywords_unknownID(api_client):
    with pytest.raises(TLResponseError, match='5040.*TC-40000712'):
        api_client.removeTestCaseKeywords({'TC-40000712' : ['KeyWord01']}) 
 
def test_deleteTestProject_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7013.*TProjectPrefix'):
        api_client.deleteTestProject('TProjectPrefix') 
 
def test_createTestPlan_projectname_optArg_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7011.*40000712'):
        api_client.createTestPlan('plan 40000711', 
                                   testprojectname='project 40000712')
 
def test_createTestPlan_prefix_unknownID(api_client):
    with pytest.raises(TLResponseError, match='NO.*TProjectPrefix'):
        api_client.createTestPlan('plan 40000713', 
                                   prefix='TProjectPrefix')
 
def test_updateTestSuiteCustomFieldDesignValue_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000712'):
        api_client.updateTestSuiteCustomFieldDesignValue(
                        '40000712 TP-ID', '40000711 TS-ID',  
                        {'cf_tc_ex_string' : 'a custom exec value', 
                         'cf_tc_ex_numeric' : 111} )
 
def test_getTestSuite_unknownID(api_client):
    with pytest.raises(TLResponseError, match='NO.*TProjectPrefix'):
        api_client.getTestSuite('suite 40000712', 'TProjectPrefix')
          
 
def test_updateTestSuite_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000711'):
        api_client.updateTestSuite(40000712, testprojectid=40000711, 
                                testsuitename = 'suite 40000712 updated',
                                details = 'detail 40000713 updated',
                                order =1)
          
def test_getIssueTrackerSystem_unknownITS(api_client):
    with pytest.raises(TLResponseError, match='13000.*Unable to find'):
        api_client.getIssueTrackerSystem('unknownITS')
 
def test_updateBuildCustomFieldsValues_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000712'):
        api_client.updateBuildCustomFieldsValues(
                        '40000712 project', '40000713 plan', '40000714 build', 
                        {'cf_b_ex_string' : 'a custom exec value', 
                         'cf_b_ex_numeric' : 111} )
          
def test_getExecutionSet_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000713'):
        api_client.getExecutionSet(
                        '40000713 plan', testcaseexternalid = 'TC-40000712')
       
def test_getRequirements_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000712'):
        api_client.getRequirements(
                        '40000712 project', 
                        testplanid = '40000713 plan', 
                        platformid = '40000714 platform')
       
def test_getReqCoverage_unknownID(api_client):
    with pytest.raises(TLResponseError, match='7000.*40000712'):
        api_client.getReqCoverage(
                        '40000712 project', '40000721 req')
       
def test_setTestCaseTestSuite_unknownID(api_client):
    with pytest.raises(TLResponseError, match='5040.*TC-40000712'):
        api_client.setTestCaseTestSuite(
                        'TC-40000712', '40000713 suite')
 
def test_getTestSuiteAttachments_unknownID(api_client):
    with pytest.raises(TLResponseError, match='8000.*40000712'):
        api_client.getTestSuiteAttachments(40000712)
       
def test_getAllExecutionsResults_unknownID(api_client):
    with pytest.raises(TLResponseError, match='3000.*40000711'):
        api_client.getAllExecutionsResults(40000711)

def test_closeBuild_unknownID(api_client):
    with pytest.raises(TLResponseError, match='4000.*40000713'):
        api_client.closeBuild(40000713)

def test_createUser_invalidMail(api_client):
    with pytest.raises(TLResponseError, match='14003: Email.*seems no good'):
        api_client.createUser('myLogin','myFname','myLname', 'myInvalidMail')


# if __name__ == "__main__":
# #import sys;sys.argv = ['', 'Test.testName']
# unittest.main()