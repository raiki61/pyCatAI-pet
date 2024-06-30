# import google.generativeai as genai
import pyttsx3
from threading import Thread

from PIL import ImageGrab

from g4f.client import Client
import g4f


class Commenter:
    def __init__(self):
        # update your API key
        # self.API_KEY = ""
        # self.MODEL = self.Configure()

        self.latest_response = None
        self.client = Client()
    
    # def Configure(self):
    #     # genai.configure(api_key=self.API_KEY)
    #     # model = genai.GenerativeModel("gemini-pro-vision")

    #     model = g4f.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[{"role": "user", "content": "Hello"}],
    #         stream=True,
    #     )

    #     return model
    
    def TakeScreenshot(self):
        screenshot = ImageGrab.grab()
        return screenshot
    
    def GenerateComment(self):
        # prompt = "this is a screnshot of my Windows computer screen. Pretend that you are a cat and do your best to generate a funny comment based on whatever you see me doing."
        prompt = "あなたは猫です。日本語で話します。デスクトップ上を動きまわる猫です。思うままに話てください。最初の紹介文は不要です。"

        screenshot = self.TakeScreenshot()

        # self.latest_response = self.MODEL.generate_content([prompt, screenshot]).text
        
        return self.GenerateCommentByInput(prompt)
    
    def GenerateCommentByInput(self, input):
        prompt = "You are cat living in desktop. Detect and match the language entered by the user and speak it. The user's input is next."
        response = self.client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4",
            provider=g4f.Provider.Theb,
            messages=[{"role": "user", "content": prompt + input}],
        )
        self.latest_response = response.choices[0].message.content
        return self.latest_response
    
    def ThreadedSpeaker(self):
        _ = Thread(target=self.SpeakComment)
        _.run()

    def SpeakComment(self):
        tts = pyttsx3.init()
        tts.say(f'<pitch middle="10">{self.latest_response}</pitch>')
        tts.runAndWait()