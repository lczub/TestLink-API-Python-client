#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013-2019 Luiko Czub, TestLink-API-Python-client developers
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


"""

Shows how to use the TestLinkAPI for custom fields
This example requires a special existing project with special custom fields 
assigned

a) run example TestLinkExample.py
   - this creates a project like NEW_PROJECT_API-37
b) load custom field definitions customFields_ExampleDefs.xml
   TL - Desktop - System - Define Custom Fields - Import
c) assign custom fields to project NEW_PROJECT_API-37
   TL - Desktop - Test Project - Assign Custom Fields
d) load keyword definitions keywords_ExampleDefs.xml
   TL - Desktop - Test Project - Keyword Management
   
Script works with:

TestProject NEW_PROJECT_API-37
- TestSuite B - First Level
  - TestCase TESTCASE_B
- TestPlan TestPlan_API A (Platform Small Bird)
  - Build TestlinkAPIClient v0.x.y
  
Script creates custom values for TestCase TESTCASE_B
- scope test specification and test execution

Script returns custom field values from TestPlan and TestSuite, if the user has 
added manually some values.

Cause of missing knowledge, how ids of kind
- requirement and requirement specifications
- testplan - testcase link
could be requested via api, these example does not work currently. 

Script adds keywords KeyWord01 KeyWord02 KeyWord03 to test case TESTCASE_B,
removes keyword KeyWord02 again.

Script adds keywords KeyWord01 KeyWord02 to test case TESTCASE_AA,
removes keyword KeyWord01 again.
   
"""                                       
from testlink import TestlinkAPIClient, TestLinkHelper
from testlink.testlinkerrors import TLResponseError
import sys, os.path
from platform import python_version  

# precondition a)
# SERVER_URL and KEY are defined in environment
# TESTLINK_API_PYTHON_SERVER_URL=http://YOURSERVER/testlink/lib/api/xmlrpc.php
# TESTLINK_API_PYTHON_DEVKEY=7ec252ab966ce88fd92c25d08635672b
# 
# alternative precondition b)
# SERVEUR_URL and KEY are defined as command line arguments
# python TestLinkExample.py --server_url http://YOURSERVER/testlink/lib/api/xmlrpc.php
#                           --devKey 7ec252ab966ce88fd92c25d08635672b
#
# ATTENTION: With TestLink 1.9.7, cause of the new REST API, the SERVER_URL 
#            has changed from 
#               (old) http://YOURSERVER/testlink/lib/api/xmlrpc.php
#            to
#               (new) http://YOURSERVER/testlink/lib/api/xmlrpc/v1/xmlrpc.php
tl_helper = TestLinkHelper()
tl_helper.setParamsFromArgs('''Shows how to use the TestLinkAPI for CustomFields.
=> requires an existing project NEW_PROJECT_API-*''')
myTestLink = tl_helper.connect(TestlinkAPIClient) 

myPyVersion = python_version()
myPyVersionShort = myPyVersion.replace('.', '')[:2]

NEWTESTPLAN_A="TestPlan_API A"
# NEWTESTPLAN_B="TestPlan_API B"
# NEWTESTPLAN_C="TestPlan_API C - DeleteTest"
# NEWPLATFORM_A='Big Birds %s' % myPyVersionShort
NEWPLATFORM_B='Small Birds'
# NEWPLATFORM_C='Ugly Birds'
NEWTESTSUITE_A="A - First Level"
NEWTESTSUITE_B="B - First Level"
NEWTESTSUITE_AA="AA - Second Level"
NEWTESTCASE_AA="TESTCASE_AA"
NEWTESTCASE_B="TESTCASE_B"
# myApiVersion='%s v%s' % (myTestLink.__class__.__name__ , myTestLink.__version__)
# NEWBUILD_A='%s' % myApiVersion
# NEWBUILD_B='%s' % myApiVersion
# NEWBUILD_C='%s - DeleteTest' % myApiVersion
# NEWBUILD_D='%s - copyTestersTest' % myApiVersion

this_file_dirname=os.path.dirname(__file__)
NEWATTACHMENT_PY= os.path.join(this_file_dirname, 'TestLinkExample.py')
NEWATTACHMENT_PNG=os.path.join(this_file_dirname, 'PyGreat.png')

# Servers TestLink Version
myTLVersion = myTestLink.testLinkVersion()
myTLVersionShort = myTLVersion.replace('.', '')

NEWPROJECT="NEW_PROJECT_API-%s" % myPyVersionShort
NEWPREFIX="NPROAPI%s" % myPyVersionShort
ITSNAME="myITS"

# used connection settings
print( myTestLink.connectionInfo() )
print( "" )

# get information - TestProject
newProject = myTestLink.getTestProjectByName(NEWPROJECT)
print( "getTestProjectByName", newProject )
newProjectID = newProject['id'] 
print( "Project '%s' - id: %s" % (NEWPROJECT,newProjectID) )
response = myTestLink.getProjectKeywords(newProjectID) 
print("getProjectKeywords", response)

