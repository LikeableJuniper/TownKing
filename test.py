import timeit

print(timeit.timeit(
"""a = 0
for i in range(1000):
    if i < a:
        pass
"""
))