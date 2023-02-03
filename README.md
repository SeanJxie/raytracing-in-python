# raytracing-in-python

A raytracer I implemented following [_Ray Tracing in One Weekend_](https://raytracing.github.io/books/RayTracingInOneWeekend.html) by Peter Shirley.
Extra features will be added as I decide to expand the project to a somewhat useable raytracing software.

Why's it written in Python and not in C++ as indended? It's simple and readable. I wanted to focus on the raytracing more than the coding.

Is it slow? Yes. Very, very, very unbearably slow. I paid the appropriate price.

There are some solutions to the slowness, though.
- I recommend running the raytracer with [PyPy](https://www.pypy.org/) (which is a Python implementation that comes with a [JIT compiler](https://en.wikipedia.org/wiki/Just-in-time_compilation), among other useful features).

- On top of PyPy, the renderer uses Python's `multiprocessing` package which allows the computational workload to be split over multiple processes.

With those two improvements, the render time is orders of magnitude faster. For example, the image below takes about *a day* to render with what is taught in the tutorial (clearly, it was made to be written in C++). However, with PyPy and multiprocessing, the time is reduced to about *35 seconds*. 

![demo](https://github.com/SeanJxie/raytracing-in-python/blob/main/out.png)
