from testlink.testlinkerrors import TLResponseError


class TestReporter(dict):
    def __init__(self, tls, testcases, *args, **kwargs):
        """This can be given one or more testcases, but they all must have the same project, plan, and platform."""
        super(TestReporter, self).__init__(*args, **kwargs)
        self.tls = tls
        # handle single testcase
        self.testcases = testcases if isinstance(testcases, list) else [testcases]
        self._plan_testcases = None
        self.remove_non_report_kwargs()
        self._platformname_generated = False

    def remove_non_report_kwargs(self):
        self.buildname = self.pop('buildname')
        self.buildnotes = self.pop('buildnotes', "Created with automation.")

    def setup_testlink(self):
        """Call properties that may set report kwarg values."""
        self.testprojectname
        self.testprojectid
        self.testplanid
        self.testplanname
        self.platformname
        self.platformid
        self.buildid

    def _get_project_name_by_id(self):
        if self.testprojectid:
            for project in self.tls.getProjects():
                if project['id'] == self.testprojectid:
                    return project['name']

    def _projectname_getter(self):
        if not self.get('testprojectname') and self.testprojectid:
            self['testprojectname'] = self._get_project_name_by_id()
        return self.get('testprojectname')

    @property
    def testprojectname(self):
        return self._projectname_getter()

    def _get_project_id(self):
        tpid = self.get('testprojectid')
        if not tpid and self.testprojectname:
            self['testprojectid'] = self.tls.getProjectIDByName(self['testprojectname'])
            return self['testprojectid']
        return tpid

    def _get_project_id_or_none(self):
        project_id = self._get_project_id()
        # If not found the id will return as -1
        if project_id == -1:
            project_id = None
        return project_id

    @property
    def testprojectid(self):
        self['testprojectid'] = self._get_project_id_or_none()
        return self.get('testprojectid')

    @property
    def testplanid(self):
        return self.get('testplanid')

    @property
    def testplanname(self):
        return self.get('testplanname')

    @property
    def platformname(self):
        """Return a platformname added to the testplan if there is one."""
        return self.get('platformname')

    @property
    def platformid(self):
        return self.get('platformid')

    @property
    def buildid(self):
        return self.get('buildid')

    @property
    def plan_tcids(self):
        if not self._plan_testcases:
            self._plan_testcases = set()
            tc_dict = self.tls.getTestCasesForTestPlan(self.testplanid)
            try:
                for _, platform in tc_dict.items():
                    for k, v in platform.items():
                        self._plan_testcases.add(v['full_external_id'])
            except AttributeError:
                # getTestCasesForTestPlan returns an empty list instead of an empty dict
                pass
        return self._plan_testcases

    def reportgen(self):
        """For use if you need to look at the status returns of individual reporting."""
        self.setup_testlink()
        for testcase in self.testcases:
            yield self.tls.reportTCResult(testcaseexternalid=testcase, **self)

    def report(self):
        for _ in self.reportgen():
            pass


class AddTestReporter(TestReporter):
    """Add testcase to testplan if not added."""
    def setup_testlink(self):
        super(AddTestReporter, self).setup_testlink()
        self.ensure_testcases_in_plan()

    def ensure_testcases_in_plan(self):
        # Get the platformid if possible or else addition will fail
        self.platformid
        for testcase in self.testcases:
            # Can't check if testcase is in plan_tcids, because that won't work if it's there, but of the wrong platform
            try:
                self.tls.addTestCaseToTestPlan(
                    self.testprojectid, self.testplanid, testcase, self.get_latest_tc_version(testcase),
                    platformid=self.platformid
                )
            except TLResponseError as e:
                # Test Case version is already linked to Test Plan
                if e.code == 3045:
                    pass
                else:
                    raise

    def get_latest_tc_version(self, testcaseexternalid):
        return int(self.tls.getTestCase(None, testcaseexternalid=testcaseexternalid)[0]['version'])


