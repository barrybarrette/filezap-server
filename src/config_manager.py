import os


def get_config():
    return {
        'FILE_DB_TABLE': _get_file_db_table(),
        'USER_DB_TABLE': _get_user_db_table(),
        'USER_REGISTRATION_ENABLED': _get_user_registration_enabled()
    }


def _get_user_db_table():
    return _PROD_USER_DB_TABLE if _is_production_environment() else _DEV_USER_DB_TABLE


def _get_file_db_table():
    return _PROD_FILE_DB_TABLE if _is_production_environment() else _DEV_FILE_DB_TABLE


def _get_user_registration_enabled():
    return False if _is_production_environment() else True


def _is_production_environment():
    return True if os.environ.get('FILEZAP_ENV') == PROD_ENV else False


DEV_ENV = 'DEVELOPMENT'
PROD_ENV = 'PRODUCTION'
_DEV_FILE_DB_TABLE = 'files-dev'
_DEV_USER_DB_TABLE = 'users-dev'
_PROD_FILE_DB_TABLE = 'files'
_PROD_USER_DB_TABLE = 'users'