# get information - TestPlan
newTestPlan = myTestLink.getTestPlanByName(NEWPROJECT, NEWTESTPLAN_A)
print( "getTestPlanByName", newTestPlan )
newTestPlanID_A = newTestPlan[0]['id'] 
print( "Test Plan '%s' - id: %s" % (NEWTESTPLAN_A,newTestPlanID_A) )
response = myTestLink.getTotalsForTestPlan(newTestPlanID_A)
print( "getTotalsForTestPlan", response )
response = myTestLink.getBuildsForTestPlan(newTestPlanID_A)
print( "getBuildsForTestPlan", response )
newBuildID_A = response[0]['id']
newBuildName_A = response[0]['name']
# get information - TestSuite
response = myTestLink.getTestSuitesForTestPlan(newTestPlanID_A)
print( "getTestSuitesForTestPlan", response )
newTestSuiteID_A=response[0]['id']
newTestSuiteID_AA=response[1]['id']
newTestSuiteID_B=response[2]['id']
newTestSuite = myTestLink.getTestSuiteByID(newTestSuiteID_B)
print( "getTestSuiteByID", newTestSuite )
# get informationen - TestCase_B
response = myTestLink.getTestCaseIDByName(NEWTESTCASE_B, testprojectname=NEWPROJECT)
print( "getTestCaseIDByName", response )
newTestCaseID_B = response[0]['id'] 
tc_b_full_ext_id = myTestLink.getTestCase(newTestCaseID_B)[0]['full_tc_external_id']
print( "Test Case '%s' - id: %s - ext-id %s" % (NEWTESTCASE_B, newTestCaseID_B, tc_b_full_ext_id) )
# get informationen - TestCase_AA
response = myTestLink.getTestCaseIDByName(NEWTESTCASE_AA, testprojectname=NEWPROJECT)
print( "getTestCaseIDByName", response )
newTestCaseID_AA = response[0]['id'] 
tc_aa_full_ext_id = myTestLink.getTestCase(newTestCaseID_AA)[0]['full_tc_external_id']
print( "Test Case '%s' - id: %s - ext-id %s" % (NEWTESTCASE_AA, newTestCaseID_AA, tc_aa_full_ext_id) )


# add keywords to TestCase B and TestCase AA
response = myTestLink.addTestCaseKeywords(
                {tc_b_full_ext_id : ['KeyWord01', 'KeyWord03', 'KeyWord02'],
                 tc_aa_full_ext_id : ['KeyWord01', 'KeyWord02', 'KeyWord03']})
print( "addTestCaseKeywords", response )
# remove keywords from TestCase B and TestCase AA
response = myTestLink.removeTestCaseKeywords(
                            {tc_b_full_ext_id : ['KeyWord02'],
                             tc_aa_full_ext_id : ['KeyWord01', 'KeyWord03']})
print( "removeTestCaseKeywords", response )


# list test cases with assigned keywords B
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_B, True, 
                                               'full', getkeywords=True)
print( "getTestCasesForTestSuite B (deep=True)", response )
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_B, False, 
                                               'full', getkeywords=True)
print( "getTestCasesForTestSuite B (deep=False)", response )

# get informationen - TestCase_B again 
newTestCase_B = myTestLink.getTestCase(testcaseid=newTestCaseID_B)[0]
print( "getTestCase B", newTestCase_B )

# return keyword list for TestCase_B
response =  myTestLink.listKeywordsForTC(newTestCaseID_B)
print( "listKeywordsForTC B", response )
# return keyword lists for all test cases of test newTestSuite_B
response =  myTestLink.listKeywordsForTS(newTestSuiteID_B)
print( "listKeywordsForTS B", response )

# list test cases with assigned keywords AA
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_A, True, 
                                               'full', getkeywords=True)
print( "getTestCasesForTestSuite A (deep=True)", response )
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_A, False, 
                                               'full', getkeywords=True)
print( "getTestCasesForTestSuite A (deep=False)", response )

# get informationen - TestCase_AA again 
newTestCase_AA = myTestLink.getTestCase(testcaseid=newTestCaseID_AA)[0]
print( "getTestCase AA", newTestCase_AA )

# return keyword list for TestCase_AA
response =  myTestLink.listKeywordsForTC(newTestCaseID_AA)
print( "listKeywordsForTC AA", response )
# return keyword lists for all test cases of test newTestSuite_A
response =  myTestLink.listKeywordsForTS(newTestSuiteID_AA)
print( "listKeywordsForTS AA", response )


response = myTestLink.getTestCaseKeywords(testcaseid=newTestCaseID_B)
print("getTestCaseKeywords B", response)
response = myTestLink.getTestCaseKeywords(testcaseid=newTestCaseID_AA)
print("getTestCaseKeywords AA", response)

