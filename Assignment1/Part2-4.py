import sys
import random
import argparse
import numpy as np
import queue as Q
import matplotlib.pyplot as pl
from scipy.stats import sem, norm
from Part2Classes import ServiceTime, Client, Server, LunchBreak

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=str, default="09:00")
	parser.add_argument('--end', type=str, default="17:30")
	parser.add_argument('--random', type=int, default=0)
	parser.add_argument('--scheduled', type=int, default=0)
	parser.add_argument('--servers', type=int, default=1)
	parser.add_argument('--priority', action="store_true")
	parser.add_argument('--breaks', type=str, nargs='+') # In format start_time/end_time/break_length
	parser.add_argument('--appointment_times', type=int, nargs='+')
	parser.add_argument('--new_proportion', type=int, default=6) # Proportion of new patients
	args = parser.parse_args()

	assert args.servers == len(args.breaks)
	assert len(args.appointment_times) == 2

	start_time = ServiceTime(args.start)
	end_time = ServiceTime(args.end)

	service_minutes = end_time.to_minutes() - start_time.to_minutes()

	if args.random != 0:
		intervals = []
		last_time = 0
		lmbda = args.random / 60
		while last_time < service_minutes:
			last_time += int(random.expovariate(lmbda))
			if last_time < service_minutes:
				intervals.append(last_time)
	elif args.scheduled != 0:
		scheduled_intervals = [i for i in range(5, service_minutes, args.scheduled)]
		std_dev = np.std(np.array([scheduled_intervals[0], scheduled_intervals[1]]))
		intervals = []
		for time in scheduled_intervals:
			lower_bound = int(0 if std_dev > time else time - std_dev)
			upper_bound = int(time + std_dev + 1)
			intervals.append(random.choice(range(lower_bound, upper_bound)))
	else:
		print("Please pass either '--random' or '--scheduled' parameter")

	if args.priority:
		q = Q.PriorityQueue()
	else:
		q = Q.Queue()

	q_count = []
	finished_clients = []
	server_list = [] 

	for i in range(args.servers):
		break_values = args.breaks[i].split("/")
		break_one_time = ServiceTime(break_values[0])
		break_two_time = ServiceTime(break_values[1])

		break_one_minutes = break_one_time.to_minutes() - start_time.to_minutes()
		break_two_minutes = break_two_time.to_minutes() - start_time.to_minutes()

		break_one = LunchBreak(break_one_minutes, int(break_values[2]))
		break_two = LunchBreak(break_two_minutes, int(break_values[2]))

		server = Server([break_one, break_two])
		server_list.append(server)

	n = 1
	for i in range(service_minutes):
		for server in server_list:
			#Case for when a server is finished with a client
			if server.is_serving and server.current_client.get_estimated_end() == i:
				server.is_serving = False
				server.current_client.time_left = i
				finished_clients.append(server.current_client)
				server.current_client = None
			for j in range(len(server.lunch_break)):
				#Case for when a server is going on break
				if not server.is_serving and not server.lunch_break[j].is_finished and server.lunch_break[j].taken_at == 0 and server.lunch_break[j].start <= i:
					#print("Lunch taken at: {}".format(i))
					server.lunch_break[j].taken_at = i
					server.on_lunch = True
				#Case for when a server is finished their break
				if not server.lunch_break[j].is_finished and server.lunch_break[j].is_over(i):
					server.lunch_break[j].is_finished = True
					server.on_lunch = False
			#Case for when a server is able to take a client
			if not server.is_serving and not q.empty():
				q_client = q.get()
				q_client.set_queue_time(i)
				server.current_client = q_client
				server.is_serving = True
			#Case for when a server is idle
			if not server.is_serving and q.empty() and len(finished_clients) > 0:
				server.time_idle += 1
		if i in intervals:
			assigned_to_server = False
			for server in server_list:
				#Check if server is free when a new client arrives
				if not server.is_serving and not server.on_lunch and not assigned_to_server:
					if n % args.new_proportion:
						client = Client(i, args.appointment_times[0], 0)
					else:
						client = Client(i, args.appointment_times[1], 0)
					server.current_client = client
					server.is_serving = True
					assigned_to_server = True
				n += 1
			if not assigned_to_server:
				if n % args.new_proportion:
					client = Client(i, args.appointment_times[0])
				else:
					client = Client(i, args.appointment_times[1])
				q.put(client)
				n += 1
		q_count.append(q.qsize())

	finished_clients = sorted(finished_clients, key = lambda x: x.time_entered)

	for client in finished_clients:
		print(client)

	average_system_time = sum([x.time_in_system() for x in finished_clients]) / len(finished_clients)
	average_system_time_error = sem([x.time_in_system() for x in finished_clients])

	average_queue_time = sum([x.time_in_queue for x in finished_clients]) / len(finished_clients)
	average_queue_time_error = (sem([x.time_in_queue for x in finished_clients]))

	max_system_time = max([x.time_in_system() for x in finished_clients])
	max_system_time_error = sem([x.time_in_system() for x in finished_clients])

	max_queue_time = max([x.time_in_queue for x in finished_clients])
	max_queue_time_error = sem([x.time_in_queue for x in finished_clients])

	idle_list = [server.time_idle * 100 / len(q_count) for server in server_list]

	average_clients_in_q = sum(q_count) / len(q_count)
	average_clients_in_q_error = sem(q_count)
	
	print("Average time for a client in the system: {:.2f} (Standard Error: {:.2f})".format(average_system_time, average_system_time_error))
	print("Average time for a client in the queue: {:.2f} (Standard Error: {:.2f})".format(average_queue_time, average_queue_time_error))
	print("Max time for a client in the system: {} (Standard Error: {:.2f})".format(max_system_time, max_system_time_error))
	print("Max time for a client in the queue: {} (Standard Error: {:.2f})".format(max_queue_time, max_queue_time_error))
	for i, idle_ratio in enumerate(idle_list):
		print("Proportion of time server {} is idle: {:.2f}%".format(i, idle_ratio))
	print("Average number of clients in the queue: {:.2f} (Standard Error: {:.2f})".format(average_clients_in_q, average_clients_in_q_error))

	h = sorted([x.time_in_queue for x in finished_clients])
	fit = norm.pdf(h, np.mean(h), np.std(h))
	pl.plot(h,fit,'-o')
	pl.hist(h,normed=True)
	if args.priority:
		pl.title('Regular Client Priority Times')
	else:
		pl.title('Varied Service Times')
	pl.xlabel('Time')
	pl.ylabel('Clients')
	pl.show()

if __name__ == "__main__":
	main()
