# program used for playing sounds
player = '/usr/bin/mplayer'

sound_dir = "/srv/data/bell/sounds"
mixer_prog = '/sbin/mixer'
# after bell is finished executing sound is turned down to value
# indicated by mixer_low before starting again, it's turned up to
# mixer_high 
mixer_low = '0% mute'
mixer_high = '100% unmute'
mixer_medium = '60% unmute'

# sound clip definitions
# 'mixer' key tells what mixer settings are set right _before_ playing the given file
# if 'mixer' key is not present then mixer_high is used
sounds = {
	'beginning1': {'file': 'KDE-Im-Low-Priority-Message.ogg', 'mixer_high': mixer_high},
	'beginning2': {'file': 'KDE-Im-Sms.ogg', 'mixer_high': mixer_high},
	'ending1': {'file': 'KDE-Sys-Log-In-Long.ogg', 'mixer_high': mixer_high},
	'background': {'file': 'Oxygen-Im-Phone-Ring.ogg', 'mixer_high': mixer_medium},
}


# define schedules for different day types
default_day = (
	{'start': '07:59:00', 'sound': 'beginning1'},
	{'start': '08:00:00', 'sound': 'beginning2'},
	{'start': '08:45:00', 'sound': 'ending1'},
	{'start': '08:54:00', 'sound': 'beginning1'},
	{'start': '08:55:00', 'sound': 'beginning2'},
	{'start': '09:40:00', 'sound': 'ending1'},
	{'start': '09:59:00', 'sound': 'beginning1'},
	{'start': '10:00:00', 'sound': 'beginning2'},
	{'start': '10:45:00', 'sound': 'ending1'},
	{'start': '10:59:00', 'sound': 'beginning1'},
	{'start': '11:00:00', 'sound': 'beginning2'},
	{'start': '11:45:00', 'sound': 'ending1'},
	{'start': '11:59:00', 'sound': 'beginning1'},
	{'start': '12:00:00', 'sound': 'beginning2'},
	{'start': '12:45:00', 'sound': 'ending1'},
	{'start': '12:59:00', 'sound': 'beginning1'},
	{'start': '13:00:00', 'sound': 'beginning2'},
	{'start': '13:45:00', 'sound': 'ending1'},
	{'start': '13:59:00', 'sound': 'beginning1'},
	{'start': '14:00:00', 'sound': 'beginning2'},
	{'start': '14:45:00', 'sound': 'ending1'},
	{'start': '14:59:00', 'sound': 'beginning1'},
	{'start': '15:00:00', 'sound': 'beginning2'},
	{'start': '15:45:00', 'sound': 'ending1'},
	{'start': '15:54:00', 'sound': 'beginning1'},
	{'start': '15:55:00', 'sound': 'beginning2'},
	{'start': '16:40:00', 'sound': 'ending1'},
	{'start': '16:49:00', 'sound': 'beginning1'},
	{'start': '16:50:00', 'sound': 'beginning2'},
	{'start': '17:35:00', 'sound': 'ending1'},
)

test_day = (
    {'start': '18:17:00', 'sound': 'beginning1'},
    {'start': '18:18:00', 'sound': 'ending1'},
    {'start': '18:39:00', 'sound': 'beginning2'},	
)

short_day = (
    {'start': '08:00:00', 'sound': 'beginning2'},
    {'start': '08:45:00', 'sound': 'ending1'},
)

long_day = (
    {'start': '08:00:00', 'sound': 'beginning1'},
    {'start': '08:45:00', 'sound': 'ending1'},
)

empty_day = ()


# days dict defines the most generic bell schedule which is used if there are not
# overrides from datemap or no_bell
days = {
	'Monday': default_day,
	'Tuesday': default_day,
	'Wednesday': default_day,
	'Thursday': default_day,
	'Friday': default_day,
	'Saturday': empty_day,
	'Sunday': empty_day,
}


# datemap can be used to specify override schedule for specific dates (i.e. days before certain holidays)
datemap = {
	'2004.7.24' : short_day,
	'2004.6.24' : long_day,
}

# date ranges where no bell is rung no matter what the other rules say.
# Useful for defining school holidays
# format is:
# ((year, month, day, hour, minute, sec),(year, month, day, hour, minute, sec))
# where the first tuple defines beginning of the range and the second defines end
no_bell = (
	((2003, 8, 26), (2003, 8, 27)),
	((2003, 9, 23), (2003, 9, 28)),
	((2003, 9, 23), (2003, 9, 28)),
)
