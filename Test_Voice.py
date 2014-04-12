'''
Test program to demo  Text to Speech routine in say.py

SETUP - change constants below to match your environment:
* change the IP to the IP of your Sonos box
* change the PATH to a path you program can read and write to and
  Sonos has access to (e.g. your music library on NAS
* copy the alert file(s) to this location
* try the program
* Note: takes words from command line (in inverted commas)
  or if none on command line uses DEFAULT_TEXT below

@author: David
'''
import sys
from soco import SoCo
from say import text2mp3 # this is the say_it function in say.py

# Constants to customise for your environment
IP = "192.168.0.73"             #Sonos player to use
PATH = '//nas/music'   #eg a Music share - Sonos must be able to access

#Constants of your choice
ALERT = 'alert4.mp3' #alert MP3 in PATH to use at start of MP3 (optional)
LANGUAGE = 'en' # language for speech (en = English)

# text below used if nothing input on command line
DEFUALT_TEXT = '%greet. Today is %day the %date, and the time is %time'  
               
#=============================================================================
def main():
    '''
    Test stub to call the say routine.
    Command line provides the words to say in inverted commas
    If omitted then uses a default text
    '''
    #use text argument from command line if present - else use default
    if len(sys.argv) < 2:
        txt = DEFUALT_TEXT
    else:
        txt = sys.argv[1]
    
    print ('Testing using %s character string "%s"' %  (len(txt), txt) )
    ok, file_name =  text2mp3(txt, PATH, LANGUAGE, ALERT)
    
    #if TTS worked OK, use file name returned to play MP3 on Sonos
    if ok:
        zp = SoCo(IP)
        zp.play_uri('x-file-cifs:%s' % file_name)
        print 'Listen to your Sonos - check volume turned up!'
  
#=============================================================================  
if __name__ == "__main__":
    main()
    print 'End'
        