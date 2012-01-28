"""
    LessCss tests
"""
import unittest
import sys, os
import re

here = os.path.dirname(__file__)
path = os.path.abspath(here)
while os.path.dirname(path) != path:
    if os.path.exists(os.path.join(path, 'lesscpy', '__init__.py')):
        sys.path.insert(0, path)
        break
    path = os.path.dirname(path)

def find():
    svn = re.compile('\.svn')
    test = re.compile('test.+\.py$')
    skip = re.compile('testissues.*')
    alltests = unittest.TestSuite()
    for path, dirs, files in os.walk(here):
        if svn.search(path):
            continue
        for f in files:
            if skip.search(f):
                continue
            if test.search(f):
                module = __import__(f.split('.')[0])
                alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='find')