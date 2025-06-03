import io
from operator import and_, invert

class Reader():
    def __init__(self, f):
        in_stream = open(f, "rb")
        self.in_stream = io.BufferedReader(in_stream)
    def read(self, data, count):
        consumed = 0
        while(consumed < count):
            chunk = self.in_stream.read1()
            if(len(chunk) <= 0):
                break
            consumed += len(chunk)
            data.extend(chunk)
        return consumed
    def seek(self, offset):
        return self.in_stream.seek(int(offset))
    def tell(self):
        return self.in_stream.tell()

class Writer():
    def __init__(self, f):
        self.out_stream = open(f, "wb")
    def write(self, data):
        return self.out_stream.write(bytes(data))

def copy(source, sink, count, pos=False):
    buffer = []
    if(pos):
        source.seek(pos)
    source.read(buffer, count)
    return sink.write(buffer)

# crude non-overlap granulation without windowing
class CrudeGranulator():

    def __init__(self, source, sink, **params):
        self.source = source
        self.sink = sink
        self.input_step = params.pop('input_step', 10)
        self.grain_duration = params.pop('grain_duration', 10000)
        self.grain_delta = params.pop('grain_delta', 1)

    def gen(self, rep):
        start = self.source.tell()
        for i in range(rep):
            forward = i*self.input_step
            self.source.seek(start + forward)
            dur = self.grain_duration + (i * self.grain_delta)
            buffer = []
            self.source.read(buffer, dur)
            self.sink.write(buffer)

# truncate to a multiple of 4, so we don't flip byte order or swap channels
# unintentionally (2 channels, 2 bytes per sample = 4 bytes per item)
def align(n):
    return and_(int(n), invert(3))

# align is still useful here, because n can be a floating point value
def secs(n):
    return align(n*2*2*44100)
