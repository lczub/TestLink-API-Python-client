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

# this test works WITHOUT an online TestLink Server
# no calls are send to a TestLink Server

import sys, os.path
import unittest
    
if sys.version_info[0] == 2 and sys.version_info[1] == 7:
    # py27 and py31 assertRaisesRegexp was renamed in py32 to assertRaisesRegex
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp
    # py27 and py31 assertRegexpMatches was renamed in py32 to assertRegex
    unittest.TestCase.assertRegex = unittest.TestCase.assertRegexpMatches
    

from testlink import TestlinkAPIGeneric, TestLinkHelper
from testlink.testlinkerrors import TLArgError, TLResponseError, TLAPIError


#from testlink.testlinkapigeneric import positionalArgNamesDefault
# scenario_a includes response from a testlink 1.9.8 server
SCENARIO_A = {'repeat' : 'You said: One World',
              'sayHello' : 'Hey Folks!',
              'doesUserExist' : {
                'Big Bird' :  [{'message': '(doesUserExist) - Cannot Find User Login provided (Big Bird).', 
                                'code': 10000}],
                'admin' : True },
              'getProjectTestPlans' : {
                'onePlan' : [{'name': 'TestPlan_API', 
                         'notes': 'New TestPlan created with the API', 
                         'active': '1', 'is_public': '1', 
                         'testproject_id': '21', 'id': '22'}] ,
                'noPlan' : '' },
              'getBuildsForTestPlan' : {'noBuild' : '' },
              'getTestPlanPlatforms' : {
                'twoPlatforms' : [{'notes': '', 'id': '1', 'name': 'dutch'}, 
                                  {'notes': '', 'id': '2', 'name': 'platt'}],
                'noPlatform' : [{'message': 'Test plan (noPlatform) has no platforms linked', 
                         'code': 3041}]},
              'getTestSuitesForTestPlan' : {'noSuite' : ''},
              'getTestSuitesForTestSuite' : {'noSuite' : ''},
              'getFirstLevelTestSuitesForTestProject' : {
                'noSuite' : [{'message': 'Test Project (noSuite) is empty.', 
                              'code': 7008}]},
              'getTestCasesForTestSuite' : {'noTestCase' : [] },
              'getTestCasesForTestPlan'  : {'noTestCase' : [] },
              'getTestCaseIDByName' : {
                'dictResult' :  {'1': {'parent_id': '24', 'tc_external_id': '2', 
                                       'id': '33', 'tsuite_name': 'B - First Level', 
                                       'name': 'TESTCASE_B'}}, 
                'listResult' : [{'parent_id': '25', 'tc_external_id': '1', 
                                 'id': '26', 'tsuite_name': 'AA - Second Level', 
                                 'name': 'TESTCASE_AA'}]},
              'getProjectPlatforms' : {
                   'twoPlatforms' : {'dutch' : {'id': '1', 'name': 'dutch'}, 
                                     'platt' : {'id': '2', 'name': 'platt'}},
                    'noPlatform'  : {}   
                    },
              'reportTCResult' :  [{'status': True, 'operation': 'reportTCResult', 
                                    'message': 'Success!', 'overwrite': False, 'id': '773'}],              
              'getProjectKeywords' : {
                   'twoKeywords' : {'25': 'KeyWord01', '26': 'KeyWord02'},
                   'noKeyword'   : {}   
                    },              
              'getTestCaseKeywords' : {
                   'twoKeywords' : {'25': 'KeyWord01', '26': 'KeyWord02'},
                   'noKeyword'   : {}
                   }   
              }

# scenario_tl198 used by test with older responses, changed in TL 1.9.9
SCENARIO_TL198 = {'testLinkVersion' : 'unknown',
                  'about' : 'Testlink API Version: 1.0 ...'}

# scenario_tl199 used by test with newer responses, changed in TL 1.9.9
SCENARIO_TL199 = {'testLinkVersion' : '1.9.9',
                  'about' : 'Testlink API Version: 1.0 ...'}

