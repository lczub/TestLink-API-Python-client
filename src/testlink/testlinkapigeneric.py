#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2013-2018 Luiko Czub, TestLink-API-Python-client developers
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

import sys, os.path
IS_PY3 = sys.version_info[0] < 3
if IS_PY3:
    import xmlrpclib
    # in py 3 encodestring is deprecated and an alias for encodebytes
    # see issue #39 and compare py2 py3 doc 
    # https://docs.python.org/2/library/base64.html#base64.encodestring
    # https://docs.python.org/3/library/base64.html#base64.encodebytes
    from base64 import encodestring as encodebytes
else:
    import xmlrpc.client as xmlrpclib
    from base64 import encodebytes
    
from platform import python_version    
from mimetypes import guess_type
    
from . import testlinkerrors
from .testlinkhelper import TestLinkHelper, VERSION
from .testlinkargs import getMethodsWithPositionalArgs, getArgsForMethod
from .testlinkdecorators import decoApiCallAddAttachment,\
decoApiCallAddDevKey, decoApiCallWithoutArgs, \
decoMakerApiCallReplaceTLResponseError, decoMakerApiCallWithArgs, \
decoMakerApiCallChangePosToOptArg

class TestlinkAPIGeneric(object): 
    """ client for XML-RPC communication between Python and TestLink 
        Implements the TestLink API methods as generic PY methods with 
        error handling.
        
        Allows the configuration of arguments for these API method as positional
        or optional arguments.
        
        Changes of TestLink API methods should be implemented in this base class.
        Service Methods like "countProjects" should be implemented on subclasses
        like TestlinkAPIClient
    """   
    
    __slots__ = ['server', 'devKey', '_server_url', '_positionalArgNames']
 
    __version__ = VERSION
    __author__ = 'Luiko Czub, TestLink-API-Python-client developers'

    def __init__(self, server_url, devKey, **args):
        transport=args.get('transport')
        encoding=args.get('encoding')
        verbose=args.get('verbose',False)
        allow_none=args.get('allow_none',False)
        use_datetime = args.get('use_datetime', False)
        context = args.get('context', None)
        # named arg context is used, cause in Py36 it is place in a different 
        # order as in Py27 and Py35
        self.server = xmlrpclib.Server(server_url, transport, encoding,
                                       verbose, allow_none, use_datetime, 
                                       context=context)
        self.devKey = devKey
        self._server_url = server_url
        self._positionalArgNames = getMethodsWithPositionalArgs()
        
        
        
    # GENERIC API CALLS - using decorators
    # http://stackoverflow.com/questions/1015307/python-bind-an-unbound-method
    
    # Method definitions should be build either with 
    # @decoMakerApiCallWithArgs(argNamesPositional, argNamesOptional)
    #    for calling a server method with arguments 
    #    - argNamesPositional = list default positional args
    #    - argNamesOptional   = list additional optional args
    #    to check the server response, if it includes TestLink Error Codes or 
    #    an empty result (which raise a TLResponseError) 
    # or   
    # @decoApiCallWithoutArgs
    #    for calling server methods without arguments
    #    to check the server response, if it includes TestLink Error Codes or 
    #    an empty result (which raise a TLResponseError)
    #  
    # Additional behavior could be added with
    #    
    # @decoApiCallAddDevKey
    #    - to expand the parameter list with devKey key/value pair
    #      before calling the server method
    # @decoMakerApiCallReplaceTLResponseError(replaceCode)
    #    - to catch an TLResponseError after calling the server method and 
    #      with an empty list
    #      - replaceCode : TestLink Error Code, which should be handled 
    #                      default is None for "Empty Results"
    # @decoApiCallAddAttachment(methodAPI):
    #     - to add an mandatory argument 'attachmentfile'
    #       - attachmentfile is a python file descriptor pointing to the file 
    #     - to expand parameter list with key/value pairs
    #          'filename', 'filetype', 'content'
    #       from 'attachmentfile' before calling the server method


    @decoApiCallAddDevKey            
    @decoMakerApiCallWithArgs(['testplanid'])
    def getLatestBuildForTestPlan(self):
        """ Gets the latest build by choosing the maximum build id for a specific test plan """
    
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'], 
                              ['testcaseid', 'testcaseexternalid',
                               'platformid', 'platformname', 
                               'buildid', 'buildname', 'options'])
    def getLastExecutionResult(self):
        """ Gets the result of LAST EXECUTION for a particular testcase on a test plan.
If there are no filter criteria regarding platform and build,
result will be get WITHOUT checking for a particular platform and build. 

following optional arguments could only used with 
TL version >= 1.9.9 
- platformid, platformname, buildid, buildname

TL version >= 1.9.11
- options : dictionary with key value pair
                    'getBugs' : True / False 
"""

    @decoApiCallWithoutArgs
    def sayHello(self):
        """ Lets you see if the server is up and running """

    def ping(self):
        """ alias for methodAPI sayHello """ 
        return self.sayHello()
    
    @decoMakerApiCallWithArgs(['str'])
    def repeat(self):
        """ Repeats a message back """
    
    @decoApiCallWithoutArgs
    def about(self):
        """ Gives basic information about the API """

#   /**
#    * Creates a new build for a specific test plan
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testplanid"]
#    * @param string $args["buildname"];
#    * @param string $args["buildnotes"];
#    * @param string $args["active"];
#    * @param string $args["open"];
#    * @param string $args["releasedate"]: YYYY-MM-DD;
#    * @param int $args["copytestersfrombuild"] OPTIONAL,
#    *        if > 0 and valid buildid tester assignments will be copied.
#    *   
#    * @return mixed $resultInfo
#    *         
#    * @access public
#    */    
#   public function createBuild($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid', 'buildname'], 
                              ['buildnotes', 'active', 'open', 'releasedate',
                               'copytestersfrombuild'])
    def createBuild(self):
        """ Creates a new build for a specific test plan 
        
        active      : 1 (default) = activ  0 = inactiv 
        open        : 1 (default) = open   0 = closed
        releasedate : YYYY-MM-DD
        copytestersfrombuild : valid buildid tester assignments will be copied.
          """
        
    @decoMakerApiCallReplaceTLResponseError() 
    @decoApiCallAddDevKey            
    @decoMakerApiCallWithArgs()
    def getProjects(self):
        """ Gets a list of all projects   
        
        returns an empty list, if no test project exist """

    @decoMakerApiCallReplaceTLResponseError()            
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testprojectid'])
    def getProjectTestPlans(self):
        """ Gets a list of test plans within a project   
        
        returns an empty list, if no testplan is assigned """

    @decoMakerApiCallReplaceTLResponseError()          
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'])
    def getBuildsForTestPlan(self):
        """ Gets a list of builds within a test plan 
        
        returns an empty list, if no build is assigned """

    @decoMakerApiCallReplaceTLResponseError()          
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'])
    def getTestSuitesForTestPlan(self):
        """ List test suites within a test plan alphabetically
        
        returns an empty list, if no suite is assigned """
        
        
#   /**
#    * create a test project
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param string $args["testprojectname"]
#    * @param string $args["testcaseprefix"]
#    * @param string $args["notes"] OPTIONAL
#    * @param map $args["options"] OPTIONAL ALL int treated as boolean
#    *        keys  requirementsEnabled,testPriorityEnabled,automationEnabled,inventoryEnabled
#    *
#    * @param int $args["active"]  OPTIONAL
#    * @param int $args["public"]  OPTIONAL
#    * @param string $args["itsname"]  OPTIONAL  
#    * @param boolean $args["itsEnabled"]  OPTIONAL  
#    * 
#    *
#    * @return mixed $resultInfo
#    */
#   public function createTestProject($args)
        
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectname', 'testcaseprefix'],
                              ['notes', 'active', 'public', 'options',
                               'itsname', 'itsenabled'])
    def createTestProject(self):
        """ Create a test project  
        
        options : dictionary with keys
                    requirementsEnabled, testPriorityEnabled, 
                    automationEnabled,inventoryEnabled
                 and values 0 (false) and 1 (true)     """
        
    @decoMakerApiCallReplaceTLResponseError()          
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testsuiteid'], ['deep', 'details', 
                                                'getkeywords'])
    def getTestCasesForTestSuite(self):
        """ List test cases within a test suite alphabetically
        
        details - default is 'simple', 
                  use 'full' if you want to get summary,steps & expected_results
                  or 'only_id', if you just need an ID list
                  
        deep - True/False - default is True
               if True, return also test case of child suites
               
        getkeywords - True/False - default is False
               if True AND details='full', dictionary includes for each test
               case, which as assigned keywords, an additional key value pair 
               'keywords'
        
        returns an empty list, if no build is assigned """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcasename'], 
                    ['testsuitename', 'testprojectname', 'testcasepathname'])
    def getTestCaseIDByName(self):
        """ Find a test case by its name 
        
        testcasepathname : Full test case path name, 
                starts with test project name , pieces separator -> ::   
        server return can be a list or a dictionary 
        - optional arg testprojectname seems to create a dictionary response """
 
