#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012 pade (Patrick Dassier), TestLink-API-Python-client developers
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
from __future__ import print_function
from .testlinkapi import TestlinkAPIClient, TestLinkHelper
from .testlinkerrors import TestLinkError
from datetime import date
import warnings

class TestLink(TestlinkAPIClient):
    """
    TestLink API library 
    provide a user friendly library, with more robustness and error management
    
    v0.4.5: 
    this class is deprecated, please use TestlinkAPIGeneric or TestlinkAPIClient
    """

    __author__ = 'pade (Patrick Dassier), TestLink-API-Python-client developers'

    def __init__(self, server_url, key):
        """
        Class initialisation
        """
        warnings.warn("""class TestLink is deprecated!
please use testlinkapigeneric.TestlinkAPIGeneric or testlinkapi.TestlinkAPIClient""", 
        DeprecationWarning)
        super(TestLink, self).__init__(server_url, key)

    def getTestCaseIDByName(self, testCaseName, testSuiteName, testProjectName):
        """
        Find a test case by its name, by its suite and its project
        Suite name must not be duplicate, so only one test case must be found 
        Return test case id if success 
        or raise TestLinkError exception with error message in case of error
        """    
        results = super(TestLink, self).getTestCaseIDByName(testCaseName, testSuiteName, testProjectName)
        if "message" in results[0]:
            raise TestLinkError(results[0]["message"])
        elif len(results) > 1:
            raise TestLinkError("(getTestCaseIDByName) - Several case test found. Suite name must not be duplicate for the same project")
        else:
            if results[0]["name"] == testCaseName:
                    return results[0]["id"]
            raise TestLinkError("(getTestCaseIDByName) - Internal server error. Return value is not expected one!")


    def reportResult(self, testResult, testCaseName, testSuiteName, testNotes="", **kwargs):
        """
        Report results for test case
        Arguments are:
        - testResult: "p" for passed, "b" for blocked, "f" for failed
        - testCaseName: the test case name to report
        - testSuiteName: the test suite name that support the test case
        - testNotes: optional, if empty will be replace by a default string. To let it blank, just set testNotes to " " characters
        - an anonymous dictionnary with followings keys:
            - testProjectName: the project to fill
            - testPlanName: the active test plan
            - buildName: the active build.
        Raise a TestLinkError error with the error message in case of trouble
        Return the execution id needs to attach files to test execution
        """
        
        # Check parameters
        for data in ["testProjectName", "testPlanName", "buildName"]:
            if data not in kwargs:
                raise TestLinkError("(reportResult) - Missing key %s in anonymous dictionnary" % data)

        # Get project id
        project = self.getTestProjectByName(kwargs["testProjectName"])

        # Check if project is active
        if project['active'] != '1':
            raise TestLinkError("(reportResult) - Test project %s is not active" % kwargs["testProjectName"])

        # Check test plan name
        plan = self.getTestPlanByName(kwargs["testProjectName"], kwargs["testPlanName"])

        # Check is test plan is open and active
        if plan['is_open'] != '1' or plan['active'] != '1':
            raise TestLinkError("(reportResult) - Test plan %s is not active or not open" % kwargs["testPlanName"])
        # Memorise test plan id
        planId = plan['id']

        # Check build name
        build = self.getBuildByName(kwargs["testProjectName"], kwargs["testPlanName"], kwargs["buildName"])

        # Check if build is open and active
        if build['is_open'] != '1' or build['active'] != '1':
            raise TestLinkError("(reportResult) - Build %s in not active or not open" % kwargs["buildName"])

        # Get test case id
        caseId = self.getTestCaseIDByName(testCaseName, testSuiteName, kwargs["testProjectName"])

        # Check results parameters
        if testResult not in "pbf":
            raise TestLinkError("(reportResult) - Test result must be 'p', 'f' or 'b'")

        if testNotes == "":
            # Builds testNotes if empty
            today = date.today()
            testNotes = "%s - Test performed automatically" % today.strftime("%c")
        elif testNotes == " ":
            #No notes
            testNotes = ""

        print("testNotes: %s" % testNotes)
        # Now report results
        results = self.reportTCResult(caseId, planId, kwargs["buildName"], testResult, testNotes)
        # Check errors
        if results[0]["message"] != "Success!":
            raise TestLinkError(results[0]["message"])
    
        return results[0]['id']

    def getTestProjectByName(self, testProjectName):
        """
        Return project
        A TestLinkError is raised in case of error
        """
        results = super(TestLink, self).getTestProjectByName(testProjectName)
        if "message" in results[0]:
            raise TestLinkError(results[0]["message"])

        return results[0]

    def getTestPlanByName(self, testProjectName, testPlanName):
        """
        Return test plan
        A TestLinkError is raised in case of error
        """
        results = super(TestLink, self).getTestPlanByName(testProjectName, testPlanName)
        if "message" in results[0]:
            raise TestLinkError(results[0]["message"])

        return results[0]

    def getBuildByName(self, testProjectName, testPlanName, buildName):
        """
        Return build corresponding to buildName
        A TestLinkError is raised in case of error
        """
        plan = self.getTestPlanByName(testProjectName, testPlanName)
        builds = self.getBuildsForTestPlan(plan['id'])

        # Check if a builds exists
        if builds == '':
            raise TestLinkError("(getBuildByName) - Builds %s does not exists for test plan %s" % (buildName, testPlanName))

        # Search the correct build name in the return builds list
        for build in builds:
            if build['name'] == buildName:
                return build
        
        # No build found with builName name
        raise TestLinkError("(getBuildByName) - Builds %s does not exists for test plan %s" % (buildName, testPlanName))

if __name__ == "__main__":
    tl_helper = TestLinkHelper()
    tl_helper.setParamsFromArgs()
    myTestLink = tl_helper.connect(TestLink)
    print(myTestLink)
    print(myTestLink.about())
