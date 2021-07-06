from PIL import Image

square_size = 64
border = 2
size = 3472, 2480


def edit_image(infile, outfile):
    image = Image.open(infile)  # open a file
    width, height = image.size  # get image sizes

    if width > height:
        ratio = 3472 // width
    else:
        ratio = 2480 // height

    size = (width * ratio // square_size) * \
        square_size, (height * ratio // square_size) * square_size
    # edit the size
    image = image.resize(size, Image.ANTIALIAS)
    image.save(outfile)

    image = Image.open(outfile)
    pixels = image.load()  # get a matrix of pixel colors
    width, height = image.size

    for i in range(height):
        for j in range(width):
            if i == 0 or (i + 1) % square_size == 0:
                pixels[j, i] = (0, 0, 0)
    for j in range(width):
        for i in range(height):
            if j == 0 or (j + 1) % square_size == 0:
                pixels[j, i] = (0, 0, 0)

    # recolor pixels
    for h in range(height):  # iterating over the squares
        for w in range(width):
            if h == 1 and w == 1 or h % square_size == 0 and w % square_size == 0:
                s = [0, 0, 0]
                for i in range(h, h + square_size - 1):
                    for j in range(w, w + square_size - 1):
                        s = [s[c] + pixels[j, i][c]
                             for c in range(3)]  # summing up the colors
                # find the arithmetic mean
                m = tuple([s[c] // (square_size - 1)**2 for c in range(3)])
                for i in range(h, h + square_size - 1):
                    for j in range(w, w + square_size - 1):
                        pixels[j, i] = m  # repaint in medium color

    # save the image
    image.save(outfile)
