import time

#To enable performance timing set self.verbose = True

class Timer(object):
    def __init__(self, message):
        self.message = message
        self.verbose = False
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        end = time.time()
        self.msecs = int((end - self.start) * 1000)
        if(self.verbose): print('{}: {} ms'.format(self.message, self.msecs))