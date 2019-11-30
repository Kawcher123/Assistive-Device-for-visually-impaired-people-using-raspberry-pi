import pyttsx3

engine = pyttsx3.init()
engine.say("it's "+str(id))
engine.runAndWait()
f1 = open("MyFile.txt", "r")
for x in f1:
	engine = pyttsx3.init()
	engine.say(x)
	engine.runAndWait()
    
