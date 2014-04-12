'''
Function to convert a text string to an MP3 sound file.
Special text key words are converted to current data:
    %day = day of week (Monday)
    %time = time (16:45)
    %date = date (2nd March)
    %greet = Good morning / Good afternoon / Good evening 
Optionally adds an alert sound to the start of the MP3 file (e.g. ding_dong)
Uses Google TTS (Text to Speech service)

Usage: 
Call create_tts_mp3 ('a text string to speak', path, alert)
    path is where mp3 files are read and written to (must have read/write)
    alert is the file name of an optional mp3 file to signal start the speech
        the alert file must be in the path location provided
        this is inserted into the start of the Speech.mp3
        Note: ideally give this MP3 a title MP3 tag for display on Sonos
        
@author: David
'''
import urllib2, sys
from datetime import datetime
from time import sleep

#==============================================================================
def text2mp3(txt, path, lang, alert=None):
    '''Function generates mp3 file from supplied text in given path.
    inputs:
        txt: a sting of text to be spoken
        path: is appended with '/speech.mp3' - will replace any existing file.
        lang: language for speech en = English
        alert: is an optional mp3 inserted in the start of speech.mp3
    Special keys words are replaced with current info (e.g. %time)
    
    returns True / False (OK or not)
    '''
    txt = replace_keys(txt) #replace special keys
    
    save_to = path + '/' + 'speech.mp3'
    
    if alert: #add path to alert file name if present, else leave as None
        alert = path + '/' + alert
        
    ok = build_mp3(txt, save_to, lang, alert) 
        
    return ok, save_to

#==============================================================================
def replace_keys(words):
    '''Parses input text to add special feature key words:
         
    returns string of original text with keys replaced with current info.
    '''    
    now = datetime.now()
        
    if '%day' in words:
        words = words.replace('%day', now.strftime('%A'))
        
    if '%time' in words:
        words = words.replace('%time', now.strftime('%H:%M'))
    
    if '%date' in words:
        d = int(now.strftime('%d'))
        suffix = 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
        mth = now.strftime('%B')
        words = words.replace('%date', str(d)+suffix+' '+mth)
    
    if '%greet' in words:
        GREET = ['morning', 'morning', 'afternoon', 'evening']
        hour = int(now.strftime('%H'))
        words = words.replace('%greet', 'Good '+GREET[hour/6])
    
    return words


def txt_chunks(chunk_size, text):
    ''' Breaks up text string into a list of text chunks each with max 
    size of the chunk_size. Tries to break on space, but if not just breaks.
    
    returns a list of text chunks
    '''
    broken_txt = [] # list of text chunks
    
    start = 0
    txt_len = len(text)
        
    while start < txt_len - chunk_size:
        end = start + chunk_size
        pos = text.rfind(' ',start,end)
        if pos <= start: #didn't find space (-1) or space first char
            pos = end #just have to cut not on a space boundary         
        broken_txt.append(text[start:pos])
        start = pos
        
    #process the final chunk
    broken_txt.append(text[start:txt_len])
       
    return broken_txt

def build_mp3(words, save_to, language, alert):
    '''converts text string supplied into an MP3 file
    Uses Google TTS
    Adds alert sound to start of MP3 file - from existing mp3 file
    
    returns nothing
    '''
      
    #open MP3 output file ( 0 buffer or don't complete before it is played!)
    try:
        f = open(save_to, 'wb',0) #binary (b) mode needed on windows
    except IOError:
        print ("Error - can't open '%s' to write MP3" % save_to )
        return False
    
    #insert the alert mp3 at the start of the speech file
    if alert:
        try:
            a = open(alert, 'rb') #open mp3 
            f.write(a.read()) #write it to the output file
            a.close()
        except IOError:
            print ('Warning - alert file "%s" not found - omitted' % alert)
        
    # create speech via Google TTS and write to MP3 file
    base_url = "http://translate.google.com/translate_tts?tl=%s&q=%s"
    
    try:
        # Google TTS has a limit of 100 characters of text.
        # If text > 100 characters text is split into blocks 
        if len(words) < 100:
            # pass text directly to Google TTS
            f.write(tts(base_url, language, words))
        else:
            # break words into a list of chunks of < 100 characters
            chunks = txt_chunks(100, words) #max size of chunks = 100
            
            # pass each chunks of text to Google TTS
            for count, word_chunk in enumerate(chunks):
                if len(word_chunk) == 0: continue #omit empty text strings            
                #extend url to include total chunks and counter
                base_url += "&total=%s&idx=%s" % (len(chunks), count)
                f.write(tts(base_url, language, word_chunk))
                sleep(.1) # wait to allow things to happen!    
        #f.flush
        f.close()
    except IOError as e:
        print ('IO Error %s' % e)
        return False
    
    return True

def tts(base_url,language, words ):
    #build url and convert words to %20 for space etc.    
    mp3url = base_url % ( language, urllib2.quote(words))
    req = urllib2.Request(mp3url)
    req.add_header('User-agent', 'Mozilla/5.0') 
    try:
        response = urllib2.urlopen(req)
        return response.read() 
    except urllib2.HTTPError as e:
        sys.exit ('HTTP Error %s' % e)

    