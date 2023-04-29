import speech_recognition as sr
from playsound import playsound

r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:
        print("Please say a number in marathi\n")
        audio = r.listen(source)
        fname = input("Please enter file name to save recording to\n")
        with open(fname+".wav", "wb") as f:
            f.write(audio.get_wav_data())
        print("Recorded successfully\n")
        playsound(fname+".wav")
        input("Press enter to proceed next\n")
