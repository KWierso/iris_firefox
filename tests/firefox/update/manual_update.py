# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a test for Firefox manual update.',
        preferences={'app.update.auto': True},
        enabled=False
    )
    def run(self, firefox):
        update_restart_pattern = Pattern('manual_restart_to_update_button.png')
        firefox_up_to_date_pattern = Pattern('firefox_up_to_date.png')

        version = firefox.application.version
        current_version = version if '-dev' not in version else version.replace('-dev', '')
        channel = firefox.application.channel
        rules_dict = get_rule_for_channel(channel, current_version)

        assert rules_dict is not None, 'No rules found for {} channel. Please update config.ini file.'.format(channel)

        starting_condition = rules_dict['starting_condition']
        update_steps_list = rules_dict['steps'].split(',')
        assert current_version in FirefoxUtils.get_firefox_version(firefox.application.path), \
            'Firefox version is incorrect.'

        if is_update_required(current_version, starting_condition):
            for update_step in update_steps_list:

                if update_step == 'latest':
                    update_step = firefox.application.latest_version

                logger.info('Current version: %s, updating to version: %s.' % (current_version, update_step))

                open_about_firefox()
                wait(update_restart_pattern.similar(.7), 200)
                type(Key.ESC)

                firefox.restart()
                assert FirefoxUtils.get_firefox_version(firefox.application.path) in update_step, \
                    'Incorrect Firefox update.'
                current_version = FirefoxUtils.get_firefox_version(firefox.application.path)

        open_about_firefox()
        wait(firefox_up_to_date_pattern, 20)
        type(Key.ESC)

        assert current_version in FirefoxUtils.get_firefox_version(firefox.application.path), \
            'Incorrect Firefox version.'

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected = exists(LocalWeb.MOZILLA_LOGO, 5)
        assert expected, 'Manual update sanity test failed.'
