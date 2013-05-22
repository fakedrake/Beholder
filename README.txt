Hopefully this will be moved somewhere else soon but here goes:

You will need: PIL and numpy

Create a folder named `boxed` in here.

Then run `python imager.py <glob expression>`, wait a while.

In the boxed folder you have a rectangle around the walker in the
images and if you run `gnuplot plotter.gplt` you will get a png of the
bbox width. You may want to remove the bg.png to rerun everything from
scratch and get the real times. I took the bare basic precautions to
be fast but you can do better. Threads proved to be doing more bad
than good.
