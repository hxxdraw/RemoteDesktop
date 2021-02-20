from pygame.mixer import init, music
from pyttsx3 import init as speech_init


class Speech(object):
    def __init__(self, rate, index, volume, text):
        """
        :param rate:
        :param index:
        :param volume:
        :param text:
        """
        self.speech_rate = rate
        self.voice_index = index
        self.sound_volume = volume
        self.phrase = text

    def Synthesize(self):
        engine = speech_init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[self.voice_index].id)
        engine.setProperty('rate', self.speech_rate)
        engine.setProperty('volume', self.sound_volume)
        engine.say(self.phrase)
        engine.runAndWait()
        engine.stop()


class Sound(object):
    def __init__(self, file_path):
        """
        :param file_path:
        """
        self.path = file_path
        init()

    def Play(self):
        """
        Playing sound using <self.path> ;== file_path
        :return:
        """
        music.load(self.path)
        music.play()
