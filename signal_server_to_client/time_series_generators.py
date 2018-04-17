"""
The Python implementation of time-series generators
All specifications for new signal content are contained in this file,
    so a new time-series type can be added here
Progammer David G Messerschmitt
16 April 2018
"""

# make use of NumPy to simplify array processing
import numpy as np

# adding a new signal generator involves two steps:
#   add name to Chooser()
#   add class to generate that signal

class Chooser():
    # this class allows the server to dynamically choose a
    #   time-series generator

    def __init__(self):

        # *** INCLUDE A LINE HERE FOR EACH TIME-SERIES GENERATOR TYPE ***
        self.generators = {}
        self.generators['cexp'] = ComplexExponentialGenerator()

    def alternatives(self):

        return list(self.generators.keys())

    def choice(self, name):
        # name = name of signal generator
        # returns signal generator object or None

        if name in self.generators:
            return self.generators[name]
        else:
            print('\nTime-series generator name {} unknown'.format(name))
            return None


class ComplexExponentialGenerator():

    def __init__(self): pass

    def parameters(self):
        # specify configuration parameters, includng values (cannot be changed)
        #   and defaults (subject to change)
        # a default = None indicates that the client must specify a value

        t = {'service_type':'cexp'}
        t['description'] = 'generator returns samples of a complex exponential \
exp(j * 2*pi * phase(t) * t) where t = time'
        t['num_samples'] = {
                          'description':'total duration of time-series in samples',
                          'default':None,
                          'minimum':1
                          }
        t['frame'] = {
                        'description':'number of time-samples in each generated \
time-series frame',
                        'default':10,
                        'minimum':1
                        }
        t['phase_initial'] = {
                          'description':'phase of first time-sample \
as fraction of 2*pi, in the range +-0.5',
                          'default':0.,
                          'minimum':-0.5,
                          'maximum':+0.5
                          }
        t['phase_increment'] = {
                        'description':'phase advance per time-sample as fraction \
of 2*pi;  by sampling theorem, must be in the range +-0.5',
                        'default':None,
                        'minimum':-0.5,
                        'maximum':+0.5
                        }
        return t

    def initialize(self,t):
        # initialize the time-series generator
        # t = dictionary of final parameter values
                  
        # store final set of parameters as variables for efficiency
        # for example, parameter 'frame' becomes self.frame
        for field in t.keys():
            setattr(self,field,t[field])

        self._count = 0  # number of time-values generated in total
        
    def generate(self):
        # generates one frame of time-samples and returns as a list

        # determine number of samples to generate this call
        total_remaining = self.num_samples - self._count
        start = self._count
        duration = min(total_remaining,self.frame)

        if duration > 0:

            t = np.arange(start,start+duration,1)  # array of time indexes
            arg = 1j * 2 * np.pi * self.phase_increment * t
            vals = np.exp(arg)
            self._count += duration
            
            return list(vals)

        else: return []
    
