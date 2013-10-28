# dont use full path here
mp3player = 'mpg123'

sound_dir = "/root/bell"
mixer_prog = '/sbin/mixer'
# after bell is finished executing sound is turned down to value
# indicated by mixer_low before starting again, it's turned up to
# mixer_high 
mixer_low = '5'
mixer_high = '90'

# helide definitsioonid
sounds = {
	'sisse1': 'tell_overture.mp3',
	'sisse2': 'tell_overture.mp3',
	'v2lja': 'beethoven_5_finale.mp3',	
}


# siin defineeri erinevate p2evade tyype niipalju kui kulub
default_day = (
	{'start': '07:59:00', 'sound': 'sisse1'},
	{'start': '08:00:00', 'sound': 'sisse2'},
	{'start': '08:45:00', 'sound': 'v2lja'},
	{'start': '08:54:00', 'sound': 'sisse1'},
	{'start': '08:55:00', 'sound': 'sisse2'},
	{'start': '09:40:00', 'sound': 'v2lja'},
	{'start': '09:59:00', 'sound': 'sisse1'},
	{'start': '10:00:00', 'sound': 'sisse2'},
	{'start': '10:45:00', 'sound': 'v2lja'},
	{'start': '10:59:00', 'sound': 'sisse1'},
	{'start': '11:00:00', 'sound': 'sisse2'},
	{'start': '11:45:00', 'sound': 'v2lja'},
	{'start': '11:59:00', 'sound': 'sisse1'},
	{'start': '12:00:00', 'sound': 'sisse2'},
	{'start': '12:45:00', 'sound': 'v2lja'},
	{'start': '12:59:00', 'sound': 'sisse1'},
	{'start': '13:00:00', 'sound': 'sisse2'},
	{'start': '13:45:00', 'sound': 'v2lja'},
	{'start': '13:59:00', 'sound': 'sisse1'},
	{'start': '14:00:00', 'sound': 'sisse2'},
	{'start': '14:45:00', 'sound': 'v2lja'},
	{'start': '14:59:00', 'sound': 'sisse1'},
	{'start': '15:00:00', 'sound': 'sisse2'},
	{'start': '15:45:00', 'sound': 'v2lja'},
	{'start': '15:54:00', 'sound': 'sisse1'},
	{'start': '15:55:00', 'sound': 'sisse2'},
	{'start': '16:40:00', 'sound': 'v2lja'},
	{'start': '16:49:00', 'sound': 'sisse1'},
	{'start': '16:50:00', 'sound': 'sisse2'},
	{'start': '17:35:00', 'sound': 'v2lja'},
)

test_day = (
	{'start': '18:17:00', 'sound': 'sisse1'},
        {'start': '18:18:00', 'sound': 'v2lja'},
	{'start': '18:39:00', 'sound': 'sisse2'},	
)

short_day = (
	{'start': '08:00:00', 'sound': 'normal'},
	{'start': '08:45:00', 'sound': 'fucked'},
)

long_day = (
        {'start': '08:00:00', 'sound': 'normal'},
        {'start': '08:45:00', 'sound': 'fucked'},
)

empty_day = ()


# see on k8ige yldisem kellalaskmise graafik mille alusel lastakse siis kui datemap v8i
# no_bell mingeid erandeid ei kehtesta
days = {
	'Monday': default_day,
	'Tuesday': default_day,
	'Wednesday': default_day,
	'Thursday': default_day,
	'Friday': default_day,
	'Saturday': empty_day,
	'Sunday': empty_day,
}


# sisaldab erilisi p2evi ja overrideib days mapi poolt antud graafiku
datemap = {
	'2004.7.24' : short_day,
	'2004.6.24' : long_day,
}

# ajad kus kella ei lasta, olenemata sellest mida ytleb days conf v8i date conf
# vahemikud kujul:
# ((year, month, day, hour, minute, sec),(year, month, day, hour, minute, sec))
# kus esimene on siis piirangu algus ja teine l8pp
# 
no_bell = (
	((2003, 8, 26), (2003, 8, 27)),
	((2003, 9, 23), (2003, 9, 28)),
	((2003, 9, 23), (2003, 9, 28)),
)