#    /**
#     * createTestCase
#     * @param struct $args
#     * @param string $args["devKey"]
#     * @param string $args["testcasename"]
#     * @param int    $args["testsuiteid"]: test case parent test suite id
#     * @param int    $args["testprojectid"]: test case parent test suite id
#     *
#     * @param string $args["authorlogin"]: to set test case author
#     * @param string $args["summary"]
#     * @param array  $args["steps"]
#     *
#     * @param string $args["preconditions"] - optional
#     * @param int    $args["importance"] - optional - see const.inc.php for domain
#     * @param int    $args["execution"] - optional - see ... for domain
#     * @param int    $args["order'] - optional
#     * @param int    $args["internalid"] - optional - do not use
#     * @param string $args["checkduplicatedname"] - optional
#     * @param string $args["actiononduplicatedname"] - optional
#     * @param int    $args["status"] - optional - see const.inc.php $tlCfg->testCaseStatus
#     * @param number $args["estimatedexecduration"] - optional
#     *
#     * @return mixed $resultInfo
#     * @return string $resultInfo['operation'] - verbose operation
#     * @return boolean $resultInfo['status'] - verbose operation
#     * @return int $resultInfo['id'] - test case internal ID (Database ID)
#     * @return mixed $resultInfo['additionalInfo'] 
#     * @return int $resultInfo['additionalInfo']['id'] same as $resultInfo['id']
#     * @return int $resultInfo['additionalInfo']['external_id'] without prefix
#     * @return int $resultInfo['additionalInfo']['status_ok'] 1/0
#     * @return string $resultInfo['additionalInfo']['msg'] - for debug 
#     * @return string $resultInfo['additionalInfo']['new_name'] only present if new name generation was needed
#     * @return int $resultInfo['additionalInfo']['version_number']
#     * @return boolean $resultInfo['additionalInfo']['has_duplicate'] - for debug 
#     * @return string $resultInfo['message'] operation message
#     */
#   public function createTestCase($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcasename', 'testsuiteid', 'testprojectid', 
                               'authorlogin', 'summary', 'steps'], 
                ['preconditions', 'importance', 'executiontype', 'order', 
                 'internalid', 'checkduplicatedname', 'actiononduplicatedname',
                 'status', 'estimatedexecduration'])
    def createTestCase(self):
        """ Create a test case
                        
            steps is a list with dictionaries , example
            [{'step_number' : 1, 'actions' : "action A" , 
                'expected_results' : "result A", 'execution_type' : 0},
                 {'step_number' : 2, 'actions' : "action B" , 
                'expected_results' : "result B", 'execution_type' : 1},
                 {'step_number' : 3, 'actions' : "action C" , 
                'expected_results' : "result C", 'execution_type' : 0}]
                
            possible values for optional arguments testlink/cfg/const.inc.php
            importance:    1 (low)    2 (medium) 3 (high)   
            status:        1 (draft)             2 (readyForReview)
                           3 (reviewInProgress)  4 (rework) 
                           5 (obsolete)          6 (future)
                           7 (final)
            executiontype: 1 (Manual)            2 (Automated)
            """

#    /**
#    * Reports a result for a single test case
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testcaseid"]: optional, if not present           
#    *                                 testcaseexternalid must be present
#    *
#    * @param int $args["testcaseexternalid"]: optional, if does not is present           
#    *                                         testcaseid must be present
#    *
#    *
#    *
#    * @param int $args["testplanid"] 
#    * @param string $args["status"] - status is {@link $validStatusList}
#    * @param int $args["buildid"] - optional.
#    *                               if not present and $args["buildname"] exists
#    *                               then 
#    *                                    $args["buildname"] will be checked and used if valid
#    *                               else 
#    *                                    build with HIGHEST ID will be used
#    *
#    * @param int $args["buildname"] - optional.
#    *                               if not present Build with higher internal ID will be used
#    *
#    *
#    * @param string $args["notes"] - optional
#    * @param string $args["execduration"] - optional
#    *
#    * @param bool $args["guess"] - optional defining whether to guess optinal params or require them 
#    *                               explicitly default is true (guess by default)
#    *
#    * @param string $args["bugid"] - optional
#    *
#    * @param string $args["platformid"] - optional, if not present platformname must be present
#    * @param string $args["platformname"] - optional, if not present platformid must be present
#    *    
#    *
#    * @param string $args["customfields"] - optional
#    *               contains an map with key:Custom Field Name, value: value for CF.
#    *               VERY IMPORTANT: value must be formatted in the way it's written to db,
#    *               this is important for types like:
#    *
#    *               DATE: strtotime()
#    *               DATETIME: mktime()
#    *               MULTISELECTION LIST / CHECKBOX / RADIO: se multipli selezione ! come separatore
#    *
#    *
#    *               these custom fields must be configured to be writte during execution.
#    *               If custom field do not meet condition value will not be written
#    *
#    * @param boolean $args["overwrite"] - optional, if present and true, then last execution
#    *                for (testcase,testplan,build,platform) will be overwritten.            
#    *
#    * @param boolean $args["user"] - optional, if present and user is a valid login 
#    *                                (no other check will be done) it will be used when writting execution.
#    *
#    * @param string $args["timestamp"] - optional, if not present now is used
#    *                                    format YYYY-MM-DD HH:MM:SS
#    *                                    example 2015-05-22 12:15:45   
#    * @return mixed $resultInfo 
#    *         [status]  => true/false of success
#    *         [id]      => result id or error code
#    *         [message]  => optional message for error message string
#    * @access public
#    *
#    * @internal revisions
#    *
#    */
#   public function reportTCResult($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid', 'status'], 
                ['testcaseid', 'testcaseexternalid', 'buildid', 'buildname', 
                 'platformid', 'platformname', 'notes', 'guess', 'bugid', 
                 'customfields', 'overwrite', 'user', 'execduration', 
                 'timestamp', 'steps'])
    def reportTCResult(self):
        """ Reports a result for a single test case

        args variations: testcaseid - testcaseexternalid
                         buildid - buildname
                         platformid - platformname
        
        customfields : dictionary with customfields names + values
            VERY IMPORTANT: value must be formatted in the way it's written to db
        overwrite    : if present and true, then last execution for 
                       (testcase,testplan,build,platform) will be overwritten. 
        user : if present and user is a valid login (no other check will be done) 
               it will be used when writing execution.
        execduration : Exec (min) as float (2.5 = 2min 30sec)
        timestamp    : 'YYYY-MM-DD hh:mm[:ss]'#
        steps        : [{'step_number' : 6, 'result' : 'p', 'notes" : 'a_note'}, 
                        {'step_number' : 7, 'result' : 'f', 'notes" : 'blabla'}] 
        """

#   /**
#    * turn on/off testMode
#    *
#    * This method is meant primarily for testing and debugging during development
#    * @param struct $args
#    * @return boolean
#    * @access protected
#    */  testmode
#   public function setTestMode($args)


    #FIXME: LC 20140202 makes setTestMode sense in python client?
    # xmlrpc calls are isolated transactions. 
    # the second call works with another TL api instance than the frist one
    # so the second call works with default TestMode settings (false), even if
    # the first call has active the TestMode.
    # So using setTestMode make only sense, if the php api instance is directly
    # used
#     @decoMakerApiCallWithArgs(['testmode'])
#     def setTestMode(self):
#         """ turn on/off testMode 
#         This method is meant primarily for testing and debugging during development
#         """

#   /**
#    * getTestCasesForTestPlan
#    * List test cases linked to a test plan
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testplanid"]
#    * @param int $args["buildid"] - optional
#    * @param int $args["platformid"] - optional  
#    * @param int $args["testcaseid"] - optional
#    * @param int $args["keywordid"] - optional mutual exclusive with $args["keywords"]
#    * @param int $args["keywords"] - optional  mutual exclusive with $args["keywordid"]
#    *
#    * @param boolean $args["executed"] - optional
#    * @param int $args["$assignedto"] - optional
#    * @param string $args["executestatus"] - optional
#    * @param array $args["executiontype"] - optional
#    * @param array $args["getstepinfo"] - optional - default false
#    * @param string $args["details"] - optional 
#    *                     'full': (default) get summary,steps,expected_results,test suite name
#    *                     'simple':
#    *                     'details':
#    * @return mixed $resultInfo
#    *
#    * @internal revisions
#    * @since 1.9.13
#    * 20141230 - franciscom - TICKET 6805: platform parameter
#    */
#   public function getTestCasesForTestPlan($args)

    @decoMakerApiCallReplaceTLResponseError()          
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'], 
                ['buildid', 'platformid', 
                 'testcaseid', 'keywordid', 'keywords', 'executed', 'assignedto', 
                 'executestatus', 'executiontype', 'getstepinfo', 'details'])
    def getTestCasesForTestPlan(self):
        """ List test cases linked to a test plan
        
        details - default is 'full', 
                  'simple', 'details' ??
                  
        args variations:     keywordid - keywords 
        
        returns an empty list, if no build is assigned """

    @decoMakerApiCallReplaceTLResponseError(replaceValue='') 
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcaseexternalid', 'version', 'testprojectid', 
                               'customfieldname'], ['details'])
    def getTestCaseCustomFieldDesignValue(self):
        """ Gets value of a Custom Field with scope='design' for a given Test case
        
        details =  changes output information
            null or 'value' => just value
            'full' => a map with all custom field definition
                          plus value and internal test case id
            'simple' => value plus custom field name, label, and type (as code).
            
        attention - be careful with testcaseexternalid - it must include an '-'. 
        otherwise TL (<=1.9.8) returns 
        <ProtocolError for xmlrpc.php: 500 Internal Server Error>  """

