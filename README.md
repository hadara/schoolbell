This is a rather simple application for managing schoolbell.
Configuration file tells what soundfile to play and when. It also provides a couple of methods for overriding special
cases like holidays and ability to run pre- and after- commands to modify volume levels etc.

It was written back in 2004 for a friend of mine who managed IT for a couple of schools and complained
about the needless complexity and price of commercial schoolbell management software (yes, such things exist!). 
So in a couple of hours I hacked this together and it has been in production in several schools since then, more than 14 years so far :-)


## usage

Just edit conf.py to match your needs and then start the application with: 
```
python bell.py
```
You can start it automatically on bootup for example by placing it in the crontab:
```
@reboot cd /path/to/bell && python bell.py 1> /dev/null 2> /dev/null &
```

Ensure that the user you run this script under has sufficient privileges to play audio and change mixer settings.

You can edit conf.py while it's running and force reload by sending SIGHUP (for killall -HUP bell.py)
