#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2011-2017 Luiko Czub, Olivier Renault, James Stock, TestLink-API-Python-client developers
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

#import xmlrpclib

from __future__ import print_function
from .testlinkapigeneric import TestlinkAPIGeneric, TestLinkHelper
from .testlinkerrors import TLArgError
import sys


class TestlinkAPIClient(TestlinkAPIGeneric):
    """ client for XML-RPC communication between Python and TestLink 
    
        Inherits TestLink API methods from the generic client TestlinkAPIGeneric.
        
        Defines Service Methods like "countProjects" and change the 
        configuration for positional and optional arguments in a way, that often
        used arguments are positional.
        - see _changePositionalArgConfig()
        - configuration of positional arguments is consistent with v0.4.0
        
        Changes on Service Methods like "countProjects" should be implemented in
        this class or sub classes
        Changes of TestLink API methods should be implemented in generic API 
        TestlinkAPIGeneric. 
    """   
    
    __slots__ = ['stepsList']
    __author__ = 'Luiko Czub, Olivier Renault, James Stock, TestLink-API-Python-client developers'
    
    def __init__(self, server_url, devKey, **kwargs):
        """ call super for init generell slots, init sepcial slots for teststeps
            and define special positional arg settings """
            
        kwargs['allow_none'] = True
        super(TestlinkAPIClient, self).__init__(server_url, devKey, **kwargs)
        # allow_none is an argument from xmlrpclib.Server()
        # with set to True, it is possible to set positional args to None, so 
        # alternative optional arguments could be set
        # example - testcaseid is set : 
        # reportTCResult(None, newTestPlanID, None, 'f', '', guess=True,
        #                             testcaseexternalid=tc_aa_full_ext_id)
        # otherwise xmlrpclib raise an error, that None values are not allowed
        self.stepsList = []
        self._changePositionalArgConfig()
        
    def _changePositionalArgConfig(self):
        """ set special positional arg configuration, which differs from the 
            generic configuration """
        pos_arg_config = self._positionalArgNames
         
        # createTestCases sets argument 'steps' with values from .stepsList
        # - user must not passed a separate stepList
        pos_arg_config['createTestCase'] = ['testcasename', 'testsuiteid', 
                        'testprojectid', 'authorlogin', 'summary'] #, 'steps']
        # getTestCase 
        pos_arg_config['getTestCase'] = ['testcaseid']
        # createVuild
        pos_arg_config['createBuild'] = ['testplanid', 'buildname', 'buildnotes']
        # reportTCResult
        pos_arg_config['reportTCResult'] = ['testcaseid', 'testplanid', 
                                            'buildname', 'status', 'notes']
        # uploadExecutionAttachment
        pos_arg_config['uploadExecutionAttachment'] = ['executionid', 'title', 
                                                       'description']
        # getTestCasesForTestSuite
        pos_arg_config['getTestCasesForTestSuite'] = ['testsuiteid', 'deep', 
                                                      'details']
        # getLastExecutionResult
        pos_arg_config['getLastExecutionResult'] = ['testplanid', 'testcaseid']
        # getTestCaseCustomFieldDesignValue
        pos_arg_config['getTestCaseCustomFieldDesignValue'] = [
                        'testcaseexternalid', 'version' , 'testprojectid', 
                        'customfieldname', 'details']
        # getTestCaseAttachments
        pos_arg_config['getTestCaseAttachments'] = ['testcaseid']
        
        
    #
    #  BUILT-IN API CALLS - extented / customised against generic behaviour
    #
    
    def echo(self, message):
        return self.repeat(message)

    def getTestCaseIDByName(self, *argsPositional, **argsOptional):
        """ getTestCaseIDByName : Find a test case by its name 
        positional args: testcasename, 
        optional args : testsuitename, testprojectname, testcasepathname
        
        testcasepathname : Full test case path name, 
                starts with test project name , pieces separator -> :: 
                  
        server return can be a list or a dictionary 
        - optional arg testprojectname seems to create a dictionary response 
        
        this methods customize the generic behaviour and converts a dictionary 
        response into a list, so methods return will be always a list """

        response = super(TestlinkAPIClient, self).getTestCaseIDByName(
                                                *argsPositional, **argsOptional)
        if type(response) == dict:
            # convert dict into list - just use dicts values
            response = list(response.values())
        return response

    def createTestCase(self, *argsPositional, **argsOptional):
        """ createTestCase: Create a test case
        positional args: testcasename, testsuiteid, testprojectid, authorlogin,
                         summary
        optional args : steps, preconditions, importance, executiontype, order,
                        internalid, checkduplicatedname, actiononduplicatedname,
                        status, estimatedexecduration
                        
        argument 'steps' will be set with values from .stepsList, 
        - when argsOptional does not include a 'steps' item
        - .stepsList can be filled before call via .initStep() and .appendStep()
        
        otherwise, optional arg 'steps' must be defined as a list with 
        dictionaries , example
            [{'step_number' : 1, 'actions' : "action A" , 
                'expected_results' : "result A", 'execution_type' : 0},
                 {'step_number' : 2, 'actions' : "action B" , 
                'expected_results' : "result B", 'execution_type' : 1},
                 {'step_number' : 3, 'actions' : "action C" , 
                'expected_results' : "result C", 'execution_type' : 0}]

        """ 
        
        # store current stepsList as argument 'steps', when argsOptional defines
        # no own 'steps' item
        if self.stepsList:
            if 'steps' in argsOptional:
                raise TLArgError('confusing createTestCase arguments - ' +
                                 '.stepsList and method args define steps')
            argsOptional['steps'] = self.stepsList
            self.stepsList = []
        return super(TestlinkAPIClient, self).createTestCase(*argsPositional, 
                                                             **argsOptional)
        
    #
    #  ADDITIONNAL FUNCTIONS- copy test cases
    #                                   

    def getProjectIDByNode(self, a_nodeid):
        """ returns project id , the nodeid belongs to."""
        
        # get node path 
        node_path = self.getFullPath(int(a_nodeid))[a_nodeid]
        # get project and id
        a_project = self.getTestProjectByName(node_path[0])
        return a_project['id']

    def copyTCnewVersion(self, origTestCaseId, origVersion=None, **changedAttributes):
        """ creates a new version for test case ORIGTESTCASEID
        
        ORIGVERSION specifies the test case version, which should be copied,
                    default is the max version number

        if the new version should differ from the original test case, changed 
        api arguments could be defined as key value pairs. 
        Example for changed summary and importance:
        -  copyTCnewVersion('4711', summary = 'The summary has changed', 
                                    importance = '1')
        Remarks for some special keys:
        'steps': must be a complete list of all steps, changed and unchanged steps
                 Maybe its better to change the steps in a separat call using
                 createTestCaseSteps with action='update'. 
        """
        
        return self._copyTC(origTestCaseId, changedAttributes, origVersion, 
                            duplicateaction = 'create_new_version')
        
    def copyTCnewTestCase(self, origTestCaseId, origVersion=None, **changedAttributes):
        """ creates a test case with values from test case ORIGTESTCASEID
        
        ORIGVERSION specifies the test case version, which should be copied,
                    default is the max version number
        
        if the new test case should differ from the original test case, changed 
        api arguments could be defined as key value pairs. 
        Example for changed test suite and importance:
        -  copyTCnewTestCaseVersion('4711', testsuiteid = '1007', 
                                            importance = '1')
                                            
        Remarks for some special keys:
        'testsuiteid': defines, in which test suite the TC-copy is inserted. 
                 Default is the same test suite as the original test case. 
        'steps': must be a complete list of all steps, changed and unchanged steps
                 Maybe its better to change the steps in a separat call using
                 createTestCaseSteps with action='update'. 
                 
        """
        
        return self._copyTC(origTestCaseId, changedAttributes, origVersion,
                            duplicateaction = 'generate_new')
        
    def getTestCaseByVersion(self, testCaseID, version=None):
        """
        Gets testcase information based on the version.

        :param testCaseID: test case to search for
        :param version: version to search for defaults to None. None searches for latest
        :return: test case info dictionary
        """
        testcases = self.getTestCase(testCaseID, version=version)
        if version is None:
            return testcases[0]
        for testcase in testcases:
            if str(testcase['version']) == str(version):
                return testcase
        else:
            raise RuntimeError("Testcase {} doesn't have version {}.".format(testCaseID, version))

    def _copyTC(self, origTestCaseId, changedArgs, origVersion=None, **options):
        """ creates a copy of test case with id ORIGTESTCASEID
        
        returns createTestCase response for the copy
        
        CHANGEDARGUMENTS defines a dictionary with api arguments, expected from 
                 createTestCase. Only arguments, which differ between TC-orig 
                 and TC-copy must be defined
        Remarks for some special keys:
        'testsuiteid': defines, in which test suite the TC-copy is inserted. 
                 Default is the same test suite as the original test case. 
        'steps': must be a complete list of all steps, changed and unchanged steps
                 Maybe its better to change the steps in a separat call using
                 createTestCaseSteps with action='update'. 
        
        ORIGVERSION specifies the test case version, which should be copied,
                    default is the max version number

        OPTIONS are optional key value pairs to influence the copy process
        - details see comments _copyTCbuildArgs()
    
        """

        # get orig test case content 
        origArgItems = self.getTestCaseByVersion(origTestCaseId, version=origVersion)
        # get orig test case project id 
        origArgItems['testprojectid'] = self.getProjectIDByNode(origTestCaseId)
         
        # build args for the TC-copy
        (posArgValues, newArgItems) = self._copyTCbuildArgs(origArgItems, 
                                                        changedArgs, options)
        # create the TC-Copy
        response = self.createTestCase(*posArgValues, **newArgItems)
        return response
        
    def _copyTCbuildArgs(self, origArgItems, changedArgs, options):
        """  build Args to create a new test case . 
        ORIGARGITEMS is a dictionary with getTestCase response of an existing 
                     test case
        CHANGEDARGS is a dictionary with api argument for createTestCase, which 
                     should differ from these
        OPTIONS is a dictionary with settings for the copy process 

        'duplicateaction': decides, how the TC-copy is inserted
           - 'generate_new' (default): a separate new test case is created, even
                 if name and test suite are equal
           - 'create_new_version': if the target test suite includes already a
                 test case with the same name, a new version is created.
                 if the target test suite includes not a test case with the 
                 defined name, a new test case with version 1 is created
        """

        # collect info, which arguments createTestCase expects
        (posArgNames, optArgNames, manArgNames) = \
                            self._apiMethodArgNames('createTestCase')
        # some argNames not realy needed
        optArgNames.remove('internalid')
        optArgNames.remove('devKey')
                                     
        # mapping between getTestCase response and createTestCase arg names                                      
        externalArgNames = posArgNames[:]
        externalArgNames.extend(optArgNames)
        externalTointernalNames = {'testcasename' : 'name', 
                'testsuiteid' : 'testsuite_id', 'authorlogin' : 'author_login', 
                'executiontype' : 'execution_type', 'order' : 'node_order',
                'estimatedexecduration' : 'estimated_exec_duration' }
        
        # extend origItems with some values needed in createTestCase 
        origArgItems['checkduplicatedname'] = 1 
        origArgItems['actiononduplicatedname'] = options.get('duplicateaction', 
                                                             'generate_new')  
        # build arg dictionary for TC-copy with orig values
        newArgItems = {}
        for exArgName in externalArgNames:
            inArgName = externalTointernalNames.get(exArgName, exArgName) 
            newArgItems[exArgName] = origArgItems[inArgName]
            
        # if changed values defines a different test suite, add the correct 
        # project id
        if 'testsuiteid' in changedArgs:
            changedProjID = self.getProjectIDByNode(changedArgs['testsuiteid'])
            changedArgs['testprojectid'] = changedProjID
         
        # change orig values for TC-copy 
        for (argName, argValue) in list(changedArgs.items()):
            newArgItems[argName] = argValue
        
        # separate positional and optional createTestCase arguments          
        posArgValues = []
        for argName in posArgNames:
            posArgValues.append(newArgItems[argName])
            newArgItems.pop(argName)
            
        return (posArgValues, newArgItems)

    #
    #  ADDITIONNAL FUNCTIONS- keywords
    #                                   

    def listKeywordsForTC(self, internal_or_external_tc_id):
        """ Returns list with keyword for a test case
        INTERNAL_OR_EXTERNAL_TC_ID defines 
        - either the internal test case ID (8111 or '8111')
        - or the full external test case ID ('NPROAPI-2')
        
        Attention: 
        - the tcversion_id is not supported
        - it is not possible to ask for a special test case version, cause TL
          links keywords against a test case and not a test case version 
        """
        
        #ToDo LC 12.01.15 - simplify code with TL 1.9.13 api getTestCaseKeywords
        # - indirect search via test suite and getTestCasesForTestSuite() isn't 
        #   necessary any more
        # - see enhancement issue #45
        
        a_tc_id = str(internal_or_external_tc_id)
        
        if '-' in a_tc_id:
            # full external ID like 'NPROAPI-2', but we need the internal
            a_tc = self.getTestCase(None, testcaseexternalid=a_tc_id )[0]
            a_tc_id = a_tc['testcase_id']

        # getTestCaseKeywords  returns a dictionary like
        #   {'12622': {'34': 'KeyWord01', '36': 'KeyWord03'}}
        # key is the testcaseid, why that? cause it is possible to ask for
        # a set of test cases.  we are just interested in one tc
        a_keyword_dic = self.getTestCaseKeywords(testcaseid=a_tc_id )[a_tc_id]
        keywords = a_keyword_dic.values()

        return list(keywords)

    def listKeywordsForTS(self, internal_ts_id):
        """ Returns dictionary with keyword lists for all test cases of 
            test suite with id == INTERNAL_TS_ID
        """
        
        a_ts_id = str(internal_ts_id) 
        all_tc_for_ts = self.getTestCasesForTestSuite(a_ts_id, False, 
                                                     'full', getkeywords=True)
        response = {}
        for a_ts_tc in all_tc_for_ts:
            tc_id = a_ts_tc['id']
            keyword_details =  a_ts_tc.get('keywords', {})
            if sys.version_info[0] < 3:
                keywords = map((lambda x: x['keyword']), keyword_details.values())
            else:
                keywords = [kw['keyword'] for kw in keyword_details.values()]
            response[tc_id] = keywords
        
        return response
    
    #
    #  ADDITIONNAL FUNCTIONS
    #                                   

    def countProjects(self):
        """ countProjects :
        Count all the test project   
        """
        projects=self.getProjects()
        return len(projects)
    
    def countTestPlans(self):
        """ countProjects :
        Count all the test plans   
        """
        projects=self.getProjects()
        nbTP = 0
        for project in projects:
            ret = self.getProjectTestPlans(project['id'])
            nbTP += len(ret)
        return nbTP

    def countTestSuites(self):
        """ countProjects :
        Count all the test suites   
        """
        projects=self.getProjects()
        nbTS = 0
        for project in projects:
            TestPlans = self.getProjectTestPlans(project['id'])
            for TestPlan in TestPlans:
                TestSuites = self.getTestSuitesForTestPlan(TestPlan['id'])
                nbTS += len(TestSuites)
        return nbTS
               
    def countTestCasesTP(self):
        """ countProjects :
        Count all the test cases linked to a Test Plan   
        """
        projects=self.getProjects()
        nbTC = 0
        for project in projects:
            TestPlans = self.getProjectTestPlans(project['id'])
            for TestPlan in TestPlans:
                TestCases = self.getTestCasesForTestPlan(TestPlan['id'])
                nbTC += len(TestCases)
        return nbTC
        
    def countTestCasesTS(self):
        """ countProjects :
        Count all the test cases linked to a Test Suite   
        """
        projects=self.getProjects()
        nbTC = 0
        for project in projects:
            TestPlans = self.getProjectTestPlans(project['id'])
            for TestPlan in TestPlans:
                TestSuites = self.getTestSuitesForTestPlan(TestPlan['id'])
                for TestSuite in TestSuites:
                    TestCases = self.getTestCasesForTestSuite(
                                                 TestSuite['id'],'true','full')
                    for TestCase in TestCases:
                        nbTC += len(TestCases)
        return nbTC

    def countPlatforms(self):
        """ countPlatforms :
        Count all the Platforms in TestPlans 
        """
        projects=self.getProjects()
        nbPlatforms = 0
        for project in projects:
            TestPlans = self.getProjectTestPlans(project['id'])
            for TestPlan in TestPlans:
                Platforms = self.getTestPlanPlatforms(TestPlan['id'])
                nbPlatforms += len(Platforms)
        return nbPlatforms
        
    def countBuilds(self):
        """ countBuilds :
        Count all the Builds  
        """
        projects=self.getProjects()
        nbBuilds = 0
        for project in projects:
            TestPlans = self.getProjectTestPlans(project['id'])
            for TestPlan in TestPlans:
                Builds = self.getBuildsForTestPlan(TestPlan['id'])
                nbBuilds += len(Builds)
        return nbBuilds
        
    def listProjects(self):
        """ listProjects :
        Lists the Projects (display Name & ID)  
        """
        projects=self.getProjects()
        for project in projects:
            print("Name: %s ID: %s " % (project['name'], project['id']))
  

    def initStep(self, actions, expected_results, execution_type):
        """ initStep :
        Initializes the list which stores the Steps of a Test Case to create  
        """
        self.stepsList = []
        lst = {}
        lst['step_number'] = '1'
        lst['actions'] = actions
        lst['expected_results'] = expected_results
        lst['execution_type'] = str(execution_type)
        self.stepsList.append(lst)
        return True
        
    def appendStep(self, actions, expected_results, execution_type):
        """ appendStep :
        Appends a step to the steps list  
        """
        lst = {}
        lst['step_number'] = str(len(self.stepsList)+1)
        lst['actions'] = actions
        lst['expected_results'] = expected_results
        lst['execution_type'] = str(execution_type)
        self.stepsList.append(lst)
        return True                
                                        
    def getProjectIDByName(self, projectName):   
        projects=self.getProjects()
        result=-1
        for project in projects:
            if (project['name'] == projectName): 
                result = project['id']
                break
        return result

    
if __name__ == "__main__":
    tl_helper = TestLinkHelper()
    tl_helper.setParamsFromArgs()
    myTestLink = tl_helper.connect(TestlinkAPIClient)
    print(myTestLink)



