#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2012-2019 Luiko Czub, TestLink-API-Python-client developers
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

import sys
import unittest

if sys.version_info[0] == 2 and sys.version_info[1] == 7:
    # py27 and py31 assertRaisesRegexp was renamed in py32 to assertRaisesRegex
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

from testlink import TestlinkAPIClient, TestLinkHelper
from testlink.testlinkerrors import TLArgError

# scenario_a includes response from a testlink 1.9.3 server
SCENARIO_A = {'getProjects' : [
               {'opt': {'requirementsEnabled': 0, 'testPriorityEnabled': 1, 
                        'automationEnabled': 1, 'inventoryEnabled': 0}, 
                'prefix': 'NPROAPI', 'name': 'NEW_PROJECT_API', 'color': '', 
                'notes': 'This is a Project created with the API', 
                'option_priority': '0', 
                'options': 'O:8:"stdClass":4:{s:19:"requirementsEnabled";i:0;s:19:"testPriorityEnabled";i:1;s:17:"automationEnabled";i:1;s:16:"inventoryEnabled";i:0;}', 
                'tc_counter': '2', 'option_reqs': '0', 'active': '1', 
                'is_public': '1', 'id': '21', 'option_automation': '0'}, 
               {'opt': {'requirementsEnabled': 1, 'testPriorityEnabled': 1, 
                        'automationEnabled': 1, 'inventoryEnabled': 1}, 
                'prefix': 'TP', 'name': 'TestProject', 'color': '', 
                'notes': '<p>Initiales TestProject, um &nbsp;TestLink kennen zu lernen</p>', 
                'option_priority': '0', 
                'options': 'O:8:"stdClass":4:{s:19:"requirementsEnabled";i:1;s:19:"testPriorityEnabled";i:1;s:17:"automationEnabled";i:1;s:16:"inventoryEnabled";i:1;}', 
                'tc_counter': '0', 'option_reqs': '0', 'active': '1', 
                'is_public': '1', 'id': '1', 'option_automation': '0'}],
              'getProjectTestPlans' : {
                '21' : [{'name': 'TestPlan_API', 
                         'notes': 'New TestPlan created with the API', 
                         'active': '1', 'is_public': '1', 
                         'testproject_id': '21', 'id': '22'},
                        {'name': 'TestPlan_NoSuite', 
                         'notes': 'TestPlan with No Suites and No Platforms', 
                         'active': '1', 'is_public': '1', 
                         'testproject_id': '21', 'id': '222'}] ,
                '1' : '' },
              'getFirstLevelTestSuitesForTestProject' : {
                '21' :  [{'node_type_id': '2', 'name': 'A - First Level', 
                          'parent_id': '21', 'node_order': '0', 
                          'node_table': 'testsuites', 'id': '23'}, 
                         {'node_type_id': '2', 'name': 'B - First Level', 
                          'parent_id': '21', 'node_order': '0', 
                          'node_table': 'testsuites', 'id': '24'}],
                '1' : [{'message': '(getFirstLevelTestSuitesForTestProject) - Test Project (TestProject) is empty.', 
                        'code': 7008}] },
              'getTestSuitesForTestPlan' : {'22' : '', '222' : ''},
              'getTestCasesForTestPlan' : {'22' : '', '222' : ''},
              # TL(1.9.3)->getTestSuitesForTestSuite really returns {...} and not [{....}] !!!
              'getTestSuitesForTestSuite' : {
                '23' : {'node_type_id': '2', 'name': 'AA - Second Level', 
                        'parent_id': '23', 'node_order': '0', 
                        'details': 'Details of the Test Suite AA', 'id': '25'},
                '24' : ''},
              'getTestCasesForTestSuite' : {
                '23' : [{'node_type_id': '3', 'tcversion_id': '25', 
                         'name': 'TESTCASE_AA', 'parent_id': '25', 
                         'node_order': '0', 'node_table': 'testcases', 
                         'external_id': 'NPROAPI-1', 'id': '26'}],
                '24' : [{'node_type_id': '3', 'tcversion_id': '24', 
                         'name': 'TESTCASE_B', 'parent_id': '24', 
                         'node_order': '0', 'node_table': 'testcases', 
                         'external_id': 'NPROAPI-2', 'id': '33'}],
                '25' : [{'node_type_id': '3', 'tcversion_id': '25', 
                         'name': 'TESTCASE_AA', 'parent_id': '25', 
                         'node_order': '0', 'node_table': 'testcases', 
                         'external_id': 'NPROAPI-1',  'id': '26'}]
                 },
              'getTestPlanPlatforms' : {
                '22' : [{'notes': '', 'id': '1', 'name': 'dutch'}, {'notes': '', 'id': '2', 'name': 'platt'}],
                '222' : [{'message': 'Test plan (name:TestPlan_API) has no platforms linked', 
                         'code': 3041}]},
              'getBuildsForTestPlan' : {'22' : '', '222' : ''},
              'getTestCaseIDByName' : {
                'dictResult' :  {'1': {'parent_id': '24', 'tc_external_id': '2', 
                                       'id': '33', 'tsuite_name': 'B - First Level', 
                                       'name': 'TESTCASE_B'}}, 
                'listResult' : [{'parent_id': '25', 'tc_external_id': '1', 
                                 'id': '26', 'tsuite_name': 'AA - Second Level', 
                                 'name': 'TESTCASE_AA'}]},
              'getTestCase' : {
                '26-1' : [{'full_tc_external_id': 'NPROAPI-1', 'node_order': '0', 'is_open': '1', 'id': '27', 
                         'author_last_name': 'LkaTlinkD7', 'updater_login': '', 'layout': '1', 'tc_external_id': '1', 
                         'version': '1', 'estimated_exec_duration': '', 'testsuite_id': '25', 'updater_id': '', 
                         'status': '1', 'updater_first_name': '', 'testcase_id': '26', 'author_first_name': 'Tester', 
                         'importance': '2', 'modification_ts': '', 'execution_type': '1', 'preconditions': 'V1', 
                         'active': '1', 'creation_ts': '2013-12-26 21:17:43', 'name': 'TC-C', 'summary': 'SumSumSum', 
                         'updater_last_name': '', 
                         'steps': [{'step_number': '1', 'actions': 'Step action 1', 'execution_type': '2', 'active': '1', 
                                    'id': '5101', 'expected_results': 'Step result 1'}], 
                         'author_id': '3', 'author_login': 'tester'}],
                '26-2' : [{'full_tc_external_id': 'NPROAPI-1', 'node_order': '0', 'is_open': '1', 'id': '127', 
                         'author_last_name': 'LkaTlinkD7', 'updater_login': '', 'layout': '1', 'tc_external_id': '1', 
                         'version': '2', 'estimated_exec_duration': '', 'testsuite_id': '25', 'updater_id': '', 
                         'status': '1', 'updater_first_name': '', 'testcase_id': '26', 'author_first_name': 'Tester', 
                         'importance': '2', 'modification_ts': '', 'execution_type': '1', 'preconditions': 'V2', 
                         'active': '1', 'creation_ts': '2013-12-26 22:17:43', 'name': 'TC-C', 'summary': 'SumSumSum', 
                         'updater_last_name': '', 
                         'steps': [{'step_number': '1', 'actions': 'Step action 1', 'execution_type': '2', 'active': '1', 
                                    'id': '5101', 'expected_results': 'Step result 1'}], 
                         'author_id': '3', 'author_login': 'tester'}],
                '26-None' : [{'full_tc_external_id': 'NPROAPI-1', 'node_order': '0', 'is_open': '1', 'id': '127', 
                         'author_last_name': 'LkaTlinkD7', 'updater_login': '', 'layout': '1', 'tc_external_id': '1', 
                         'version': '2', 'estimated_exec_duration': '', 'testsuite_id': '25', 'updater_id': '', 
                         'status': '1', 'updater_first_name': '', 'testcase_id': '26', 'author_first_name': 'Tester', 
                         'importance': '2', 'modification_ts': '', 'execution_type': '1', 'preconditions': 'V2 None', 
                         'active': '1', 'creation_ts': '2013-12-26 22:17:43', 'name': 'TC-C', 'summary': 'SumSumSum', 
                         'updater_last_name': '', 
                         'steps': [{'step_number': '1', 'actions': 'Step action 1', 'execution_type': '2', 'active': '1', 
                                    'id': '5101', 'expected_results': 'Step result 1'}], 
                         'author_id': '3', 'author_login': 'tester'}]
                               
                               },
              'getFullPath' : {
                               
                26 : {'26' : ['NEW_PROJECT_API', 'A - First Level', 'AA - Second Level']},
                4711 : {'4711' : ['OLD_PROJECT_API']},
                    },
              'getTestProjectByName' : {
                'NEW_PROJECT_API' : {
                    'prefix': 'NPROAPI', 'name': 'NEW_PROJECT_API', 'color': '',
                    'notes': 'This is a Project created with the API', 
                    'is_public': '1', 'id': '21', 'option_automation': '0'},
                'OLD_PROJECT_API' : {
                     'prefix': 'OPROAPI', 'name': 'OLD_PROJECT_API', 'color': '',
                    'notes': 'This is a Project created with the API', 
                    'is_public': '1', 'id': '2211', 'option_automation': '0'},
                    },
              'createTestCase' : 'dummy response createTestCase',
              'reportTCResult' :  [{'status': True, 'operation': 'reportTCResult', 
                                    'message': 'Success!', 'overwrite': False, 'id': '773'}]              

              }

