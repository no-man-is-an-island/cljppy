from distutils.core import setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_suite = True
        self.test_args = []

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='cljppy',
      version='0.1',
      py_modules=['cljppy'],
      tests_require=['pytest==2.3.5'],
      cmdclass = {'test': PyTest}
      )
