import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
# with open(os.path.join(here, 'CHANGES.txt')) as f:
#    CHANGES = f.read()
CHANGES = ''

requires = [
    'pyramid',
]

setup(name='f6a_tw_backend',
      version='0.0',
      description='f6a_tw_backend',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="f6a_tw_backend",
      entry_points="""\
      [pyramid.scaffold]
      module = scaffolds:ModuleProjectTemplate
      dev_starter = scaffolds:DevStarterProjectTemplate
      django = scaffolds:DjangoProjectTemplate
      pkg = scaffolds:PkgProjectTemplate
      """,
      )
