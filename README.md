# raytracing-in-python

<p align="center">
  <img src="https://github.com/SeanJxie/raytracing-in-python/blob/main/images/glass_cornell.png" />
</p>

<p align="center">
  <img src="https://github.com/SeanJxie/raytracing-in-python/blob/main/images/artwork.png" />
</p>

A raytracer I implemented based on Peter Shirley's wonderful [raytracing book series](https://raytracing.github.io/).
As it's implemented in Python and not in C++ as intended, the structure of the code may slightly deviate from that taught in the books. Furthermore, extra features will be added as I decide to expand the project to a useable raytracing software.

Why's it written in Python and not in C++ as indended? Python is simple and readable. I wanted to focus on the raytracing more than the coding.

There are several optimizations that have been made to combat the slowness of Python:
- I recommend running the raytracer with [PyPy](https://www.pypy.org/) (which is a Python implementation that uses a [JIT compiler](https://en.wikipedia.org/wiki/Just-in-time_compilation)).

- On top of PyPy, the renderer uses Python's `multiprocessing` package which allows the computational workload to be split over multiple processes.

With those two improvements, the render time is orders of magnitude faster. For example, the image below takes about *a day* to render with regular CPython and no multiprocessing, but only about *3 minutes* with PyPy and multiprocessing.

![p2](https://github.com/SeanJxie/raytracing-in-python/blob/main/images/better.png)

# Setup
To get started, install and setup [PyPy](https://www.pypy.org/) and get it working with `pip`. [Here](https://www.activestate.com/resources/quick-reads/how-to-install-and-work-with-pypy/)'s a quick walkthrough.

The raytracer only uses two external libraries:
- `Pillow` - for saving rendered images to memory and loading image textures.
- `numpy` - for converting data used internally to data compatible with `Pillow`.

The rest of the project uses the Python Standard Library.

Install both of the packages with
```
pypy -m pip install Pillow
pypy -m pip install numpy
```

Next, clone this repo with
```
git clone https://github.com/SeanJxie/raytracing-in-python
```
and move into the cloned directory with
```
cd raytracing-in-python
```

Now, you should be ready to use the raytracer!

# Using the raytracer
There isn't really any type of user interface setup at the moment. Running
```
pypy ./main.py
```
will render the second image from the top of this README. Beware, though. It took a hefty 13 hours and 18 minutes to render on a typical quad-core laptop.

If you want to play around with it, there are a few presets you can find in `scene_presets.py`. 
In `main.py`, simply replace the call to `artwork()` with any of the presets to change the scene. There are some image options in `main.py` as well, so changes can be made as desired.

