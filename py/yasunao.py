import io

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
        return self.in_stream.seek(offset)
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

class StutterFlutters():
    def __init__(self, source, sink, **params):
        self.source = source
        self.sink = sink
        self.advance = params.pop('advance', 10)
        self.grain_duration = params.pop('grain_duration', 10000)
        self.grain_delta = params.pop('grain_delta', 1)
    def gen(self, rep):
        start = self.source.tell()
        for i in range(rep):
            forward = i*self.advance
            self.source.seek(start + forward)
            dur = self.grain_duration + (i * self.grain_delta)
            buffer = []
            self.source.read(buffer, dur)
            self.sink.write(buffer)

def secs2bytes(n):
    return n*2*2*44100

def process(source, sink):
    # copy(source, sink, 240, pos=0)
    in_point = secs2bytes(80)
    source.seek(in_point)
    reps = 256
    grain_step = 1024
    StutterFlutters(source, sink,
                    punch_in=in_point, advance=grain_step,
                    grain_duration=200, grain_delta=2.1).gen(reps)
    in_point += grain_step*reps
    source.seek(in_point)
    StutterFlutters(source, sink,
                    punch_in=in_point, advance=(grain_step * -1),
                    grain_duration=2000, grain_delta=(1 / 2.1)).gen(reps)

data_source = Reader("resource/tone.wav")
data_sink = Writer("y_t.cdda.raw")
process(data_source, data_sink)