class AddTestPlanReporter(TestReporter):
    @property
    def testplanid(self):
        if not self.get('testplanid'):
            try:
                self['testplanid'] = self.tls.getTestPlanByName(self.testprojectname, self.testplanname)[0]['id']
            except TLResponseError as e:
                # Name does not exist
                if e.code == 3033:
                    self['testplanid'] = self.generate_testplanid()
                else:
                    raise
            except TypeError:
                self['testplanid'] = self.generate_testplanid()
        return self['testplanid']

    def generate_testplanid(self):
        """This won't necessarily be able to create a testplanid. It requires a planname and projectname."""
        if 'testplanname' not in self:
            raise RuntimeError("Need testplanname to generate a testplan for results.")

        tp = self.tls.createTestPlan(self['testplanname'], self.testprojectname)
        self['testplanid'] = tp[0]['id']
        return self['testplanid']


class AddPlatformReporter(TestReporter):
    @property
    def platformname(self):
        """Return a platformname added to the testplan if there is one."""
        pn_kwarg = self.get('platformname')
        if pn_kwarg and self._platformname_generated is False:
            # If we try to create platform and catch platform already exists error (12000) it sometimes duplicates a
            # platformname
            try:
                self.tls.addPlatformToTestPlan(self.testplanid, pn_kwarg)
            except TLResponseError as e:
                if int(e.code) == 235:
                    self.tls.createPlatform(self.testprojectname, pn_kwarg)
                    self.tls.addPlatformToTestPlan(self.testplanid, pn_kwarg)
                    self._platformname_generated = True
                else:
                    raise
        return pn_kwarg

    @property
    def platformid(self):
        if not self.get('platformid'):
            self['platformid'] = self.getPlatformID(self.platformname)
        # This action is idempotent
        self.tls.addPlatformToTestPlan(self.testplanid, self.platformname)
        return self['platformid']

    def getPlatformID(self, platformname, _firstrun=True):
        """
        This is hardcoded for platformname to always be self.platformname
        """
        platforms = self.tls.getTestPlanPlatforms(self.testplanid)
        for platform in platforms:
            if platform['name'] == platformname:
                return platform['id']
        # Platformname houses platform creation as platform creation w/o a name isn't possible
        if not self.platformname:
            raise RuntimeError(
                "Couldn't find platformid for {}.{}, "
                "please provide a platformname to generate.".format(self.testplanid, self.platformname)
            )
        if _firstrun is True:
            return self.getPlatformID(self.platformname, _firstrun=False)
        else:
            raise RuntimeError("PlatformID not found after generated from platformname '{}' "
                               "in test plan {}.".format(self.platformname, self.testplanid))


class AddBuildReporter(TestReporter):
    @property
    def buildid(self):
        bid = self.get('buildid')
        if not bid or bid not in self.tls.getBuildsForTestPlan(self.testplanid):
            self['buildid'] = self._generate_buildid()
        return self.get('buildid')

    def _generate_buildid(self):
        r = self.tls.createBuild(self.testplanid, self.buildname, self.buildnotes)
        return r[0]['id']


class TestGenReporter(AddTestReporter, AddBuildReporter, AddTestPlanReporter, AddPlatformReporter, TestReporter):
    """This is the default generate everything it can version of test reporting.

    If you don't want to generate one of these values you can 'roll your own' version of this class with only the
    needed features that you want to generate.

    For example if you wanted to add platforms and/or tests to testplans, but didn't want to ever make a new testplan
    you could use a class like:
    `type('MyOrgTestGenReporter', (AddTestReporter, AddPlatformReporter, TestReporter), {})`

    Example usage with fake testlink server test and a manual project.
    ```
    tls = testlink.TestLinkHelper('https://testlink.corp.com/testlink/lib/api/xmlrpc/v1/xmlrpc.php',
                                  'devkeyabc123').connect(testlink.TestlinkAPIClient)
    tgr = TestGenReporter(tls, ['TEST-123'], testprojectname='MANUALLY_MADE_PROJECT', testplanname='generated',
                          platformname='gend', buildname='8.fake', status='p')
    ```
    """
