from .testreporter import AddTestReporter, AddBuildReporter, AddTestPlanReporter, AddPlatformReporter, TestReporter


class TestGenReporter(AddTestReporter, AddBuildReporter, AddTestPlanReporter, AddPlatformReporter, TestReporter):
    """
    This is the default generate everything it can version of test reporting.

    This class will always try to report a result. It will generate everything possible and will change with additional
    Add*Reporter's added to the repo. As such you should only use this if you want to always generate everything this
    repo is capable of. If you want what it does at any specific time you should create this class in your project and
    use directly.

    If you don't want to generate one of these values you can 'roll your own' version of this class with only the
    needed features that you want to generate. As stated above if you *only* want to generate what this class currently
    does. Copying it into your project is the best practice as this class is mutable inside the project!

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
