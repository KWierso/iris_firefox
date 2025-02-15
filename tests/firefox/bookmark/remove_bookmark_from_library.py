# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Bookmarks can be removed from the Bookmarks Library.',
        locale=['en-US'],
        test_case_id='169264',
        test_suite_id='2525',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        library_bookmarks_pattern = Library.BOOKMARKS_TOOLBAR
        moz_library_pattern = Pattern('moz_library_bookmark.png')
        delete_pattern = Pattern('delete_bookmark.png')

        navigate('about:blank')

        open_library()

        bookmarks_menu_library_assert = exists(library_bookmarks_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert bookmarks_menu_library_assert, 'Bookmarks menu has been found.'

        click(library_bookmarks_pattern)

        type(Key.ENTER)
        type(Key.DOWN)

        try:
            wait(moz_library_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Moz bookmark can be accessed in Library section.')
            right_click(moz_library_pattern)
        except FindError:
            raise FindError('Moz bookmark is not present in Library section, aborting.')

        click(delete_pattern)

        try:
            deleted_bookmark_assert = wait_vanish(moz_library_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert deleted_bookmark_assert is True, 'Moz bookmark has been removed from the Library.'
        except FindError:
            raise FindError('MOz bookmark can NOT be removed from the Library, aborting.')

        click_window_control('close')
