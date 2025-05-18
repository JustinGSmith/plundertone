play: y_t.wav
	mplayer y_t.wav

y_t.wav: y_t.cdda
	sox -x y_t.cdda y_t.wav

y_t.cdda: py/yasunao.py resource/tone.wav
	python3 py/yasunao.py

clean:
	rm -f *.m4a *.wav *.ogg *.raw *.cdda
