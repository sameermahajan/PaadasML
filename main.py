import kivy
from kivy.app import App
from kivy.core.audio import SoundLoader
import random
from kivy.uix.textinput import TextInput
import time
import speech_recognition as sr

def play(file):
    sound = SoundLoader.load(file)
    if sound:
        sound.play()
    time.sleep(1)

class PaadasML(App):
    def load_transcription(self):
        self.transcription = []
        with open("marathi_number_transcription.txt") as file:
            for line in file:
                self.transcription.append(line.split())

    def build(self):
        self.load_transcription()

        while True:
            number = random.randint(1,10)
            times = random.randint(1,10)
            play("numbers/" + str(number) + ".wav")
            play("times/" + str(times) + ".wav")

            # listen to the answer
            while True:
                answer = ""
                print("Please state your answer in marathi")
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
              
                    print("Recognizing the marathi number Now .... ")
        
                    try:
                        answer = r.recognize_google(audio, language="mr-IN")
                        print("You have said: " + answer)
                        break
                    except Exception as e:
                        print("Error :  " + str(e))
                        play("prompt/repeat.wav")
                        continue

            # check answer
            product = number * times

            number_transcriptions = []

            if len(self.transcription) >= product:
                number_transcriptions = self.transcription[product - 1]

            is_correct = False

            for s in number_transcriptions:
                if s == answer:
                    is_correct = True

            if is_correct:
                play("prompt/correct.wav")
            else:
                print(answer)
                play("prompt/incorrect.wav")
                play("numbers/" + answer + ".wav")
                play("prompt/incorrect.wav")

            # revise the problem

            play("numbers/" + str(number) + ".wav")
            play("times/" + str(times) + ".wav")
            play("numbers/" + str(product) + ".wav")
            time.sleep(1)

if __name__ == '__main__':
    PaadasML().run()
