def clamp(x: float, min: float, max: float):
    if x < min:
        return min
    if x > max:
        return max
    return x