SCENARIO_STEPS = {'createTestCase' : ['noRealReponseData - ok for step tests']}

# scenario_keywords defines response with keywords
SCENARIO_KEYWORDS = {'getTestCasesForTestSuite' : {
                    'noTestCase' : [] ,
                    
                     'deepTrue1' : [{'node_order': '0', 'is_open': '1', 
                        'keywords': {'3': {'keyword_id': '3', 'notes': 'a third key word', 'testcase_id': '8136', 'keyword': 'KeyWord03'}}, 
                        'id': '8136', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '1', 'parent_id': '8135', 'version': '1', 
                        'estimated_exec_duration': '', 'updater_id': '2', 'status': '1', 'tsuite_name': 'AA - Second Level', 
                        'importance': '2', 'modification_ts': '2014-07-01 21:21:59', 'execution_type': '2', 
                        'preconditions': '<p>\n\tthese are the preconditions</p>\n', 'active': '1', 'creation_ts': '2014-06-28 22:06:17', 
                        'node_table': 'testcases', 'tcversion_id': '8137', 'name': 'TESTCASE_AA', 
                        'summary': '<p>\n\tThis is the summary of the Test Case AA</p>\n', 
                        'steps': [{'step_number': '1', 'actions': 'Step action 1 - aa', 'execution_type': '1', 'active': '1', 'id': '8138', 'expected_results': 'Step result 1 - aa'}, 
                                  {'step_number': '2', 'actions': 'Step action 2 - aa', 'execution_type': '1', 'active': '1', 'id': '8139', 'expected_results': 'Step result 2 - aa'}, 
                                  {'step_number': '3', 'actions': 'Step action 3 - aa', 'execution_type': '1', 'active': '1', 'id': '8140', 'expected_results': 'Step result 3 - aa'}, 
                                  {'step_number': '4', 'actions': 'Step action 4 - aa', 'execution_type': '1', 'active': '1', 'id': '8141', 'expected_results': 'Step result 4 - aa'}, 
                                  {'step_number': '5', 'actions': 'Step action 5 - aa', 'execution_type': '1', 'active': '1', 'id': '8142', 'expected_results': 'Step result 5 - aa'}], 
                        'author_id': '1', 'external_id': 'GPROAPI10-1'}],
                    
                    'deepFalse3' :  [{'node_order': '0', 'is_open': '1', 
                        'keywords': {'1': {'keyword_id': '1', 'notes': 'a key word', 'testcase_id': '8144', 'keyword': 'KeyWord01'}, 
                                     '3': {'keyword_id': '3', 'notes': 'a third key word', 'testcase_id': '8144', 'keyword': 'KeyWord03'}}, 
                        'id': '8144', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '2', 'parent_id': '8134', 'version': '1', 
                        'details': '<p>\n\tDetails of the Test Suite B</p>\n', 'estimated_exec_duration': '3.00', 'updater_id': '2', 'status': '1', 
                        'importance': '3', 'modification_ts': '2014-06-30 20:45:40', 'execution_type': '1', 
                        'preconditions': '<p>\n\tthese are the preconditions</p>\n', 'active': '1', 'creation_ts': '2014-06-28 22:06:17', 
                        'node_table': 'testcases', 'tcversion_id': '8145', 'name': 'TESTCASE_B', 
                        'summary': '<p>\n\tThis is the summary of the Test Case B</p>\n', 
                        'steps': [{'step_number': '1', 'actions': 'Step action 1 -b ', 'execution_type': '2', 'active': '1', 'id': '8151', 'expected_results': 'Step result 1 - b'}, 
                                  {'step_number': '2', 'actions': 'Step action 2 -b ', 'execution_type': '2', 'active': '1', 'id': '8152', 'expected_results': 'Step result 2 - b'}, 
                                  {'step_number': '3', 'actions': 'action 3 createTestCaseSteps.update', 'execution_type': '2', 'active': '1', 'id': '8153', 'expected_results': 'update - cause step 3 already exist'}, 
                                  {'step_number': '4', 'actions': 'Step action 4 -b ', 'execution_type': '2', 'active': '1', 'id': '8154', 'expected_results': 'Step result 4 - b'}, 
                                  {'step_number': '5', 'actions': 'Step action 5 -b changed by updateTestCase', 'execution_type': '2', 'active': '1', 'id': '8155', 'expected_results': 'Step result 5 - b changed'}, 
                                  {'step_number': '6', 'actions': 'Step action 6 -b added by updateTestCase', 'execution_type': '2', 'active': '1', 'id': '8156', 'expected_results': 'Step result 6 - b added'}, 
                                  {'step_number': '7', 'actions': 'action 7 createTestCaseSteps.create', 'execution_type': '2', 'active': '1', 'id': '8157', 'expected_results': 'create - cause step 7 not yet exist'}, 
                                  {'step_number': '8', 'actions': 'action 8 createTestCaseSteps.update', 'execution_type': '2', 'active': '1', 'id': '8158', 'expected_results': 'create - cause step 8 not yet exist'}], 
                        'author_id': '1'}, 
                                     {'node_order': '1', 'is_open': '1', 
                        'keywords': {'2': {'keyword_id': '2', 'notes': 'another key word', 'testcase_id': '8159', 'keyword': 'KeyWord02'}}, 
                        'id': '8159', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '3', 'parent_id': '8134', 'version': '1', 
                        'details': '<p>\n\tDetails of the Test Suite B</p>\n', 'estimated_exec_duration': '3.00', 'updater_id': '2', 'status': '1', 
                        'importance': '3', 'modification_ts': '2014-07-02 21:03:02', 'execution_type': '1', 
                        'preconditions': '<p>\n\tthese are the preconditions</p>\n', 'active': '1', 'creation_ts': '2014-07-02 20:53:45', 
                        'node_table': 'testcases', 'tcversion_id': '8160', 'name': 'TESTCASE_B2', 
                        'summary': '<p>\n\tThis is the summary of the Test Case B2</p>\n', 
                        'steps': [{'step_number': '1', 'actions': '<p>\n\tStep action 1 -b2</p>\n', 'execution_type': '2', 'active': '1', 'id': '8161', 'expected_results': '<p>\n\tStep result 1 - b2</p>\n'}, 
                                  {'step_number': '2', 'actions': '<p>\n\tStep action 2 -b2</p>\n', 'execution_type': '2', 'active': '1', 'id': '8162', 'expected_results': '<p>\n\tStep result 2 - b2</p>\n'}], 
                        'author_id': '2'}, 
                                     {'node_order': '2', 'is_open': '1', 
                     'id': '8169', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '4', 'parent_id': '8134', 'version': '1', 
                     'details': '<p>\n\tDetails of the Test Suite B</p>\n', 'estimated_exec_duration': '3.00', 'updater_id': '2', 'status': '1', 
                     'importance': '3', 'modification_ts': '2014-07-02 21:02:23', 'execution_type': '1', 
                     'preconditions': '<p>\n\tthese are the preconditions</p>\n', 'active': '1', 'creation_ts': '2014-07-02 20:55:46', 
                     'node_table': 'testcases', 'tcversion_id': '8170', 'name': 'TESTCASE_B3', 
                     'summary': '<p>\n\tThis is the summary of the Test Case B3</p>\n', 
                     'steps': [{'step_number': '1', 'actions': '<p>\n\tStep action 1 -b3</p>\n', 'execution_type': '2', 'active': '1', 'id': '8171', 'expected_results': '<p>\n\tStep result 1 - b3</p>\n'}, 
                               {'step_number': '2', 'actions': '<p>\n\tStep action 2 -b3</p>\n', 'execution_type': '2', 'active': '1', 'id': '8172', 'expected_results': '<p>\n\tStep result 2 - b3</p>\n'}], 
                     'author_id': '2'}],
                                                   
                '4711' :  [{'node_order': '0', 'is_open': '1', 
                        'keywords': {'1': {'keyword_id': '1', 'notes': 'a key word', 'testcase_id': '8144', 'keyword': 'KeyWord01'}, 
                                     '3': {'keyword_id': '3', 'notes': 'a third key word', 'testcase_id': '8144', 'keyword': 'KeyWord03'}}, 
                        'id': '8144', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '2', 'parent_id': '8134', 'version': '1', 
                        'details': '<p>\n\tDetails of the Test Suite B</p>\n', 'estimated_exec_duration': '3.00', 'updater_id': '2', 'status': '1', 
                        'importance': '3', 'modification_ts': '2014-06-30 20:45:40', 'execution_type': '1', 
                        'preconditions': '<p>\n\tthese are the preconditions</p>\n', 'active': '1', 'creation_ts': '2014-06-28 22:06:17', 
                        'node_table': 'testcases', 'tcversion_id': '8145', 'name': 'TESTCASE_B', 
                        'summary': '<p>\n\tThis is the summary of the Test Case B</p>\n', 
                        'steps': [{'step_number': '1', 'actions': 'Step action 1 -b ', 'execution_type': '2', 'active': '1', 'id': '8151', 'expected_results': 'Step result 1 - b'}], 
                        'author_id': '1'} ],

                'noKeywords' :  [{'node_order': '0', 'is_open': '1', 
                        'id': '8144', 'node_type_id': '3', 'layout': '1', 'tc_external_id': '2', 'parent_id': '8134', 'version': '1', 
                        'details': '<p>\n\tDetails of the Test Suite B</p>\n', 'estimated_exec_duration': '3.00', 'updater_id': '2', 'status': '1', 
                        'importance': '3', 'modification_ts': '2014-06-30 20:45:40', 'execution_type': '1', 
                        'preconditions': '<p>\n\tthese are the preconditions</p>\n', 'active': '1', 'creation_ts': '2014-06-28 22:06:17', 
                        'node_table': 'testcases', 'tcversion_id': '8145', 'name': 'TESTCASE_B', 
                        'summary': '<p>\n\tThis is the summary of the Test Case B</p>\n', 
                        'steps': [{'step_number': '1', 'actions': 'Step action 1 -b ', 'execution_type': '2', 'active': '1', 'id': '8151', 'expected_results': 'Step result 1 - b'}], 
                        'author_id': '1'} ]

                                            },
                     'getTestCase' : {
                                    '8144' : [{'full_tc_external_id': 'NPROAPI-2', 'id': '8145', 'tc_external_id': '2', 'version': '1', 
                                                    'testsuite_id': 'deepFalse3', 'testcase_id': '8144', 'name': 'TESTCASE_B'}],
                                    'NPROAPI-2' : [{'full_tc_external_id': 'NPROAPI-2', 'id': '8145', 'tc_external_id': '2', 'version': '1', 
                                                    'testsuite_id': 'deepFalse3', 'testcase_id': '8144', 'name': 'TESTCASE_B'}],
                                    '8159' : [{'full_tc_external_id': 'NPROAPI-3', 'id': '8160', 'tc_external_id': '3', 'version': '1', 
                                                    'testsuite_id': 'deepFalse3', 'testcase_id': '8159', 'name': 'TESTCASE_B2'}],
                                    'NPROAPI-3' : [{'full_tc_external_id': 'NPROAPI-3', 'id': '8160', 'tc_external_id': '3', 'version': '1', 
                                                    'testsuite_id': 'deepFalse3', 'testcase_id': '8159', 'name': 'TESTCASE_B2'}],
                                    '8169' : [{'full_tc_external_id': 'NPROAPI-4', 'id': '8170', 'tc_external_id': '3', 'version': '1', 
                                                    'testsuite_id': 'deepFalse3', 'testcase_id': '8169', 'name': 'TESTCASE_B3'}],
                                    'NPROAPI-4' : [{'full_tc_external_id': 'NPROAPI-4', 'id': '8170', 'tc_external_id': '3', 'version': '1', 
                                                    'testsuite_id': 'deepFalse3', 'testcase_id': '8169', 'name': 'TESTCASE_B3'}] },
                     'getTestCaseKeywords' : {
                                               #{'12622': {'34': 'KeyWord01', '36': 'KeyWord03'}}
                                    '8144' : {'8144' : {'1': 'KeyWord01', '3': 'KeyWord03'} },
                                    'NPROAPI-2' : {'8144' : {'1': 'KeyWord01', '3': 'KeyWord03'} },
                                    '8159' : {'8159' : {'2': 'KeyWord02'}},
                                    'NPROAPI-3' : {'8159' : {'2': 'KeyWord02'}},
                                    '8169' : {'8169' : {}},
                                    'NPROAPI-4' : {'8169' : {}} 
                                              }
                     }

