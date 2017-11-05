#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2011-2012 Olivier Renault, James Stock, TestLink-API-Python-client developers
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

# This example shows, how the API could be used to list all test cases,
# which have been created during the last 7 days


from __future__ import print_function
from testlink import TestlinkAPIClient, TestLinkHelper
import time


def iterTCasesfromTProject(api, TProjName, date1, date2):
    """ returns as iterator all test cases of project TPROJTNAME, which are 
    created between DATE1 and DATE2 
    DATE1 and DATE2 must be of type time.struct_time """
    TProjId = api.getTestProjectByName(TProjName)['id']
    for TSinfo in api.getFirstLevelTestSuitesForTestProject(TProjId):
        TSuiteId = TSinfo['id']
        for TCid in api.getTestCasesForTestSuite(TSuiteId, deep=1,details='only_id'):
            TCdata = api.getTestCase(TCid)[0] #really only one TC?
            dateTC=time.strptime(TCdata['creation_ts'][:10], '%Y-%m-%d')
            if (date1 <= dateTC) and (dateTC <= date2):
                yield TCdata


if __name__ == '__main__':
    tlapi = TestLinkHelper().connect(TestlinkAPIClient)
    projName = 'NEW_PROJECT_API'
    currentTime = time.localtime() 
    oldTime     = time.localtime(time.time() - 3600 * 24 * 7)
    
    print('%s test cases created between %s and %s' % \
            (projName, time.strftime('%Y-%m-%d', oldTime),  
             time.strftime('%Y-%m-%d', currentTime)))
    for TCdata in iterTCasesfromTProject(tlapi, projName, oldTime, currentTime):
        print('  %(name)s %(version)s %(creation_ts)s' % TCdata)
