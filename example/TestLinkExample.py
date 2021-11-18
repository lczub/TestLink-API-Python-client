#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2011-2021 Olivier Renault, Luiko Czub, TestLink-API-Python-client developers
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

TestLinkExample - v0.20
Created on 6 nov. 2011
@author: Olivier Renault (admin@sqaopen.net)

Shows how to use the TestLinkAPI.

=> Counts and lists the Projects 
=> Create a new Project with the following structure:


NewProject 
   |
   ----NewTestPlan
            |
            ------ Test Suite A
            |           |
            |           ------- Test Suite AA 
            |                          |
            |                          --------- Test Case AA
            |                                      |
            ------ Test Suite B                    --- 5 manual test steps
                          |
                          --------- Test Case B
                                           |   
                                           --- 5 automated test steps
                                           
Update Oct. 2013, L. Czub
Integrates v0.4.5 changes for  optional arguments and response error handling
The v0.4.0 method calls are still visible as comments (look for CHANGE v0.4.5)
So this file helps to understand where existing own code needs adjustment.

Update Dec. 2013, L. Czub - examples for v0.4.6 api extensions added 
Update Jan. 2014, L. Czub - examples for v0.4.7 api and service extensions added 
                                    
"""                                       
from __future__ import print_function
from testlink import TestlinkAPIClient, TestLinkHelper, TestGenReporter
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
tl_helper.setParamsFromArgs('''Shows how to use the TestLinkAPI.
=> Counts and lists the Projects 
=> Create a new Project with the following structure:''')
myTestLink = tl_helper.connect(TestlinkAPIClient) 

myPyVersion = python_version()
myPyVersionShort = myPyVersion.replace('.', '')[:2]

NEWTESTPLAN_A="TestPlan_API A"
NEWTESTPLAN_B="TestPlan_API B"
NEWTESTPLAN_C="TestPlan_API C - DeleteTest"
NEWTESTPLAN_G="TestPlan_API G - generated"
NEWPLATFORM_A='Big Birds %s' % myPyVersionShort
NEWPLATFORM_B='Small Birds'
NEWPLATFORM_C='Ugly Birds'
NEWPLATFORM_G='generated Birds'
NEWTESTSUITE_A="A - First Level"
NEWTESTSUITE_B="B - First Level"
NEWTESTSUITE_AA="AA - Second Level"
NEWTESTCASE_AA="TESTCASE_AA"
NEWTESTCASE_B="TESTCASE_B"
myApiVersion='%s v%s' % (myTestLink.__class__.__name__ , myTestLink.__version__)
NEWBUILD_A='%s' % myApiVersion
NEWBUILD_B='%s' % myApiVersion
NEWBUILD_C='%s - DeleteTest' % myApiVersion
NEWBUILD_D='%s - copyTestersTest' % myApiVersion
NEWBUILD_G='%s - generated' % myApiVersion

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
print(myTestLink.connectionInfo())
print("")

# ensure tester and expert users exists
myTestUserName="myTester"
myTestUser1_ID=myTestLink.ensureUserExist(myTestUserName, 
    firstname="myFirstName", lastname="myLastName", mail="myTester@example.com")
print("ensureUserExist", myTestUserName, myTestUser1_ID)

myTestUserName2="myExpert"
myTestUser2_ID=myTestLink.ensureUserExist(myTestUserName2)
print("checkUser", myTestUserName2, myTestUser2_ID)

# get user information
response = myTestLink.getUserByLogin(myTestUserName)
print("getUserByLogin", response)
myTestUserID=response[0]['dbID']
response = myTestLink.getUserByID(myTestUserID)
print("getUserByID   ", response)


# example asking the api client about methods arguments
print(myTestLink.whatArgs('assignTestCaseExecutionTask'))


# example handling Response Error Codes
# first check an invalid devKey and than the own one
try:
     myTestLink.checkDevKey(devKey='007')
except TLResponseError as tl_err:
    if tl_err.code == 2000:
        # expected invalid devKey Error
        # now check the own one - just call with default settings
        myTestLink.checkDevKey()
    else:
        # seems to be another response failure - we forward it 
        raise   

print("Number of Projects in TestLink: %s " % (myTestLink.countProjects()))
print("")
myTestLink.listProjects()
print("")

# Delete the project, if it already exists
try:
    response = myTestLink.deleteTestProject(NEWPREFIX)
    print("deleteTestProject", response)
except TLResponseError:
    print("No project with prefix %s exists" % NEWPREFIX)
    
# # get IssueTrackerSystem
# aITS=myTestLink.getIssueTrackerSystem(aITSNAME)
# print("getIssueTrackerSystem", aITS)    

# Creates the project
projInfo = 'Example created with Python %s API class %s in TL %s' % \
            ( python_version(), myApiVersion, myTLVersion )
newProject = myTestLink.createTestProject(NEWPROJECT, NEWPREFIX,
    notes=projInfo, active=1, public=1,
#    itsname=ITSNAME, itsenabled=1,
    options={'requirementsEnabled' : 0, 'testPriorityEnabled' : 1,
             'automationEnabled' : 1, 'inventoryEnabled' : 0})
print("createTestProject", newProject)
newProjectID = newProject[0]['id']
print("New Project '%s' - id: %s" % (NEWPROJECT,newProjectID))

# assign project roles to user 1 and get user information
response = myTestLink.ensureUserExistWithProjectRole(myTestUserName, "tester", NEWPROJECT)
print("ensureUserExistWithProjectRole user1 role tester", response)

# assign project roles to user 2 and get user information
response = myTestLink.ensureUserExistWithProjectRole(myTestUserName2, "senior tester", NEWPROJECT)
print("ensureUserExistWithProjectRole user2 role senior tester", response)
response = myTestLink.ensureUserExistWithProjectRole(myTestUserName2, "test designer", NEWPROJECT)
print("ensureUserExistWithProjectRole user2 role test designer", response)

# Creates the test plan
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN_A, testprojectname=NEWPROJECT,
            notes='New TestPlan created with the API',active=1, public=1)    
print("createTestPlan", newTestPlan)
newTestPlanID_A = newTestPlan[0]['id']
print("New Test Plan '%s' - id: %s" % (NEWTESTPLAN_A,newTestPlanID_A))

# Create test plan B  - uses no platforms
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN_B, prefix=NEWPREFIX,
            notes='New TestPlan created with the Generic API - uses no platforms.',
            active=1, public=1)    
print("createTestPlan", newTestPlan)
newTestPlanID_B = newTestPlan[0]['id'] 
print("New Test Plan '%s' - id: %s" % (NEWTESTPLAN_B,newTestPlanID_B))

# Create platform 'Big Birds x' 
newPlatForm = myTestLink.createPlatform(NEWPROJECT, NEWPLATFORM_A, 
        notes='Platform for Big Birds, unique name, only used in this project',
        platformondesign=True, platformonexecution=True)
print("createPlatform", newPlatForm)
newPlatFormID_A = newPlatForm['id']
# Add Platform  'Big Bird x' to platform 
response = myTestLink.addPlatformToTestPlan(newTestPlanID_A, NEWPLATFORM_A) 
print("addPlatformToTestPlan", response)

# Create platform 'Small Birds'
newPlatForm = myTestLink.createPlatform(NEWPROJECT, NEWPLATFORM_B, 
        notes='Platform for Small Birds, name used in all example projects',
        platformondesign=True, platformonexecution=True)
print("createPlatform", newPlatForm)
newPlatFormID_B = newPlatForm['id']
# Add Platform  'Small Bird' to platform 
response = myTestLink.addPlatformToTestPlan(newTestPlanID_A, NEWPLATFORM_B) 
print("addPlatformToTestPlan", response)

# Create platform 'Ugly Birds'
newPlatForm = myTestLink.createPlatform(NEWPROJECT, NEWPLATFORM_C, 
            notes='Platform for Ugly Birds, will be removed from test plan',
            platformondesign=True, platformonexecution=True)
print("createPlatform", newPlatForm)
newPlatFormID_C = newPlatForm['id']
# Add Platform  'Ugly Bird' to platform 
response = myTestLink.addPlatformToTestPlan(newTestPlanID_A, NEWPLATFORM_C) 
print("addPlatformToTestPlan", response)

#Creates the test Suite A      
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_A,
            "Details of the Test Suite A")  
print("createTestSuite", newTestSuite)
newTestSuiteID_A = newTestSuite[0]['id']
print("New Test Suite '%s' - id: %s" % (NEWTESTSUITE_A, newTestSuiteID_A))

FirstLevelID = newTestSuiteID_A
 
#Creates the test Suite B      
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_B,
            "Details of the Test Suite B")               
print("createTestSuite", newTestSuite)
newTestSuiteID_B = newTestSuite[0]['id']
print("New Test Suite '%s' - id: %s" % (NEWTESTSUITE_B, newTestSuiteID_B))

#Creates the test Suite AA       
newTestSuite = myTestLink.createTestSuite(newProjectID, NEWTESTSUITE_AA,
            "Details of the Test Suite AA",parentid=FirstLevelID)               
print("createTestSuite", newTestSuite)
newTestSuiteID_AA = newTestSuite[0]['id']
print("New Test Suite '%s' - id: %s" % (NEWTESTSUITE_AA, newTestSuiteID_AA))

MANUAL = 1
AUTOMATED = 2
READFORREVIEW=2
REWORK=4
HIGH=3
MEDIUM=2
LOW=1

#Creates the test case TC_AA  with state ready for review
myTestLink.initStep("Step action 1", "Step result 1", MANUAL)
myTestLink.appendStep("Step action 2", "Step result 2", MANUAL)
myTestLink.appendStep("Step action 3", "Step result 3", MANUAL)
myTestLink.appendStep("Step action 4", "Step result 4", MANUAL)
myTestLink.appendStep("Step action 5", "Step result 5", MANUAL)
myTestLink.appendStep("Dummy step for delete tests", 
                      "should be delete with deleteTestCaseSteps", MANUAL)
     
newTestCase = myTestLink.createTestCase(NEWTESTCASE_AA, newTestSuiteID_AA, 
          newProjectID, myTestUserName, "This is the summary of the Test Case AA", 
          preconditions='these are the preconditions',
          importance=LOW, state=READFORREVIEW, estimatedexecduration=10.1)
print("createTestCase", newTestCase)
newTestCaseID_AA = newTestCase[0]['id']
print("New Test Case '%s' - id: %s" % (NEWTESTCASE_AA, newTestCaseID_AA))              

#Creates the test case TC_B  with state rework - in wrong test suite A
myTestLink.initStep("Step action 1", "Step result 1", AUTOMATED)
myTestLink.appendStep("Step action 2", "Step result 2", AUTOMATED)
myTestLink.appendStep("Step action 3", "Step result 3", AUTOMATED)
myTestLink.appendStep("Step action 4", "Step result 4", AUTOMATED)
myTestLink.appendStep("Step action 5", "Step result 5", AUTOMATED)
     
newTestCase = myTestLink.createTestCase(NEWTESTCASE_B, newTestSuiteID_A, 
          newProjectID, myTestUserName, "This is the summary of the Test Case B", 
          preconditions='these are the preconditions', executiontype=AUTOMATED, 
          status=REWORK, estimatedexecduration=0.5)   
print("createTestCase TC-B in TS-A", newTestCase)
newTestCaseID_B = newTestCase[0]['id']
print("New Test Case '%s' - id: %s" % (NEWTESTCASE_B, newTestCaseID_B))               

# Move test case TC_B to correct test suite B
tc_b_full_ext_id = myTestLink.getTestCase(newTestCaseID_B)[0]['full_tc_external_id']
response = myTestLink.setTestCaseTestSuite(tc_b_full_ext_id, newTestSuiteID_B)
print("setTestCaseTestSuite TC-B to TS-B" , response)
  
# Add  test cases to test plan - we need the full external id !
# for every test case version 1 is used
tc_version=1
# TC AA should be tested with platforms 'Big Birds'+'Small Birds'
tc_aa_full_ext_id = myTestLink.getTestCase(newTestCaseID_AA)[0]['full_tc_external_id']
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_A, 
                    tc_aa_full_ext_id, tc_version, platformid=newPlatFormID_A)
print("addTestCaseToTestPlan", response)
tc_aa_full_ext_id = myTestLink.getTestCase(newTestCaseID_AA)[0]['full_tc_external_id']
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_A, 
                    tc_aa_full_ext_id, tc_version, platformid=newPlatFormID_B)
print("addTestCaseToTestPlan", response)
# change test case TC_AA - delete step 6 (step 7 does not exist)
response = myTestLink.deleteTestCaseSteps(tc_aa_full_ext_id, [7,6], 
                                          version=tc_version)
print("deleteTestCaseSteps", response)

# TC B should be tested with platform 'Small Birds'
tc_b_full_ext_id = myTestLink.getTestCase(testcaseid=newTestCaseID_B)[0]['full_tc_external_id']
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_A, 
                    tc_b_full_ext_id, tc_version, platformid=newPlatFormID_B)
print("addTestCaseToTestPlan", response)

#Update test case TC_B -> high, change step 5, new step 6
steps_tc_b = myTestLink.getTestCase(testcaseid=newTestCaseID_B)[0]['steps']
steps_tc_b_v1u = steps_tc_b[:4] 
steps_tc_b_v1u.append(
    {'step_number' : 5, 'actions' : "Step action 5 -b changed by updateTestCase" , 
     'expected_results' : "Step result 5 - b changed", 'execution_type' : AUTOMATED})
steps_tc_b_v1u.append(
    {'step_number' : 6, 'actions' : "Step action 6 -b added by updateTestCase" , 
     'expected_results' : "Step result 6 - b added", 'execution_type' : AUTOMATED})                 
response = myTestLink.updateTestCase(tc_b_full_ext_id, version=tc_version,
                steps=steps_tc_b_v1u, importance=MEDIUM, estimatedexecduration=3)
print("updateTestCase", response)

# create additional steps via createTestCaseSteps - action create
steps_tc_b_c67 = [
    {'step_number' : 6, 'actions' : "action 6 createTestCaseSteps.create" , 
     'expected_results' : "skip - cause step 6 already exist", 'execution_type' : AUTOMATED},
    {'step_number' : 7, 'actions' : "action 7 createTestCaseSteps.create" , 
     'expected_results' : "create - cause step 7 not yet exist", 'execution_type' : AUTOMATED}]
response = myTestLink.createTestCaseSteps('create', steps_tc_b_c67, 
                        testcaseexternalid=tc_b_full_ext_id, version=tc_version)
print("createTestCaseSteps.create", response)
# create additional steps via createTestCaseSteps - action update
steps_tc_b_c38 = [
    {'step_number' : 3, 'actions' : "action 3 createTestCaseSteps.update" , 
     'expected_results' : "update - cause step 3 already exist", 'execution_type' : AUTOMATED},
    {'step_number' : 8, 'actions' : "action 8 createTestCaseSteps.update" , 
     'expected_results' : "create - cause step 8 not yet exist", 'execution_type' : AUTOMATED}]
response = myTestLink.createTestCaseSteps('update', steps_tc_b_c38, 
                        testcaseid=newTestCaseID_B, version=tc_version)
print("createTestCaseSteps.update", response)


# In test plan B TC B  should be tested without  platform 
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_B, 
                                            tc_b_full_ext_id, tc_version)
print("addTestCaseToTestPlan", response)

# # Try to Remove Platform  'Big Birds' from platform 
# response = myTestLink.removePlatformFromTestPlan(newTestPlanID_A, NEWPLATFORM_C) 
# print "removePlatformFromTestPlan", response

# Remove Platform  'Ugly Birds' from platform 
response = myTestLink.removePlatformFromTestPlan(newTestPlanID_A, NEWPLATFORM_C) 
print("removePlatformFromTestPlan", response)
  
# -- Create Build for TestPlan A (uses platforms)
newBuild = myTestLink.createBuild(newTestPlanID_A, NEWBUILD_A, 
                            'Notes for the Build', releasedate="2016-12-31")
print("createBuild", newBuild)
newBuildID_A = newBuild[0]['id'] 
print("New Build '%s' - id: %s" % (NEWBUILD_A, newBuildID_A))

# assign user to test case execution tasks - test plan with platforms
response = myTestLink.assignTestCaseExecutionTask( myTestUserName, 
                        newTestPlanID_A, tc_aa_full_ext_id,
                        buildid=newBuildID_A, platformname=NEWPLATFORM_A)
print("assignTestCaseExecutionTask", response)
response = myTestLink.assignTestCaseExecutionTask( myTestUserName2, 
                        newTestPlanID_A, tc_aa_full_ext_id,
                        buildname=NEWBUILD_A, platformid=newPlatFormID_B)  
print("assignTestCaseExecutionTask", response)
response = myTestLink.assignTestCaseExecutionTask( myTestUserName, 
                        newTestPlanID_A, tc_b_full_ext_id,
                        buildname=NEWBUILD_A, platformname=NEWPLATFORM_B)  
print("assignTestCaseExecutionTask", response)

# get test case assigned tester
response = myTestLink.getTestCaseAssignedTester(  
                        newTestPlanID_A, tc_aa_full_ext_id,
                        buildid=newBuildID_A, platformname=NEWPLATFORM_A)
print("getTestCaseAssignedTester TC_AA TP_A Platform A", response)
response = myTestLink.getTestCaseAssignedTester( 
                        newTestPlanID_A, tc_aa_full_ext_id,
                        buildname=NEWBUILD_A, platformid=newPlatFormID_B)  
print("getTestCaseAssignedTester TC_AA TP_A Platform B", response)
response = myTestLink.getTestCaseAssignedTester(
                        newTestPlanID_A, tc_b_full_ext_id,
                        buildname=NEWBUILD_A, platformname=NEWPLATFORM_B)  
print("getTestCaseAssignedTester TC_B TP_A Platform B", response)

# get bugs for test case TC_AA in test plan A - state TC not executed
response = myTestLink.getTestCaseBugs(newTestPlanID_A, 
                                      testcaseexternalid=tc_aa_full_ext_id)
print("getTestCaseBugs TC_AA in TP_A (TC is not executed)", response)

# report Test Case Results for platform 'Big Bird' with step results
# TC_AA failed, build should be guessed, TC identified with external id
newResult = myTestLink.reportTCResult(None, newTestPlanID_A, None, 'f', '', guess=True,
                                      testcaseexternalid=tc_aa_full_ext_id,
                                      platformname=NEWPLATFORM_A,
                                      execduration=3.9, timestamp='2015-09-18 14:33',
         steps=[{'step_number' : 3, 'result' : 'p', 'notes' : 'result note for passed step 3'}, 
                {'step_number' : 4, 'result' : 'f', 'notes' : 'result note for failed step 4'}]  ) 
print("reportTCResult", newResult)
newResultID_AA = newResult[0]['id']

# get bugs for test case TC_AA in test plan A - state TC is executed
response = myTestLink.getTestCaseBugs(newTestPlanID_A, 
                                      testcaseexternalid=tc_aa_full_ext_id)
print("getTestCaseBugs TC_AA in TP_A (TC is executed, no bug)", response)

# report Test Case Results for platform 'Small Bird'
# TC_AA passed, build should be guessed, TC identified with external id
newResult = myTestLink.reportTCResult(None, newTestPlanID_A, None, 'p', '', guess=True,
                                      testcaseexternalid=tc_aa_full_ext_id,
                                      platformname=NEWPLATFORM_B,
                                      execduration='2.2', timestamp='2015-09-19 14:33:02')
print("reportTCResult", newResult)
newResultID_AA_p = newResult[0]['id']
# TC_B passed, explicit build and some notes , TC identified with internal id
newResult = myTestLink.reportTCResult(newTestCaseID_B, newTestPlanID_A, NEWBUILD_A,
                                      'p', 'first try', platformname=NEWPLATFORM_B)
print("reportTCResult", newResult) 
newResultID_B = newResult[0]['id']

#FIXME: know 1.9.20_fixed issue 
# testlink.testlinkerrors.TLResponseError: 6002: (uploadExecutionAttachment) - Error inserting attachment on DB
#
# E_WARNING base64_decode() expects parameter 1 to be string, array given 
# - in /var/www/html/lib/api/xmlrpc/v1/xmlrpc.class.php - Line 5834
#
# # add this (text) file as Attachemnt to last execution of TC_B  with 
# # different filename 'MyPyExampleApiClient.py'
# a_file=open(NEWATTACHMENT_PY)
# newAttachment = myTestLink.uploadExecutionAttachment(a_file, newResultID_B, 
#             'Textfile Example', 'Text Attachment Example for a TestCase Execution',
#             filename='MyPyExampleApiClient.py')
# print("uploadExecutionAttachment", newAttachment)
# # add png file as Attachemnt to last execution of TC_AA
# # !Attention - on WINDOWS use binary mode for none text file
# # see http://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
# a_file=open(NEWATTACHMENT_PNG, mode='rb')
# newAttachment = myTestLink.uploadExecutionAttachment(a_file, newResultID_AA, 
#             'PNG Example', 'PNG Attachment Example for a TestCase Execution')
# print("uploadExecutionAttachment", newAttachment)

# -- Create Build for TestPlan B (uses no platforms)
newBuild = myTestLink.createBuild(newTestPlanID_B, NEWBUILD_B, 
            'Build for TestPlan without platforms', releasedate='2016-11-30')
print("createBuild", newBuild)
newBuildID_B = newBuild[0]['id'] 
print("New Build '%s' - id: %s" % (NEWBUILD_B, newBuildID_B))

# assign user to test case execution tasks - test plans without platforms
response = myTestLink.assignTestCaseExecutionTask( myTestUserName, 
                        newTestPlanID_B, tc_b_full_ext_id, buildname=NEWBUILD_B)  
print("assignTestCaseExecutionTask", response)

# get test case assigned tester
response = myTestLink.getTestCaseAssignedTester(  
                        newTestPlanID_B, tc_b_full_ext_id, buildname=NEWBUILD_B)
print("getTestCaseAssignedTester TC_B TP_B no Platform", response)

# try to remove not assigned tester 
response = myTestLink.unassignTestCaseExecutionTask(
                        newTestPlanID_B, tc_b_full_ext_id, buildname=NEWBUILD_B,
                        user=myTestUserName2)
print("unassignTestCaseExecutionTask not assigned user", response)
response = myTestLink.getTestCaseAssignedTester(  
                        newTestPlanID_B, tc_b_full_ext_id, buildname=NEWBUILD_B)
print("getTestCaseAssignedTester TC_B TP_B no Platform", response)

# try to remove all assigned tester 
response = myTestLink.unassignTestCaseExecutionTask(
                        newTestPlanID_B, tc_b_full_ext_id, buildid=newBuildID_B,
                        action='unassignAll')
print("unassignTestCaseExecutionTask unassignAll", response)
response = myTestLink.getTestCaseAssignedTester(  
                        newTestPlanID_B, tc_b_full_ext_id, buildname=NEWBUILD_B)
print("getTestCaseAssignedTester TC_B TP_B no Platform", response)

# reassign user to test case execution tasks - test plans without platforms
response = myTestLink.assignTestCaseExecutionTask( myTestUserName, 
                        newTestPlanID_B, tc_b_full_ext_id, buildid=newBuildID_B)  
print("assignTestCaseExecutionTask", response)
response = myTestLink.getTestCaseAssignedTester(  
                        newTestPlanID_B, tc_b_full_ext_id, buildname=NEWBUILD_B)
print("getTestCaseAssignedTester TC_B TP_B no Platform", response)


# TC_B blocked (without platform), explicit build and some notes , 
# TC identified with internal id, report by myTestUserName
newResult = myTestLink.reportTCResult(newTestCaseID_B, newTestPlanID_B, NEWBUILD_B,
                                      'f', "no birds are singing", bugid='007',
                                      user=myTestUserName)
print("reportTCResult", newResult)
newResultID_B_f = newResult[0]['id']
newResult = myTestLink.reportTCResult(newTestCaseID_B, newTestPlanID_B, NEWBUILD_B,
                                      'b', "hungry birds blocks the execution", 
                                      bugid='008', user=myTestUserName)
print("reportTCResult", newResult)
newResultID_B_b = newResult[0]['id']
# get bugs for test case TC_B in test plan B - state TC is executed with bug
response = myTestLink.getTestCaseBugs(newTestPlanID_B, 
                                      testcaseid=newTestCaseID_B)
print("getTestCaseBugs TC_B in TP_B (TC is executed with 2 bugs)", response)

# now we make a mistake and commit the same result a second time
# and try to delete this mistake 
newResult = myTestLink.reportTCResult(newTestCaseID_B, newTestPlanID_B, NEWBUILD_B,
                                      'b', "mistake, commit same result a second time")
print("reportTCResult", newResult)
newResultID_B_b2 = int(newResult[0]['id'])
try:
    # if TL configuration allows deletion of executions, no error will occur
    response = myTestLink.deleteExecution(newResultID_B_b2)
    print("deleteExecution", response)
except TLResponseError as tl_err:
    if tl_err.code == 232:
        # TL configuration does not allow deletion of executions
        pass
    else:
        # sh..: another problem occurs
        raise

# now we try to change the execution types of the test cases
# - AA from manual -> auto  and B from auto -> manual 
newResult = myTestLink.setTestCaseExecutionType(tc_aa_full_ext_id, tc_version, 
                                                newProjectID, AUTOMATED)
print("setTestCaseExecutionType", response)
newResult = myTestLink.setTestCaseExecutionType(tc_b_full_ext_id, tc_version, 
                                                newProjectID, MANUAL)
print("setTestCaseExecutionType", response)

# create TestPlan C with Platform, Build , TestCase, assigned TestCase 
# and delete it 
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN_C, NEWPROJECT,
            notes='TestPlan for delete test.',
            active=1, public=1)    
print("createTestPlan for DeleteTest", newTestPlan)
newTestPlanID_C = newTestPlan[0]['id'] 
print("Test Plan '%s' - id: %s" % (NEWTESTPLAN_C,newTestPlanID_C))
newBuild = myTestLink.createBuild(newTestPlanID_C, NEWBUILD_C, 
                                  'Build for TestPlan delete test')
print("createBuild for DeleteTest", newBuild)
newBuildID_C = newBuild[0]['id'] 
print("Build '%s' - id: %s" % (NEWBUILD_C, newBuildID_C))
response = myTestLink.addPlatformToTestPlan(newTestPlanID_C, NEWPLATFORM_C) 
print("addPlatformToTestPlan", response)
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_C, 
                    tc_aa_full_ext_id, tc_version, platformid=newPlatFormID_C)
print("addTestCaseToTestPlan", response)
response = myTestLink.assignTestCaseExecutionTask( myTestUserName, 
                        newTestPlanID_C, tc_aa_full_ext_id, buildid=newBuildID_C,
                        platformid=newPlatFormID_C)  
print("assignTestCaseExecutionTask", response)
newResult = myTestLink.reportTCResult(newTestCaseID_AA, newTestPlanID_C, 
                                      NEWBUILD_C, 'p', "TP delete test",
                                      platformname=NEWPLATFORM_C)
print("reportTCResult", newResult)
newResultID_B = newResult[0]['id']

#FIXME: know 1.9.20_fixed issue 
# testlink.testlinkerrors.TLResponseError: 6002: (uploadExecutionAttachment) - Error inserting attachment on DB
#
# E_WARNING base64_decode() expects parameter 1 to be string, array given 
# - in /var/www/html/lib/api/xmlrpc/v1/xmlrpc.class.php - Line 5834
#
# newAttachment = myTestLink.uploadExecutionAttachment(NEWATTACHMENT_PY, newResultID_B, 
#         'Textfile Example', 'Attachment Example for a TC Execution and TP delete test',
#         filename='MyPyTPDeleteTest.py')
# print("uploadExecutionAttachment", newAttachment)
response = myTestLink.getTotalsForTestPlan(newTestPlanID_C)
print("getTotalsForTestPlan before delete", response)
response = myTestLink.deleteTestPlan(newTestPlanID_C)
print("deleteTestPlan", response)
try:
    response = myTestLink.getTotalsForTestPlan(newTestPlanID_C)
    print("getTotalsForTestPlan after delete", response)
except TLResponseError as tl_err:
    print(tl_err.message)

# -- Create Build D and copy Testers from Build A
newBuild = myTestLink.createBuild(newTestPlanID_A, NEWBUILD_D, 
            'Build with copied testers from Build ' + NEWBUILD_A,
            active=1, open=1, copytestersfrombuild=newBuildID_A)
print("createBuild", newBuild)
newBuildID_D = newBuild[0]['id'] 
print("New Build '%s' - id: %s" % (NEWBUILD_D, newBuildID_D))

# close build A - buildid must be converted to an integer
response = myTestLink.closeBuild( int(newBuildID_A) )
print("closeBuild", response)

# get information - TestProject
response = myTestLink.getTestProjectByName(NEWPROJECT)
print("getTestProjectByName", response)
response = myTestLink.getProjectTestPlans(newProjectID)
print("getProjectTestPlans", response)
response = myTestLink.getFirstLevelTestSuitesForTestProject(newProjectID)
print("getFirstLevelTestSuitesForTestProject", response)
response = myTestLink.getProjectPlatforms(newProjectID) 
print("getProjectPlatforms", response)
response = myTestLink.getProjectKeywords(newProjectID) 
print("getProjectKeywords", response)

# get information - testPlan
response = myTestLink.getTestPlanByName(NEWPROJECT, NEWTESTPLAN_A)
print("getTestPlanByName", response)
response = myTestLink.getTotalsForTestPlan(newTestPlanID_A)
print("getTotalsForTestPlan", response)
response = myTestLink.getBuildsForTestPlan(newTestPlanID_A)
print("getBuildsForTestPlan", response)
response = myTestLink.getLatestBuildForTestPlan(newTestPlanID_A)
print("getLatestBuildForTestPlan", response)
response = myTestLink.getTestPlanPlatforms(newTestPlanID_A)
print("getTestPlanPlatforms", response)
response = myTestLink.getTestSuitesForTestPlan(newTestPlanID_A)
print("getTestSuitesForTestPlan", response)
# get failed Testcases 
# -- Start CHANGE v0.4.5 -- 
#response = myTestLink.getTestCasesForTestPlan(newTestPlanID_A, 'executestatus=f')
response = myTestLink.getTestCasesForTestPlan(newTestPlanID_A, executestatus='f')
# -- END CHANGE v0.4.5 -- 
print("getTestCasesForTestPlan A failed ", response)
# get Testcases for Plattform SmallBird
response = myTestLink.getTestCasesForTestPlan(newTestPlanID_A, platformid=newPlatFormID_B)
print("getTestCasesForTestPlan A SmallBirds", response)

# get information - TestSuite
response = myTestLink.getTestSuiteByID(newTestSuiteID_B)
print("getTestSuiteByID", response)
response = myTestLink.getTestSuitesForTestSuite(newTestSuiteID_A)
print("getTestSuitesForTestSuite A", response)
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_A, True, 'full')
print("getTestCasesForTestSuite A", response)
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_B, False, 'only_id')
print("getTestCasesForTestSuite B", response)

# Update test suite B details - Using Project ID
updatedTestSuite = myTestLink.updateTestSuite(newTestSuiteID_B, 
                            testprojectid=newProjectID, 
                            details="updated Details of the Test Suite B")               
print("updateTestSuite", updatedTestSuite)

# Update test suite A name and order details - Using Project Name
# with TL 1.9.15 this step fails - solution see TL Mantis Ticket 7696 
# <http://mantis.testlink.org/view.php?id=7696>
changedNEWTESTSUITE_A = NEWTESTSUITE_A + ' - Changed'
updatedTestSuite = myTestLink.updateTestSuite(newTestSuiteID_A, prefix=NEWPREFIX, 
            testsuitename = changedNEWTESTSUITE_A, order=1)               
print("updateTestSuite", updatedTestSuite)

# get all test suites, using the same name - test Suite B
response = myTestLink.getTestSuite(NEWTESTSUITE_B, NEWPREFIX)
print("getTestSuite", response)

# get informationen - TestCase
# -- Start CHANGE v0.4.5 -- 
#response = myTestLink.getTestCaseIDByName(NEWTESTCASE_B, None, NEWPROJECT)
response = myTestLink.getTestCaseIDByName(NEWTESTCASE_B, testprojectname=NEWPROJECT)
# -- END CHANGE v0.4.5 -- 
print("getTestCaseIDByName", response)
tcpathname = '::'.join([NEWPROJECT, changedNEWTESTSUITE_A, NEWTESTSUITE_AA, NEWTESTCASE_AA])
response = myTestLink.getTestCaseIDByName('unknown', testcasepathname=tcpathname)
print("getTestCaseIDByName", response)
# get execution result
response = myTestLink.getLastExecutionResult(newTestPlanID_A, None,
                                             testcaseexternalid=tc_aa_full_ext_id)
print("getLastExecutionResult", response)
response = myTestLink.getExecutionSet(newTestPlanID_A, 
                                             testcaseexternalid=tc_aa_full_ext_id)
print("getExecutionSet", response)
response = myTestLink.getLastExecutionResult(newTestPlanID_A, newTestCaseID_B)
print("getLastExecutionResult", response)
response = myTestLink.getExecutionSet(newTestPlanID_A, 
                                             testcaseid=newTestCaseID_B)
print("getExecutionSet", response)
response = myTestLink.getLastExecutionResult(newTestPlanID_A, newTestCaseID_AA, 
                                             platformid=newPlatFormID_A)
print("getLastExecutionResult", response)
response = myTestLink.getExecutionSet(newTestPlanID_A, 
                        testcaseid=newTestCaseID_AA, platformid=newPlatFormID_A)
print("getExecutionSet", response)

response = myTestLink.getAllExecutionsResults(newTestPlanID_A, 
                        testcaseid=newTestCaseID_AA, options={'getBugs' : 1})
print("getAllExecutionsResults", response)
response = myTestLink.getAllExecutionsResults(newTestPlanID_B, 
                        testcaseid=newTestCaseID_B, options={'getBugs' : 1})
print("getAllExecutionsResults", response)
    
    
response = myTestLink.getExecCountersByBuild(newTestPlanID_A)
print("getExecCountersByBuild", response)
response = myTestLink.getExecCountersByBuild(newTestPlanID_B)
print("getExecCountersByBuild", response)
response = myTestLink.getTestCaseKeywords(testcaseexternalid=tc_b_full_ext_id)
print("getTestCaseKeywords noKeyWords", response)

# get information - general 
response = myTestLink.getFullPath(int(newTestSuiteID_AA))
print("getFullPath", response)
response = myTestLink.getFullPath([int(newTestCaseID_AA), int(newTestCaseID_B)])
print("getFullPath", response)

# attachments
# add png file as Attachment to test project 
a_file=open(NEWATTACHMENT_PNG, mode='rb')
newAttachment = myTestLink.uploadTestProjectAttachment(a_file, newProjectID, 
            title='PNG Example', description='PNG Attachment Example for a TestProject')
print("uploadTestProjectAttachment", newAttachment)
# add png file as Attachnent to test suite A - uploadXxzAttachmemt also file path
newAttachment = myTestLink.uploadTestSuiteAttachment(NEWATTACHMENT_PNG, newTestSuiteID_A, 
            title='PNG Example', description='PNG Attachment Example for a TestSuite')
print("uploadTestSuiteAttachment", newAttachment)
# get Attachment of test suite A
response = myTestLink.getTestSuiteAttachments(newTestSuiteID_A)
print("getTestSuiteAttachments", response)

# copy test case - as a new TC version
print("create new version of TC B")
response = myTestLink.copyTCnewVersion(newTestCaseID_B, 
                summary='new version of TC B', importance='1')
print('copyTCnewVersion', response)

# get the different TC versions
response = myTestLink.getTestCaseByVersion(newTestCaseID_B, 1)
print('getTestCaseByVersion v1', response)
response = myTestLink.getTestCaseByVersion(newTestCaseID_B, 2)
print('getTestCaseByVersion v2', response)
response = myTestLink.getTestCaseByVersion(newTestCaseID_B)
print('getTestCaseByVersion vNone', response)

#FIXME: know 1.9.19 issue 
# E_WARNING base64_decode() expects parameter 1 to be string, array given 
# - in /var/www/html/lib/api/xmlrpc/v1/xmlrpc.class.php - Line 5103
#
# # add png file as Attachment to test case B version 1
# a_file=open(NEWATTACHMENT_PNG, mode='rb')
# newAttachment = myTestLink.uploadTestCaseAttachment(a_file, newTestCaseID_B, 1,
#             title='PNG Example v1', description='PNG Attachment Example for a TestCase v1')
# print("uploadTestCaseAttachment v1", newAttachment)
# # add py file as Attachment to test case B version 2
# a_file=open(NEWATTACHMENT_PY, mode='rb')
# newAttachment = myTestLink.uploadTestCaseAttachment(a_file, newTestCaseID_B, 2,
#             title='Textfile Example v2', description='Text Attachment Example for a TestCase v2')
# print("uploadTestCaseAttachment v2", newAttachment)
#
# # get Attachment of test case B v1
# # response = myTestLink.getTestCaseAttachments(testcaseexternalid=tc_aa_full_ext_id)
# # print "getTestCaseAttachments", response
# response = myTestLink.getTestCaseAttachments(testcaseid=newTestCaseID_B, version=1)
# print("getTestCaseAttachments v1", response)
#
# # get Attachment of test case B - last version
# # response = myTestLink.getTestCaseAttachments(testcaseexternalid=tc_aa_full_ext_id)
# # print "getTestCaseAttachments", response
# response = myTestLink.getTestCaseAttachments(testcaseid=newTestCaseID_B, version=2)
# attachment_id = list(response)[0]
# print("getTestCaseAttachments v2", response[attachment_id]['title'])
# response = myTestLink.getTestCaseAttachments(testcaseid=newTestCaseID_B)
# print("getTestCaseAttachments vNone", response[attachment_id]['name'])


# copy test case - as new TC in a different TestSuite
print("copy TC B as TC BA into Test suite A")
response = myTestLink.copyTCnewTestCase(newTestCaseID_B, 
                testsuiteid=newTestSuiteID_A, testcasename='%sA' % NEWTESTCASE_B)
print('copyTCnewTestCase', response)
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_B, False, 'simple')
print('getTestCasesForTestSuite B', response)
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_A, True, 'simple')
print('getTestCasesForTestSuite A', response)




# sample, how the test plan can be updated to use the new tc version
# site effect of this step, assigned testers and existing execution results are 
# not accessible anymore via the TL Web Gui. 
# That is the reason, why we have uncomment it for the normal sample execution
# response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_B, 
#                                             tc_b_full_ext_id, tc_version+1,
#                                             overwrite=1)
# print("addTestCaseToTestPlan overwrite", response)

# sample, how to use TestGenReporter for adding test case result for test plans,
# test builds, which are not yet defined
tgr = TestGenReporter(myTestLink, [tc_aa_full_ext_id, tc_b_full_ext_id], 
                testprojectname=NEWPROJECT, 
                testplanname=NEWTESTPLAN_G, platformname=NEWPLATFORM_G, 
                buildname=NEWBUILD_G, status='p')
tgr.report()
print("TestPlan, Build, Platform generated with reporting TC results", tgr )


print("")
print("Number of Projects      in TestLink: %s " % myTestLink.countProjects())
print("Number of Platforms  (in TestPlans): %s " % myTestLink.countPlatforms())
print("Number of Builds                   : %s " % myTestLink.countBuilds())
print("Number of TestPlans                : %s " % myTestLink.countTestPlans())
print("Number of TestSuites               : %s " % myTestLink.countTestSuites())
print("Number of TestCases (in TestSuites): %s " % myTestLink.countTestCasesTS())
print("Number of TestCases (in TestPlans) : %s " % myTestLink.countTestCasesTP())
print("")

print() 
print("")
myTestLink.listProjects()


 