# scenario_custom_fields defines response for custom field request
# {'default_value': '', 'enable_on_execution': '1', 'name': 'cf_tc_ex_string', 'location': '1', 'enable_on_design': '0', 'valid_regexp': '', 'length_min': '0', 'possible_values': '', 'value': 'a custom string', 'label': 'CF Exec String', 'show_on_testplan_design': '0', 'display_order': '1', 'length_max': '0', 'show_on_design': '0', 'required': '0', 'show_on_execution': '1', 'type': '0', 'id': '24', 'node_id': '7691', 'enable_on_testplan_design': '0'}
SCENARIO_CUSTOM_FIELDS = {
            'getTestCaseCustomFieldDesignValue' : {
                'cf_notAssigned' : [{'message': '(getTestCaseCustomFieldDesignValue) - Custom Field (name:cf_tc_sd_string), is not assigned to Test Project(name=PROJECT_API_GENERIC-8 / id=7760)', 
                                  'code': 9003}],
                'cf_full' : {'default_value': '', 'enable_on_execution': '0', 'name': 'cf_tc_sd_string', 
                          'location': '1', 'enable_on_design': '1', 'valid_regexp': '', 'length_min': '0', 'possible_values': '', 
                          'value': 'a custom spec design string', 'label': 'CF SpecDesign String', 'show_on_testplan_design': '0', 
                          'display_order': '1', 'length_max': '0', 'show_on_design': '1', 'required': '0', 'show_on_execution': '1', 
                          'type': '0', 'id': '22', 'node_id': '7691', 'enable_on_testplan_design': '0'},
                'cf_value'  : 'a custom spec design string',
                'cf_valueEmpty'  : '',
                'cf_simple' : {'type': '0', 'name': 'cf_tc_sd_string', 
                            'value': 'a custom spec design string', 'label': 'CF SpecDesign String'}
                                                     },
            'updateTestCaseCustomFieldDesignValue' : {
                'cf_notAssigned' : '',
                'a_string' : ''
                },
                          
            'getTestCaseCustomFieldExecutionValue' : {
                'cf_notAssigned' : '',
                'cf_full' : {'default_value': '', 'enable_on_execution': '1', 'name': 'cf_tc_ex_string', 
                             'location': '1', 'enable_on_design': '0', 'valid_regexp': '', 'length_min': '0', 'possible_values': '', 
                             'value': 'a custom exec string', 'label': 'CF Exec String', 'show_on_testplan_design': '0', 
                             'display_order': '1', 'length_max': '0', 'show_on_design': '0', 'required': '0', 'show_on_execution': '1', 
                             'type': '0', 'id': '24', 'node_id': '7691', 'enable_on_testplan_design': '0'}
                                                      },

            'getTestCaseCustomFieldTestPlanDesignValue' : {
                'cf_notAssigned' : '',
                'cf_full' : {'default_value': '', 'enable_on_execution': '0', 'name': 'cf_tc_pd_string', 
                             'enable_on_design': '0', 'valid_regexp': '', 'length_min': '0', 'possible_values': '', 
                             'value': 'a custom PlanDesign string', 'label': 'CF PlanDesign String', 'show_on_testplan_design': '1', 
                             'display_order': '1', 'length_max': '0', 'show_on_design': '0', 'required': '0', 'show_on_execution': '1', 
                             'type': '0', 'id': '28', 'node_id': '779', 'enable_on_testplan_design': '1'}
                                                           },
            'getTestSuiteCustomFieldDesignValue' : {
                'cf_notAssigned' : '',
                'cf_full' : {'default_value': '', 'enable_on_execution': '0', 'name': 'cf_ts_string', 'location': '1', 
                             'enable_on_design': '1', 'valid_regexp': '', 'length_min': '0', 'possible_values': '', 
                             'value': 'a custom TSuite string', 'label': 'CF TestSuite String', 'show_on_testplan_design': '0', 
                             'display_order': '1', 'length_max': '0', 'show_on_design': '1', 'required': '0', 'show_on_execution': '1', 
                             'type': '0', 'id': '30', 'node_id': '', 'enable_on_testplan_design': '0'}
                                                    },

            'getTestPlanCustomFieldDesignValue' : {
                'cf_notAssigned' : '',
                'cf_full' : {'default_value': '', 'enable_on_execution': '0', 'name': 'cf_tp_string', 'location': '1', 
                             'enable_on_design': '1', 'valid_regexp': '', 'length_min': '0', 'possible_values': '', 
                             'value': 'a custom TPlan string', 'label': 'CF TPlan String', 'show_on_testplan_design': '0',
                             'display_order': '1', 'length_max': '0', 'show_on_design': '1', 'required': '0', 'show_on_execution': '1', 
                             'type': '0', 'id': '31', 'node_id': '', 'enable_on_testplan_design': '0'}
                                                   },
                          
            'getReqSpecCustomFieldDesignValue' :  {
                'cf_notAssigned' : '',
                'cf_full' : {'default_value': '', 'enable_on_execution': '0', 'name': 'cf_req_sd_string', 'location': '1', 
                             'enable_on_design': '1', 'valid_regexp': '', 'length_min': '0', 'possible_values': '', 
                             'value': 'a custom ReqSpec string', 'label': 'CF ReqSpec String', 'show_on_testplan_design': '0', 
                             'display_order': '1', 'length_max': '0', 'show_on_design': '1', 'required': '0', 'show_on_execution': '0', 
                             'type': '0', 'id': '32', 'node_id': '', 'enable_on_testplan_design': '0'}
                                                   },
            'getRequirementCustomFieldDesignValue' : {
                'cf_notAssigned' : '',
                'cf_full' : {'default_value': '', 'enable_on_execution': '0', 'name': 'cf_req_string', 'location': '1', 
                             'enable_on_design': '1', 'valid_regexp': '', 'length_min': '0', 'possible_values': '', 
                             'value': 'a custom Req string', 'label': 'CF Req String', 'show_on_testplan_design': '0', 
                             'display_order': '1', 'length_max': '0', 'show_on_design': '1', 'required': '0', 'show_on_execution': '0', 
                             'type': '0', 'id': '33', 'node_id': '', 'enable_on_testplan_design': '0'}
                                                      }

                          }

