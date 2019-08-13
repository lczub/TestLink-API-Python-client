#  Copyright 2014-2019 Luiko Czub
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

*** Settings ***
Documentation     Resource file for testing TestLink XMLRPC api with web app interaction
Library           Selenium2Library
Library           TestlinkSeLibExtension    ${TL_URL}    ${TL_USER}    ${TL_PASSWORD}

*** Variables ***
${SERVER}         lkatlinkd7/testlink
${BROWSER}        ff
${DELAY}          0.1
${TL_USER}        admin
${TL_PASSWORD}    admin
${TL_URL}         http://${SERVER}/

*** Keywords ***
Open Browser with TestLink Page
    [Documentation]    prepares the browser for testing the TestLink web app
    Open Browser    ${TL_URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
