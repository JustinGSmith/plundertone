default: clean
	python3 py/yasunao.py && sox -x y_t.cdda y_t.wav && mplayer y_t.wav

clean:
	rm -f y_t.m4a y_t.wav
