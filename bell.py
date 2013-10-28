#!/usr/bin/env python3

"""Rather simplistic application for managing schoolbell
usage:
	just edit config.py to match your need and 
then start application with:
python bell.py
you can edit conf.py while it's running and force reload
with SIGHUP

Sven Petai <hadara a t bsd.ee> Tue Aug 24 14:40:21 EEST 2004
"""

import os
import sys
import time 
import sched
import signal
import logging
import datetime

CONFIG_FILENAME = "conf.py"

schedule = sched.scheduler(time.time, time.sleep)

today = ()

def str_to_tuple(timestr):
    a = time.localtime()
    return a[:3] + tuple(map(int, timestr.split(':'))) + (0, 0, -1)

def is_no_bell_day():
    """checks if no_bell map doesn't prohibit bells today"""
    today = time.localtime()[:3]
    for r in no_bell:
        if today >= r[0] and today <= r[1]:
            return True
    return False

def tuple_to_str(timetuple):
    return '-'.join(map(lambda a: '%02d' % a, timetuple))

def run_event(event):
    logging.info('event:'+str(event))
    start_bell(sounds[event['sound']])

def schedule_day(events):
    logging.info('scheduling day. events:'+str(events))

    if not is_no_bell_day():
        for event in events:
            starting = str_to_tuple(event['start'])
            # dont schedule events that are in the past
            if starting < time.localtime():
                continue	
            schedule.enterabs(time.mktime(starting), 1, run_event, (event,))
            logging.info('scheduled event:'+str(event))
    else:
        logging.info('no bell day!')

    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()
    # scedule reload event for 00:10 to reload bell schedule for the next day
    schedule.enterabs(time.mktime(tomorrow[:3] + (0, 10, 0, 0, 0, -1)), 1, reschedule, ())

def reschedule():
    """schedule events for current day, this is usually called at the begginning of each new day
    to scedule events for that day only + one event for rescheduling next day"""
    if not schedule.empty():
        purge_events()  

    today_s = tuple_to_str(time.localtime()[:3])

    # first check if exception entry exist for today in datemap
    if datemap.has_key(today_s):
    	schedule_day(datemap[today_s])
    else:
        # otherwise schedule it as normal weekday
        schedule_day(days[time.strftime("%A")])	
    
def start_bell(sound):
    os.system("killall %s" % (mp3player))
    os.system("%s %s" % (mixer_prog, str(mixer_high)))
    os.system("%s %s/%s &&  %s %s &" % (mp3player, sound_dir, sound, mixer_prog, str(mixer_low)))

def purge_events():
    for event in schedule.queue:
        logging.info("removing event "+str(event))
        schedule.cancel(event)

def check_config(configd):
    """verify that things that should exist in the config indeed do exist and
    the referenced binaries are actually present
    """
    # XXX: verify first that the required config parameters are present
    if not os.path.exists(configd['player']):
        logging.error("player %s wasn't found" % (configd['player'],))
        return False
    if not os.path.isdir(configd['sound_dir']):
        logging.error("sound directory %s wasn't found" % (configd['sound_dir'],))
        return False
    return True

def reload_config(_='', notused=''):
    # FIXME: we shouldn't allow config to overwrite stuff in the global namespace
    exec(compile(open(CONFIG_FILENAME).read(), CONFIG_FILENAME, 'exec'), globals())
    if not check_config(globals()):
        logging.error("reading configuration failed. Exiting.")
        sys.exit(-1)
    reschedule()

tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).timetuple()
# scedule reload event for 00:10 to reload bell schedule for the next day
schedule.enterabs(time.mktime(tomorrow[:3] + (0, 10, 0, 0, 0, -1)), 1, reschedule, ())

if __name__ == '__main__':
    signal.signal(signal.SIGHUP, reload_config)
    reload_config()
    schedule.run()
