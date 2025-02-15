# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks that more search engines can be added and are well displayed on one-off '
                    'searches bar.',
        locale=['en-US'],
        test_case_id='108261',
        test_suite_id='1902'
    )
    def run(self, firefox):
        moz_pattern = Pattern('moz.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        search_engine_pattern = Pattern('search_engine.png')
        search_settings_pattern = Pattern('search_settings.png')
        amazon_one_off_button_pattern = Pattern('amazon_one_off_button.png')
        bing_one_off_button_pattern = Pattern('bing_one_off_button.png')
        duck_duck_go_one_off_button_pattern = Pattern('duck_duck_go_one_off_button.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        twitter_one_off_button_pattern = Pattern('twitter_one_off_button.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')
        moz_search_amazon_search_engine_pattern = Pattern('moz_search_amazon_search_engine.png')
        add_startpage_https_privacy_search_engine_pattern = Pattern('add_startpage_https_privacy_search_engine.png')
        find_more_search_engines_pattern = Pattern('find_more_search_engines.png')
        add_to_firefox_pattern = Pattern('add_to_firefox.png')
        add_button_pattern = Pattern('add_button.png')
        startpage_https_search_engine_pattern = Pattern('startpage_https_search_engine.png')
        startpage_one_off_button_pattern = Pattern('startpage_one_off_button.png')
        find_add_ons = Pattern('find_add_ons.png')

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        paste('moz')

        pattern_list = [moz_pattern, search_settings_pattern, amazon_one_off_button_pattern,
                        bing_one_off_button_pattern, duck_duck_go_one_off_button_pattern, google_one_off_button_pattern,
                        twitter_one_off_button_pattern, wikipedia_one_off_button_pattern]

        # Deleted assert for ebay because we no longer have the ebay search engine in some locations.

        # Check that the default one-off list is displayed in the awesomebar.
        for index, pattern in enumerate(pattern_list):
            if OSHelper.is_mac():
                expected = region.exists(pattern.similar(0.7), 10)
                assert expected, 'Element found at position {} in the list found.'.format(index)
            else:
                expected = region.exists(pattern.similar(0.8), 10)
                assert expected, 'Element found at position {} in the list found.'.format(index)

        click(search_settings_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected, 'The \'about:preferences#search\' page successfully loaded.'

        expected = exists(default_search_engine_dropdown_pattern, 10)
        assert expected, 'Default search engine dropdown found.'

        click(default_search_engine_dropdown_pattern)

        # Change the default search engine.
        repeat_key_down(2)

        type(Key.ENTER)

        # Check that default search engine successfully changed.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        paste('moz')
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        type(Key.SPACE)

        expected = exists(moz_search_amazon_search_engine_pattern, 10)
        assert expected, 'Default search engine successfully changed.'

        # Remove the 'Google' search engine.
        next_tab()

        for i in range(4):
            type(Key.TAB)

        if OSHelper.is_windows() or OSHelper.is_linux():
            type(Key.SPACE)
        else:
            type(Key.TAB)
            click(search_engine_pattern.target_offset(20, 150), align=Alignment.TOP_LEFT)

        expected = exists(search_engine_pattern, 10)
        assert expected, 'One-Click Search Engines section found.'

        # Check that unchecked search engine is successfully removed from the one-off searches bar.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        paste('moz')
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        type(Key.SPACE)

        if OSHelper.is_windows() or OSHelper.is_linux():
            try:
                expected = wait_vanish(google_one_off_button_pattern, 10)
                assert expected, 'Unchecked search engine successfully removed from the one-off searches bar.'
            except FindError:
                raise FindError('Unchecked search engine not removed from the one-off searches bar.')
        else:
            expected = exists(google_one_off_button_pattern.similar(0.9), 10)
            assert not expected, 'Unchecked search engine successfully removed from the one-off searches bar.'

        next_tab()
        for i in range(12):
            type(Key.TAB)

        if OSHelper.is_windows() or OSHelper.is_linux():
            type(Key.SPACE)
        else:
            type(Key.TAB)

        type(Key.DOWN)
        expected = exists(find_more_search_engines_pattern, 10)
        assert expected, '\'Find more search engines\' link found.'

        click(find_more_search_engines_pattern)

        try:
            wait(find_add_ons, 10)
            logger.debug('Find add-ons field is present on the page.')
            click(find_add_ons)
        except FindError:
            raise FindError('Find add-ons field is NOT present on the page, aborting.')

        paste('startpage')

        expected = exists(add_startpage_https_privacy_search_engine_pattern, 10)
        assert expected, '\'Startpage HTTPS Privacy Search Engine\' engine successfully found.'

        click(add_startpage_https_privacy_search_engine_pattern)

        expected = exists(add_to_firefox_pattern, 10)
        assert expected, '\'Add to Firefox\' button found.'

        click(add_to_firefox_pattern)

        expected = exists(add_button_pattern, 10)
        assert expected, '\'Add\' button found.'

        click(add_button_pattern)

        previous_tab()

        expected = exists(startpage_https_search_engine_pattern, 10)
        assert expected, 'The search engine added found in the \'One-Click Search Engines\' section.'

        # Perform a new search in the url bar and make sure that everything looks ok after all the above changes.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        paste('moz')
        type(Key.SPACE)

        expected = exists(moz_search_amazon_search_engine_pattern, 10)
        assert expected, 'Default search engine is still changed.'

        expected = exists(startpage_one_off_button_pattern, 10)
        assert expected, 'Newly added search engine successfully found in the one-off searches bar.'

        if OSHelper.is_mac():
            expected = exists(google_one_off_button_pattern.similar(0.9), 10)
            assert not expected, 'Unchecked search engine is still removed from the one-off searches bar.'
        else:
            expected = exists(google_one_off_button_pattern, 10)
            assert not expected, 'Unchecked search engine is still removed from the one-off searches bar.'
