Changes in TestLink-API-Python-client Source Distribution
=========================================================

TestLink-API-Python-client release notes v0.6 (Nov. 2014)
---------------------------------------------------------
support for python 3 (3.3 and 3.4)
added tox, pytest and travis for tests and ci

**Note: tests are still unreliable as order of keywords is not maintained. Need to implement ordered dict to ensure all tests pass consistently**


TestLink-API-Python-client release notes v0.5.2 (Oct. 2014)
-----------------------------------------------------------
support for TestLink release 1.9.12

implement 1.9.12 new api method - getTestCaseAssignedTester #29
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api method

- getTestCaseAssignedTester(<testplanid>, <testcaseexternalid>,
  [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], 
  [platformname=<platformname>], [devKey=<devKey>])

examples see `<example/TestLinkExample.py>`_  

implement 1.9.12 new api method - getTestCaseBugs #30
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api method

- getTestCaseBugs(<testplanid>, 
  [testcaseid]=<testcaseid>], [testcaseexternalid=<testcaseexternalid>], 
  [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], 
  [platformname=<platformname>], [devKey=<devKey>])

examples see `<example/TestLinkExample.py>`_  
  
TestLink-API-Python-client release notes v0.5.1 (Aug. 2014) 
-----------------------------------------------------------
support for TestLink release 1.9.11

implement 1.9.11 api change - getLastExecutionResult #27
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TestlinkAPIGeneric and TestlinkAPIClient api method getLastExecutionResult() 
accepts now following additional optional arguments

- options = {'getBugs' : True / False}

example:

 >>> tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
 >>> tls.getLastExecutionResult(aTPlanID, aTCaseID, options={'getBugs' : True})
  [{ ... , 'tcversion_id': '8929', ... , 'bugs': [{'bug_id': '4711'}], ... }]

implement 1.9.11 new api method - assignTestCaseExecutionTask #26
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api method

- assignTestCaseExecutionTask(<user>, <testplanid>, <testcaseexternalid>, 
  [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], 
  [platformname=<platformname>], [devKey=<devKey>])
  
examples see `<example/TestLinkExample.py>`_  


TestLink-API-Python-client release notes v0.5.0 (Jul. 2014) 
-----------------------------------------------------------
support for TestLink release 1.9.10

new service methods - list keywords #25
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIClient service methods, which returns keyword lists without 
internal details (like getTestCasesForTestSuite() does)

- listKeywordsForTC(internal_or_external_tc_id) 
- listKeywordsForTC(internal_ts_id)

Example::

 >>> import testlink
 >>> tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
 >>> tc_kw = tls.listKeywordsForTC('NPROAPI-3')
  ['KeyWord01', 'KeyWord03']
 >>> tc_kw = tls.listKeywordsForTC(5440)
  ['KeyWord01', 'KeyWord03']
 >>> tc_kw = tls.listKeywordsForTC('5440')
  ['KeyWord01', 'KeyWord03']
 >>> ts_kw = tls.listKeywordsForTS('5415')
  {'5440' : ['KeyWord01', 'KeyWord03'], '5445' : ['KeyWord03'], '5450' : []}
  
                                        
Known limitations:

- it is not possible to ask for a special test case version, cause TL links 
  keywords against a test case and not a test case version

implement 1.9.10 api change - getTestCasesForTestSuite #23
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TestlinkAPIGeneric and TestlinkAPIClient api method getTestCasesForTestSuite() 
accepts now following additional optional arguments (usable with TL >= 1.9.10) 

- parameter getkeywords

implement 1.9.10 api change - reportTCResult #24
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TestlinkAPIGeneric and TestlinkAPIClient api method reportTCResult() 
accepts now following additional optional arguments (usable with TL >= 1.9.10) 
 
- user


implement missing 1.9.8 api method - CustomField #12
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api methods

- updateTestCaseCustomFieldDesignValue, getTestCaseCustomFieldExecutionValue  
  getTestCaseCustomFieldTestPlanDesignValue
- getTestSuiteCustomFieldDesignValue, getTestPlanCustomFieldDesignValue
- getReqSpecCustomFieldDesignValue , getRequirementCustomFieldDesignValue


TestLink-API-Python-client release notes v0.4.8 (Mar. 2014)
-----------------------------------------------------------

add Python 2.6 support #21
~~~~~~~~~~~~~~~~~~~~~~~~~~

Installation failed under Python 2.6 with on error, cause TestlinkAPIGeneric
used in *_convertPostionalArgs()* a
`Py31 feature, back ported to Py27 <http://docs.python.org/2/whatsnew/2.7.html#python-3-1-features>`_

- Dictionary and set comprehensions ({i: i*2 for i in range(3)}).

TestLink-API-Python-client is now installable under Py26 and Py27.
To use it under Py26, the module *argparse* must be installed additionally::

    pip install argparse
    pip install TestLink-API-Python-client
    

implement 1.9.9 api changes - getLastExecutionResult #16
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TestlinkAPIGeneric and TestlinkAPIClient api method getLastExecutionResult() 
accepts now following additional optional arguments (usable with TL >= 1.9.9) 
 
- platformid, platformname, buildid, buildname

implement missing 1.9.9 api method - testLinkVersion #16
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
new TestlinkAPIGeneric and TestlinkAPIClient api method to return the TL version

- testLinkVersion()

new TestlinkAPIGeneric and TestlinkAPIClient service method to return connection informations

- connectionInfo()

implement missing 1.9.8 api method - miscellaneous #14
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api methods

- getUserByLogin(), getUserByID()
- deleteExecution()
- setTestCaseExecutionType()
- assignRequirements()
- getExecCountersByBuild()

