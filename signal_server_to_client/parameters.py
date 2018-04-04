"""
Managment of a parameter database, including checking for consistency,
extracting default values, and similar functions

Progammer David G Messerschmitt
4 April 2018
"""

class Parameters:
  # class to store and manage parameter dictionaries

  def __init__(self):

    # a dictonary t storing default values overridden by
    #   client-specified values
    self.t = {}

  def set(self,p):
    # p = full parameter metadata as a Python dictionary
    self.p = p
    # extract a smaller dictionary d with only default values
    self.d = {}   
    for field in self.p.keys():
      if 'default' in self.p[field]:
        self.d[field] = self.p[field]['default']
    
  def parameters(self):
    return self.p
  
  def defaults(self):
    return self.d

  def update(self,c):
    # c = dictionary of values that are to override the current values
    # returns self.d overridden by c
    self.t = self.d.copy()
    self.t.update(c)
    return

  def complete(self):
    # checks final parameters r to make sure there are no missing values
    # returns either None or the name of the first encountered missing parameter
    for field in self.t.keys():
        if self.t[field] == None:
          return field
    return None

  def bounds(self):
    # checks final parameters r to make sure there are no
    #   value below minimum or above maximum
    # returns either None or the name of the first encountered problematic value
    for field in self.p.keys():
      if 'minimum' in self.p[field]:
        if self.t[field] < self.p[field]['minimum']:
          return field
      if 'maximum' in self.p[field]:
        if self.t[field] > self.p[field]['maximum']:
          return field
    return None

  def final(self):
    # return final set of parameters for signal generation
    return self.t