# scenario_no_project simulates a fresh empty test link application
SCENARIO_NO_PROJECT = {'getProjects' : [] }

class DummyAPIClient(TestlinkAPIClient):
    """ Dummy for Simulation TestLinkAPICLient. 
    Overrides _callServer() Method to return test scenarios
    """

    __slots__ = ['scenario_data', 'callArgs']

    def __init__(self, server_url, devKey, **args):
        super(DummyAPIClient, self).__init__(server_url, devKey, **args)
        self.scenario_data = {}
        self.callArgs = None

    def loadScenario(self, a_scenario):
        self.scenario_data = a_scenario
        self.callArgs = None

    def _callServer(self, methodAPI, argsAPI=None):
        self.callArgs = argsAPI
        data = self.scenario_data[methodAPI]
        response = None
        if methodAPI in ['getProjectTestPlans', 
                         'getFirstLevelTestSuitesForTestProject']:
            response = data[argsAPI['testprojectid']]
        elif methodAPI in ['getTestSuitesForTestPlan', 
                           'getTestCasesForTestPlan', 'getTestPlanPlatforms',
                           'getBuildsForTestPlan']:
            response = data[argsAPI['testplanid']]
        elif methodAPI in ['getTestCasesForTestSuite', 
                           'getTestSuitesForTestSuite']:
            response = data[argsAPI['testsuiteid']]
        elif methodAPI in ['getTestCaseIDByName']:
            response = data[argsAPI['testcasename']]
        elif methodAPI in ['getTestCase', 'getTestCaseKeywords']:
            datakey = argsAPI.get('testcaseid')
            if datakey:
                datakey = str(datakey)
            else:
                datakey = argsAPI.get('testcaseexternalid', '')
            if 'version' in argsAPI:
                datakey += '-%(version)s' % argsAPI
            response = data[datakey]
        elif methodAPI in ['getFullPath']:
            response = data[argsAPI['nodeid']]
        elif methodAPI in ['getTestProjectByName']:
            response = data[argsAPI['testprojectname']]
        else:
            response = data
        return response


