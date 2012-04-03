# -*- coding: utf8 -*-
"""
.. module:: lesscpy.plib.node
    :synopsis: Base Node
    
    Copyright (c)
    See LICENSE for details.
.. moduleauthor:: Jóhann T. Maríusson <jtm@robot.is>
"""
from lesscpy.lessc import utility

class Node(object):
    def __init__(self, tokens, lineno=0):
        """ Base Node
        args:
            tokens (list): tokenlist
            lineno (int): Line number of node
        """
        self.tokens = tokens
        self.lineno = lineno
        self.parsed = False
    
    def parse(self, scope):
        """ Base parse function
        args:
            scope (Scope): Current scope
        returns:
            self
        """
        return self
    
    def process(self, tokens, scope):
        """ Process tokenslist, flattening and parsing it
        args:
            tokens (list): tokenlist
            scope (Scope): Current scope
        returns:
            list
        """
        while True:
            tokens = list(utility.flatten(tokens))
            done = True
            if any(t for t in tokens if hasattr(t, 'parse')):
                tokens = [t.parse(scope) 
                          if hasattr(t, 'parse') 
                          else t
                          for t in tokens]
                done = False
            if any(t for t in tokens if utility.is_variable(t)):
                tokens = self.replace_variables(tokens, scope)
                done = False
            if done: break
        return tokens
    
    def replace_variables(self, tokens, scope):
        """ Replace variables in tokenlist
        args:
            tokens (list): tokenlist
            scope (Scope): Current scope
        returns:
            list
        """
        return [scope.swap(t)
                if utility.is_variable(t)
                else t 
                for t in tokens]

    def fmt(self, fills):
        """ Format node
        args:
            fills (dict): replacements
        returns:
            str
        """
        raise ValueError('No defined format')