# scenario_keywords defines response with keywords
SCENARIO_KEYWORDS = {'getTestCasesForTestSuite' : {
                    'noTestCase' : [] ,
                    'keyWords'  : [{'node_order': '0', 'is_open': '1', 
                        'keywords': {'1': {'keyword_id': '1', 'notes': 'a key word', 'testcase_id': '8144', 'keyword': 'KeyWord01'}, 
                                     '3': {'keyword_id': '3', 'notes': 'a third key word', 'testcase_id': '8144', 'keyword': 'KeyWord03'}}, 
                        'id': '8144', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '2', 'parent_id': '8134', 
                        'version': '1', 'estimated_exec_duration': '3.00', 'updater_id': '2', 'status': '1', 
                        'tsuite_name': 'B - First Level', 'importance': '3', 'modification_ts': '2014-06-30 20:45:40', 
                        'execution_type': '1', 'preconditions': '<p>\n\tthese are the preconditions</p>\n', 'active': '1', 
                        'creation_ts': '2014-06-28 22:06:17', 'node_table': 'testcases', 'tcversion_id': '8145', 
                        'name': 'TESTCASE_B', 'summary': '<p>\n\tThis is the summary of the Test Case B</p>\n', 
                        'steps': [{'step_number': '1', 'actions': 'Step action 1 -b ', 'execution_type': '2', 'active': '1', 'id': '8151', 'expected_results': 'Step result 1 - b'}, 
                                  {'step_number': '2', 'actions': 'Step action 2 -b ', 'execution_type': '2', 'active': '1', 'id': '8152', 'expected_results': 'Step result 2 - b'}, 
                                  {'step_number': '3', 'actions': 'action 3 createTestCaseSteps.update', 'execution_type': '2', 'active': '1', 'id': '8153', 'expected_results': 'update - cause step 3 already exist'}, 
                                  {'step_number': '4', 'actions': 'Step action 4 -b ', 'execution_type': '2', 'active': '1', 'id': '8154', 'expected_results': 'Step result 4 - b'}, 
                                  {'step_number': '5', 'actions': 'Step action 5 -b changed by updateTestCase', 'execution_type': '2', 'active': '1', 'id': '8155', 'expected_results': 'Step result 5 - b changed'}, 
                                  {'step_number': '6', 'actions': 'Step action 6 -b added by updateTestCase', 'execution_type': '2', 'active': '1', 'id': '8156', 'expected_results': 'Step result 6 - b added'}, 
                                  {'step_number': '7', 'actions': 'action 7 createTestCaseSteps.create', 'execution_type': '2', 'active': '1', 'id': '8157', 'expected_results': 'create - cause step 7 not yet exist'}, 
                                  {'step_number': '8', 'actions': 'action 8 createTestCaseSteps.update', 'execution_type': '2', 'active': '1', 'id': '8158', 'expected_results': 'create - cause step 8 not yet exist'}], 
                                    'author_id': '1', 'external_id': 'GPROAPI10-2'}]
                                            } 
                     }

# scenario_no_project simulates a fresh empty test link application
SCENARIO_NO_PROJECT = {'getProjects' : [] }

