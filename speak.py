import pyttsx3
engine = pyttsx3.init()
engine.setProperty('voice', 'english+f3')  # changes the voice
engine.setProperty('rate', 125)  
engine.say(' The quick brown fox jumped over the lazy dog.')
 
engine.runAndWait()
