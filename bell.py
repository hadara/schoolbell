#!/usr/local/bin/python

"""Rather simplistic application for managing schoolbell
usage:
	just edit config.py to match your need and 
then start application with:
python bell.py
you can edit conf.py while it's running and force reload
with SIGHUP

Sven Petai <hadara a t bsd.ee> Tue Aug 24 14:40:21 EEST 2004
"""


from time import time,sleep,localtime,struct_time,mktime
from datetime import datetime, timedelta
from time import strftime
import os
import signal
import sched

schedule = sched.scheduler(time, sleep)

today = ()

def reload_config(_='', notused=''):
	execfile('conf.py', globals())
	reschedule()

def str_to_tuple(timestr):
	a = localtime()
	return a[:3] + tuple(map(int, timestr.split(':'))) + (0, 0, -1)

def is_no_bell_day():
	"""checks if no_bell map doesn't prohibit bells today"""
	today = localtime()[:3]
	for r in no_bell:
		if today >= r[0] and today <= r[1]:
			return True
	return False

def tuple_to_str(timetuple):
	return '-'.join(map(lambda a: '%02d' % a, timetuple))

def run_event(event):
	print event
	start_bell(sounds[event['sound']])

def schedule_day(events):
	i = 0
	print events
	today = events
	print today
	if not is_no_bell_day():
		for event in events:
			starting = str_to_tuple(event['start'])
			# dont schedule events that are in the past
			if starting < localtime():
				i += 1
				continue	
			schedule.enterabs(mktime(starting), 1, run_event, (event,))
			print "scheduler event "+str(event)
			i += 1
	else:
		print "NO BELL DAY!"
	tomorrow = (datetime.now() + timedelta(days=1)).timetuple()
	# scedule reload event for 00:10 to reaload bells for next day
	schedule.enterabs(mktime(tomorrow[:3] + (0, 10, 0, 0, 0, -1)), 1, reschedule, ())

def reschedule():
	"""schedule events for current day, this is usually called at the begginning of each new day
	to scedule events for that day only + one event for rescheduling next day"""
	if not schedule.empty():
        	purge_events()  
	today_s = tuple_to_str(localtime()[:3])
	# first check if exception entry exist for today in datemap
	if datemap.has_key(today_s):
		schedule_day(datemap[today_s])
	# otherwise schedule it as normal weekday
	else:
		schedule_day(days[strftime("%A")])	

def start_bell(sound):
	os.system("killall %s" % (mp3player))
	os.system("%s %s" % (mixer_prog, str(mixer_high)))
	os.system("%s %s/%s &&  %s %s &" % (mp3player, sound_dir, sound, mixer_prog, str(mixer_low)))

def purge_events():
	for event in schedule.queue:
		print "removing event "+str(event)
		schedule.cancel(event)

if __name__ == '__main__':
	signal.signal(signal.SIGHUP, reload_config)
	reload_config()
	schedule.run()
