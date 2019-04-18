class Client(object):

	def __init__(self, time_entered, estimated_time=None, time_in_queue=None, time_left=None, gender=None):
		self.time_entered = time_entered
		self.estimated_time = estimated_time
		self.time_in_queue = time_in_queue
		self.time_left = time_left
		self.gender = gender

	def time_in_system(self):
		return self.time_left - self.time_entered

	def set_queue_time(self, current_time):
		self.time_in_queue = current_time - self.time_entered

	def get_estimated_end(self):
		return self.time_entered + self.time_in_queue + self.estimated_time

	def __str__(self):
		return "Time Entered: {}\nTime In Queue: {}\nTime Exited: {}\n".format(self.time_entered, self.time_in_queue, self.time_left)

	def __eq__(self, other):
		return self.estimated_time == other.estimated_time

	def __gt__(self, other):
		return self.estimated_time > other.estimated_time

	def __ge__(self, other):
		return self.estimated_time >= other.estimated_time

	def __lt__(self, other):
		return self.estimated_time < other.estimated_time

	def __le__(self, other):
		return self.estimated_time <= other.estimated_time


class Server(object):

	def __init__(self, lunch_break=None, completion_rate=1.0, serving_gender=None):
		self.lunch_break = lunch_break
		self.completion_rate = completion_rate
		self.serving_gender = serving_gender
		self.on_lunch = False
		self.is_serving = False
		self.time_idle = 0
		self.current_client = None


class ServiceTime(object):

	def __init__(self, time):
		self.hours = int(time.split(":")[0])
		self.minutes = int(time.split(":")[1])

	def to_minutes(self):
		return (self.hours * 60) + self.minutes


class LunchBreak(object):

	def __init__(self, start, length):
		self.start = start
		self.length = length
		self.taken_at = 0
		self.is_finished = False

	def is_over(self, current_time):
		return self.taken_at + self.length == current_time and self.taken_at != 0
