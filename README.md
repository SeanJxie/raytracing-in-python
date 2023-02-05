# raytracing-in-python

A raytracer I implemented based on Peter Shirley's wonderful [raytracing book series](https://raytracing.github.io/).
As it's implemented in Python and not in C++ as intended, the structure of the code may slightly deviate from that taught in the books. Furthermore, extra features will be added as I decide to expand the project to a useable raytracing software.

Why's it written in Python and not in C++ as indended? Python is simple and readable. I wanted to focus on the raytracing more than the coding.

There are several optimizations that have been made to combat the slowness of Python:
- I recommend running the raytracer with [PyPy](https://www.pypy.org/) (which is a Python implementation that comes with a [JIT compiler](https://en.wikipedia.org/wiki/Just-in-time_compilation), among other useful features).

- On top of PyPy, the renderer uses Python's `multiprocessing` package which allows the computational workload to be split over multiple processes.

With those two improvements, the render time is orders of magnitude faster. For example, the image below takes about *a day* to render with regular CPython and no multiprocessing, but only about *3 minutes* with PyPy and multiprocessing.

![demo](https://github.com/SeanJxie/raytracing-in-python/blob/main/out.png)

# Setup
To get started, install and setup [PyPy](https://www.pypy.org/) and get it working with `pip`. [Here](https://www.activestate.com/resources/quick-reads/how-to-install-and-work-with-pypy/)'s a quick walkthrough.

The raytracer only uses two external libraries (which are both used on the same line of code):
- `Pillow` - for saving rendered images to memory.
- `numpy` - for converting data used internally to data compatible with `Pillow`.

The rest of the project uses the Python Standard Library only.

Install both the packages with
```
pypy -m pip install Pillow
pypy -m pip install numpy
```

Next, clone this repo with
```
git clone https://github.com/SeanJxie/raytracing-in-python
```
and move into it with
```
cd raytracing-in-python
```

Now, you should be ready to use the raytracer!


