Changes in TestLink-API-Python-client Source Distribution
=========================================================

TestLink-API-Python-client v0.8.2 (under develop)
------------------------------------------------
support for TL 1.9.20_fixed changes and py39

main topic is to support TL 1.9.20_fixed api changes

implement 1.9.20_fixed new api interfaces - #141
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api methods

- createUser(<login>, <firstname>, <lastname>, <email>, [password=<password>])
- setUserRoleOnProject(<userid>, <rolename>, <testprojectid>)

new TestlinkAPIClient service methods

- ensureUserExist(<login>, [firstname=<firstname>], [lastname=<lastname>], 
  [email=<email>, [password=<password>])
- ensureUserExistWithProjectRole(<login>, <rolename>, <projectname>, 
  [firstname=<firstname>], [lastname=<lastname>], [email=<email>, [password=<password>])

implement 1.9.20_fixed changed api interfaces - #139
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

changed TestlinkAPIGeneric and TestlinkAPIClient api methods

- createPlatform() is adapted to support new optional boolean arguments 
  <platformondesign> and <platformonexecution>
  - When they are not set to <True>, assignTestCaseExecutionTask() might fail 
    with an error like
  - TLResponseError: 3041: Test plan (name:TestPlan_API A) has no platforms linked

TestLink-API-Python-client v0.8.1-fix131 (Mar. 2020)
------------------------------------------------------------

fix missing supported API 1.9.17 interfaces
- Pull request #131 by heuy - add closeBuild api function

TestLink-API-Python-client v0.8.1 (Aug. 2019)
------------------------------------------------------------
support for TL 1.9.20 (dev) release and py27, py36, py37

main topic is to support TL 1.9.19 and TL 1.9.20 (dev) api changes related to 
test case attachments, which are stored since TL 1.9.19 with a reference to
the test case version instead the test case id .

Parameter <version> is now mandatory for _uploadTestCaseAttachment_ and optional
for _getTestCaseAttachments_. 
 
implement other 1.9.20 (dev) changed api interfaces - #122
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

changed TestlinkAPIGeneric and TestlinkAPIClient api methods

- getTestCasesForTestPlan() is adapted to support the new optional argument <customfields> . 
  Sample see `<example/TestLinkExample_CF_KW.py>`_ 

known TL 1.9.19 issue:
~~~~~~~~~~~~~~~~~~~~~~~ 
API-XMLRPC - getTestCaseAttachments returns no attachment, uploaded with uploadTestCaseAttachment

- see TL Mantis Ticket 8658 <http://mantis.testlink.org/view.php?id=8658>`_
- recommended to use the TL 1.9.20 development state with github commit 
  6a4984164 or later (even for the TL upgrade or installation). 
 
known TL 1.9.20 development state issue (github commit a1c7aca97):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Calling getTestCasesForTestPlan() with the new optional argument <customfields> returns only internal db values.
As alternative, loop over all returned test cases and call getTestCaseCustomFieldDesignValue(). 
Sample see `<example/TestLinkExample_CF_KW.py>`_

TestLink-API-Python-client v0.8.0 (May. 2018)
---------------------------------------------
support for TL 1.9.17 release and py27, py36


implement 1.9.17 new api interfaces - #76, #81, #82, #83, #101
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- getExecutionSet(<testplanid>, [testcaseid=<testcaseid>], [testcaseexternalid=<testcaseexternalid>], 
  [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], 
  [platformname=<platformname>], [options=<options>], [devKey=<devKey>])
- getRequirements(<testprojectid>, [testplanid=<testplanid>], [platformid=<platformid>], [devKey=<devKey>])
- getReqCoverage(<testprojectid>, <requirementdocid>, [devKey=<devKey>])
- setTestCaseTestSuite(<testcaseexternalid>, <testsuiteid>, [devKey=<devKey>])
- getTestSuiteAttachments(<testsuiteid>, [devKey=<devKey>])
- getAllExecutionsResults(<testplanid>, [testcaseid=<testcaseid>], 
  [testcaseexternalid=<testcaseexternalid>], [platformid=<platformid>], 
  [buildid=<buildid>], [options=<options>])

TestReporter and other improvements pull request #94
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

pull request by Brian-Williams:

- TestReporter's subclasses can be used to idempotently generate required 
  components of testlink before sending the report to a specified testcase.
- TestGenReporter is a default combination of all the TestReporter's subclasses 
  and will try to generate everything it's subclasses is capable of.
- Added TestLinkHelper._setParams to simplify libraries that need to overwrite 
  how a helper aquires it's parameters
- Added TestlinkAPIClient.getTestCaseByVersion to expose the common need of 
  gettting the latest testcase by default. It was already used, but not a 
  function in this class and has uses elsewhere.

`<example/TestLinkExample.py>`_  includes sample, how to use 
TestGenReporter and TestlinkAPIClient.getTestCaseByVersion

Self signed / Let's Encrypt SSL certificate support #90
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TestlinkAPIGeneric and TestlinkAPIClient accepts know the additional 
xmlrpclib.ServerProxy() arguments *use_datetime* and *context* (new with Py2.7.9)
-  https://docs.python.org/2/library/xmlrpclib.html

*context* allows to define a SSL context, which can holds various data 
longer-lived than single SSL connections, such as SSL configuration options, 
certificate(s) and private key(s). (new with Py2.7.9)
- https://docs.python.org/2/library/ssl.html#ssl-contexts 

TestLinkHelper will set the *unverified_context()* if the server url starts with
*https* and no *context* is defined, calling 
- TestLinkHelper().connect(TestlinkAPIClient)


known TL 1.9.17 issues:
~~~~~~~~~~~~~~~~~~~~~~~
API-XMLRPC - new 1.9.17 xmlrpc.class function getAllExecutionsResults not callable via XMLRPC api

- see `TL Mantis Ticket 8259 <http://mantis.testlink.org/view.php?id=8259>`_

fixed TL 1.9.17-DEV issues:
~~~~~~~~~~~~~~~~~~~~~~~~~~~
API-XMLRPC - getRequirements raise PHP Fatal error (github commit 0c8feb6)

- see `TL Mantis Ticket 7902 <http://mantis.testlink.org/view.php?id=7900>`_

API-XMLRPC - getExecutionSet raise database error (github commit 1ee5f78)

- see `TL Mantis Ticket 7900 <http://mantis.testlink.org/view.php?id=7900>`_

TestLink-API-Python-client release notes v0.6.4 (Mar. 2017)
-----------------------------------------------------------
support for TL 1.9.16 release and py27, py34, py35 and py36

implement 1.9.16 new api interfaces - #80
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api method

- updateBuildCustomFieldsValues(<testprojectid>, <testplanid>, <buildid>, 
  <customfields>, [devKey=<devKey>])
  
example `<example/TestLinkExample_CF_KW.py>`_ shows, how to set and get 
customer field values

TestLink-API-Python-client release notes v0.6.3 (Nov. 2016)
-----------------------------------------------------------
support for TL 1.9.15 release and py26, py27, py33, py34 and py35

- further releases will be developed only against py27, py34 and py35
- If there is a need to support other py versions, please give feedback

implement 1.9.15 new api interfaces - #54 #67 #69
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api methods

- updateTestSuite(<testsuiteid>, [testprojectid=<testprojectid>], 
  [prefix=<prefix>], [parentid=<parentid>], [testsuitename=<testsuitename>], 
  [details=<details>], [order=<order>], [devKey=<devKey>])
- getTestSuite(<testsuitename>, <prefix>, [devKey=<devKey>])
- getIssueTrackerSystem(<itsname>, [devKey=<devKey>])
 
implement 1.9.15 changed api interfaces - #68 #70 #72 #71 #69
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

changed TestlinkAPIGeneric and TestlinkAPIClient api methods

- reportTCResult() is adapted to support the new optional argument <steps>
  for setting test step results
- createBuild() is adapted to support new optional arguments

  - <active> : 1 (default) = activ  0 = inactiv 
  - <open>   : 1 (default) = open   1 = closed
  - <releasedate> : YYYY-MM-DD
  - <copytestersfrombuild> : valid buildid tester assignments will be copied.
  
- addTestCaseToTestPlan() is adapted to to support the new optional argument 
  <overwrite> to update linked Test Case Versions
- createTestCase() is adapted to to support the new optional arguments <status>
  and <estimatedexecduration>
- createTestProject() is adapted to to support the new optional arguments 
  <itsname> and <itsenabled> to link a project with an ITS

examples:

 >>> tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
 >>> tls.reportTCResult(None, 'aTPlanID', 'aBuildName', 'f', 'result note',
 >>>                    testcaseexternalid='aTCaseFullExID', overwrite=True,
 >>>                    platformname='Small Birds', execduration=4.1,
 >>>                    timestamp='2015-09-19 14:33:02',
 >>>     steps=[{'step_number' : 3, 'result' : 'p', 'notes' : 'a exec note3'},
 >>>            {'step_number' : 4, 'result' : 'f', 'notes' : 'a exec note4'}])
 >>> tls.createBuild(aTPlanID, 'newBuildName',  'a build note', 
 >>>                 active=1, open=1, releasedate='2016-11-30'
 >>>                 copytestersfrombuild=existingBuildID)
 >>> tls.addTestCaseToTestPlan(aTProjectID, aTPlanID, 'aTCaseFullExID',
 >>>                           aTCVersion, overwrite=1)
 
 
known TL 1.9.15 issues:
~~~~~~~~~~~~~~~~~~~~~~~

changing test suite order with updateTestSuite raise internal server error

- same reason as `TL Mantis Ticket 7696 <http://mantis.testlink.org/view.php?id=7696>`_
- solution: change *testlink-1.9.15/lib/functions/testsuite.class.php - update* as
  descriped in `TL GitHub Commit 1fa41e7 <https://github.com/TestLinkOpenSourceTRMS/testlink-code/commit/1fa41e7ca1eefa55ceaffac8c44a219c05e710e2>`_
  
TestLink web presents no login page (internal server error)

- see `TL Mantis Ticket 7708 <http://mantis.testlink.org/view.php?id=7708>`_
- solution: change *testlink-1.9.15/lib/functions/common.php* as described in `TL GitHub Commit db74644 <https://github.com/TestLinkOpenSourceTRMS/testlink-code/commit/db746440924aa3a572c8058a0595a9572cf36979>`_

Test projects with execution step results can not be deleted
- details and solution see `TL Mantis Ticket 7765 <http://mantis.testlink.org/view.php?id=7765>`_

TestLink-API-Python-client v0.6.2 release notes v0.6.2 (Oct. 2015)
------------------------------------------------------------------
support for TL 1.9.14 release and py26, py27, py33 and py34

- further releases will be developed only against py27 and py34. 
- If there is a need to support other py versions, please give feedback

implement 1.9.14 new api interfaces - #53 #61
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api methods

- deleteTestProject(<testprojectprefix>) 
- updateTestSuiteCustomFieldDesignValue(<testprojectid>, <testsuiteid>, <customfields>)

examples  `<example/TestLinkExample.py>`_  and 
`<example/TestLinkExampleGenericApi.py>`_ now deletes the sample project, if it
already exist.

example `<example/TestLinkExample_CF_KW.py>`_ shows, how to set and get 
customer field values

implement 1.9.14 changed api interfaces - #48 #49 #54 #59
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

changed TestlinkAPIGeneric and TestlinkAPIClient api methods
 
- addTestCaseKeywords() and removeTestCaseKeywords() are adapted to work with a set of keywords.

- getTestCaseKeywords() is adapted to work with a set of test cases ids.

- createTestPlan() is adapted to work with new optional argument <prefix>

- reportTCResult() is adapted to work with new optional arguments <execduration>
  and <timestamp>

examples:

 >>> tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
 >>> tls.addTestCaseKeywords( {TCa_exID : ['KW01', 'KW03', 'KW02'], 
 >>>                           TCb_exID : ['KW01', 'KW02', 'KW04']})
 >>> tls.removeTestCaseKeywords( {TCa_exID : ['KW02'], 
 >>>                              TCb_exID : ['KW01', 'KW04']})  
 >>> tls.getTestCaseKeywords( testcaseid=[TCa_ID, TCb_ID] )  
 >>> tls.getTestCaseKeywords( testcaseexternalid=[TCa_exID, TCb_exID] )  
 >>> tls.createTestPlan('aTPlanName', 'aTProjectName')
 >>> tls.createTestPlan('aTPlanName', testprojectname='aTProjectName')
 >>> tls.createTestPlan('aTPlanName', prefix='aTProjectPrefix')  
 >>> tls.reportTCResult(None, 'aTPlanID', 'aBuildName', 'f', 'result one', 
 >>>                    testcaseexternalid='aTCaseFullExID', overwrite=True,
 >>>                    platformname='Small Birds', execduration=4.1,
 >>>                    timestamp='2015-09-19 14:33:02')
 
Attention:
the api getTestCaseKeywords() returns for the situation **invalid test case id**
a different error code

- 1.9.13 error code *5000* - 1.9.14 error code *5040*

Bugfixes TestLink-API-Python-client v0.6.1 - #51 #55 #56 #45
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

whatArgs reports incorrect arg name for createTestCase
 
- wrong arg name <execution>, correct arg name <executiontype>

TestlinkAPIClient service method countProjects() raise 'Empty Response!' error, 
when no project exist

- general problem of all 'count*' service methods
- api method 'getProjects()' now returns an empty list when no projects exists

TestlinkAPIClient does not accept optional argument 'transport' for proxy 
configuration 

- *TestlinkAPIClient* accepts now like *TestlinkAPIGeneric* optional arguments

TestlinkAPIClient service method listKeywordsForTC() uses now getTestCaseKeywords()

- internal change to reduce code complexity 

Known TL 1.9.14 limitations:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- 7282 updateTestSuiteCustomFieldDesignValue() does change customer field values

TestLink-API-Python-client release notes v0.6.1 (Mar. 2015)
-----------------------------------------------------------
support for TL 1.9.13 release  

Proxy configuration support in TestLinkHelper - pull request #36
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
Integrates `Maberi <https://github.com/Maberi/TestLink-API-Python-client>`_ 
pull request `#36 <https://github.com/lczub/TestLink-API-Python-client/pull/36>`_ 

- allows easy proxy configuration using TestLinkHelper
- Adds a new --proxy option in command line.
- Recognizes "http_proxy" environment variable.
 
implement 1.9.13 new api methods #32 #41 #42 #44 #47 #46
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

new TestlinkAPIGeneric and TestlinkAPIClient api methods

- unassignTestCaseExecutionTask(<testplanid>, <testcaseexternalid>, 
  [buildid=<buildid>], [buildname=<buildname>], [platformid=<platformid>], 
  [platformname=<platformname>], [user=<loginname>], 
  [action='unassignAll'|'unassignOne'], [devKey=<devKey>])
  
- getProjectKeywords(<testprojectid>)  

- getTestCaseKeywords([testcaseid=<testcaseid>], 
  [testcaseexternalid=<testcaseexternalid>])
  
- deleteTestPlan(<testplanid>) 

- addTestCaseKeywords(<testcaseexternalid>, <keywords>)
    Attention: with TL 1.9.14, this api method will change the interface (args)
    see `TL Mantis Task 6934 <http://mantis.testlink.org/view.php?id=6934>`_ 
    
- removeTestCaseKeywords(<testcaseexternalid>, <keywords>)
    Attention: with TL 1.9.14, this api method will change the interface (args)
    see `TL Mantis Task 6907 <http://mantis.testlink.org/view.php?id=6907>`_ 

  
examples see `<example/TestLinkExample.py>`_ and `<example/TestLinkExample_CF_KW.py>`_
 
implement 1.9.13 api change - getTestCasesForTestPlan #41
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TestlinkAPIGeneric and TestlinkAPIClient api method getTestCasesForTestPlan() 
accepts now the additional optional argument platformid=<platformid>

example:

 >>> tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
 >>> tls.getTestCasesForTestPlan(aTPlanID, platformid=aPlatFormID)
  {'12996': {'949': {'platform_name': 'Small Bird',  ... }}
  
Also the optional argument buildid=<buildid> could now be used


TestLink-API-Python-client release notes v0.6.0 (Dec. 2014)
-----------------------------------------------------------

support for TestLink release 1.9.12 and py26, py27, py33 and py34

python 3 support - pull requests #33 #37
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrates `manojklm <https://github.com/manojklm/TestLink-API-Python-client>`_ 
pull requests 
`#33 <https://github.com/lczub/TestLink-API-Python-client/pull/33>`_ 
and `#37 <https://github.com/lczub/TestLink-API-Python-client/pull/37>`_

- add source and unittest support for py33 and py34  
- extend py26 support for unittest2
- add *.travis.yml* configuration for `Travis CI <http://docs.travis-ci.com/>`_ 
- add *tox.ini* configuration for `Tox <http://tox.readthedocs.org>`_  

Track now TestLink-API-Python-client build results on Travis CI - see
https://travis-ci.org/lczub/TestLink-API-Python-client 

extend upload attachments - handling file path #40
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

uploading attachments excepts now also a file path as parameter. 

still supported 0.5.2 behavior - file descriptor::

 a_file_obj=open(A_VALID_FILE_PATH)
 newAttachment = myTestLink.uploadExecutionAttachment(a_file_obj, A_Result_ID, 
                                  'Attachment Title', 'Attachment Description')

new supported 0.6.0 behaviour - file path::

 a_file_path=A_VALID_FILE_PATH
 newAttachment = myTestLink.uploadExecutionAttachment(a_file_path, A_Result_ID, 
                                   'Attachment Title', 'Attachment Description')

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
