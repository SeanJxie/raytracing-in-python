# raytracing-in-python

A raytracer I implemented following [_Ray Tracing in One Weekend_](https://raytracing.github.io/books/RayTracingInOneWeekend.html) by Peter Shirley.
Extra features will be added as I decide to expand the project to a somewhat useable raytracing software.

Why's it written in Python and not in C++ as indended? I like Python. I didn't want to get caught up in memory management bugs for hours.

Is it slow? Yes. Very, very, very unbearably slow. I paid the appropriate price.

I recommend running the raytracer with [PyPy](https://www.pypy.org/), which I've measured to be many orders of magnitude faster than running with CPython.

---

The image below takes about *a day* to render with what is taught in the tutorial (clearly, it was made to be written in C++). However, with PyPy and multiprocessing, the time is reduced to about *35 seconds*. 

![demo](https://github.com/SeanJxie/raytracing-in-python/blob/main/out.png)