# new execution result with custom field data
# TC_B passed, explicit build and some notes , TC identified with internal id
newResult = myTestLink.reportTCResult(newTestCaseID_B, newTestPlanID_A, 
                newBuildName_A, 'p', "bugid 4711 is assigned", 
                platformname=NEWPLATFORM_B, bugid='4711',
                customfields={'cf_tc_ex_string' : 'a custom exec value set via api',
                              'cf_tc_sd_listen' : 'ernie'})
print( "reportTCResult", newResult )

# get execution results
lastResult = myTestLink.getLastExecutionResult(newTestPlanID_A, newTestCaseID_B, 
                                               options={'getBugs' : True})[0]
print( "getLastExecutionResult", lastResult )

# map of used ids
args =  {'devKey' : myTestLink.devKey,
         'testprojectid' : newProjectID,
         'testcaseexternalid' : newTestCase_B['full_tc_external_id'],
         'version' : int(newTestCase_B['version']),
         'tcversion_number' : lastResult['tcversion_number'],
         'executionid' : lastResult['id'],
         'linkid' : 779,
         'testsuiteid': newTestSuiteID_B,
         'testplanid': lastResult['testplan_id'],
         'reqspecid': 7789,
         'requirementid': 7791,
         'buildid':newBuildID_A}

# get CustomField Value - TestCase Execution
response = myTestLink.getTestCaseCustomFieldExecutionValue(
                'cf_tc_ex_string', args['testprojectid'], args['tcversion_number'],
                args['executionid'] , args['testplanid'] )
print( "getTestCaseCustomFieldExecutionValue", response )

# update CustomField Value - TestCase SpecDesign
response = myTestLink.updateTestCaseCustomFieldDesignValue( 
                 args['testcaseexternalid'], args['version'], 
                 args['testprojectid'],
                 {'cf_tc_sd_string' : 'A custom SpecDesign value set via api',
                  'cf_tc_sd_list' : 'bibo'})
print( "updateTestCaseCustomFieldDesignValue", response )

# get CustomField Value - TestCase SpecDesign
#response = myTestLink._callServer('getTestCaseCustomFieldDesignValue', args)
response = myTestLink.getTestCaseCustomFieldDesignValue( 
                args['testcaseexternalid'], args['version'],
                args['testprojectid'], 'cf_tc_sd_string', 'full')
print( "getTestCaseCustomFieldDesignValue full", response )

response = myTestLink.getTestCaseCustomFieldDesignValue( 
                args['testcaseexternalid'], args['version'],
                args['testprojectid'], 'cf_tc_sd_string', 'value')
print( "getTestCaseCustomFieldDesignValue value", response )

response = myTestLink.getTestCaseCustomFieldDesignValue( 
                args['testcaseexternalid'], args['version'], 
                args['testprojectid'], 'cf_tc_sd_list', 'simple')
print( "getTestCaseCustomFieldDesignValue simple", response )

# get CustomField Value - TestCase Testplan Design
response = myTestLink.getTestCaseCustomFieldTestPlanDesignValue(
                'cf_tc_pd_string', args['testprojectid'], args['tcversion_number'],
                args['testplanid'], args['linkid'])
print( "getTestCaseCustomFieldTestPlanDesignValue", response )

# get CustomFields Values from all test cases of a TestPlan
response = myTestLink.getTestCasesForTestPlan(args['testplanid'], 
                                              customfields=True)
print("getTestCasesForTestPlan with all customfields", response)
response = myTestLink.getTestCasesForTestPlan(args['testplanid'], 
                                              customfields=['cf_tc_sd_string'])
print("getTestCasesForTestPlan with specific customfields", response)

# update CustomField Value - TestSuite SpecDesign
response = myTestLink.updateTestSuiteCustomFieldDesignValue( 
                 args['testprojectid'], args['testsuiteid'],
                 {'cf_ts_string' : 'A custom TestSuite value set via api'})
print( "updateTestSuiteCustomFieldDesignValue", response )

# get CustomField Value - TestSuite
response = myTestLink.getTestSuiteCustomFieldDesignValue(
                'cf_ts_string', args['testprojectid'], args['testsuiteid'])
print( "getTestSuiteCustomFieldDesignValue", response )

# get CustomField Value - TestPlan
response = myTestLink.getTestPlanCustomFieldDesignValue(
                'cf_tp_string', args['testprojectid'], args['testplanid'])
print( "getTestPlanCustomFieldDesignValue", response )

# get CustomField Value - Requirement Specification
response = myTestLink.getReqSpecCustomFieldDesignValue(
                'cf_req_sd_string', args['testprojectid'], args['reqspecid'])
print( "getReqSpecCustomFieldDesignValue", response )


# get CustomField Value - Requirement Specification
response = myTestLink.getRequirementCustomFieldDesignValue(
                'cf_req_string',args['testprojectid'], args['requirementid'])
print( "getRequirementCustomFieldDesignValue", response )

# update CustomField Value - Build
response = myTestLink.updateBuildCustomFieldsValues( 
                 args['testprojectid'], args['testplanid'], args['buildid'], 
                 {'cf_b_string' : 'A custom Build value set via api'})
print( "updateBuildCustomFieldsValues", response )


