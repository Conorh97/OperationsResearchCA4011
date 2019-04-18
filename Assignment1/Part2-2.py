import sys
import random
import argparse
import numpy as np
from scipy.stats import sem
from Part2Classes import ServiceTime, Client, Server

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--start', type=str, default="09:00")
	parser.add_argument('--end', type=str, default="17:30")
	parser.add_argument('--random', type=int, default=0)
	parser.add_argument('--scheduled', type=int, default=0)
	parser.add_argument('--servers', type=int, default=1)
	parser.add_argument('--mu', type=int, default=6)
	args = parser.parse_args()

	start_time = ServiceTime(args.start)
	end_time = ServiceTime(args.end)

	service_minutes = end_time.to_minutes() - start_time.to_minutes()
	mu = 60 // args.mu

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

	q = []
	q_count = []
	finished_clients = []
	server_list = [Server(serving_gender='M'), Server(serving_gender='F')] 

	for i in range(service_minutes):
		for server in server_list:
			if server.is_serving and server.current_client.get_estimated_end() == i:
				server.is_serving = False
				server.current_client.time_left = i
				finished_clients.append(server.current_client)
				server.current_client = None
			if not server.is_serving and len(q) > 0 and q[-1].gender == server.serving_gender:
				q_client = q.pop()
				q_client.set_queue_time(i)
				server.current_client = q_client
				server.is_serving = True
			if not server.is_serving and len(q) == 0 and len(finished_clients) > 0:
				server.time_idle += 1
		if i in intervals:
			gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
			assigned_to_server = False
			for server in server_list:
				if not server.is_serving and not assigned_to_server and gender == server.serving_gender:
					client = Client(i, mu, 0, gender=gender)
					server.current_client = client
					server.is_serving = True
					assigned_to_server = True
			if not assigned_to_server:
				client = Client(i, mu, gender=gender)
				q.insert(0, client)
		q_count.append(len(q))

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
	print("Average number of clients in the system: {:.2f} (Standard Error: {:.2f})".format(average_clients_in_q, average_clients_in_q_error))


if __name__ == "__main__":
	main()