class TestLinkAPIOfflineTestCase(unittest.TestCase):
    """ TestCases for TestlinkAPIClient - does not interacts with a TestLink Server.
    works with DummyAPIClientm which returns special test data
    """

    example_steps = [{'step_number' : '1', 'actions' : "action A" , 
                'expected_results' : "result A", 'execution_type' : "0"},
                 {'step_number' : '2', 'actions' : "action B" , 
                'expected_results' : "result B", 'execution_type' : "1"},
                 {'step_number' : '3', 'actions' : "action C" , 
                'expected_results' : "result C", 'execution_type' : "0"}]

    @classmethod
    def setUpClass(cls):
        cls.api = TestLinkHelper().connect(DummyAPIClient)
        
    def setUp(self):
        self.api._emptyStepsList()

#    def tearDown(self):
#        pass

    def test_countProjects(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countProjects()
        self.assertEqual(2, response)
        
    def test_countProjects_NoProject(self):
        self.api.loadScenario(SCENARIO_NO_PROJECT)
        response = self.api.countProjects()
        self.assertEqual(0, response)

    def test_countTestPlans(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countTestPlans()
        self.assertEqual(2, response)

    def test_countTestPlans_NoProject(self):
        self.api.loadScenario(SCENARIO_NO_PROJECT)
        response = self.api.countTestPlans()
        self.assertEqual(0, response)

    def test_countTestSuites(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countTestSuites()
        self.assertEqual(0, response)

    def test_countTestSuites_NoProject(self):
        self.api.loadScenario(SCENARIO_NO_PROJECT)
        response = self.api.countTestSuites()
        self.assertEqual(0, response)

    def test_countTestCasesTP(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countTestCasesTP()
        self.assertEqual(0, response)

    def test_countTestCasesTP_NoProject(self):
        self.api.loadScenario(SCENARIO_NO_PROJECT)
        response = self.api.countTestCasesTP()
        self.assertEqual(0, response)

    def test_countTestCasesTS(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countTestCasesTS()
        self.assertEqual(0, response)

    def test_countTestCasesTS_NoProject(self):
        self.api.loadScenario(SCENARIO_NO_PROJECT)
        response = self.api.countTestCasesTS()
        self.assertEqual(0, response)

    def test_countPlatforms(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countPlatforms()
        self.assertEqual(2, response)
        
    def test_countPlatforms_NoProject(self):
        self.api.loadScenario(SCENARIO_NO_PROJECT)
        response = self.api.countPlatforms()
        self.assertEqual(0, response)

    def test_countBuilds(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.countBuilds()
        self.assertEqual(0, response)
        
    def test_countBuilds_NoProject(self):
        self.api.loadScenario(SCENARIO_NO_PROJECT)
        response = self.api.countBuilds()
        self.assertEqual(0, response)


#    def test_listProjects(self):
#        self.api.loadScenario(SCENARIO_A)
#        self.api.listProjects()
#         no assert check cause method returns nothing
#         'just' prints to stdout

    def test_getProjectIDByName(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getProjectIDByName('NEW_PROJECT_API')
        self.assertEqual('21', response)
        response = self.api.getProjectIDByName('UNKNOWN_PROJECT')
        self.assertEqual(-1, response)
        
    def test_getProjectIDByName_NoProject(self):
        self.api.loadScenario(SCENARIO_NO_PROJECT)
        response = self.api.getProjectIDByName('UNKNOWN_PROJECT')
        self.assertEqual(-1, response)
        

    def test_initStep(self):
        self.api.initStep("action A", "result A", 0)
        steps = self.example_steps[:1]
        self.assertEqual(steps, self.api.stepsList)

    def test_appendStep(self):
        steps = self.example_steps
        self.api.stepsList = steps[:1] 
        self.api.appendStep("action B", "result B", 1)
        self.api.appendStep("action C", "result C", 0)
        self.assertEqual(steps, self.api.stepsList)

    def test_createTestCaseWithSteps(self):
        self.api.loadScenario(SCENARIO_STEPS)
        self.api.initStep("action A", "result A", 0)
        self.api.appendStep("action B", "result B", 1)
        self.api.appendStep("action C", "result C", 0)
        self.api.createTestCase('case 4711', 4712, 4713, 'Big Bird', 
                                'summary 4714')
        self.assertEqual(self.example_steps, self.api.callArgs['steps'])
        self.assertEqual([], self.api.stepsList)

    def test_createTestCaseWithConfusingSteps(self):
        self.api.loadScenario(SCENARIO_STEPS)
        self.api.initStep("action A", "result A", 0)
        self.api.appendStep("action B", "result B", 1)
        self.api.appendStep("action C", "result C", 0)
        with self.assertRaisesRegex(TLArgError, 'confusing createTestCase*'):
            self.api.createTestCase('case 4711', 4712, 4713, 'Big Bird', 
                                    'summary 4714', steps=[])

    def test_getTestCaseIDByName_dictResult(self):
        "test that getTestCaseIDByName converts dictionary result into a list"
        self.api.loadScenario(SCENARIO_A)
        # v0.4.0 version for optional args testsuitename + testprojectname
        #response = self.api.getTestCaseIDByName('dictResult', None, 'NEW_PROJECT_API')
        # v0.4.5 version
        response = self.api.getTestCaseIDByName('dictResult', 
                                            testprojectname='NEW_PROJECT_API')
        self.assertEqual(list, type(response))
        self.assertEqual('TESTCASE_B', response[0]['name']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getTestCaseIDByName_listResult(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.getTestCaseIDByName('listResult')
        self.assertEqual(list, type(response))
        self.assertEqual('TESTCASE_AA', response[0]['name']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_getProjectIDByNode(self):
        self.api.loadScenario(SCENARIO_A)
        self.assertEqual('2211', self.api.getProjectIDByNode('4711'))

    def test__copyTC_generate_new(self):
        self.api.loadScenario(SCENARIO_A)
        self.api._copyTC('26', {}, duplicateaction = 'generate_new')
        self.assertEqual('generate_new',  
                         self.api.callArgs['actiononduplicatedname'])

    def test__copyTC_create_new_version(self):
        self.api.loadScenario(SCENARIO_A)
        self.api._copyTC('26', {}, duplicateaction = 'create_new_version')
        self.assertEqual('create_new_version',  
                         self.api.callArgs['actiononduplicatedname'])
        self.assertEqual('V2 None', self.api.callArgs['preconditions'])

    def test__copyTC_changedArgs(self):
        self.api.loadScenario(SCENARIO_A)
        self.api._copyTC('26', {'testsuiteid' :'4711'}, 
                         duplicateaction = 'generate_new')
        self.assertEqual('4711', self.api.callArgs['testsuiteid'])
        self.assertEqual('2211', self.api.callArgs['testprojectid'])

    def test__copyTC_changedArgs_version(self):
        self.api.loadScenario(SCENARIO_A)
        self.api._copyTC('26', {'testsuiteid' :'4711'}, 1,
                         duplicateaction = 'generate_new')
        self.assertEqual('4711', self.api.callArgs['testsuiteid'])
        self.assertEqual('2211', self.api.callArgs['testprojectid'])
        self.assertEqual('V1', self.api.callArgs['preconditions'])

    def test_copyTCnewVersion(self):
        self.api.loadScenario(SCENARIO_A)
        self.api.copyTCnewVersion('26', summary = 'The summary has changed', 
                                    importance = '33')
        self.assertEqual('create_new_version',  
                         self.api.callArgs['actiononduplicatedname'])
        self.assertEqual('V2 None', self.api.callArgs['preconditions'])
        self.assertEqual('The summary has changed', self.api.callArgs['summary'])
        self.assertEqual('33', self.api.callArgs['importance'])
        self.assertEqual('TC-C', self.api.callArgs['testcasename'])
        self.assertEqual('25', self.api.callArgs['testsuiteid'])
        self.assertEqual('21', self.api.callArgs['testprojectid'])

    def test_copyTCnewVersion_version(self):
        self.api.loadScenario(SCENARIO_A)
        self.api.copyTCnewVersion('26', 1, summary = 'The summary has changed', 
                                    importance = '33')
        self.assertEqual('create_new_version',  
                         self.api.callArgs['actiononduplicatedname'])
        self.assertEqual('V1', self.api.callArgs['preconditions'])
        self.assertEqual('The summary has changed', self.api.callArgs['summary'])
        self.assertEqual('33', self.api.callArgs['importance'])
        self.assertEqual('TC-C', self.api.callArgs['testcasename'])
        self.assertEqual('25', self.api.callArgs['testsuiteid'])
        self.assertEqual('21', self.api.callArgs['testprojectid'])

    def test_copyTCnewTestCase(self):
        self.api.loadScenario(SCENARIO_A)
        self.api.copyTCnewTestCase('26', testsuiteid = '4711')
        self.assertEqual('generate_new',  
                         self.api.callArgs['actiononduplicatedname'])
        self.assertEqual('V2 None', self.api.callArgs['preconditions'])
        self.assertEqual('4711', self.api.callArgs['testsuiteid'])
        self.assertEqual('2211', self.api.callArgs['testprojectid'])

    def test_copyTCnewTestCase_version(self):
        self.api.loadScenario(SCENARIO_A)
        self.api.copyTCnewTestCase('26', 1, testsuiteid = '4711')
        self.assertEqual('generate_new',  
                         self.api.callArgs['actiononduplicatedname'])
        self.assertEqual('V1', self.api.callArgs['preconditions'])
        self.assertEqual('4711', self.api.callArgs['testsuiteid'])
        self.assertEqual('2211', self.api.callArgs['testprojectid'])

    def test_reportTCResult_user(self):
        self.api.loadScenario(SCENARIO_A)
        response = self.api.reportTCResult(4711, 4712, 'build 4713', 'p', 
                                           'note 4714', user='a login name') 
        self.assertEqual('reportTCResult', response[0]['operation']) 
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])
        self.assertEqual('a login name', self.api.callArgs['user'])
        
    def test_getTestCasesForTestSuite_keyWords(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.getTestCasesForTestSuite('deepFalse3', False, 
                                                     'full', getkeywords=True)
        self.assertIn('keywords', response[0])
        self.assertNotIn('keywords', response[2])
        self.assertEqual(self.api.devKey, self.api.callArgs['devKey'])

    def test_listKeywordsForTC_FullExternalId(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTC('NPROAPI-2')
        self.assertEqual(set(['KeyWord01', 'KeyWord03']), set(response))

    def test_listKeywordsForTC_InternalId_Int(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTC(8144)
        self.assertEqual(set(['KeyWord01', 'KeyWord03']), set(response))

    def test_listKeywordsForTC_InternalId_String(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTC('8144')
        self.assertEqual(set(['KeyWord01', 'KeyWord03']), set(response))

    def test_listKeywordsForTC_One(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTC('NPROAPI-3')
        self.assertEqual(['KeyWord02'], response)

    def test_listKeywordsForTC_None(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTC('NPROAPI-4')
        self.assertEqual([], response)

    def test_listKeywordsForTS_NoneTC(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTS('noTestCase')
        self.assertEqual({}, response)

    def test_listKeywordsForTS_NoneKW(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTS('noKeywords')
        self.assertEqual({'8144': []}, response)
        
    def test_listKeywordsForTS_Id_Int(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTS(4711)
        set_response = response
        for item in set_response:
            set_response[item] = set(response[item])
        self.assertEqual({'8144': set(['KeyWord01', 'KeyWord03'])}, set_response)

    def test_listKeywordsForTS_Id_String(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTS('4711')
        set_response = response
        for item in set_response:
            set_response[item] = set(response[item])
        self.assertEqual({'8144': set(['KeyWord01', 'KeyWord03'])}, set_response)

    def test_listKeywordsForTS_Multi(self):
        self.api.loadScenario(SCENARIO_KEYWORDS)
        response = self.api.listKeywordsForTS('deepFalse3')
        set_response = response
        for item in set_response:
            set_response[item] = set(response[item])
        self.assertEqual({'8144': set(['KeyWord01', 'KeyWord03']),
                          '8159': set(['KeyWord02']), '8169': set()}, set_response)

    def test_connect_with_proxy(self):
        """ create a TestLink API dummy with ProxiedTransport"""
        self.api = DummyAPIClient('http://SERVER-URL-71', 'DEVKEY-71', 
                                   transport='PROXY-71')
        self.assertEqual('PROXY-71', self.api.server.__call__('transport'))        

    def test_connect_with_use_datetime(self):
        """ create a TestLink Generic API dummy with use_datetime"""
        self.api = DummyAPIClient('http://SERVER-URL-71', 'DEVKEY-71', 
                                   use_datetime='datetime?')
        a_transport = self.api.server.__call__('transport')
        self.assertEqual('datetime?', a_transport._use_datetime)

    def test_connect_with_context(self):
        """ create a TestLink Generic API dummy with use_datetime"""
        self.api = DummyAPIClient('https://SERVER-URL-71', 'DEVKEY-71', 
                                   context='ssl_context')
        a_transport = self.api.server.__call__('transport')
        self.assertEqual('ssl_context', a_transport.context)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()