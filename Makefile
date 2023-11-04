all: stegano_image
stegano_image : stegano_image.py
	python3 stegano_image.py
clean:
	rm -f imageRecuperee.* imageSteganographiee.*