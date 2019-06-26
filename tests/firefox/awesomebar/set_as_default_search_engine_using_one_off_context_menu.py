# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case verifies that \'Set as Default Search Engine\' option works correctly using an '
                    'one-off.',
        locale=['en-US'],
        test_case_id='108251',
        test_suite_id='1902',
        preferences={'browser.contentblocking.enabled': False}
    )
    def run(self, firefox):
        moz_pattern = Pattern('moz.png')
        url = LocalWeb.FIREFOX_TEST_SITE
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png').similar(.7)
        set_as_default_search_engine_pattern = Pattern('set_as_default_search_engine.png')
        search_in_new_tab_pattern = Pattern('search_in_new_tab.png')
        magnifying_glass_pattern = Pattern('magnifying_glass.png').similar(.7)
        wikipedia_search_results_pattern = Pattern('wikipedia_search_results.png')
        test_pattern = Pattern('test.png')
        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        navigate(url)

        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        paste('test')
        type(Key.ENTER)

        expected = region.exists(magnifying_glass_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'The default search engine is \'Google\', page successfully loaded.'

        expected = region.exists(test_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Searched item is successfully found in the page opened by the default search engine.'

        select_location_bar()
        paste('moz')

        expected = region.exists(moz_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Searched string found at the bottom of the drop-down list.'

        wiki_button_displayed = region.exists(wikipedia_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert wiki_button_displayed, 'wikipedia_one_off_button_pattern'

        hover(wikipedia_one_off_button_pattern)

        try:
            expected = region.wait_vanish(moz_pattern)
            assert expected, 'The \'Wikipedia\' one-off button is highlighted.'
        except FindError:
            raise FindError('The \'Wikipedia\' one-off button is not highlighted.')

        right_click(wikipedia_one_off_button_pattern)

        expected = exists(search_in_new_tab_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'The \'Search in New Tab\' option found.'

        expected = exists(set_as_default_search_engine_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'The \'Set As Default Search Engine\' option found.'

        click(set_as_default_search_engine_pattern)

        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)

        select_location_bar()
        paste('test')
        type(Key.ENTER)

        expected = exists(wikipedia_search_results_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Wikipedia results are opened.'

        expected = exists('Test', FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Searched item is successfully found in the page opened by the wikipedia search engine.'