#    /**
#     * Add a test case version to a test plan 
#     *
#     * @param args['testprojectid']
#     * @param args['testplanid']
#     * @param args['testcaseexternalid']
#     * @param args['version']
#     * @param args['platformid'] - OPTIONAL Only if  test plan has no platforms
#     * @param args['executionorder'] - OPTIONAL
#     * @param args['urgency'] - OPTIONAL
#     * @param args['overwrite'] - OPTIONAL
#     *
#     */
#   public function addTestCaseToTestPlan($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectid',
                               'testplanid', 'testcaseexternalid', 'version'],
                    ['platformid', 'executionorder', 'urgency', 'overwrite'])
    def addTestCaseToTestPlan(self):
        """ Add a test case version to a test plan """
        
    @decoMakerApiCallReplaceTLResponseError(7008)            
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectid'])
    def getFirstLevelTestSuitesForTestProject(self):
        """ get set of test suites AT TOP LEVEL of tree on a Test Project
                            
        returns an empty list, if no suite is assigned (api error 7008) 
        - details see comments for decoMakerApiCallReplaceTLResponseError """

#    /**
#     *  Assign Requirements to a test case 
#     *  we can assign multiple requirements.
#     *  Requirements can belong to different Requirement Spec
#     *         
#   *  @param struct $args
#   *  @param string $args["devKey"]
#   *  @param int $args["testcaseexternalid"]
#   *  @param int $args["testprojectid"] 
#     *  @param string $args["requirements"] 
#     *                array(array('req_spec' => 1,'requirements' => array(2,4)),
#     *                array('req_spec' => 3,'requirements' => array(22,42))
#     *
#     */
#    public function assignRequirements($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcaseexternalid', 'testprojectid', 
                               'requirements'])
    def assignRequirements(self):
        """ Assign Requirements to a test case 
        It is possible to assign multiple requirements, belonging to different 
        requirement specifications. (the internal IDs must be known!)
        
        Argument REQUIREMENTS expects an array of dictionaries, example:
        .assignRequirements('GPROAPI4-2', 6652, 
                           [{'req_spec' : 6729, 'requirements' : [6731]},
                            {'req_spec' : 6733, 'requirements' : [6735, 6737]}])
        This would assign to testcase 'GPROAPI4-2' (in testproject with id 6652)
        a) requirement with ID 6731 of requirement spec 6729 AND
        b) requirements with ID 6735 and 6737 of requirement spec 6733
        """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs([], ['testcaseid', 'testcaseexternalid'])
    def getTestCaseAttachments(self):
        """ Gets attachments for specified test case.
        The attachment file content is Base64 encoded. To save the file to disk 
        in client, Base64 decode the content and write file in binary mode.  """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectid', 'testsuitename', 'details'], 
                              ['parentid', 'order', 'checkduplicatedname', 
                               'actiononduplicatedname'])
    def createTestSuite(self):
        """ create a test suite """

    @decoApiCallAddDevKey            
    @decoMakerApiCallWithArgs(['testprojectname'])
    def getTestProjectByName(self):
        """ Gets info about target test project """

    @decoApiCallAddDevKey            
    @decoMakerApiCallWithArgs(['testprojectname', 'testplanname'])
    def getTestPlanByName(self):
        """ Gets info about target test project """


    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs([], ['testcaseid', 'testcaseexternalid', 'version'])
    def getTestCase(self):
        """ get test case specification using external or internal id
        
        attention - be careful with testcaseexternalid - it must include an '-'. 
        otherwise TL (<=1.9.8) returns 
        <ProtocolError for xmlrpc.php: 500 Internal Server Error>"""

    @decoMakerApiCallChangePosToOptArg(2,'testprojectname')
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanname'], 
                    ['testprojectname', 'prefix', 'note', 'active', 'public'])
    def createTestPlan(self):
        """ create a test plan 
                
            args variations: testprojectname - prefix
                
            supports also pre 1.9.14 arg definition, where 'testprojectname'
            was mandatory ('prefix' comes as alternative with 1.9.14)
            
            examples:
            - createTestPlan('aTPlanName', 'aTProjectName')
            - createTestPlan('aTPlanName', testprojectname='aTProjectName')
            - createTestPlan('aTPlanName', prefix='aTProjectPrefix')

        """


    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['nodeid'])
    def getFullPath(self):
        """ Gets full path from the given node till the top using nodes_hierarchy_table
        
        nodeid = can be just a single id or a list with ids 
                 ATTENTION: id must be an integer. """

#    /**
#    * delete an execution
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["executionid"]
#    *
#    * @return mixed $resultInfo 
#    *         [status]  => true/false of success
#    *         [id]      => result id or error code
#    *         [message]  => optional message for error message string
#    * @access public
#    */  
#    public function deleteExecution($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['executionid'])
    def deleteExecution(self):
        """ delete an execution 
        
        Default TL server configuration does not allow deletion of exections
        see Installation & Configuration Manual Version 1.9
            chap. 5.8. Test execution settings 
            $tlCfg->exec_cfg->can_delete_execution """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testsuiteid'])
    def getTestSuiteByID(self):
        """ Return a TestSuite by ID """

    @decoMakerApiCallReplaceTLResponseError()            
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testsuiteid'])
    def getTestSuitesForTestSuite(self):
        """ get list of TestSuites which are DIRECT children of a given TestSuite
        
        returns an empty list, if no TestSuite is assigned """

    @decoMakerApiCallReplaceTLResponseError(3041)            
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'])
    def getTestPlanPlatforms(self):
        """ Returns the list of platforms associated to a given test plan
        
        returns an empty list, if no platform is assigned (api error 3041) 
        - details see comments for decoMakerApiCallReplaceTLResponseError """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'])
    def getTotalsForTestPlan(self):
        """ Gets the summarized results grouped by platform. """

    @decoMakerApiCallWithArgs(['user'])
    def doesUserExist(self):
        """ Checks if user name exists 
        returns true if everything OK, otherwise error structure """
               
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['devKey'])
    def checkDevKey(self):
        """ check if Developer Key exists 
        returns true if everything OK, otherwise error structure """
        
# /**
#  * Uploads an attachment for a Requirement Specification.
#  * 
#  * The attachment content must be Base64 encoded by the client before sending it.
#  * 
#  * @param struct $args
#  * @param string $args["devKey"] Developer key
#  * @param int $args["reqspecid"] The Requirement Specification ID
#  * @param string $args["title"] (Optional) The title of the Attachment 
#  * @param string $args["description"] (Optional) The description of the Attachment
#  * @param string $args["filename"] The file name of the Attachment (e.g.:notes.txt)
#  * @param string $args["filetype"] The file type of the Attachment (e.g.: text/plain)
#  * @param string $args["content"] The content (Base64 encoded) of the Attachment
#  * 
#  * @since 1.9beta6
#  * @return mixed $resultInfo an array containing the fk_id, fk_table, title, 
#  * description, file_name, file_size and file_type. If any errors occur it 
#  * returns the error map.
#  */
# public function uploadRequirementSpecificationAttachment($args)

    @decoApiCallAddAttachment            
    @decoMakerApiCallWithArgs(['reqspecid'], 
                    ['title', 'description', 'filename', 'filetype', 'content'])
    def uploadRequirementSpecificationAttachment(self):
        """ Uploads an attachment for a Requirement Specification.
        
        reqspecid - The Requirement Specification ID
        
        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path
        
        default values for filename, filetype, content are determine from 
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name 
        """
        
    @decoApiCallAddAttachment            
    @decoMakerApiCallWithArgs(['requirementid'], 
                    ['title', 'description', 'filename', 'filetype', 'content'])
    def uploadRequirementAttachment(self):
        """ Uploads an attachment for a Requirement.
        
        requirementid - The Requirement ID
        
        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path
        
        default values for filename, filetype, content are determine from 
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name 
        """
        
    @decoApiCallAddAttachment            
    @decoMakerApiCallWithArgs(['testprojectid'], 
                    ['title', 'description', 'filename', 'filetype', 'content'])
    def uploadTestProjectAttachment(self):
        """ Uploads an attachment for a Test Project.
        
        testprojectid - The Test Project ID
        
        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path
        
        default values for filename, filetype, content are determine from 
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name 
        """
        
    @decoApiCallAddAttachment            
    @decoMakerApiCallWithArgs(['testsuiteid'], 
                    ['title', 'description', 'filename', 'filetype', 'content'])
    def uploadTestSuiteAttachment(self):
        """ Uploads an attachment for a Test Suite.
        
        testsuiteid - The Test Suite ID
        
        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path
        
        default values for filename, filetype, content are determine from 
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name 
        """

    @decoApiCallAddAttachment            
    @decoMakerApiCallWithArgs(['testcaseid'], 
                    ['title', 'description', 'filename', 'filetype', 'content'])
    def uploadTestCaseAttachment(self):
        """ Uploads an attachment for a Test Case.
        
        testcaseid - Test Case INTERNAL ID
        
        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path
        
        default values for filename, filetype, content are determine from 
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name 
        """

    @decoApiCallAddAttachment            
    @decoMakerApiCallWithArgs(['executionid'], 
                    ['title', 'description', 'filename', 'filetype', 'content'])
    def uploadExecutionAttachment(self):
        """ Uploads an attachment for an execution
        
        executionid - execution ID
        
        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path
        
        default values for filename, filetype, content are determine from 
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name 
        """


    @decoApiCallAddAttachment            
    @decoMakerApiCallWithArgs(['fkid', 'fktable'], 
                    ['title', 'description', 'filename', 'filetype', 'content'])
    def uploadAttachment(self):
        """ Uploads an attachment for an execution
        
        fkid    - The Attachment Foreign Key ID
        fktable - The Attachment Foreign Key Table

        mandatory non api args: attachmentfile
        - python file descriptor pointing to the file
        - or a valid file path
        
        default values for filename, filetype, content are determine from 
        ATTACHMENTFILE, but user could overwrite it, if user want to store the
        attachment with a different name 
        """

