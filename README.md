say
===

Text to Speech using Google TTS with test program to play on Sonos

The Test_Voice.py module should be run after changing a couple 
of constants to match your environment.

The alert file is optional and can be any ding-dong sound that if 
present prefaces any speech. Any MP3 file can be used and it must 
be placed in the specified path. If not found it will be ignored 
with a warning.

To run the program using the default text:
	$ Python Test_Voice.py

To use your text:
	$ Python Test_Voice.py "my text string"

The text sting can contain special text keys that get translated based 
on the time and date of your machine:
 * %day = day of week (Monday)
 * %time = time (16:45)
 * %date = date (2nd March)
 * %greet = Good morning / Good afternoon / Good evening 

Have fun.......

License
This is released under the MIT license. 
