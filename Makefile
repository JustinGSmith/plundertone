PREFIX=py/noisesmith
play: y_t.wav
	mplayer y_t.wav

y_t.wav: y_t.cdda
	sox -x y_t.cdda y_t.wav

y_t.cdda: ${PREFIX}/yasunao.py ${PREFIX}/tone.py resource/tone.wav
	PYTHONPATH=py:${PYTHONPATH} python3 ${PREFIX}/tone.py

clean:
	rm -f *.m4a *.wav *.ogg *.raw *.cdda