#     /**
#      * Gets value of a Custom Field for a entity in a given scope (e.g.: a custom
#      * field for a test case in design scope).
#      *
#      * BUGID-4188: feature request - new method - getTestSuiteCustomFieldValue
#      *
#      * @param struct $args
#      * @param string $args["devKey"]: used to check if operation can be done.
#      *                                if devKey is not valid => abort.
#      *
#      * @param string $args["customfieldname"]: custom field name
#      * @param int     $args["testprojectid"]: project id
#      * @param string $args["nodetype"]: note type (testcase, testsuite, ...)
#      * @param int    $args["nodeid"]: node id (test case version id, project id, ...)
#      * @param string $args["scope"]: cf scope (execution, design or testplan_design)
#      * @param int    $args["executionid"]: execution id
#      * @param int    $args["testplanid"]: test plan id
#      * @param int    $args["linkid"]: link id for nodes linked at test plan design scope
#      *
#      * @return mixed $resultInfo
#      *
#      * @access protected
#      */
#     protected function getCustomFieldValue($args)

#     /**
#      * Gets a Custom Field of a Test Case in Execution Scope.
#      * 
#      * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["customfieldname"]: custom field name
#    * @param int    $args["testprojectid"]: project id
#    * @param int    $args["version"]: test case version id
#    * @param int    $args["executionid"]: execution id
#    * @param int    $args["testplanid"]: test plan id
#    *
#    * @return mixed $resultInfo
#    *
#    * @access public
#      */
#   public function getTestCaseCustomFieldExecutionValue($args)

    @decoMakerApiCallReplaceTLResponseError(replaceValue=None) 
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['customfieldname', 'testprojectid', 'version', 
                               'executionid', 'testplanid'])
    def getTestCaseCustomFieldExecutionValue(self):
        """ Gets a Custom Field of a Test Case in Execution Scope.   """

     
#   /**
#     * Gets a Custom Field of a Test Case in Test Plan Design Scope.
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                 if devKey is not valid => abort.
#    *
#    * @param string $args["customfieldname"]: custom field name
#    * @param int    $args["testcaseid"]: project id
#    * @param int    $args["version"]: test case version id
#    * @param int    $args["testplanid"]: test plan id
#    * @param int    $args["linkid"]: link id (important!)
#    *
#    * @return mixed $resultInfo
#    *
#    * @access public
#    */
#   public function getTestCaseCustomFieldTestPlanDesignValue($args)
 
    @decoMakerApiCallReplaceTLResponseError(replaceValue=None) 
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['customfieldname', 'testprojectid', 'version', 
                               'testplanid', 'linkid'])
    def getTestCaseCustomFieldTestPlanDesignValue(self):
        """ Gets a Custom Field of a Test Case in Test Plan Design Scope.  """

               
#   /**
#    * Gets a Custom Field of a Test Suite in Design Scope.
#    *
#    * @param struct $args
#     * @param string $args["devKey"]: used to check if operation can be done.
#     *                                 if devKey is not valid => abort.
#    *
#    * @param string $args["customfieldname"]: custom field name
#    * @param int   $args["testprojectid"]: project id
#     * @param int    $args["testsuiteid"]: test suite id
#    * 
#    * @return mixed $resultInfo
#    *
#    * @access public
#    */
#   public function getTestSuiteCustomFieldDesignValue($args)

    @decoMakerApiCallReplaceTLResponseError(replaceValue=None) 
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['customfieldname', 'testprojectid', 
                               'testsuiteid'])
    def getTestSuiteCustomFieldDesignValue(self):
        """ Gets a Custom Field of a Test Suite in Design Scope."""
               
#   /**
#    * Gets a Custom Field of a Test Plan in Design Scope.
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["customfieldname"]: custom field name
#    * @param int    $args["testprojectid"]: project id
#    * @param int    $args["testplanid"]: test plan id
#    *
#    * @return mixed $resultInfo
#    *
#    * @access public
#    */
#   public function getTestPlanCustomFieldDesignValue($args)

    @decoMakerApiCallReplaceTLResponseError(replaceValue=None) 
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['customfieldname', 'testprojectid', 
                               'testplanid'])
    def getTestPlanCustomFieldDesignValue(self):
        """ Gets a Custom Field of a Test Plan in Design Scope. """

#     /**
#      * Gets a Custom Field of a Requirement Specification in Design Scope.
#      * 
#      * @param struct $args
#      * @param string $args["devKey"]: used to check if operation can be done.
#      *                                if devKey is not valid => abort.
#      *
#      * @param string $args["customfieldname"]: custom field name
#      * @param int    $args["testprojectid"]: project id
#      * @param int    $args["reqspecid"]: requirement specification id
#      * 
#      * @return mixed $resultInfo
#      * 
#      * @access public
#      */
#     public function getReqSpecCustomFieldDesignValue($args)

    @decoMakerApiCallReplaceTLResponseError(replaceValue=None) 
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['customfieldname', 'testprojectid', 
                               'reqspecid'])
    def getReqSpecCustomFieldDesignValue(self):
        """ Gets a Custom Field of a Requirement Specification in Design Scope. """
               
#     /**
#      * Gets a Custom Field of a Requirement in Design Scope.
#      * 
#      * @param struct $args
#      * @param string $args["devKey"]: used to check if operation can be done.
#      *                                if devKey is not valid => abort.
#      *
#      * @param string $args["customfieldname"]: custom field name
#      * @param int    $args["testprojectid"]: project id
#      * @param int    $args["requirementid"]: requirement id
#      * 
#      * @return mixed $resultInfo
#      * 
#      * @access public
#      */
#     public function getRequirementCustomFieldDesignValue($args)

    @decoMakerApiCallReplaceTLResponseError(replaceValue=None) 
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['customfieldname', 'testprojectid', 
                               'requirementid'])
    def getRequirementCustomFieldDesignValue(self):
        """ Gets a Custom Field of a Requirement Specification in Design Scope. """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['action', 'steps'], 
                              ['testcaseexternalid', 'testcaseid', 'version'])
    def createTestCaseSteps(self):
        """ creates new test steps or updates existing test steps 
        
        action - possible values: 'create','update','push'
            create: if step exist NOTHING WILL BE DONE
            update: if step DOES NOT EXIST will be created else will be updated.
            push: NOT IMPLEMENTED YET (TL 1.9.9)
                  shift down all steps with step number >= step number provided
                  and use provided data to create step number requested.
        steps - each element is a hash with following keys
            step_number,actions,expected_results,execution_type
        args variations: testcaseid - testcaseexternalid
        version - optional if not provided LAST ACTIVE version will be used
                  if all versions are INACTIVE, then latest version will be used. 
        """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcaseexternalid', 'steps'], 
                              ['version'])
    def deleteTestCaseSteps(self):
        """ deletes test cases steps
        
        steps - each element is a step_number
        version - optional if not provided LAST ACTIVE version will be used
        """