# scenario_requirements defines response with requirements
SCENARIO_REQUIREMENTS = {
    'getRequirements' : {
            'allReqs' : [{'id': '15344', 'req_doc_id': 'use-case-01'}, 
                             {'id': '15346', 'req_doc_id': 'none-function-01'}, 
                             {'id': '15350', 'req_doc_id': 'restriction-01'}, 
                             {'id': '15352', 'req_doc_id': 'user-gui-01'}, 
                             {'id': '15356', 'req_doc_id': 'system-func-01'}, 
                             {'id': '15358', 'req_doc_id': 'feature-01'}],
            'noReqs' : [],
            'with_srs_id' : [{'id': '15344', 'req_doc_id': 'use-case-01', 'srs_id': '15342'}, 
                             {'id': '15346', 'req_doc_id': 'none-function-01', 'srs_id': '15342'}, 
                             {'id': '15350', 'req_doc_id': 'restriction-01', 'srs_id': '15348'}, 
                             {'id': '15352', 'req_doc_id': 'user-gui-01', 'srs_id': '15348'}, 
                             {'id': '15356', 'req_doc_id': 'system-func-01', 'srs_id': '15354'}, 
                             {'id': '15358', 'req_doc_id': 'feature-01', 'srs_id': '15354'}] 
                         },
    'getReqCoverage' : {
            'reqCovered' : [{'id': '15326', 'name': 'TESTCASE_B', 'tc_external_id': '2', 
                             'login': 'pyTLapi', 'creation_ts': '2017-04-05 20:55:51'}],
            'reqNotCovered' : '',
            'reqUnknown' : [{'code': 11004, 
                             'message': '(getReqCoverage) - Requirement (docid=req_doc_unknown) does not belong to project (id=15312).'}]
                         }
                         }


# example text file attachment = this python file
# why not using os.path.realpath(__file__)
# -> cause __file__ could be compiled python file *.pyc, if the test run is 
#    repeated without changing the test code
ATTACHMENT_EXAMPLE_TEXT= os.path.join(os.path.dirname(__file__), 
                                      'testlinkapigeneric_offline_test.py')

                          
class DummyAPIGeneric(TestlinkAPIGeneric):
    """ Dummy for Simulation TestLinkAPIGeneric. 
    Overrides 
    - _callServer() Method to return test scenarios
    - extend positional_arg_names for  method 'DummyMethod'
    """

    __slots__ = ['scenario_data', 'callArgs']
  
    def __init__(self, server_url, devKey, **args):
        super(DummyAPIGeneric, self).__init__(server_url, devKey, **args)
        self._positionalArgNames['DummyMethod'] = ['Uno', 'due', 'tre']
        self.scenario_data = {}
        self.callArgs = None


    def loadScenario(self, a_scenario):
        self.scenario_data = a_scenario
        self.callArgs = None

    def _callServer(self, methodAPI, argsAPI=None):
        self.callArgs = argsAPI
        response = None
        if methodAPI in ['DummyMethod']:
            response = [argsAPI]
        else:
            data = self.scenario_data[methodAPI]
            if methodAPI in ['doesUserExist']:
                response = data[argsAPI['user']]
            elif methodAPI in ['getProjectTestPlans', 'getProjectPlatforms',
                               'getFirstLevelTestSuitesForTestProject', 
                               'getProjectKeywords', 'getRequirements',
                               'getReqCoverage']:
                response = data[argsAPI['testprojectid']]
            elif methodAPI in ['getBuildsForTestPlan', 'getTestPlanPlatforms', 
                        'getTestSuitesForTestPlan', 'getTestCasesForTestPlan']:
                response = data[argsAPI['testplanid']]
            elif methodAPI in ['getTestSuitesForTestSuite', 
                               'getTestCasesForTestSuite']:
                response = data[argsAPI['testsuiteid']]
            elif methodAPI in ['getTestCaseIDByName']:
                response = data[argsAPI['testcasename']]
            elif methodAPI in ['getTestCaseKeywords']:
                response = data[argsAPI['testcaseid']]
            elif methodAPI in ['testLinkVersion']:
                response = data
                if data == 'unknown':
                    raise TLAPIError('problems calling the API method testLinkVersion1')
            elif methodAPI == 'updateTestCaseCustomFieldDesignValue':
                response = data[argsAPI['customfields']['cf_field1']]               
            elif 'CustomField' in methodAPI:
                response = data[argsAPI['customfieldname']]
            else:
                response = data
        return response
    
    
class TestLinkAPIGenericOfflineTestCase(unittest.TestCase):
    """ TestCases for TestlinkAPIGeneric - does not interacts with a TestLink Server.
    works with DummyAPIGeneric which returns special test data
    """

    @classmethod
    def setUpClass(cls):
        cls.api = TestLinkHelper().connect(DummyAPIGeneric)

