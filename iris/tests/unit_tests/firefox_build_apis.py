# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a unit test to verify basic Firefox build info.'

    def run(self):
        # These tests are for APIs that query the about:config preferences
        assert_equal(self, self.app.version, get_firefox_version(), 'API for Firefox version is correct')
        assert_equal(self, self.app.build_id, get_firefox_build_id(), 'API for Firefox build ID is correct')
        assert_equal(self, self.app.fx_channel, get_firefox_channel(), 'API for Firefox channel is correct')
        assert_equal(self, self.app.fx_locale, get_firefox_locale(), 'API for Firefox locale is correct')
