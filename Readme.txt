SETUP:
save a suitable CD format wav file as resource/tone.wav
(16 bit PCM, 44.1khz, interleaved stereo)

file should contain new jack swing style pop music

the code will error if the file is missing or has insufficient duration

the python generated output will be 16 bit PCM, 44.1khz, interleaved stereo,
with no header. the Makefile can be used to turn this into a proper wav file

REQUIREMENTS:
requires make, sox, python3, mplayer

the only hard requirement to run the code is python3, and the resulting
headerless output can be imported into your preferred audio tool, but it's
easier to use the Makefile to automate tasks like file format conversion and
playback

TODO:
the eventual plan is to separate the plunderphonic utilities from the specific
composition, and to replace as many external utilities as possible with python
code, while avoiding libraries that are not included in the default python3
distribution