#   /**
#    * Update value of Custom Field with scope='design' for a given Test case
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["testcaseexternalid"]:  
#    * @param string $args["version"]: version number  
#    * @param string $args["testprojectid"]: 
#    * @param string $args["customfields"] - optional
#    *               contains an map with key:Custom Field Name, value: value for CF.
#    *               VERY IMPORTANT: value must be formatted in the way it's written to db,
#    *               this is important for types like:
#    *
#    *               DATE: strtotime()
#    *               DATETIME: mktime()
#    *               MULTISELECTION LIST / CHECKBOX / RADIO: se multipli selezione ! come separatore
#    *
#    *
#    *               these custom fields must be configured to be writte during execution.
#    *               If custom field do not meet condition value will not be written
#    *
#    * @return mixed null if everything ok, else array of IXR_Error objects
#    *         
#    * @access public
#    */    
#   public function updateTestCaseCustomFieldDesignValue($args)

    @decoMakerApiCallReplaceTLResponseError(replaceValue='') 
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcaseexternalid', 'version', 'testprojectid', 
                               'customfields'])
    def updateTestCaseCustomFieldDesignValue(self):
        """ Update value of Custom Field with scope='design' for a given Test case
        
       customfields : dictionary with customfields names + values
            VERY IMPORTANT: value must be formatted in the way it's written to db  """


#   /**
#    * Update execution type for a test case version
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["testcaseexternalid"]:  
#    * @param string $args["version"]: version number  
#    * @param string $args["testprojectid"]: 
#      * @param string $args["executiontype"]: TESTCASE_EXECUTION_TYPE_MANUAL,
#      *                     TESTCASE_EXECUTION_TYPE_AUTOMATIC
#      *
#      * @return mixed null if everything ok, else array of IXR_Error objects
#    *         
#    * @access public
#    */    
#   public function setTestCaseExecutionType($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testcaseexternalid', 'version', 'testprojectid',
                               'executiontype'])
    def setTestCaseExecutionType(self):
        """ Update execution type for a test case version 
        
        possible executiontype values
        1 = TESTCASE_EXECUTION_TYPE_MANUAL, 2 = TESTCASE_EXECUTION_TYPE_AUTO """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testplanid'])
    def getExecCountersByBuild(self):
        """ Gets execution metrics information for a testplan """

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectname', 'platformname'], 
                              ['notes'])
    def createPlatform(self):
        """ Creates a platform for test project """


    @decoMakerApiCallReplaceTLResponseError(replaceValue={})            
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testprojectid'])
    def getProjectPlatforms(self):
        """ Gets a dictionary of platforms for a project   
        
        returns an empty dictionary, if no platform is assigned """

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testplanid', 'platformname'])
    def addPlatformToTestPlan(self):
        """ Adds a platform to a test plan """

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testplanid', 'platformname'])
    def removePlatformFromTestPlan(self):
        """ Removes a platform from a test plan """

#   /**
#    * if everything ok returns an array on just one element with following user data
#    *
#    * firstName,lastName,emailAddress,locale,isActive,defaultTestprojectID,
#    * globalRoleID 
#    * globalRole    array with role info
#    * tprojectRoles array  
#    * tplanRoles    array
#    * login 
#    * dbID
#    * loginRegExp
#    *
#    * ATTENTION: userApiKey will be set to NULL, because is worst that access to user password
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]   
#    * @param string $args["user"]   Login Name   
#    * 
#    * @return mixed $ret
#    * 
#    */
#   public function getUserByLogin($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['user'])
    def getUserByLogin(self):
        """  returns user data for account with login name USER
         
        if everything ok returns an array on just one element with following user data
    *
    * firstName,lastName,emailAddress,locale,isActive,defaultTestprojectID,
    * globalRoleID 
    * globalRole    array with role info
    * tprojectRoles array  
    * tplanRoles    array
    * login 
    * dbID
    * loginRegExp
    *
    * ATTENTION: userApiKey will be set to NULL, because is worst that access to user password """


#   /**
#    * if everything ok returns an array on just one element with following user data
#    *
#    * firstName,lastName,emailAddress,locale,isActive,defaultTestprojectID,
#    * globalRoleID 
#    * globalRole    array with role info
#    * tprojectRoles array  
#    * tplanRoles    array
#    * login 
#    * dbID
#    * loginRegExp
#    *
#    * ATTENTION: userApiKey will be set to NULL, because is worst that access to user password
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]   
#    * @param string $args["userid"]   user ID as present on users table, column ID
#    * 
#    * @return mixed $ret
#    * 
#    */
#   public function getUserByID($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['userid'])
    def getUserByID(self):
        """  returns user data for account with USERID in users table, column ID
        
    * if everything ok returns an array on just one element with following user data
    *
    * firstName,lastName,emailAddress,locale,isActive,defaultTestprojectID,
    * globalRoleID 
    * globalRole    array with role info
    * tprojectRoles array  
    * tplanRoles    array
    * login 
    * dbID
    * loginRegExp
    *
    * ATTENTION: userApiKey will be set to NULL, because is worst that access to user password
    """

#    /**
#     * Update an existing test case
#     * Not all test case attributes will be able to be updated using this method
#     * See details below
#     * 
#     * @param struct $args
#     * @param string $args["devKey"]
#     * @param string $args["testcaseexternalid"] format PREFIX-NUMBER
#     * @param int    $args["version"] optional version NUMBER (human readable) 
#     * @param string $args["testcasename"] - optional
#     * @param string $args["summary"] - optional
#     * @param string $args["preconditions"] - optional
#     * @param array  $args["steps"] - optional
#     *               each element is a hash with following keys
#     *               step_number,actions,expected_results,execution_type
#     *
#     * @param int    $args["importance"] - optional - see const.inc.php for domain
#     * @param int    $args["executiontype"] - optional - see ... for domain
#     * @param int    $args["status'] - optional
#     * @param int    $args["estimatedexecduration'] - optional
#     * @param string $args["user'] - login name used as updater - optional
#     *                               if not provided will be set to user that request update
#     */
#    public function updateTestCase($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testcaseexternalid'], 
            ['version', 'testcasename','summary', 'preconditions', 'steps', 
             'importance', 'executiontype', 'status', 'estimatedexecduration', 
             'user'])
    def updateTestCase(self):
        """ Update an existing test case
        
        steps     array - each element is a hash with following keys
                  step_number,actions,expected_results,execution_type
        user      login name used as updater - optional
                  if not provided will be set to user that request update

        Not all test case attributes will be able to be updated using this method
 """

    def testLinkVersion(self):
        """ Returns the TestLink Version
        usable with TL>= 1.9.9 , returns '<= 1.9.8' for older versions """
        
        tl_version = '<= 1.9.8'
        try:
            tl_version = self.callServerWithPosArgs('testLinkVersion')
        except testlinkerrors.TLAPIError:
            # TL does not know this api method, version must be < 1.9.9
            pass
        return tl_version
 
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['user', 'testplanid', 'testcaseexternalid'],
                        ['buildid', 'buildname', 'platformid', 'platformname'])
    def assignTestCaseExecutionTask(self):
        """ assigns a user to a test case execution task
        
        user                 login name => tester
        testplanid           test plan id
        testcaseexternalid   format PREFIX-NUMBER
        
        args variations:     buildid - buildname 
                             platformid - platformname
        build information is general mandatory
        platform information is required, when test plan has assigned platforms
        """
    
#  /**
#   * Returns all bugs linked to a particular testcase on a test plan.
#   * If there are no filter criteria regarding platform and build,
#   * result will be get WITHOUT checking for a particular platform and build.
#   *
#   * @param struct $args
#   * @param string $args["devKey"]
#   * @param int $args["tplanid"]
#   * @param int $args["testcaseid"]: Pseudo optional.
#   *                                 if does not is present then testcaseexternalid MUST BE present
#   *
#   * @param int $args["testcaseexternalid"]: Pseudo optional.
#   *                                         if does not is present then testcaseid MUST BE present
#   *
#   * @param string $args["platformid"]: optional. 
#   *                                    ONLY if not present, then $args["platformname"] 
#   *                                    will be analized (if exists)
#   *
#   * @param string $args["platformname"]: optional (see $args["platformid"])
#   *
#   * @param int $args["buildid"]: optional
#   *                              ONLY if not present, then $args["buildname"] will be analized (if exists)
#   * 
#   * @param int $args["buildname"] - optional (see $args["buildid"])
#   *
#   *
#   * @return mixed $resultInfo
#   *               if execution found
#   *               array that contains a map with these keys:
#   *               bugs
#   *
#   *               if test case has not been execute,
#   *               array('id' => -1)
#   *
#   * @access public
#   */
#    public function getTestCaseBugs($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testplanid' ], 
                        ['testcaseid', 'testcaseexternalid', 
                         'buildid', 'buildname', 'platformid', 'platformname'])
    def getTestCaseBugs(self):
        """ Returns all bugs linked to a particular testcase on a test plan.
        If there are no filter criteria regarding platform and build, 
        result will be get WITHOUT checking for a particular platform and build.
        
        
        testplanid       test plan id
        
        args variations: testcaseid - testcaseexternalid  (mandatory!)
                         buildid - buildname
                         platformid - platformname
        test case information is general mandatory
        """

