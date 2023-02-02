# raytracing-in-python

![demo](https://github.com/SeanJxie/raytracing-in-python/blob/main/scattered.png)

A raytracer I implemented following [_Ray Tracing in One Weekend_](https://raytracing.github.io/books/RayTracingInOneWeekend.html) by Peter Shirley.

Why's it written in Python and not in C++ as indended? I like Python. I didn't want to get caught up in memory management bugs for hours.

Is it slow? Yes. Very, very, very unbearably slow. I paid the appropriate price.

To remedy the slowness of this all, I recommend running the raytracer with [PyPy](https://www.pypy.org/), which is reportedly 4.8 times faster than CPython 3.7.

