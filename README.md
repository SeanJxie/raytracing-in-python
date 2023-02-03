# raytracing-in-python

A raytracer I implemented following [_Ray Tracing in One Weekend_](https://raytracing.github.io/books/RayTracingInOneWeekend.html) by Peter Shirley.
Extra features will be added as I decide to expand the project to a somewhat useable raytracing software.

Why's it written in Python and not in C++ as indended? Python is simple and readable. I wanted to focus on the raytracing more than the coding.

Is it slow? By itself, yes. Very, very, very unbearably slow. I paid the appropriate price.

There are some solutions to the slowness, though.
- I recommend running the raytracer with [PyPy](https://www.pypy.org/) (which is a Python implementation that comes with a [JIT compiler](https://en.wikipedia.org/wiki/Just-in-time_compilation), among other useful features).

- On top of PyPy, the renderer uses Python's `multiprocessing` package which allows the computational workload to be split over multiple processes.

With those two improvements, the render time is orders of magnitude faster. For example, the image below takes about *a day* to render with regular CPython and no multiprocessing, but only about *3 minutes* with PyPy and multiprocessing.

![demo](https://github.com/SeanJxie/raytracing-in-python/blob/main/out.png)

# How to run
To get started, install and setup [PyPy](https://www.pypy.org/) and get it working with `pip`. [Here](https://www.activestate.com/resources/quick-reads/how-to-install-and-work-with-pypy/)' a quick walkthrough.

The raytracer only uses two external libraries (which are both used on the same line of code):
- `Pillow` - for saving rendered images to memory.
- `numpy` - for converting data used internally to data compatible with `Pillow`.

The rest of the project uses the Python Standard Library only.

Install both the packages with
```
pypy -m pip install Pillow
```
and
```
pypy -m pip install numpy
```

Next, clone this repo with
```
git clone https://github.com/SeanJxie/raytracing-in-python
```
and
```
cd raytracing-in-python
```

To run the raytracer, simply
```
pypy .\main.py
```
