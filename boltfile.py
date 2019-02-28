import os

import bolt

bolt.register_task('clear-pyc', ['delete-pyc.src', 'delete-pyc.tests'])
bolt.register_task('ct', ['clear-pyc', 'conttest'])
bolt.register_task('cov', ['clear-pyc', 'nose.with-coverage'])
bolt.register_task('ut', ['clear-pyc', 'nose'])

_PROJECT_ROOT = os.getcwd()
_SOURCE_CODE_DIR = os.path.join(_PROJECT_ROOT, 'src')
_UNIT_TEST_DIR = os.path.join(_PROJECT_ROOT, 'tests', 'unit')

config = {
    'delete-pyc': {
        'src': {
            'sourcedir': _SOURCE_CODE_DIR,
            'recursive': True
        },
        'tests': {
            'sourcedir': _UNIT_TEST_DIR,
            'recursive': True
        }
    },
    'nose': {
        'directory': _UNIT_TEST_DIR,
        'with-coverage': {
            'options': {
                'with-coverage': True,
                'cover-erase': True,
                'cover-package': 'src',
                'cover-html': True,
                'cover-html-dir': 'output/coverage',
            }
        }
    },
    'conttest': {
        'task': 'nose',
        'directory': _PROJECT_ROOT
    }
}
