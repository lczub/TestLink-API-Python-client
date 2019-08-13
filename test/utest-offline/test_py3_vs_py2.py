#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2018-2019 Luiko Czub, TestLink-API-Python-client developers
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

# TestCases for Testlink API clients handling py2 and py3 differences
# - TestlinkAPIClient, TestlinkAPIGeneric
# 

import pytest
#from conftest import api_general_client, api_generic_client

def test_IS_PY3_same_state():
    from testlink.proxiedtransport import IS_PY3 as proxie_is_py3
    from testlink.testlinkapigeneric import IS_PY3 as tl_is_py3
    assert proxie_is_py3 == tl_is_py3
    