#   /**
#    * Gets the result of LAST EXECUTION for a particular testcase on a test plan.
#    * If there are no filter criteria regarding platform and build,
#    * result will be get WITHOUT checking for a particular platform and build.
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["tplanid"]
#    * @param string $args["testcaseexternalid"] format PREFIX-NUMBER
#    * @param int $args["buildid"] Mandatory => you can provide buildname as alternative
#    * @param int $args["buildname"] Mandatory => you can provide buildid (DB ID) as alternative
#    * @param int $args["platformid"] optional - BECOMES MANDATORY if Test plan has platforms
#    *                                           you can provide platformname as alternative  
#    *  
#    * @param int $args["platformname"] optional - BECOMES MANDATORY if Test plan has platforms
#    *                                           you can provide platformid as alternative  
#    *
#    *
#    * @return mixed $resultInfo
#    *
#    * @access public
#    */
#   public function getTestCaseAssignedTester($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testplanid', 'testcaseexternalid'],
                        ['buildid', 'buildname', 'platformid', 'platformname'])
    def getTestCaseAssignedTester(self):
        """ Gets the result of LAST EXECUTION for a particular testcase on a 
        test plan.
        
        testplanid           test plan id
        testcaseexternalid   format PREFIX-NUMBER
        
        args variations:     buildid - buildname 
                             platformid - platformname
        build information is general mandatory
        platform information is required, when test plan has assigned platforms
        """
#   /**
#     * @param struct $args
#     * @param string $args["devKey"]
#     * @param int $args["testplanid"]
#     * @param string $args["testcaseexternalid"] format PREFIX-NUMBER
#     * @param int $args["buildid"] Mandatory => you can provide buildname as alternative
#     * @param int $args["buildname"] Mandatory => you can provide buildid (DB ID) as alternative
#     * @param int $args["platformid"] optional - BECOMES MANDATORY if Test plan has platforms
#     *                                           you can provide platformname as alternative  
#     *  
#     * @param int $args["platformname"] optional - BECOMES MANDATORY if Test plan has platforms
#     *                                           you can provide platformid as alternative  
#     * @param string $args["user'] - login name => tester 
#     *                             - NOT NEEDED f $args['action'] = 'unassignAll'
#     * ¸
#     *
#     */
#   public function unassignTestCaseExecutionTask($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testplanid', 'testcaseexternalid'],
                        ['buildid', 'buildname', 'platformid', 'platformname',
                         'user', 'action'])
    def unassignTestCaseExecutionTask(self):
        """ assigns a user to a test case execution task
        
        testplanid           test plan id
        testcaseexternalid   format PREFIX-NUMBER
        
        args variations:     buildid - buildname 
                             platformid - platformname
                             user (login name) - action ('unassignAll')
        build information is general mandatory
        platform information is required, when test plan has assigned platforms
        if action=='unassignAll', user information is not needed
        - otherwise, TL itself will set action to 'unassignOne' and expects a
          valid user information (login name => tester)
        
        """

    @decoMakerApiCallReplaceTLResponseError(replaceValue={})            
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testprojectid'])
    def getProjectKeywords(self):
        """ Gets a dictionary of valid keywords for a project   
        
        returns an empty dictionary, if no keywords are defined """


# #   /**
# #    * Gets list of keywords for a given Test case
# #    *
# #    * @param $testcaseid
# #    *
# #    * @return map indexed by bug_id
# #    *
# #    * @access public
# #    */
# #   public function getTestCaseKeywords($args)
# 
    @decoMakerApiCallReplaceTLResponseError(replaceValue={})            
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs([], ['testcaseid', 'testcaseexternalid'])
    def getTestCaseKeywords(self):
        """ Gets a dictionary of keywords for a given Test case 
        
        args variations: testcaseid - testcaseexternalid  (mandatoy!)
         
        returns an empty dictionary, if no keywords are defined """
        
#   /**
#    *  Delete a test plan and all related link to other items
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["$tplanID"]
#    *
#    * @return mixed $resultInfo
#    *         [status]  => true/false of success
#    *         [id]      => result id or error code
#    *         [message]  => optional message for error message string
#    * @access public
#    */
#   public function deleteTestPlan($args)
        
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testplanid'])
    def deleteTestPlan(self):
        """ Delete a test plan and all related link to other items """
 
    #
    #  public methods for general server calls
    #                                   

    def callServerWithPosArgs(self, methodNameAPI, *argsPositional, **argsOptional):
        """ concat argsPositional and argsOptional before calling 
        server method methodNameAPI """

        if argsPositional:
            # search keys for values and store these pairs in a dictionary
            dictPos = self._convertPostionalArgs(methodNameAPI, argsPositional)
            # extent optional keys+values with positional keys+vales  
            argsOptional.update(dictPos)
        # now, start calling the server with basic error handling
        response = self._callServer(methodNameAPI, argsOptional)
        # check if response is not empyt and not includes error code
        self._checkResponse(response, methodNameAPI, argsOptional) 
        # seams to be ok, so let give them the data
        return response
    
#   /**
#    * addTestCaseKeywords
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param array array $args["keywords"]: map key testcaseexternalid
#    *                                       values array of keyword name 
#    * @return mixed $resultInfo
#    *
#    * call examples:
#    * c$args=array();
#    * c$args["devKey"]=isset($_REQUEST['apiKey']) ? $_REQUEST['apiKey'] : $devKey;
#    * c$args["keywords"] = array('MAB-3' => array('Barbie','Barbie'),
#                                 'MAB-2' => array('Barbie','Jessie'));
#    *
#    * @internal revisions
#    * @since 1.9.13, interface changed in 1.9.14
#    */
#   function addTestCaseKeywords($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['keywords'], [])
    def addTestCaseKeywords(self):
        """ adds list of keywords to a set of test cases 
        
        expects as arg <keywords> a dictionary with 
          <testcaseexternalid> as a key and <list of keywords> as value
        
        example:
          {'TC-4711' : ['KeyWord02'], 'TC-4712' : ['KeyWord01', KeyWord03']}
          
          adds to test case 'TC-4711' the keyword 'KeyWord02'
          adds to test case 'TC-4712' the keywords 'KeyWord01' + KeyWord03'
          """
    
#   /**
#    * removeTestCaseKeywords
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param array array $args["keywords"]: map key testcaseexternalid
#    *                                       values array of keyword name 
#    * @return mixed $resultInfo
#    *
#    * call examples:
#    * c$args=array();
#    * c$args["devKey"]=isset($_REQUEST['apiKey']) ? $_REQUEST['apiKey'] : $devKey;
#    * c$args["keywords"] = array('MAB-3' => array('Barbie','Barbie'),
#                                 'MAB-2' => array('Barbie','Jessie'));
#    *
#    * @internal revisions
#    * @since 1.9.13, interface changed in 1.9.14
#    */
#   function removeTestCaseKeywords($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['keywords'], [])
    def removeTestCaseKeywords(self):
        """ removes list of keywords from a set of test cases 
        
        expects as arg <keywords> a dictionary with 
          <testcaseexternalid> as a key and <list of keywords> as value
        
        example:
          {'TC-4711' : ['KeyWord02'], 'TC-4712' : ['KeyWord01', KeyWord03']}
          
          removes from test case 'TC-4711' the keyword 'KeyWord02'
          removes from test case 'TC-4712' the keywords 'KeyWord01' + KeyWord03'
         """

#   /**
#    *  Delete a test project and all related link to other items
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["prefix"]
#    *
#    * @return mixed $resultInfo
#    *         [status]  => true/false of success
#    *         [message]  => optional message for error message string
#    * @access public
#    */
#    public function deleteTestProject($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['prefix'], [])
    def deleteTestProject(self):
        """ Delete a test project and all related link to other items  """ 
        
#  /**
#    * Update value of Custom Field with scope='design' 
#    * for a given Test Suite
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["testsuiteid"]:  
#    * @param string $args["testprojectid"]: 
#    * @param string $args["customfields"]
#    *               contains an map with key:Custom Field Name, value: value for CF.
#    *               VERY IMPORTANT: value must be formatted in the way it's written to db,
#    *               this is important for types like:
#    *
#    *               DATE: strtotime()
#    *               DATETIME: mktime()
#    *               MULTISELECTION LIST / CHECKBOX / RADIO: se multipli selezione ! come separatore
#    *
#    *
#    *               these custom fields must be configured to be writte during execution.
#    *               If custom field do not meet condition value will not be written
#    *
#    * @return mixed null if everything ok, else array of IXR_Error objects
#    *         
#    * @access public
#    */    
#   public function updateTestSuiteCustomFieldDesignValue($args)
        
  
    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectid', 'testsuiteid', 'customfields'])
    def updateTestSuiteCustomFieldDesignValue(self):
        """ Update value of Custom Field with scope='design' for a given Test Suite

        customfields  : dictionary with customfields names + values
        VERY IMPORTANT: value must be formatted in the way it's written to db
        """

#  /**
#   * Returns all test suites inside target 
#   * test project with target name
#   *
#   * @param
#   * @param struct $args
#   * @param string $args["devKey"]
#   * @param int $args["testsuitename"]
#   * @param string $args["prefix"]
#   * @return mixed $resultInfo
#   * 
#   * @access public
#   */
#   public function getTestSuite($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testsuitename', 'prefix'])
    def getTestSuite(self):
        """ Returns list with all test suites named TESTUITENAME defined for
        test project using PREFIX """


