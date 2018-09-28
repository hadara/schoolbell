#!/usr/bin/env python3

"""
Sven Petai <hadara a t bsd.ee> Tue Aug 24 14:40:21 EEST 2004
"""

import os
import sys
import time 
import sched
import signal
import logging
import datetime

#if sys.version_info.major < 3:
#    print("python 3.X required")
#    sys.exit(-2)

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

def get_sound(sound_name):
    sound = sounds.get(sound_name)
    if sound is None:
        logging.error('sound %s not defined in config' % (sound_name,))
        return None
    if not isinstance(sound, dict) or 'file' not in sound:
        logging.error('sound definition should be a dict containing at least filename key. Is: %s' % (str(sound),))
        return None
    if 'mixer_high' not in sound:
        sound['mixer_high'] = mixer_high
    if 'mixer_low' not in sound:
        sound['mixer_low'] = mixer_low
    return sound

def run_event(event):
    logging.info('event:'+str(event))
    sound = get_sound(event['sound'])
    if sound is None:
        logging.error('event %s not run because sound definition is missing' % (str(event),))
        return
    start_bell(sound)

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
    if today_s in datemap:
    	schedule_day(datemap[today_s])
    else:
        # otherwise schedule it as normal weekday
        schedule_day(days[time.strftime("%A")])	
    
def start_bell(sound):
    # XXX: using system() directly is unsafe in general of course but in this case all of the parameters come from the
    # config file so it should be good enough
    os.system("killall %s" % (player))
    os.system("%s %s" % (mixer_prog, str(sound['mixer_high'])))
    os.system("%s %s/%s &&  %s %s &" % (player, sound_dir, sound['file'], mixer_prog, str(sound['mixer_low'])))

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
# schedule reload event for 00:10 to reload bell schedule for the next day
schedule.enterabs(time.mktime(tomorrow[:3] + (0, 10, 0, 0, 0, -1)), 1, reschedule, ())

if __name__ == '__main__':
    signal.signal(signal.SIGHUP, reload_config)
    reload_config()
    schedule.run()
