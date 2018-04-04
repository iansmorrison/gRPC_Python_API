
# performance-related parameters (no effect on functionalty)
INITIAL_BUFFER_SIZE = 10
# increase in buffer size when needed; must be > 1
BUFFER_GROWTH_FACTOR = 1.5

class CircularBuffer:
    '''
    Implements FIFO buffer requiring no rearrangements of
        data in memory during operation
    Each location in the buffer stores a list of floating-point values
    '''

    def __init__(self):
        # size = number of buffer locations, with a list of values
        #   potentially occupying each location
        
        # initial buffer state
        self._size = INITIAL_BUFFER_SIZE
        self._buffer = [None] * INITIAL_BUFFER_SIZE
        self._oldest = 0 # index of the oldest value stored in buffer
        self._count = 0 # number of values currently stored in buffer
        # newest value is stored at (oldest+count-1) % size
    
    def write(self,vals):
        # vs = value or data structure (typically a list) to be added to buffer
        # adds this to buffer
        
        if self._count == self._size:
            # this operation would be lossy, so grow buffer
            self.grow()           
        self._count += 1
        self._buffer[(self._oldest+self._count -1) % self._size] = vals
            
    def read(self):
        # returns oldest data stored in buffer
        #   and removes that data from the buffer reducing count by one
        
        if self._count == 0: # buffer is empty
            return []
        else:
            vals = self._buffer[self._oldest]
            self._count -=1
            self._oldest = (self._oldest+1) % self._size
        return vals

    def contents(self):
        # service routine that prints the current contents of the buffer
        #   (comes in handy for diagnostic purposes)
        
        print('\nCurrent buffer state:')
        print('Number of locations: ',self._count)
        print('First value is the oldest:')
        for i in range(self._count):
            print(self._buffer[(self._oldest+i) % self._size])
        print('Last value is the newest\n')

    def examine(self):
        # returns oldest data stored in buffer
        #   without removing that data from the buffer
        # returns None if buffer is empty
        # number of locations in buffer is not affected

        if self._count == 0: # buffer is empty
            return None
        else:
            return self._buffer[self._oldest]

    def replace(self,vals):
        # replaces oldest data stored in buffer
        #   with new data
        # returns 0 if operation is successful

        if self._count == 0: # buffer is empty
            return 1
        else:
            self._buffer[self._oldest] = vals
            return 0

    def grow(self):
        # grow the size of the buffer exponentially
        # the buffer is never allowed to shrink
        # values already stored in buffer are not disturbed by this operation
        # this method used to prevent buffer overwrite and loss of data

        add_size = int(self._size * (BUFFER_GROWTH_FACTOR - 1))+1
        add = [None] * add_size
        # added buffer locations located in front of oldest value
        self._buffer = self._buffer[:self._oldest] + add + self._buffer[self._oldest:]
        self._size += add_size
        self._oldest += add_size

        
class ListBuffer(CircularBuffer):
    '''
    Class manages a CircularBuffer where each location stores
        a list of values (value type not specified)
    To prevent side effects (call by reference), the routines
        consistently work with shadow copies (vals[:] rather than vals)
    Keeps track of the total number of values stored in buffer
        and calls signal server when that number is insufficient
    '''

    def __init__(self,server,bypass=False):
        # server = signal generator which provides list of
        #   signal samples on request
        
        super().__init__()

        self.server = server
        self._bypass = bypass
        self.initialize()

    def initialize(self):

        # total number of signal samples stored in buffer; note that this
        #   is different from the number of buffer locations occupied
        #   because each location stores a list of signal samples
        self._sample_count = 0
        self.finished = False # server exhaused
        
    def bypass(self):
        # call to get list of signal samples from server
        #   and return those values
        # use this method rather than get() if no buffering is desired
        return self.server.get()[:]
        
    def add(self,vals):
        # vals = list of values to write to the buffer
        
        self._sample_count += len(vals)
        self.write(vals[:])

    def subtract(self,size):
        # size = number of values to attempt to remove from buffer
        # removed may = size or fewer
        #   (never removes more than one buffer location)
        # returns the list of values that have been removed

        extracted = self.examine()
        wanted = extracted[:size] # values to extract
        left_over = extracted[size:] # left over values to be returned to buffer

        if len(left_over) > 0:
            self.replace(left_over[:])
        else:
            self.read() # removes this location from buffer
            
        self._sample_count -= len(wanted)
        return wanted[:]

    def get(self,size):
        # size = number of values requested by a signal client
        # returns a list of oldest values from the buffer of length size
        # if the buffer contains less than size values, repetitively
        #   call the signal server until sufficient values are stored in buffer
        # if the signal server exhausts, return a list with len(list) < size
        #   containing all the remaining values from the buffer

        # until we find otherwise, server is assumed to have
        #   more signal values available
        
        while not self.finished and self._sample_count < size:
            # more values should be added to buffer
            # no control over how many samples get() generates,
            #   so may need to call more than once
            vals = self.server.get()
            if len(vals) > 0:
                self.add(vals[:])
            else: # server is generating no more data
                self.finished = True

        if self.finished: # server has exausted, so extract everything in buffer
            extracted = []
            while self._sample_count > 0:
                extracted += self.subtract(size)
            return extracted[:]
        
        else: # buffer has sufficient values to satisfy request
            remaining = size
            extracted = []
            while True:
                extracted += self.subtract(remaining)
                remaining -= len(extracted)
                if remaining == 0:
                    return extracted[:]

    
