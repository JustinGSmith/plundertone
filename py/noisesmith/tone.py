import sys
import noisesmith.yasunao as y

# uses the direction variable to reverse the "parameter automation"
# across the granulations loop
def _tro(source, sink, direction):
    reps = 40
    base_step = y.align(y.secs(0.125) / reps)
    base_duration = y.align(y.secs(0.25) / reps)
    base_chunk_size = 30.0 / reps
    # step forward for iteration step varying values
    def steps(i):
        return i
    # step backward for iteration step varying values
    def rsteps(i):
        return reps - i
    # optionally swap steps and rsteps to reverse direction
    # the iteration step varying values
    if(direction < 0):
        swp = steps
        steps = rsteps
        rsteps = swp
    for i in range(reps):
        step = rsteps(i) * base_step
        duration = rsteps(i) * base_duration
        chunk_size = y.align(steps(i) * base_chunk_size)+4
        y.CrudeGranulator(source, sink,
                          input_step=step, grain_duration=duration
                          ).gen(chunk_size)

def part_a(source, sink):
    in_point = source.tell()
    reps = 256
    grain_step = 1024
    y.CrudeGranulator(source, sink,
                      input_step=grain_step, grain_duration=200,
                      grain_delta=2.1
                      ).gen(reps)
    in_point += grain_step*reps
    source.seek(in_point)
    y.CrudeGranulator(source, sink,
                      input_step=(grain_step * -1), grain_duration=2000,
                      grain_delta=(1 / 2.1)
                      ).gen(reps)

def part_b(source, sink):
    pass

def part_c(source, sink):
    pass

def process(source, sink):
    skip_intro = y.secs(7.5)
    source.seek(skip_intro)
    _tro(source, sink, 1)
    # furthest forward traversal of input file during _tro
    _tro_duration = source.tell() - skip_intro

    print("source at ", source.tell(), " after _tro\n")
    source.seek(y.secs(20))
    part_a(source, sink)

    source.seek(y.secs(40))
    part_b(source, sink)

    source.seek(y.secs(60))
    part_a(source, sink)

    source.seek(y.secs(80))
    part_b(source, sink)

    source.seek(y.secs(100))
    part_c(source, sink)

    source.seek(y.secs(400))
    part_a(source, sink)

    # cue so we consume to the end of the input
    # for now total duration of input is hardcoded and
    # must be changed for new input - ugh
    cue_out = y.secs(352.314) - _tro_duration
    source.seek(cue_out)
    _tro(source, sink, -1)

def main() -> int:
    data_source = y.Reader("resource/tone.wav")
    data_sink = y.Writer("y_t.cdda")
    process(data_source, data_sink)
    return 0

if __name__ == '__main__':
    sys.exit(main())
