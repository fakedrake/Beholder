import functools
from PIL import Image, ImageDraw
import numpy
import glob

from itertools import izip, imap, groupby, izip_longest
from multiprocessing import Pool
import sys

THRESHOLD = 50


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def save_boxed(img, box, size):
    try:
        save_boxed.myid += 1
    except:
        save_boxed.myid = 0

    mi = Image.fromstring("RGB", size, img)
    draw = ImageDraw.Draw(mi)

    draw.rectangle(box)
    mi.save("boxed/img%04d.png" % save_boxed.myid)


def bbox(img, bg, size, thresh):

    width, height = size

    minx = miny = float("Inf")
    maxx = maxy = -1

    assert len(img) == len(bg)
    assert len(img) % 3 == 0

    for i, (ip, bp) in enumerate(izip(grouper(img, 3), grouper(bg, 3))):
        if abs(ord(ip[0]) - ord(bp[0])) > thresh:
            if i % width < minx:
                minx = i % width
                continue

            if i % width > maxx:
                maxx = i % width
                continue

            if i // width < miny:
                miny = i // width
                continue

            if i // width > maxy:
                maxy = i // width
                continue

    ret = (minx, miny, maxx, maxy)

    save_boxed(img, ret, size)
    return ret


THREAD_NUM = 5

p = Pool(THREAD_NUM)

imgs = map(Image.open, sys.argv[1:])

img_data = map(lambda i: i.tostring(), imgs)
size = imgs[0].size

print "# of imgs: %d -> %s" % (len(imgs), size)

try:
    bg = Image.open("bg.png").tostring()
except IOError:
    # Note that this only works for grayscale images. Otherwise we would have to combine the colors.
    bg = "".join(map(lambda x:chr(int(numpy.median(map(ord, x)))), izip(*img_data)))
    print "Background created."

bg_img = Image.fromstring("RGB", size, bg)
bg_img.save("bg.png", "PNG")

bboxes = map(functools.partial(bbox, bg=bg, size=size, thresh=THRESHOLD), img_data)
strides = map(lambda (xt,yt,xb,yb): xb-xt, bboxes)

print "Bboxes:"
print "\n".join(map(str, bboxes[-10:]))
print "Last box:"
print bboxes[-1]

with open("strides.dat", "w") as f:
    for i, s in enumerate(strides):
        f.write("%d %d\n" % (i, s))

print "writen strides.dat"
