import argparse
import random
import numpy as np
import queue as Q
from scipy.stats import sem
from Part2Classes import ServiceTime, Client, Server, LunchBreak


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=str, default='10:00')
	parser.add_argument('--end', type=str, default='17:00')
	parser.add_argument('--peak_start', type=str, default='12:00')
	parser.add_argument('--peak_end', type=str, default='13:45')
	parser.add_argument('--service_time', type=int, default=20)
	parser.add_argument('--deviation', type=int, default=5)
	parser.add_argument('--stream', type=int, default=6)
	parser.add_argument('--peak_stream', type=int, default=12)
	parser.add_argument('--barbers', type=int, default=3)
	parser.add_argument('--breaks', type=str, nargs='+')
	parser.add_argument('--chairs', type=int, default=3)
	parser.add_argument('--probabilities', type=float, nargs='+')
	parser.add_argument('--replications', type=int, default=100)
	args = parser.parse_args()

	assert args.barbers == len(args.breaks)
	assert args.chairs == len(args.probabilities)

	start_time = ServiceTime(args.start)
	end_time = ServiceTime(args.end)
	peak_start = ServiceTime(args.peak_start)
	peak_end = ServiceTime(args.peak_end)

	service_minutes = end_time.to_minutes() - start_time.to_minutes()
	
	proportion_of_customers_who_left = []

	for x in range(args.replications): 
		customers_arrived = 0
		left_without_haircut = 0

		barbers = []
		for i in range(args.barbers):
			break_values = args.breaks[i].split("/")
			start = ServiceTime(break_values[0])
			end = ServiceTime(break_values[1])
			start_minutes = start.to_minutes() - start_time.to_minutes()
			end_minutes = end.to_minutes() - start_time.to_minutes()

			lunch_break = LunchBreak(start_minutes, end_minutes - start_minutes)
			barber = Server(lunch_break)
			barbers.append(barber)

		arrivals = []
		last_time = 0
		lmbda = args.stream / 60
		while last_time < peak_start.to_minutes() - start_time.to_minutes():
			last_time += int(random.expovariate(lmbda))
			if last_time < peak_start.to_minutes() - start_time.to_minutes():
				arrivals.append(last_time)

		lmbda = args.peak_stream / 60
		while last_time < peak_end.to_minutes() - start_time.to_minutes():
			last_time += int(random.expovariate(lmbda))
			if last_time < peak_end.to_minutes() - start_time.to_minutes():
				arrivals.append(last_time) 

		lmbda = args.stream / 60
		while last_time < end_time.to_minutes() - start_time.to_minutes():
			last_time += int(random.expovariate(lmbda))
			if last_time < end_time.to_minutes() - start_time.to_minutes():
				arrivals.append(last_time)

		arrivals.sort()

		q = []

		for i in range(service_minutes):
			for j, barber in enumerate(barbers):
				if barber.is_serving and barber.current_client.get_estimated_end() == i:
					barber.is_serving = False
					barber.current_client = None
		#			print('Barber number {} finishes haircut at: {}'.format(j, i))
				if not barber.is_serving and not barber.lunch_break.is_finished and barber.lunch_break.taken_at == 0 and barber.lunch_break.start <= i:
					barber.lunch_break.taken_at = i
					barber.on_lunch = True
		#			print('Barber number {} takes lunch at: {}'.format(j, i))
				if not barber.lunch_break.is_finished and barber.lunch_break.is_over(i):
					barber.lunch_break.is_finished = True
					barber.on_lunch = False
		#			print('Barber number {} finishes lunch at: {}'.format(j, i))
				if not barber.is_serving and not barber.on_lunch and len(q) != 0:
					q_client = q.pop()
					q_client.set_queue_time(i)
					barber.current_client = q_client
					barber.is_serving = True
		#			print("Customer goes to barber number {} at: {}".format(j, i))
			for k in range(args.chairs):
				if len(q) > k: 
					if i - q[k].time_entered >= 15:
						leave_choice = np.random.choice([True, False], p=[0.5, 0.5])
					else:
						chair_prob = args.probabilities[k]
						leave_choice = np.random.choice([True, False], p=[chair_prob, 1 - chair_prob])
					if leave_choice:
						q[k].time_entered = False
						left_without_haircut += 1
		#				print('Customer leaving barber shop without haircut at: {}'.format(i))
			q = [client for client in q if client.time_entered != False]
			if i in arrivals:
				assigned_to_barber = False
				for m, barber in enumerate(barbers):
					if not barber.is_serving and not barber.on_lunch and not assigned_to_barber:
						deviated_service_time = random.choice(range(args.service_time - args.deviation, args.service_time + args.deviation + 1))
						client = Client(i, deviated_service_time, 0)
						barber.current_client = client
						barber.is_serving = True
						assigned_to_barber = True
						customers_arrived += 1
		#				print("New customer goes to barber number {} at: {}".format(m, i))
				if not assigned_to_barber and len(q) <= args.chairs:
					deviated_service_time = random.choice(range(args.service_time - args.deviation, args.service_time + args.deviation + 1))
					client = Client(i, deviated_service_time)
					q.insert(0, client)
					customers_arrived += 1
		#			print("Customer joins the queue at: {}".format(i))

		proportion_of_customers_who_left.append(left_without_haircut / customers_arrived)
		print('Amount of customers who left without service: {} ({:.2f}%)'.format(left_without_haircut, left_without_haircut * 100 / customers_arrived))

	print('Average proportion of customers who left without service: {:.2f}%'.format(sum(proportion_of_customers_who_left) * 100 / len(proportion_of_customers_who_left)))
	if args.replications > 1:
		print('Standard error of proportion: {}'.format(sem(proportion_of_customers_who_left)))

if __name__ == "__main__":
	main()