#   /**
#    * update a test suite
#    * 
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["testprojectid"] OR string $args["prefix"] 
#    * @param string $args["testsuitename"] optional
#    * @param string $args["details"] optional
#    * @param int $args["parentid"] optional, if do not provided means test suite must be top level.
#    * @param int $args["order"] optional. Order inside parent container
#    *   
#    * @return mixed $resultInfo
#    */
#   public function updateTestSuite($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testsuiteid'], 
            ['testprojectid', 'prefix', 'parentid', 'testsuitename', 'details',
             'order'])
    def updateTestSuite(self):
        """ update a test suite 
        
        mandatory arg: testsuiteid - identifies the test suite to be change
        
        mandatory args variations: testprojectid or prefix 
        - test project information is general mandatory
        
        optional args:
        - testsuitename - if defined, test suite name will be changed
        - details       - if defined test suite details will be changed
        - order         - if defined, order inside parent container is changed
        """

#    /**
#     * Get Issue Tracker System by name
#     *
#     * @param struct $args
#     * @param string $args["devKey"]
#     * @param string $args["itsname"] ITS name 
#     * @return mixed $itsObject      
#     * @access public
#     */
#     public function getIssueTrackerSystem($args,$call=null)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['itsname'], [])
    def getIssueTrackerSystem(self):
        """ Get Issue Tracker System by name """

# /**
#  * Update value of Custom Field with scope='design'
#  * for a given Build
#  *
#  * @param struct $args
#  * @param string $args["devKey"]: used to check if operation can be done.
#  *                                if devKey is not valid => abort.
#  *
#  * @param string $args["buildid"]:
#  * @param string $args["testprojectid"]:
#  * @param string $args["customfields"]
#  *               contains an map with key:Custom Field Name, value: value for CF.
#  *               VERY IMPORTANT: value must be formatted in the way it's written to db,
#  *               this is important for types like:
#  *
#  *               DATE: strtotime()
#  *               DATETIME: mktime()
#  *               MULTISELECTION LIST / CHECKBOX / RADIO: se multipli selezione ! come separatore
#  *
#  *
#  *               these custom fields must be configured to be writte during execution.
#  *               If custom field do not meet condition value will not be written
#  *
#  * @return mixed null if everything ok, else array of IXR_Error objects
#  *
#  * @access public
#  */
# public function updateBuildCustomFieldsValues($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testprojectid', 'testplanid', 'buildid', 
                               'customfields'])
    def updateBuildCustomFieldsValues(self):
        """ Update value of Custom Field with scope='design' for a given Build

        customfields  : dictionary with customfields names + values
        VERY IMPORTANT: value must be formatted in the way it's written to db
        """

#   /**
#    * Gets a set of EXECUTIONS for a particular testcase on a test plan.
#    * If there are no filter criteria regarding platform and build,
#    * result will be get WITHOUT checking for a particular platform and build.
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["tplanid"]
#    * @param int $args["testcaseid"]: Pseudo optional.
#    *                 if is not present then testcaseexternalid MUST BE present
#    *
#    * @param int $args["testcaseexternalid"]: Pseudo optional.
#    *                 if is not present then testcaseid MUST BE present
#    *
#    * @param string $args["platformid"]: optional. 
#    *                    ONLY if not present, then $args["platformname"] 
#    *                    will be analized (if exists)
#    *
#    * @param string $args["platformname"]: optional (see $args["platformid"])
#    * @param int $args["buildid"]: optional
#    *        ONLY if not present, $args["buildname"] will be analized (if exists)
#    *
#    * @param int $args["buildname"] - optional (see $args["buildid"])
#    * @param int $args["options"] - optional 
#    *                               options['getOrderDescending'] 
#    *                               false(=ascending,default)
#    * @return mixed $resultInfo
#    *               if execution found
#    *               array that contains a map with these keys:
#    *               id (execution id),build_id,tester_id,execution_ts,
#    *               status,testplan_id,tcversion_id,tcversion_number,
#    *               execution_type,notes.
#    *
#    *               if test case has not been executed,
#    *               array('id' => -1)
#    * @access public
#    */
#   public function getExecutionSet($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testplanid'],
                        ['testcaseid', 'testcaseexternalid', 
                         'buildid', 'buildname', 'platformid', 'platformname',
                         'options'])
    def getExecutionSet(self):
        """ Gets a set of EXECUTIONS for a particular testcase on a test plan.
            If there are no filter criteria regarding platform and build, result
            will be get WITHOUT checking for a particular platform and build.
         
        mandatory arg: testplanid - identifies the test plan 
        
        mandatory args variations: testcaseid - testcaseexternalid
        - test case information is general mandatory

        optional args variations:  buildid - buildname
                                   platformid - platformname
        
        options : dictionary with key 'getOrderDescending' and 
                                  values 0 (false = default) or 1 (true)   
        """

# /**
#    * Get requirements
#    *
#    * @param string $args["testprojectid"]
#    * @param string $args["testplanid"] OPTIONAL
#    * @param string $args["platformid"] OPTIONAL
#    *
#    * @return mixed error if someting's wrong, else array of test cases
#    *
#    * @access public
#    */
#   public function getRequirements($args)

    @decoMakerApiCallReplaceTLResponseError()            
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testprojectid'], ['testplanid', 'platformid'])
    def getRequirements(self):
        """ Get requirements.
         
        mandatory arg: testprojectid - identifies the test project 
        
        optional args: testplanid, platformid
        """
  
# /**
#    * Get requirement coverage
#    *
#    * Retrieve the test cases associated to a requirement
#    *
#    * @param struct $args
#    * @param string $args["devKey"]: used to check if operation can be done.
#    *                                if devKey is not valid => abort.
#    *
#    * @param string $args["testprojectid"]
#    * @param string $args["requirementdocid"]
#    *
#    * @return mixed error if someting's wrong, else array of test cases
#    *
#    * @access public
#    */
#   public function getReqCoverage($args)

    @decoMakerApiCallReplaceTLResponseError()            
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testprojectid', 'requirementdocid'], [])
    def getReqCoverage(self):
        """ Get requirement coverage. 
            Retrieve the test cases associated to a requirement
         
        mandatory arg: 
            testprojectid    - identifies the test project 
            requirementdocid - identifies the requirement 

        """
        
#    /**
#     * 
#     * @param struct $args
#     * @param string $args["devKey"]
#     * @param string $args["testcaseexternalid"] format PREFIX-NUMBER
#     * @param int    $args["testsuiteid"] 
#     * 
#     */
#   public function setTestCaseTestSuite($args)      
  
    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testcaseexternalid', 'testsuiteid'], [])
    def setTestCaseTestSuite(self):
        """ move a test case to a different Test Suite 
         
        mandatory arg: 
            testcaseexternalid - identifies the test case 
            testsuiteid        - identifies the test suite 

        """

#   /**
#    * Gets attachments for specified test suite.
#    * The attachment file content is Base64 encoded. To save the file to disk in client,
#    * Base64 decode the content and write file in binary mode.
#    *
#    * @param struct $args
#    * @param string $args["devKey"] Developer key
#    * @param int $args["testsuiteid"]: id of the testsuite
#    *
#    * @return mixed $resultInfo
#    * @author dennis@etern-it.de
#    */
#   public function getTestSuiteAttachments($args)

    @decoApiCallAddDevKey               
    @decoMakerApiCallWithArgs(['testsuiteid'], [])
    def getTestSuiteAttachments(self):
        """ Gets attachments for specified test suite.
        The attachment file content is Base64 encoded. To save the file to disk 
        in client, Base64 decode the content and write file in binary mode.  """

