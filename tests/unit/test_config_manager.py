import os
import unittest

import src.config_manager as config_manager


class TestConfigManager(unittest.TestCase):

    def test_defaults_db_config_to_dev(self):
        config = config_manager.get_config()
        self.assertEqual(config.get('USER_DB_TABLE'), config_manager._DEV_USER_DB_TABLE)


    def test_sets_db_config_to_prod_if_in_prod_environment(self):
        os.environ['FILEZAP_ENV'] = config_manager.PROD_ENV
        config = config_manager.get_config()
        self.assertEqual(config.get('USER_DB_TABLE'), config_manager._PROD_USER_DB_TABLE)
        os.environ.pop('FILEZAP_ENV')


    def test_user_registration_is_enabled_by_default(self):
        config = config_manager.get_config()
        self.assertEqual(config.get('USER_REGISTRATION_ENABLED'), True)


    def test_user_registration_is_disabled_in_prod(self):
        os.environ['FILEZAP_ENV'] = config_manager.PROD_ENV
        config = config_manager.get_config()
        self.assertEqual(config.get('USER_REGISTRATION_ENABLED'), False)
        os.environ.pop('FILEZAP_ENV')