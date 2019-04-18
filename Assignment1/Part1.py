import numpy as np
import random

def multiplative_congruential(b, c, u, m):
	random_nums = []
	for i in range(1000):
		u = (b * u + c) % m
		random_nums.append(u)
	return random_nums

def uniform(upper_bound, n):
	return [round(random.uniform(0, upper_bound - 1)) for i in range(n)]

def chisquare(upper_bound, a):
	total = 0
	for i in range(upper_bound):
		total += (a.count(i) - (len(a) / upper_bound)) ** 2
	result = (upper_bound / len(a)) * total
	print(result)

	interval = 2 * (upper_bound ** 0.5)
	return result <= upper_bound + interval and result >= upper_bound - interval

def main():
	observed_mult = multiplative_congruential(21, 7, 4, 50)
	print(observed_mult)
	print(chisquare(50, observed_mult))

	observed_uniform = uniform(50, 1000)
	print(observed_uniform)
	print(chisquare(50, observed_uniform)) 

if __name__ == "__main__":
	main()