#  /**
#    * Gets ALL EXECUTIONS for a particular testcase on a test plan.
#    * If there are no filter criteria regarding platform and build,
#    * result will be get WITHOUT checking for a particular platform and build.
#    *
#    * @param struct $args
#    * @param string $args["devKey"]
#    * @param int $args["tplanid"]
#    * @param int $args["testcaseid"]: Pseudo optional.
#    *                                 if does not is present then testcaseexternalid MUST BE present
#    *
#    * @param int $args["testcaseexternalid"]: Pseudo optional.
#    *                                         if does not is present then testcaseid MUST BE present
#    *
#    * @param string $args["platform_id"]: optional.
#    *                                    will be analized ONLY if present and exists
#    *
#    * @param int $args["build_id"]: optional
#    *                               will be analized ONLY if present and exists
#    *
#    * @param int $args["options"] - optional
#    *                               options['getBugs'] = true / false
#    *
#    *
#    * @return mixed $resultInfo
#    *               if executions found
#    *               array that contains a map for each execution with these keys:
#    *               id (execution id),build_id,tester_id,execution_ts,
#    *               status,testplan_id,tcversion_id,tcversion_number,
#    *               execution_type,notes.
#    *
#    *               If user has requested getbugs, then a key bugs (that is an array)
#    *               will also exists.
#    *
#    *               if test case has not been execute, the first map will be returned with -1 as 'id'
#    *
#    * @access public
#    */
#     public function getAllExecutionsResults($args)

    @decoApiCallAddDevKey
    @decoMakerApiCallWithArgs(['testplanid'],
                        ['testcaseid', 'testcaseexternalid', 
                         'platformid', 'buildid', 'options'])
    def getAllExecutionsResults(self):
        """ Gets ALL EXECUTIONS for a particular testcase on a test plan.
            If there are no filter criteria regarding platform and build,
            result will be get WITHOUT checking for a particular platform and build.
         
        mandatory arg: testplanid - identifies the test plan 
        
        mandatory args variations: testcaseid - testcaseexternalid
        - test case information is general mandatory

        optional args:  buildid
                        platformid
        
        options : dictionary with key 'getBugs' and 
                                  values 0 (false = default) or 1 (true)   
        """
  
    #
    #  internal methods for general server calls
    #                                   

    def _callServer(self, methodNameAPI, argsAPI=None):
        """ call server method METHODNAMEAPI with error handling and 
        returns the responds
        internal method - should not be called directly """
        
        response = None
        try:
            if argsAPI is None:
                response = getattr(self.server.tl, methodNameAPI)()
            else:
                response = getattr(self.server.tl, methodNameAPI)(argsAPI)
        except (IOError, xmlrpclib.ProtocolError) as msg:
            new_msg = 'problems connecting the TestLink Server %s\n%s' %\
            (self._server_url, msg) 
            raise testlinkerrors.TLConnectionError(new_msg)
        except xmlrpclib.Fault as msg:
            new_msg = 'problems calling the API method %s\n%s' %\
            (methodNameAPI, msg) 
            raise testlinkerrors.TLAPIError(new_msg)

        return response
    
        
    def _convertPostionalArgs(self, methodName, valueList):        
        """ Returns a dictionary with values from VALUELIST and keys for 
            the expected positional argumenst of selfs method METHODNAME 
            
            if VALUELIST does not match the expectation, an error
            testlinkerrors.TLArgError is raised             """
            
        if not methodName in self._positionalArgNames:
            new_msg = '%s - missing positional args configuration' %\
            (methodName)
            raise testlinkerrors.TLArgError(new_msg)
            
        nameList = self._positionalArgNames[methodName]
        length_NameList = len(nameList)
        length_ValueList = len(valueList)
        
        if length_NameList != length_ValueList:
            new_msg = '%s - mismatching number of positional args %i vs %i' %\
            (methodName, length_NameList, length_ValueList)
            new_msg = '%s\n expected args: %s' % (new_msg, ', '.join(nameList))
            raise testlinkerrors.TLArgError(new_msg)

        # issue #20: Following line works with Py27, but not with Py26
        # return {nameList[x] : valueList[x] for x in range(len(nameList)) }
        # this line works with Py26 and Py27 (and is also nice)
        return dict(list(zip(nameList, valueList)))
    
    def _getAttachmentArgs(self, attachmentfile):
        """ returns dictionary with key/value pairs needed, to transfer 
            ATTACHMENTFILE via the api to into TL
            
            ATTACHMENTFILE could be: 
            a) a python file descriptor pointing to the file
            b) a valid file path"""
            
        try:
            # try to handle ATTACHMENTFILE as a file path
            a_file_path = attachmentfile
            a_file_obj  = self._openAttachmentForRead(a_file_path)
            already_file_obj = False
        except TypeError:
            # ATTACHMENTFILE seams to be a file object
            a_file_path = attachmentfile.name
            a_file_obj = attachmentfile
            already_file_obj = True

        try:
            encoded_data = encodebytes(a_file_obj.read())
        except TypeError:
            # a_file_obj seams to have a wrong read mode
            # try to reopen it, if ATTACHMENTFILE already was a file obj
            if already_file_obj:
                encoded_data = self._getAttachmentArgs(attachmentfile.name)
            else:
                raise testlinkerrors.TLArgError(
                                'invalid attachment file: %s' % attachmentfile)
                
            
        return {'filename':os.path.basename(a_file_path),
                'filetype':guess_type(a_file_path)[0],
                'content':encoded_data
                }
        
    def _openAttachmentForRead(self, a_file_path):
        """ open A_FILE_PATH for reading and returns the file descriptor. 
            Read mode will be set depending from py version and mimetype 
            PY2: text file = 'r', others = 'rb'  PY3: general 'rb'
            
            Raise TLArgError, if A_FILE_PATH is not valid
            
            site effect: raise TypeError, if A_FILE_PATH is not a string 
        """
        
        if not os.path.exists(a_file_path):
            # file path does not exists
            raise testlinkerrors.TLArgError(
                                'invalid attachment path: %s' % a_file_path)
            
        a_read_mode = 'rb'
        is_text_file = 'text/' in guess_type(a_file_path)
        if not IS_PY3 and is_text_file:
            # under py2 text file shpuld be open as 'r' and not 'rb'
            # for details compare py2 and py docs
            # https://docs.python.org/2/library/base64.html#base64.encodestring
            # https://docs.python.org/3/library/base64.html#base64.encodebytes
            a_read_mode = 'r'
        return open(a_file_path, a_read_mode)     
    

    def _checkResponse(self, response, methodNameAPI, argsOptional):
        """ Checks if RESPONSE is empty or includes Error Messages
            Will raise TLRepsonseError in this case """
        if response:
            try:
                if 'code' in response[0]:
                    raise testlinkerrors.TLResponseError(
                                    methodNameAPI, argsOptional,
                                    response[0]['message'], response[0]['code'])
            except (TypeError, KeyError):
                # if the reponse has not a [{..}] structure, the check
                #    'code' in response[0]
                # raise an error. Following causes are ok
                # TypeError: raised from doesUserExist, cause the postiv 
                #            response is simply 'True'
                # KeyError: raise from uploadExecutionAttachment, cause the 
                #           positiv response is directly a dictionary
                pass
        else:
            raise testlinkerrors.TLResponseError(methodNameAPI, argsOptional,
                                                 'Empty Response! ')
            
            
        
            
    
    #
    #  ADDITIONNAL FUNCTIONS
    #                                   

    def _apiMethodArgNames(self, methodNameAPI):
        """ returns triple with arg name lists for api METHODNAME
            1. positional api arg names
            2. optional api arg names
            3. other (non api) name
        """
        # collect arg names 
        posArgNames = self._positionalArgNames.get(methodNameAPI, [])
        otherArgs = ([],[])
        try:
            otherArgs = getArgsForMethod(methodNameAPI, posArgNames)
        except testlinkerrors.TLArgError:
            # no API args registered for methodName 
            pass
        return (posArgNames, otherArgs[0], otherArgs[1])
        
    def whatArgs(self, methodNameAPI):
        """ returns for METHODNAME a description with 
            - positional, optional and other (non api) mandatory args
            - methods doc/help string
        """
        
        # collect arg names 
        (posArgNames, optArgNames, manArgNames) = \
                        self._apiMethodArgNames(methodNameAPI)
            
        # get method doc string
        ownMethod = True
        docString = None
        argSeparator = ''
        try:
            apiMethod = self.__getattribute__(methodNameAPI)
            docString = apiMethod.__doc__
        except AttributeError:
            # no real method defined for methodNameAPI
            ownMethod = False
            
        # now we start to build the description
        # first the method name
        methDescr = ''
        if not ownMethod:
            methDescr = "callServerWithPosArgs('%s'" % methodNameAPI
            argSeparator = ', '
            if not optArgNames:
                optArgNames = ['apiArg']
        else:
            methDescr = "%s(" % methodNameAPI

        # description pos and mandatory args
        manArgNames.extend(posArgNames) 
        if manArgNames:
            tmp_l = ['<%s>' % x for x in manArgNames]
            methDescr += '%s%s' % (argSeparator, ", ".join(tmp_l))
            argSeparator = ', '
        # description optional args
        if optArgNames:
            tmp_l = ['%s=<%s>' % (x,x) for x in optArgNames]
            methDescr += '%s[%s]' % (argSeparator, "], [".join(tmp_l))
            
        # closing the method call
        methDescr += ")" 

        # now append methods docstring
        if docString:
            methDescr += "\n%s" % docString 
                        
        return methDescr
    
    def connectionInfo(self):
        """ print current SERVER URL and DEVKEY settings and servers VERSION """

        tl_version = ''
        tl_about = ''
        try:
            tl_version = self.testLinkVersion()
            tl_about   = self.about()
        except testlinkerrors.TLConnectionError as msg:
            tl_version = msg
            
        message = """
Current connection settings
 Server URL: %s
 DevKey    : %s
Server informations
 Version   : %s
%s 
""" 
        return message % (self._server_url, self.devKey, tl_version, tl_about)
    
    def __str__(self):
        message = """
TestLink API - class %s - version %s (PY %s)
@authors: %s
%s
"""
        return message % (self.__class__.__name__, self.__version__,
                          python_version(), 
                          self.__author__, self.connectionInfo())

    
if __name__ == "__main__":
    tl_helper = TestLinkHelper()
    tl_helper.setParamsFromArgs()
    myTestLink = tl_helper.connect(TestlinkAPIGeneric)
    print(myTestLink)




