#! /usr/bin/python
# -*- coding: UTF-8 -*-

#  Copyright 2014-2018 Luiko Czub
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

from robot.libraries.BuiltIn import BuiltIn

class TestlinkSeLibExtension(object):
    """ Extension of Robot Framework Selenium2library to access a TestLink web 
    application to collect and verify test data for Testlink XMLRPC api tests.
    """
    
    ROBOT_LIBRARY_SCOPE = 'TEST_SUITE'

    def __init__(self, url='http://demo.testlink.org/latest', 
                 username='admin', password='admin' ):
        self._get_selenium_lib_instance()
        self._store_server_url(url)
        self._store_user(username, password)
        
    def _store_server_url(self, url):
        self._server_url = url
        
    def _store_user(self, username, password):
        self._username = username
        self._password = password
        
    def _get_selenium_lib_instance(self):
        """ Gets current running Selenium2Library instance and store it 
        Uses BuiltIn().get_library_instance(), which normally should work also 
        during __init__ 
        - see https://code.google.com/p/robotframework/issues/detail?id=646
        But RIDE makes problems - the RIDE logs shows a traceback 
        - AttributeError: 'NoneType' object has no attribute 'namespace'
        after selecting a testsuite only for reading. 
        To avoid this traceback, we will catch it and do nothing.        
        """
        try:
            self._seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
        except AttributeError:
            # we do nothing see method comment
            pass

    def login_TestLink(self):
        """ Logs into the TestLink web app """
        SelLib = self._seleniumlib
        SelLib.location_should_contain('login.php')
        SelLib.input_text('tl_login', self._username)
        SelLib.input_text('tl_password', self._password)
        SelLib.click_button('login_submit')
        
    def logout_TestLink(self):
        """ Logs out of the TestLink web app"""
        SelLib = self._seleniumlib
        self.click_titlebar_element('Logout', 'login_div')
        
    def click_frame_element(self, frame_name, frame_elem, frame_unselect=True):
        """ Select frame FRAME_NAME and clicks on element FRAME_ELEM.
        Unselect this frame at the end, if FRAME_UNSELECT is True (default).
        internal keyword for testing the TestLink web app which uses framesets
        """
        SelLib = self._seleniumlib
        SelLib.select_frame(frame_name)
        SelLib.click_element(frame_elem)
        if frame_unselect is True:
            SelLib.unselect_frame()
        
    def click_titlebar_element(self, tbar_elem, expected_elem):
        """ Clicks in TestLinks *titlebar* frame on image with title TBAR_ELEM.
        Waits till _mainframe_ includes the element EXPECTED_ELEM. """
        SelLib = self._seleniumlib
        SelLib.log_location()
        img_xpath = "xpath=//img[@title='%s']" % tbar_elem
        self.click_frame_element('titlebar', img_xpath)
        SelLib.wait_until_page_contains_element(expected_elem)
        
    def click_desktop_link(self, desktop_link, expected_elem):
        """ Opens TestLinks *Desktop* page and clicks on link DESKTOP_LINK.
        Waits till _mainframe_ includes the element EXPECTED_ELEM. """
        SelLib = self._seleniumlib
        self.click_titlebar_element('Desktop', 'mainframe')
        a_link='link=%s' % desktop_link
        self.click_frame_element('name=mainframe', a_link)
        self.wait_until_frame_contains_element('mainframe', expected_elem)

    def wait_until_frame_contains_element(self, frame_name,frame_elem):
        """ Waits till frame FRAME_NAME exists, select this frame and waits 
        again till the element FRAME_ELEM exists in it.
        internal keyword for testing the TestLink web app which uses framesets
        """
        SelLib = self._seleniumlib
        a_frame = 'name=%s' % frame_name
        SelLib.wait_until_page_contains_element(a_frame)
        SelLib.select_frame(frame_name)
        SelLib.wait_until_page_contains_element(frame_elem)
        
    def get_all_visible_projects_identifier(self):
        """ Return lists with four different identifier for test projects, 
        visible in TestLinks *titlebar* selecting list *testproject*
        
        1. List with test projects internal ID
        2. list with test projects prefix
        3. list with test projects name
        4. list with selection list option text 
        
        All four lists have the same length and order equates to selecting list 
        *testproject* """
        
        js_script = """
            //var myform = document.getElementsByName("titlebar")[0].contentWindow.document.getElementsByName("testproject")[0]
            var myform = document.getElementsByName("testproject")[0]
            var myOptions = [].slice.call( myform.options );
            var tp_ids = myOptions.map(function(a_opt) {return a_opt.value})
            var tp_prefixs = myOptions.map(function(a_opt) {
                        var a_title = a_opt.title; 
                        var a_split = a_title.indexOf(":"); 
                        return a_title.substring(0,a_split)})
            var tp_names = myOptions.map(function(a_opt) {
                        var a_title = a_opt.title; 
                        var a_split = a_title.indexOf(":"); 
                        return a_title.substring(a_split+1)})
            var opt_texts = myOptions.map(function(a_opt) {return a_opt.text})                
            return [tp_ids, tp_prefixs, tp_names, opt_texts]
                """
        SelLib = self._seleniumlib
        SelLib.select_frame('titlebar')
        return SelLib.execute_javascript(js_script)
        
   