#    def tearDown(self):
#        pass


    def test_convertPositionalArgs(self):
        response = self.api._convertPostionalArgs('DummyMethod',  [1,2,3])
        self.assertEqual({'Uno' : 1, 'due' :2, 'tre' : 3}, response)
        
    def test__convertPositionalArgs_missingConf(self):
        client = self.api
        def a_func(a_api): a_api._convertPostionalArgs('NoConfigMethod',  [1,2])
        self.assertRaises(TLArgError, a_func, client)
        
    def test__convertPositionalArgs_lessValues(self):
        client = self.api
        def a_func(a_api): a_api._convertPostionalArgs('DummyMethod',  [1,2])
        self.assertRaises(TLArgError, a_func, client)
        
    def test__convertPositionalArgs_moreValues(self):
        client = self.api
        def a_func(a_api): a_api._convertPostionalArgs('DummyMethod',  [1,2,3,4])
        self.assertRaises(TLArgError, a_func, client)

    def test_callServerWithPosArgs_pos(self):
        self.api.callServerWithPosArgs('DummyMethod',  1,2,3)
        self.assertEqual({'Uno' : 1, 'due' :2, 'tre' : 3}, self.api.callArgs)

    def test_callServerWithPosArgs_pos_opt(self):
        self.api.callServerWithPosArgs('DummyMethod',  1,2,3, quad=4)
        self.assertEqual({'Uno' : 1, 'due' :2, 'tre' : 3, 'quad' : 4}, self.api.callArgs)

    def test_callServerWithPosArgs_opt(self):
        self.api.callServerWithPosArgs('DummyMethod',  quad=4)
        self.assertEqual({'quad' : 4}, self.api.callArgs)

    def test_callServerWithPosArgs_none(self):
        self.api.callServerWithPosArgs('DummyMethod')
        self.assertEqual({}, self.api.callArgs)
        
    def test_checkResponse_emptyResponse(self):
        client = self.api
        def a_func(a_api, response): 
            a_api._checkResponse(response, 'DummyMethod',  
                                 {'Uno' : 1, 'due' :2, 'tre' : 3})
        self.assertRaises(TLResponseError, a_func, client, '')
        self.assertRaises(TLResponseError, a_func, client, [])
        
    def test_checkResponse_errorResponse(self):
        client = self.api
        responseA = [{'message': '(reportTCResult) - TC ID 709 does not exist!', 
                      'code': 5000}]
        def a_func(a_api, response): 
            a_api._checkResponse(response, 'DummyMethod',  
                                 {'Uno' : 1, 'due' :2, 'tre' : 3})
        self.assertRaises(TLResponseError, a_func, client, responseA)

    def test_checkResponse_okResponse(self):
        self.api._checkResponse(
                        [{'message': 'all fine, cause no key with name code'}],
                         'DummyMethod', {'Uno' : 1, 'due' :2, 'tre' : 3})
        self.api._checkResponse(
                        'some API Call juts returns one string without codes',
                         'DummyMethod', {'Uno' : 1, 'due' :2, 'tre' : 3})
        
    def test_checkResponse_booleanResponse(self):
        response = True
        self.api._checkResponse(response, 'DummyMethod', 
                                {'Uno' : 1, 'due' :2, 'tre' : 3})
        
    def test_checkResponse_dictionaryResponse(self):
        response = {'note' : 'uploadAttachment Calls return {..} and not [{..}]'}
        self.api._checkResponse(response, 'DummyMethod', 
                                {'Uno' : 1, 'due' :2, 'tre' : 3})
        
    def test_checkResponse_errorResponse_sringCode(self):
        client = self.api
        
        responseA = [{'message': '(getUserByID) - Cannot Find User with DB ID (4711).', 
                      'code': 'NO_USER_BY_ID_LOGIN'}]
        def a_func(a_api, response): 
            a_api._checkResponse(response, 'getUserByID',  
                                 {'userid' : 4711})
        self.assertRaises(TLResponseError, a_func, client, responseA)

    def test__apiMethodArgNames_noArgs(self):
        response = self.api._apiMethodArgNames('sayHello')
        self.assertEqual(response, ([], [], []))

    def test__apiMethodArgNames_onlyOptionalArgs(self):
        response = self.api._apiMethodArgNames('getTestCaseAttachments')
        self.assertEqual(response[0], [])
        self.assertGreater(len(response[1]), 0)
        self.assertEqual(response[2], [])

    def test__apiMethodArgNames__OptionalAndPositionalArgs(self):
        response = self.api._apiMethodArgNames('createBuild')
        self.assertGreater(len(response[0]), 0)
        self.assertGreater(len(response[1]), 0)
        self.assertEqual(response[2], [])

    def test__apiMethodArgNames__MandatoryArgs(self):
        response = self.api._apiMethodArgNames('uploadExecutionAttachment')
        self.assertGreater(len(response[0]), 0)
        self.assertGreater(len(response[1]), 0)
        self.assertGreater(len(response[2]), 0)

    def test_noWrapperName_apiMethods(self):
        " decorator test: API Methods internal function name should be unchanged "
        
        # apiMethod with decorator @decoApiCallWithoutArgs
        self.assertEqual('sayHello', self.api.sayHello.__name__)
        # apiMethod with decorator @decoApiCallWithArgs
        self.assertEqual('repeat', self.api.repeat.__name__)
        # apiMethod with decorator @decoApiCallAddDevKey 
        self.assertEqual('createBuild', self.api.createBuild.__name__)
        # apiMethod with decorator @decoMakerApiCallReplaceTLResponseError()
        self.assertEqual('getProjectTestPlans', self.api.getProjectTestPlans.__name__)
        # apiMethod with decorator @decoApiCallAddAttachment
        self.assertEqual('uploadExecutionAttachment', self.api.uploadExecutionAttachment.__name__)
        
    def test_ping(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.ping()
        self.assertEqual('Hey Folks!', response)
        
        
    def test_getProjectTestPlans_noPlan(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectTestPlans('noPlan')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getProjectTestPlans_onePlan(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectTestPlans('onePlan')
        self.assertEqual('21', response[0]['testproject_id'])
        self.assertEqual(1, len(response))
        
    def test_getProjectPlatforms_noPlatform(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectPlatforms('noPlatform')
        self.assertEqual({}, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getProjectPlatforms_twoPlatforms(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectPlatforms('twoPlatforms')
        self.assertEqual('1', response['dutch']['id'])
        self.assertEqual(2, len(response))
        
        
    def test_getBuildsForTestPlan_noBuild(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getBuildsForTestPlan('noBuild')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestPlanPlatforms_noPlatform(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestPlanPlatforms('noPlatform')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestPlanPlatforms_twoPlatforms(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestPlanPlatforms('twoPlatforms')
        self.assertEqual('dutch', response[0]['name'])
        self.assertEqual(2, len(response))

    def test_getTestSuitesForTestPlan_noSuite(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestSuitesForTestPlan('noSuite')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
       
    def test_getTestSuitesForTestSuite_noSuite(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestSuitesForTestSuite('noSuite')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getFirstLevelTestSuitesForTestProject_noSuite(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getFirstLevelTestSuitesForTestProject('noSuite')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestCasesForTestSuite_noTestCase(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCasesForTestSuite('noTestCase')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getTestCasesForTestSuite_keyWords(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.getTestCasesForTestSuite('keyWords', details='full', 
                                                     getkeywords=True)
        self.assertIn('keywords', response[0])
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
           
    def test_getTestCasesForTestPlan_noTestCase(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCasesForTestPlan('noTestCase')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestCaseIDByName_dictResult(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCaseIDByName('dictResult', 
                                            testprojectname='NEW_PROJECT_API')
        self.assertEqual(dict, type(response))
        self.assertEqual('TESTCASE_B', response['1']['name']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getTestCaseIDByName_listResult(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCaseIDByName('listResult')
        self.assertEqual(list, type(response))
        self.assertEqual('TESTCASE_AA', response[0]['name']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_testLinkVersion_beforeTL199(self):
        self.api.loadScenario(SCENARIO_TL198)
        response = self.api.testLinkVersion()
        self.assertEqual('<= 1.9.8', response)
        
    def test_testLinkVersion_withTL199(self):
        self.api.loadScenario(SCENARIO_TL199)
        response = self.api.testLinkVersion()
        self.assertEqual('1.9.9', response)
        
    def test_connectionInfo_beforeTL199(self):
        self.api.loadScenario(SCENARIO_TL198)
        response = self.api.connectionInfo()
        self.assertRegex(response, r'\d*\.\d*\.\d*')
        
    def test_getTestCaseCustomFieldDesignValue_notAssigned(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        with self.assertRaisesRegex(TLResponseError, '9003.*Custom Field.*not assigned'):
            response = self.api.getTestCaseCustomFieldDesignValue('GPROAPI8-2', 
                            1, '7760', 'cf_notAssigned', details='full')
            
    def test_getTestCaseCustomFieldDesignValue_full(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestCaseCustomFieldDesignValue('GPROAPI8-2', 
                            1, '7760', 'cf_full', details='full') 
        self.assertEqual('a custom spec design string', response['value'])           
        self.assertEqual('1', response['enable_on_design'])           
        self.assertEqual('0', response['enable_on_testplan_design']) 
        self.assertEqual('0', response['enable_on_execution'])           

    def test_getTestCaseCustomFieldDesignValue_value(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestCaseCustomFieldDesignValue('GPROAPI8-2', 
                            1, '7760', 'cf_value', details='value') 
        self.assertEqual('a custom spec design string', response)           

    def test_getTestCaseCustomFieldDesignValue_valueEmpty(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestCaseCustomFieldDesignValue('GPROAPI8-2', 
                            1, '7760', 'cf_valueEmpty', details='value') 
        self.assertEqual('', response)   
                
    def test_getTestCaseCustomFieldDesignValue_simple(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestCaseCustomFieldDesignValue('GPROAPI8-2', 
                            1, '7760', 'cf_simple', details='simple') 
        self.assertEqual('a custom spec design string', response['value'])           

    def test_updateTestCaseCustomFieldDesignValue_simple(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.updateTestCaseCustomFieldDesignValue('GPROAPI8-2', 
                            1, '7760', {'cf_field1'  : 'a_string'}) 
        self.assertEqual('', response)

    def test_getTestCaseCustomFieldExecutionValue_notAssigned(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestCaseCustomFieldExecutionValue(
                                    'cf_notAssigned', '7760', 1, '792', '7761') 
        self.assertEqual(None, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getTestCaseCustomFieldExecutionValue_full(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestCaseCustomFieldExecutionValue(
                                        'cf_full', '7760', 1, '792', '7761') 
        self.assertEqual('a custom exec string', response['value'])           
        self.assertEqual('0', response['enable_on_design']) 
        self.assertEqual('0', response['enable_on_testplan_design']) 
        self.assertEqual('1', response['enable_on_execution'])           

    def test_getTestCaseCustomFieldTestPlanDesignValue_notAssigned(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestCaseCustomFieldTestPlanDesignValue(
                                    'cf_notAssigned', '7760', 1, '7761', '779') 
        self.assertEqual(None, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getTestCaseCustomFieldTestPlanDesignValue_full(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestCaseCustomFieldTestPlanDesignValue(
                                        'cf_full', '7760', 1, '7761', '779') 
        self.assertEqual('a custom PlanDesign string', response['value'])           
        self.assertEqual('0', response['enable_on_design']) 
        self.assertEqual('1', response['enable_on_testplan_design']) 
        self.assertEqual('0', response['enable_on_execution'])           

    def test_getTestSuiteCustomFieldDesignValue_notAssigned(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestSuiteCustomFieldDesignValue(
                                            'cf_notAssigned', '7760', '7762') 
        self.assertEqual(None, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getTestSuiteCustomFieldDesignValue_full(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestSuiteCustomFieldDesignValue(
                                                    'cf_full', '7760', '7762') 
        self.assertEqual('a custom TSuite string', response['value'])           
        self.assertEqual('1', response['enable_on_design']) 
        self.assertEqual('0', response['enable_on_testplan_design']) 
        self.assertEqual('0', response['enable_on_execution'])           

    def test_getTestPlanCustomFieldDesignValue_notAssigned(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestPlanCustomFieldDesignValue(
                                            'cf_notAssigned', '7760', '7761') 
        self.assertEqual(None, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getTestPlanCustomFieldDesignValue_full(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getTestPlanCustomFieldDesignValue(
                                                    'cf_full', '7760', '7761') 
        self.assertEqual('a custom TPlan string', response['value'])           
        self.assertEqual('1', response['enable_on_design']) 
        self.assertEqual('0', response['enable_on_testplan_design']) 
        self.assertEqual('0', response['enable_on_execution'])           

    def test_getReqSpecCustomFieldDesignValue_notAssigned(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getReqSpecCustomFieldDesignValue(
                                            'cf_notAssigned', '7760', '7789') 
        self.assertEqual(None, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getReqSpecCustomFieldDesignValue_full(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getReqSpecCustomFieldDesignValue(
                                                    'cf_full', '7760', '7789') 
        self.assertEqual('a custom ReqSpec string', response['value'])           
        self.assertEqual('1', response['enable_on_design']) 
        self.assertEqual('0', response['enable_on_testplan_design']) 
        self.assertEqual('0', response['enable_on_execution'])           

    def test_getRequirementCustomFieldDesignValue_notAssigned(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getRequirementCustomFieldDesignValue(
                                            'cf_notAssigned', '7760', '7791') 
        self.assertEqual(None, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getRequirementCustomFieldDesignValue_full(self):
        self.api.loadScenario(SCENARIO_CUSTOM_FIELDS)
        response = self.api.getRequirementCustomFieldDesignValue(
                                                    'cf_full', '7760', '7791') 
        self.assertEqual('a custom Req string', response['value'])           
        self.assertEqual('1', response['enable_on_design']) 
        self.assertEqual('0', response['enable_on_testplan_design']) 
        self.assertEqual('0', response['enable_on_execution'])   
        
    def test_reportTCResult_user(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.reportTCResult(4712, 'p', testcaseid=4711, 
                                    buildname='build 4713', notes='note 4714',
                                    user='a login name') 
        self.assertEqual('reportTCResult', response[0]['operation']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        self.assertEqual('a login name', self.api.callArgs['user'])
        
    def test__getAttachmentArgs_textfile(self):
        "py3 issue #39 TypeError: expected bytes-like object, not str"
        # under py2, on windows text files should be open with 'r' mode and 
        # binary files with 'rb' 
        # see http://docs.python.org/2/tutorial/inputoutput.html#reading-and-writing-files
        # under py3, text files open with 'r' on windows makes problem
        # see https://github.com/lczub/TestLink-API-Python-client/issues/39
        a_file=open(ATTACHMENT_EXAMPLE_TEXT)
        args = self.api._getAttachmentArgs(a_file)
        # repeating this test failed in second run, cause filename is then 
        # 'testlinkapigeneric_offline_test.pyc'
        self.assertEqual('testlinkapigeneric_offline_test.py', args['filename'])
        # filetype is also OS depended, either 'text/plain' or  'text/x-python' 
        self.assertIn('text/', args['filetype'])
        self.assertIsNotNone(args['content'])
       
    def test__getAttachmentArgs_filepath(self):
        "enhancement #40 handle file patch instead file object"
        args = self.api._getAttachmentArgs(ATTACHMENT_EXAMPLE_TEXT)
        self.assertEqual('testlinkapigeneric_offline_test.py', args['filename'])
        # filetype is also OS depended, either 'text/plain' or  'text/x-python' 
        self.assertIn('text/', args['filetype'])
        self.assertIsNotNone(args['content'])

    def test___str__pyversion(self):
        self.api.loadScenario(SCENARIO_TL199)
        api_info = self.api.__str__()
        py_info = '(PY %i.' % sys.version_info[0]
        self.assertIn(py_info, api_info) 
        
    def test_getProjectKeywords_noKeywords(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectKeywords('noKeyword')
        self.assertEqual({}, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getProjectKeywords_twoKeywords(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectKeywords('twoKeywords')
        self.assertEqual('KeyWord01', response['25'])
        self.assertEqual('KeyWord02', response['26'])
               
    def test_getTestCaseKeywords_noKeywords(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCaseKeywords(testcaseid='noKeyword')
        self.assertEqual({}, response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getProjectKeywords_twoKeywords(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCaseKeywords(testcaseid='twoKeywords')
        self.assertEqual('KeyWord01', response['25'])
        self.assertEqual('KeyWord02', response['26'])
               
    def test_getProjects_noProject(self):
        self.api.loadScenario(SCENARIO_NO_PROJECT)
        response = self.api.getProjects()
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_connect_with_proxy(self):
        """ create a TestLink Generic API dummy with ProxiedTransport"""
        self.api = DummyAPIGeneric('http://SERVER-URL-71', 'DEVKEY-71', 
                                   transport='PROXY-71')
        self.assertEqual('PROXY-71', self.api.server.__call__('transport'))
                    
    def test_getRequirements_allRequirements(self):
        self.api.loadScenario(SCENARIO_REQUIREMENTS)
        response = self.api.getRequirements('allReqs')
        self.assertEqual('feature-01', response[5]['req_doc_id'])
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getRequirements_noRequirements(self):
        self.api.loadScenario(SCENARIO_REQUIREMENTS)
        response = self.api.getRequirements('noReqs')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def Coveredtest_getReqCoverage_Covered(self):
        self.api.loadScenario(SCENARIO_REQUIREMENTS)
        response = self.api.getReqCoverage('reqCovered', 'a_req_doc_id')
        self.assertEqual('TESTCASE_B', response[0]['name'])
        self.assertEqual('15326', response[0]['id'])
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        
    def test_getReqCoverage_notCovered(self):
        self.api.loadScenario(SCENARIO_REQUIREMENTS)
        response = self.api.getReqCoverage('reqNotCovered', 'a_req_doc_id')
        self.assertEqual([], response)
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_connect_with_use_datetime(self):
        """ create a TestLink Generic API dummy with use_datetime"""
        self.api = DummyAPIGeneric('http://SERVER-URL-71', 'DEVKEY-71', 
                                   use_datetime='datetime?')
        a_transport = self.api.server.__call__('transport')
        self.assertEqual('datetime?', a_transport._use_datetime)

    def test_connect_with_context(self):
        """ create a TestLink Generic API dummy with use_datetime"""
        self.api = DummyAPIGeneric('https://SERVER-URL-71', 'DEVKEY-71', 
                                   context='ssl_context')
        a_transport = self.api.server.__call__('transport')
        self.assertEqual('ssl_context', a_transport.context)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()