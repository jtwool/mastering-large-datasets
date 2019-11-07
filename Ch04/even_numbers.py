def even_numbers(n):
    i = 1
    while i <= n:
        yield i*2
        i += 1

first_100_even = (i*2 for i in range(1,101))
