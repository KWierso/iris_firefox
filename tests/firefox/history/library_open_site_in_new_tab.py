# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Use \'Open in a New Tab\' button from the contextual options.',
        locale=['en-US'],
        test_case_id='174039',
        test_suite_id='2000',
        profile=Profiles.TEN_BOOKMARKS
    )
    def run(self, firefox):
        iris_bookmark_pattern = Pattern('iris_bookmark.png')
        show_all_history_pattern = History.HistoryMenu.SHOW_ALL_HISTORY
        history_today_pattern = Library.HISTORY_TODAY
        library_bookmarks_mozilla_pattern = Pattern('library_bookmarks_mozilla.png')
        iris_tab_icon = Pattern('iris_logo_tab.png')

        # Open a page to create some today's history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)

        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1 is True, 'Mozilla page loaded successfully.'

        close_tab()

        # Select the History option from the View History, saved bookmarks and more Menu.
        open_library_menu('History')
        right_upper_corner = Screen().new_region(Screen.SCREEN_WIDTH / 2, 0, Screen.SCREEN_WIDTH / 2,
                                                 Screen.SCREEN_HEIGHT / 2)

        expected_2 = right_upper_corner.exists(iris_bookmark_pattern, 10)
        assert expected_2 is True, 'Iris page is displayed in the History menu list.'

        # Click on the Show All History button.
        click(show_all_history_pattern, 2)

        expected_3 = exists(history_today_pattern, 10)
        assert expected_3 is True, 'Today history option is available.'

        # Verify if Mozilla page is present in Today's History.

        expected_4 = exists(library_bookmarks_mozilla_pattern, 10)
        assert expected_4 is True, 'Mozilla page is displayed successfully in the History list.'

        # Open the Mozilla page using the 'Open in a New Tab' button from the context menu.
        right_click(library_bookmarks_mozilla_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        type(text='w')

        # Close the library.
        open_library()
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        click_window_control('close')
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)

        # Check that the Mozilla page loaded successfully in a new tab.
        expected_5 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_5 is True, 'Mozilla page loaded successfully.'

        expected_6 = exists(iris_tab_icon, 10)
        assert expected_6 is True, 'Iris local page is still open in the first tab.'
