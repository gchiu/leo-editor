# -*- coding: utf-8 -*-
#@+leo-ver=5-thin
#@+node:maphew.20180224170853.1: * @file ../../setup.py
#@@first
'''setup.py for leo'''
#@+others
#@+node:maphew.20180305124637.1: ** imports
from codecs import open # To use a consistent encoding
import os
import platform
# from shutil import rmtree
from setuptools import setup, find_packages # Always prefer setuptools over distutils
import sys

# Ensure setup.py's folder is in module search path else import leo fails
# required for pip >v10 and pyproject.toml 
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import leo.core.leoGlobals as g
import leo.core.leoVersion as leoVersion

#@+node:mhw-nc.20190126224021.1: ** setup janitor
# Initiated by #1055 - Have 'setup clean' play nice with others
# Until accepted upstream we require this forked module pre-installed
# from: https://github.com/maphew/setupext-janitor/setupext_janitor
# to: ./leo/extensions/setupext_janitor
try:
   from leo.extensions.setupext_janitor import janitor
   CleanCommand = janitor.CleanCommand
except ImportError:
   CleanCommand = None

cmd_classes = {}
if CleanCommand is not None:
   cmd_classes['clean'] = CleanCommand

#@+node:maphew.20181010203342.385: ** get_version
def get_version(file, version=None):
    '''Determine current Leo version. Use git if in checkout, else internal Leo'''
    root = os.path.dirname(os.path.realpath(file))
    if os.path.exists(os.path.join(root,'.git')):
        version = git_version(file)
    if not version:
        version = get_semver(leoVersion.version)
    return version
#@+node:maphew.20181010203342.386: *3* git_version
def git_version(file, version=None):
    '''Fetch from Git: {tag} {distance-from-tag} {current commit hash}
       Return as semantic version string compliant with PEP440'''
    root = os.path.dirname(os.path.realpath(file))
    try:
        tag, distance, commit = g.gitDescribe(root)
            # 5.6b2, 55, e1129da
        ctag = clean_git_tag(tag)
        #version = get_semver(ctag)
        version = ctag
        if int(distance) > 0:
            version = '{}-dev{}'.format(version, distance)
    except IndexError:
        print('Attempt to `git describe` failed with IndexError')
    except FileNotFoundError:
        print('Attempt to `git describe` failed with FileNotFoundError')
    return version

#@+node:maphew.20180224170257.1: *4* clean_git_tag
def clean_git_tag(tag):
    '''Return only version number from tag name. Ignore unknown formats.
       Is specific to tags in Leo's repository.
            5.7b1          -->	5.7b1
            Leo-4-4-8-b1   -->	4-4-8-b1
            v5.3           -->	5.3
            Fixed-bug-149  -->  Fixed-bug-149
    '''
    if tag.lower().startswith('leo-'): tag = tag[4:]
    if tag.lower().startswith('v'): tag = tag[1:]
    return tag
#@+node:maphew.20180224170149.1: *3* get_semver
def get_semver(tag):
    '''Return 'Semantic Version' from tag string'''
    try:
        import semantic_version
        version = str(semantic_version.Version.coerce(tag, partial=True))
            # tuple of major, minor, build, pre-release, patch
            # 5.6b2 --> 5.6-b2
    except ImportError or ValueError as err:
        print('\n', err)
        print('''*** Failed to parse Semantic Version from git tag '{0}'.
        Expecting tag name like '5.7b2', 'leo-4.9.12', 'v4.3' for releases.
        This version can't be uploaded to PyPi.org.'''.format(tag))
        version = tag
    return version
#@+node:maphew.20171006124415.1: ** Get description
with open('README.md') as f:
    long_description = f.read()
#@+node:maphew.20141126230535.4: ** classifiers
classifiers = [
    'Development Status :: 6 - Mature',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Topic :: Software Development',
    'Topic :: Text Editors',
    'Topic :: Text Processing',
    ]
#@+node:maphew.20180415195922.1: ** Setup requirements
setup_requires = []
    # setup_requires no longer needed with PEP-518 and pip >v10
#@+node:maphew.20171120133429.1: ** User requirements
user_requires = [
    'PyQt5; python_version >= "3.0"',
    #'python-qt5; python_version < "3.0" and platform_system=="Windows"',
        # disabled, pending "pip install from .whl fails conditional dependency check" https://github.com/pypa/pip/issues/4886
    'docutils', # used by Sphinx, rST plugin
    'flexx; python_version >= "3.5"', # for LeoWapp browser gui, requires python v3.5+
    'nbformat', # for Jupyter notebook integration
    'pylint','pyflakes', # coding syntax standards
    'sphinx', # rST plugin
    'future', # python 2/3 compatibility layer, same with 'six'
    'six',
    ]
#@+node:maphew.20190207205714.1: ** define_entry_points
def define_entry_points(entry_points=None):
    '''1. Define scripts that get installed to PYTHONHOME/Scripts.
      2. Extend `python setup.py clean` to remove more files (issue #1055)   
    '''
    print('Creating entry_points for [OS name - system]: {} - {}'.format(platform.os.name, platform.system()))
    entry_points={'console_scripts': [
            'leo-c = leo.core.runLeo:run_console',
            'leo-console = leo.core.runLeo:run_console'],
            'gui_scripts': ['leo = leo.core.runLeo:run']}
    if platform.system() == 'Windows':
        entry_points.update({'console_scripts': [
            'leo-m = leo.core.runLeo:run',
            'leo-messages = leo.core.runLeo:run']})

    entry_points.update({
            'distutils.commands': [
            'clean = setupext_janitor.janitor:CleanCommand']})
    return entry_points
#@-others

setup(
    name='leo',
    # version = leo.core.leoVersion.version,
    version=get_version(__file__),
    author='Edward K. Ream',
    author_email='edreamleo@gmail.com',
    url='http://leoeditor.com',
    license='MIT License',
    description='An IDE, PIM and Outliner', # becomes 'Summary' in pkg-info
    long_description=long_description,
    long_description_content_type="text/markdown", # PEP566
    platforms=['Linux', 'Windows', 'MacOS'],
    download_url='http://leoeditor.com/download.html',
    classifiers=classifiers,
    packages=find_packages(),
    include_package_data=True, # also include MANIFEST files in wheels
    setup_requires=setup_requires,
    install_requires=user_requires,
    entry_points=define_entry_points(),
    cmdclass={'clean': janitor.CleanCommand} # clean more than setuptools, #1055
)

#@@language python
#@@tabwidth -4
#@-leo