Known TL 1.9.9 limitations:

- 6202 assignRequirements() calls assign_to_tcase() without author_id
- 6197 MSSQL - 1.9.8 Upgrade - req_coverage table
- 6193 POSTGRESQL - 1.9.8 Upgrade - req_coverage table

TestLink-API-Python-client release notes v0.4.7 (Jan. 2014)
-----------------------------------------------------------

new service methods - copy test cases #17
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
new TestlinkAPIClient service methods to copy test cases between test suites or
to create a new test case version.

- copyTCnewVersion(origTestCaseId, \*\*changedAttributes)
- copyTCnewTestCase(origTestCaseId, \*\*changedAttributes)
- getProjectIDByNode(a_nodeid)

Example::

 >>> import testlink
 >>> tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
 >>> tc_info = tls.getTestCase(None, testcaseexternalid='NPROAPI-3')
 [{'full_tc_external_id': 'NPROAPI-3', ..., 'id': '5440',  'version': '2',  
   'testsuite_id': '5415', 'tc_external_id': '3','testcase_id': '5425', ...}]
 >>> tls.copyTCnewTestCase(tc_info[0]['testcase_id'], testsuiteid=newSuiteID, 
                                          testcasename='a new test case name')
                                          
Known limitations:

- estimatedexecduration settings are not copied                                          

implement missing 1.9.8 api methods - TestCase #11
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
new TestlinkAPIGeneric and TestlinkAPIClient api methods to modify test cases

- addTestCaseToTestPlan, updateTestCase 
- createTestCaseSteps, deleteTestCaseSteps

Known TL 1.9.9 limitations:

- 6109 createTestCaseSteps with action *update* does not change existing steps
- 6108 createTestCaseSteps creates steps without test case references
- 6102 updateTestCase returns debug informations 
- 6101 updateTestCase does not set modification timestamp

implement missing 1.9.8 api methods - Attachments #13
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
new TestlinkAPIGeneric and TestlinkAPIClient api methods to upload attachments

- uploadRequirementSpecificationAttachment, uploadRequirementAttachment
- uploadTestProjectAttachment, uplodTestSuiteAttachment
- uploadTestCaseAttachment

TestLink-API-Python-client release notes v0.4.6 (Dec. 2013)
-----------------------------------------------------------

TestLink-API-Python-client is now installable via PyPI #15
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pip install TestLink-API-Python-client

new api methods for Platforms implemented #10
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
new TestlinkAPIGeneric and TestlinkAPIClient api methods to handle platforms

- createPlatform, getProjectPlatforms
- addPlatformToTestPlan, removePlatformFromTestPlan

Known TL 1.9.9 limitations:

- 6076 addPlatformToTestPlan creates invalid platform links

TestLink-API-Python-client release notes v0.4.5 (Nov. 2013)
-----------------------------------------------------------

All v0.4.0 API methods from TestlinkAPIClient are shifted to the new super class
TestlinkAPIGeneric and could be used with the new optional argument handling and
asked with whatArgs() for there arguments.

- getProject, createTestProject, createTestCase, createTestSuite, createTestPlan, 
  createTestCase
- createBuild, reportTCResult, uploadExecutionAttachment, 
- getTestProjectByName, getProjectTestPlans, getTotalsForTestPlan, getBuildsForTestPlan
- getLatestBuildForTestPlan, getTestPlanByName
- getTestSuitesForTestPlan, getTestSuiteByID, getTestSuitesForTestSuite, 
  getFirstLevelTestSuitesForTestProject 
- getTestCasesForTestSuite, getTestCasesForTestPlan, getTestCaseIDByName, getFullPath
- getLastExecutionResult, getTestCaseCustomFieldDesignValue, getTestCaseAttachments

Other API methods can be used with the new method

- callServerWithPosArgs(apiMethodame, [apiArgName=apiArgValue])

generic api class TestlinkAPIGeneric #7 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
new class TestlinkAPIGeneric implements the Testlink API methods as generic PY methods
    
- all arguments of Teslink API are supported as optional arguments
- often used (or mandatory) arguments can be configured as positional arguments
- error handling for TestLink API error codes

class TestlinkAPIClient inherits now from TestlinkAPIGeneric the Testlink API methods

- configuration for positional arguments are consistent with v0.4.0
  - except getTestCaseIDByName (see ac6ccf5)

Attention - handling for optional arguments has been changed. Existing code, 
which uses TestlinkAPIClient, must be adapted. Changes between v0.4.5 and v.0.4.0 
are documented in `example/TestLinkExample.py`

public API method callServerWithPosArgs() #4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Every implemented API method uses the new method callServerWithPosArgs() to call
the server and check the response for error codes.

- If the response include an error code, a TLResponseError is raised

This method can although be used to call not yet implemented API methods.

helper method .whatArgs(apiMethodName) #8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Teslink API Client can now be asked, what arguments a API method expects::

	import testlink
	tlh = testlink.TestLinkHelper()
	tls = tlh.connect(testlink.TestlinkAPIClient)
	print tls.whatArgs('createTestPlan')
	createTestPlan(<testplanname>, <testprojectname>, [note=<note>], [active=<active>], [public=<public>], [devKey=<devKey>])
	 create a test plan 

or for a description of all implemented api method ::

	import testlink
	tlh = testlink.TestLinkHelper()
	tls = tlh.connect(testlink.TestlinkAPIClient)
	for m in testlink.testlinkargs._apiMethodsArgs.keys():
		print tls.whatArgs(m), '\n'

other changes
~~~~~~~~~~~~~

see `Milestone v0.4.5 <https://github.com/lczub/TestLink-API-Python-client/issues?milestone=3&state=closed>`_
