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

Shows how to use the TestLinkAPIGeneric.
- does equal things as Example TestLinkAPI in TestLinkExample.py
  - exception - this test project uses platforms 

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
"""                                       
from __future__ import print_function
from testlink import TestlinkAPIGeneric, TestLinkHelper
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
myTestLink = tl_helper.connect(TestlinkAPIGeneric) 

myPyVersion = python_version()
myPyVersionShort = myPyVersion.replace('.', '')[:2]

NEWTESTPLAN_A="TestPlan_API_GENERIC A"
NEWTESTPLAN_B="TestPlan_API_GENERIC B"
NEWTESTPLAN_C="TestPlan_API_GENERIC C - DeleteTest"
NEWPLATFORM_A='Big Bird %s' % myPyVersionShort
NEWPLATFORM_B='Small Bird'
NEWPLATFORM_C='Ugly Bird'
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

this_file_dirname=os.path.dirname(__file__)
NEWATTACHMENT_PY= os.path.join(this_file_dirname, 'TestLinkExampleGenericApi.py')
NEWATTACHMENT_PNG=os.path.join(this_file_dirname, 'PyGreat.png')

# Servers TestLink Version
myTLVersion = myTestLink.testLinkVersion()
myTLVersionShort = myTLVersion.replace('.', '')

NEWPROJECT="PROJECT_API_GENERIC-%s" % myPyVersionShort
NEWPREFIX="GPROAPI%s" % myPyVersionShort
ITSNAME="myITS"

# used connection settings
print(myTestLink.connectionInfo())
print("")

# CHANGE this name into a valid account, known in your TL application
myTestUserName="pyTLapi"
myTestUserName2="admin"
# get user information
response = myTestLink.getUserByLogin(myTestUserName)
print("getUserByLogin", response)
myTestUserID=response[0]['dbID']
response = myTestLink.getUserByID(myTestUserID)
print("getUserByID   ", response)

# example asking the api client about methods arguments
print(myTestLink.whatArgs('createTestCase'))


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
        # seems to be another response failure -  we forward it
        raise   

print("Number of Projects in TestLink: %i " % len(myTestLink.getProjects()))
print("")
for project in myTestLink.getProjects():
    print("Name: %(name)s ID: %(id)s " % project)
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
            ( myPyVersion, myApiVersion, myTLVersion )
newProject = myTestLink.createTestProject(NEWPROJECT, NEWPREFIX, 
    notes=projInfo, active=1, public=1,
#    itsname=ITSNAME, itsenabled=1,
    options={'requirementsEnabled' : 1, 'testPriorityEnabled' : 1, 
             'automationEnabled' : 1,  'inventoryEnabled' : 1})
print("createTestProject", newProject)
newProjectID = newProject[0]['id'] 
print("New Project '%s' - id: %s" % (NEWPROJECT,newProjectID))
 
# Create test plan A  - uses platforms
newTestPlan = myTestLink.createTestPlan(NEWTESTPLAN_A, testprojectname=NEWPROJECT,
            notes='New TestPlan created with the Generic API - uses platforms.',
            active=1, public=1)    
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
 
# Create platform 'Big Bird x' 
newPlatForm = myTestLink.createPlatform(NEWPROJECT, NEWPLATFORM_A, 
        notes='Platform for Big Birds, unique name, only used in this project')
print("createPlatform", newPlatForm)
newPlatFormID_A = newPlatForm['id']
# Add Platform  'Big Bird x' to platform 
response = myTestLink.addPlatformToTestPlan(newTestPlanID_A, NEWPLATFORM_A) 
print("addPlatformToTestPlan", response)

# Create platform 'Small Bird'
newPlatForm = myTestLink.createPlatform(NEWPROJECT, NEWPLATFORM_B, 
                notes='Platform for Small Birds, name used in all example projects')
print("createPlatform", newPlatForm)
newPlatFormID_B = newPlatForm['id']
# Add Platform  'Small Bird' to platform 
response = myTestLink.addPlatformToTestPlan(newTestPlanID_A, NEWPLATFORM_B) 
print("addPlatformToTestPlan", response)

# Create platform 'Ugly Bird'
newPlatForm = myTestLink.createPlatform(NEWPROJECT, NEWPLATFORM_C, 
                notes='Platform for Ugly Birds, will be removed from test plan')
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
# 
# #Creates the test case TC_AA with state ready for review
steps_tc_aa = [
        {'step_number' : 1, 'actions' : "Step action 1 - aa" , 
         'expected_results' : "Step result 1 - aa", 'execution_type' : MANUAL},
        {'step_number' : 2, 'actions' : "Step action 2 - aa" , 
         'expected_results' : "Step result 2 - aa", 'execution_type' : MANUAL},
        {'step_number' : 3, 'actions' : "Step action 3 - aa" , 
         'expected_results' : "Step result 3 - aa", 'execution_type' : MANUAL},
        {'step_number' : 4, 'actions' : "Step action 4 - aa" , 
         'expected_results' : "Step result 4 - aa", 'execution_type' : MANUAL},
        {'step_number' : 5, 'actions' : "Step action 5 - aa" , 
         'expected_results' : "Step result 5 - aa", 'execution_type' : MANUAL},
        {'step_number' : 8, 'actions' : "Dummy step for delete tests" , 
         'expected_results' : "should be delete with deleteTestCaseSteps", 
         'execution_type' : MANUAL}
               ]  
newTestCase = myTestLink.createTestCase(NEWTESTCASE_AA, newTestSuiteID_AA, 
          newProjectID, myTestUserName, "This is the summary of the Test Case AA", 
          steps_tc_aa, preconditions='these are the preconditions',
          importance=LOW, state=READFORREVIEW, estimatedexecduration=10.1)                 
print("createTestCase", newTestCase)
newTestCaseID_AA = newTestCase[0]['id'] 
print("New Test Case '%s' - id: %s" % (NEWTESTCASE_AA, newTestCaseID_AA))
 
# Creates the test case TC_B with state rework - in wrong test suite A
steps_tc_b = [
        {'step_number' : 1, 'actions' : "Step action 1 -b " , 
         'expected_results' : "Step result 1 - b", 'execution_type' : AUTOMATED},
        {'step_number' : 2, 'actions' : "Step action 2 -b " , 
         'expected_results' : "Step result 2 - b", 'execution_type' : AUTOMATED},
        {'step_number' : 3, 'actions' : "Step action 3 -b " , 
         'expected_results' : "Step result 3 - b", 'execution_type' : AUTOMATED},
        {'step_number' : 4, 'actions' : "Step action 4 -b " , 
         'expected_results' : "Step result 4 - b", 'execution_type' : AUTOMATED},
        {'step_number' : 5, 'actions' : "Step action 5 -b " , 
         'expected_results' : "Step result 5 - b", 'execution_type' : AUTOMATED}]
      
newTestCase = myTestLink.createTestCase(NEWTESTCASE_B, newTestSuiteID_A, 
          newProjectID, myTestUserName, "This is the summary of the Test Case B", 
          steps_tc_b, preconditions='these are the preconditions', 
          executiontype=AUTOMATED, status=REWORK, estimatedexecduration=0.5)               
print("createTestCase TC-B in TS-A", newTestCase)
newTestCaseID_B = newTestCase[0]['id'] 
print("New Test Case '%s' - id: %s" % (NEWTESTCASE_B, newTestCaseID_B))

# Move test case TC_B to correct test suite B
tc_b_full_ext_id = myTestLink.getTestCase(testcaseid=newTestCaseID_B)[0]['full_tc_external_id']
response = myTestLink.setTestCaseTestSuite(tc_b_full_ext_id, newTestSuiteID_B)
print("setTestCaseTestSuite TC-B to TS-B" , response)

# Add  test cases to test plan - we need the full external id !
# for every test case version 1 is used
tc_version=1
# TC AA should be tested with platforms 'Big Bird'+'Small Bird'
response = myTestLink.getTestCase(testcaseid=newTestCaseID_AA)
print("getTestCase", response)
tc_aa_full_ext_id = response[0]['full_tc_external_id']
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_A, 
                    tc_aa_full_ext_id, tc_version, platformid=newPlatFormID_A)
print("addTestCaseToTestPlan", response)
tc_aa_full_ext_id = myTestLink.getTestCase(testcaseid=newTestCaseID_AA)[0]['full_tc_external_id']
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_A, 
                    tc_aa_full_ext_id, tc_version, platformid=newPlatFormID_B)
print("addTestCaseToTestPlan", response)
# change test case TC_AA - delete step 8 (step 7 does not exist)
response = myTestLink.deleteTestCaseSteps(tc_aa_full_ext_id, [7,8], 
                                          version=tc_version)
print("deleteTestCaseSteps", response)

# TC B should be tested with platform 'Small Bird'
tc_b_full_ext_id = myTestLink.getTestCase(testcaseid=newTestCaseID_B)[0]['full_tc_external_id']
response = myTestLink.addTestCaseToTestPlan(newProjectID, newTestPlanID_A, 
                    tc_b_full_ext_id, tc_version, platformid=newPlatFormID_B)
print("addTestCaseToTestPlan", response)

#Update test case TC_B -> high, change step 5, new step 6
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

# # Try to Remove Platform  'Big Bird' from platform 
# response = myTestLink.removePlatformFromTestPlan(newTestPlanID_A, NEWPLATFORM_C) 
# print "removePlatformFromTestPlan", response

# Remove Platform  'Ugly Bird' from platform 
response = myTestLink.removePlatformFromTestPlan(newTestPlanID_A, NEWPLATFORM_C) 
print("removePlatformFromTestPlan", response)


# -- Create Build for TestPlan A (uses platforms)
newBuild = myTestLink.createBuild(newTestPlanID_A, NEWBUILD_A, 
                                  buildnotes='Build for TestPlan with platforms')
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
newResult = myTestLink.reportTCResult(newTestPlanID_A, 'f', guess=True,
                                      testcaseexternalid=tc_aa_full_ext_id,
                                      platformname=NEWPLATFORM_A,
                                      execduration=2.9, timestamp='2014-09-18 14:33',
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
newResult = myTestLink.reportTCResult(newTestPlanID_A, 'p', guess=True,
                                      testcaseexternalid=tc_aa_full_ext_id,
                                      platformid=newPlatFormID_B,
                                      execduration='3.2', timestamp='2014-09-19 14:33:02')
print("reportTCResult", newResult)
newResultID_AA_p = newResult[0]['id']
# TC_B passed, explicit build and some notes , TC identified with internal id
newResult = myTestLink.reportTCResult(newTestPlanID_A, 'p', 
                buildid=newBuildID_A, testcaseid=newTestCaseID_B, 
                platformname=NEWPLATFORM_B, notes="first try")
print("reportTCResult", newResult)
newResultID_B = newResult[0]['id']

# add this python file as Attachemnt to last execution of TC_B with 
# different filename 'MyPyExampleApiGeneric.py'
a_file=open(NEWATTACHMENT_PY)
newAttachment = myTestLink.uploadExecutionAttachment(a_file, newResultID_B, 
        title='Textfile Example', description='Text Attachment Example for a TestCase Execution',
        filename='MyPyExampleApiGeneric.py')
print("uploadExecutionAttachment", newAttachment)
# add png file as Attachemnt to last execution of TC_AA
# !Attention - on WINDOWS use binary mode for none text file
# see http://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
a_file=open(NEWATTACHMENT_PNG, mode='rb')
newAttachment = myTestLink.uploadExecutionAttachment(a_file, newResultID_AA, 
            title='PNG Example', description='PNG Attachment Example for a TestCase Execution')
print("uploadExecutionAttachment", newAttachment)

# -- Create Build for TestPlan B (uses no platforms)
newBuild = myTestLink.createBuild(newTestPlanID_B, NEWBUILD_B, 
                            buildnotes='Build for TestPlan without platforms',
                            releasedate='2016-11-30')
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

# TC_B in test plan b (without platform)
# first try failed (with bug), second blocked - all by user myTestUserName
newResult = myTestLink.reportTCResult(newTestPlanID_B, 'f', 
                buildid=newBuildID_B, testcaseid=newTestCaseID_B, bugid='007',
                notes="no birds are singing", user=myTestUserName)
print("reportTCResult", newResult)
newResultID_B_f = newResult[0]['id']
newResult = myTestLink.reportTCResult(newTestPlanID_B, 'b', 
                buildid=newBuildID_B, testcaseid=newTestCaseID_B, bugid='008',
                notes="hungry birds blocks the execution", user=myTestUserName)
print("reportTCResult", newResult)
newResultID_B_b = newResult[0]['id']
# get bugs for test case TC_B in test plan B - state TC is executed with bug
response = myTestLink.getTestCaseBugs(newTestPlanID_B, 
                                      testcaseid=newTestCaseID_B)
print("getTestCaseBugs TC_B in TP_B (TC is executed with 2 bugs)", response)


# now we make a mistake and commit the same result a second time
# and try to delete this mistake 
newResult = myTestLink.reportTCResult(newTestPlanID_B, 'b', 
                buildid=newBuildID_B, testcaseid=newTestCaseID_B, 
                notes="mistake, commit same result a second time")
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
                                  buildnotes='Build for TestPlan delete test')
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
newResult = myTestLink.reportTCResult(newTestPlanID_C, 'p', 
                buildid=newBuildID_C, testcaseid=newTestCaseID_AA, 
                platformname=NEWPLATFORM_C, notes="TP delete test")
print("reportTCResult", newResult)
newResultID_B = newResult[0]['id']
newAttachment = myTestLink.uploadExecutionAttachment(NEWATTACHMENT_PY, newResultID_B, 
        title='Textfile Example', filename='MyPyTPDeleteTest.py',
        description='Attachment Example for a TC Execution and TP delete test')
print("uploadExecutionAttachment", newAttachment)
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
            buildnotes='Build with copied testers from Build ' + NEWBUILD_A,
            active=1, open=1, copytestersfrombuild=newBuildID_A)
print("createBuild", newBuild)
newBuildID_D = newBuild[0]['id'] 
print("New Build '%s' - id: %s" % (NEWBUILD_D, newBuildID_D))

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

# get information - TestPlan
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
response = myTestLink.getTestCasesForTestPlan(newTestPlanID_A, executestatus='f')
print("getTestCasesForTestPlan A failed ", response)
# get Testcases for Plattform SmallBird
response = myTestLink.getTestCasesForTestPlan(newTestPlanID_A, platformid=newPlatFormID_B)
print("getTestCasesForTestPlan A SmallBirds", response)

# get information - TestSuite
response = myTestLink.getTestSuiteByID(newTestSuiteID_B)
print("getTestSuiteByID", response)
response = myTestLink.getTestSuitesForTestSuite(newTestSuiteID_A)
print("getTestSuitesForTestSuite", response)
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_A,
                                               deep=True, details='full')
print("getTestCasesForTestSuite", response)
response = myTestLink.getTestCasesForTestSuite(newTestSuiteID_B,
                                               deep=False, details='only_id')
print("getTestCasesForTestSuite", response)

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

# get informationen - TestCase_B
response = myTestLink.getTestCaseIDByName(NEWTESTCASE_B, testprojectname=NEWPROJECT)
print("getTestCaseIDByName", response)
# get informationen - TestCase_AA via Pathname
tcpathname = '::'.join([NEWPROJECT, changedNEWTESTSUITE_A, NEWTESTSUITE_AA, NEWTESTCASE_AA])
response = myTestLink.getTestCaseIDByName('unknown', testcasepathname=tcpathname)
print("getTestCaseIDByName", response)
# get execution result
response = myTestLink.getLastExecutionResult(newTestPlanID_A, 
                                             testcaseexternalid=tc_aa_full_ext_id)
print("getLastExecutionResult", response)
response = myTestLink.getExecutionSet(newTestPlanID_A, 
                                             testcaseexternalid=tc_aa_full_ext_id)
print("getExecutionSet", response)
response = myTestLink.getLastExecutionResult(newTestPlanID_A, 
                                             testcaseid=newTestCaseID_B)
print("getLastExecutionResult", response)
response = myTestLink.getExecutionSet(newTestPlanID_A, 
                                             testcaseid=newTestCaseID_B)
print("getExecutionSet", response)

response = myTestLink.getLastExecutionResult(newTestPlanID_A, 
                        testcaseid=newTestCaseID_AA, platformid=newPlatFormID_A)
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
# add png file as Attachnent to test suite A - uploadXyzAttachmemt also file path
newAttachment = myTestLink.uploadTestSuiteAttachment(NEWATTACHMENT_PNG, newTestSuiteID_A, 
            title='PNG Example', description='PNG Attachment Example for a TestSuite')
print("uploadTestSuiteAttachment", newAttachment)
# get Attachment of test suite A
response = myTestLink.getTestSuiteAttachments(newTestSuiteID_A)
print("getTestSuiteAttachments", response)

# add png file as Attachment to test case B 
a_file=open(NEWATTACHMENT_PNG, mode='rb')
newAttachment = myTestLink.uploadTestCaseAttachment(a_file, newTestCaseID_B, 1,
            title='PNG Example', description='PNG Attachment Example for a TestCase')
print("uploadTestCaseAttachment", newAttachment)
# get Attachment of test case B 
# response = myTestLink.getTestCaseAttachments(testcaseexternalid=tc_aa_full_ext_id)
# print "getTestCaseAttachments", response
response = myTestLink.getTestCaseAttachments(testcaseid=newTestCaseID_B, version=1)
print("getTestCaseAttachments v1", response)
response = myTestLink.getTestCaseAttachments(testcaseid=newTestCaseID_B)
print("getTestCaseAttachments vNone", response)

# get requirements for the test project - empty result
response = myTestLink.getRequirements(newProjectID)
print("getRequirements test project", "Sorry currently no requirments", response)

# get requirements for the test plan - empty result
response = myTestLink.getRequirements(newProjectID, 
                                      testplanid = newTestPlanID_A,
                                      platformid = newPlatFormID_B)
print("getRequirements test plan", "Sorry currently no requirments", response)


print("")
print("Number of Projects in TestLink: %i " % len(myTestLink.getProjects()))
print("")
for project in myTestLink.getProjects():
    print("Name: %(name)s ID: %(id)s " % project)
print("")

 
# 
# 
#  
