'''
Redesign/improve Maya:
- Choose a domain of assistance
- Equip Maya with more “social competence”, i.e. features that facilitate 
    smooth interaction (e.g. more flexible/varied responses, more context 
    sensitivity, conversational devices such as bachchannels and repairs*) 
'''
import datetime
import transformers
import numpy as np

import msvcrt
import time
import sys

import argparse

class TimeoutExpired(Exception):
    pass

def input_with_timeout(prompt, timeout, timer=time.monotonic):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    endtime = timer() + timeout
    result = []
    while timer() < endtime:
        if msvcrt.kbhit():
            result.append(msvcrt.getwche()) #XXX can it block on multibyte characters?
            if result[-1] == '\r':
                return ''.join(result[:-1])
        time.sleep(0.04) # just to yield to other processes/threads
    raise TimeoutExpired

# Build the AI
class ChatBot():
    def __init__(self, name):
        print("--- starting up", name, "---")
        self.name = name

    def speech_to_text(self, text):
        self.text = text.lower()
        # print("me --> ", text)

    def text_to_speech(self, text):
        print(f"{self.name} --> ", text)

    def wake_up(self, text):
        return True if self.name in text.lower() else False

    @staticmethod
    def action_time():
        time = datetime.datetime.now().time().strftime('%H:%M')
        return f'The time is {time}'

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', type=int, default=None, required=False)
    args = parser.parse_args()
    timeout = args.timeout

    ai = ChatBot(name='edd')
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")

    helloes = ['hello', 'hi', 'hey', 'good day', 'greetings']
    goodbyes = ['goodbye', 'bye', 'goodnight', 'see you', 'exit', 'quit']
    end = False
    while not end:
        if not timeout:
            text = input(f"Talk to {ai.name}: ")
            ai.speech_to_text(text)
        else:
            try:
                text = input_with_timeout(f"Talk to {ai.name}: ", timeout)
            except TimeoutExpired:
                text = '** Awkward silence **'
                res = "you have been quiet for some time now - if you don't have anything else to ask, you can just say goodbye."
        ai.speech_to_text(text)
        print("me --> ", text)

        ## wake up
        if ai.wake_up(ai.text) is True:
            res = "Hello"
        
        if any([hello in ai.text for hello in helloes]):
            res = '''Hi. My name is Sex Edd. 
            
            I am your new sex education teacher.

            I can help educate you on the things that may be awkward or hard to talk about with your friends and family. 
            Please feel free to ask my about anything related to the topic, and I will try and answer the best I can.
            
            If you don't feel like you have any more questions, simply say goodbye and I will leave you to it.
            '''
        
        ## ask for the time
        elif "time" in ai.text:
            res = ai.action_time()

        ## Consent
        elif "consent" in ai.text:
            i = 0
            res = '''Consent means actively agreeing to be sexual with someone. Consent lets someone know that sex is wanted. Sexual activity without consent is rape or sexual assault.
            Sexual consent is an agreement to participate in a sexual activity. Before being sexual with someone, you need to know if they want to be sexual with you too. It’s also important to be honest with your partner about what you want and don’t want.
            Consenting and asking for consent are all about setting your personal boundaries and respecting those of your partner — and checking in if things aren’t clear. Both people must agree to sex — every single time — for it to be consensual.
            Without consent, sexual activity (including oral sex, genital touching, and vaginal or anal penetration) is sexual assault or rape.
            Consent is easy as FRIES:
            Freely Given.
            Reversible.
            Informed.
            Enthusiastic.
            Specific.
            '''

        ## Sex
        elif "sex" in ai.text:
            res = ''''''

        ## Protection
        elif "protection" in ai.text:
            res = '''I hear you mentioned the topic of protection. I have knowledge on the following concepts, all of which are related to protection: 
            Condoms, birth control, S T D's.
            Please write condoms, birth control or STDs, and I will expand upon it further.'''

        elif "condoms" in ai.text or "condom" in ai.text:
            res = '''A condom is a thin, fitted tube worn over the penis during sex (male condoms) or inserted into the vagina before sex (female condoms). They create a barrier that keeps semen and other body fluids out of the vagina, rectum, or mouth.
            You might hear a condom called a rubber or the barrier method. But, no matter what you call them, condoms have the same purpose. They prevent STDs (sexually transmitted diseases) and pregnancy. And they’re a good birth control option because they're cheap, easy to get, and you don't have to plan ahead to use them.'''

        ## Birth control    
        elif "birth control" in ai.text or "contraception" in ai.text:
            res = '''Birth control, also known as contraception, is designed to prevent pregnancy. Birth control methods may work in a number of different ways:
            Preventing sperm from getting to the eggs. Types include condoms, diaphragms, cervical caps, and contraceptive sponges.
            Keeping the ovaries from releasing eggs that could be fertilized. Types include birth control pills, patches, shots, vaginal rings, and emergency contraceptive pills.
            IUDs, devices which are implanted into the uterus. They can be kept in place for several years.
            Sterilization, which permanently prevents a someone from getting pregnant or from from being able to get someone else pregnant.
            Your choice of birth control should be based on several factors. These include your health, how often you have sexual activity, how sexual partners you have, and whether you want to have children in the future. 
            Your health care provider can help you select the best form of birth control for you.'''

        ## STD's
        elif "std" in ai.text or "stds" in ai.text:
            res = '''STDs are infections that are spread from one person to another, usually during vaginal, anal, and oral sex. 
            They’re really common, and lots of people who have them don’t have any symptoms. 
            Without treatment, STDs can lead to serious health problems. 
            But the good news is that getting tested is no big deal, and most STDs are easy to treat.
            Consult a doctor if you suspect you may be infected.'''

        ## respond politely
        elif any(i in ai.text for i in ["thank","thanks"]):
            res = np.random.choice(["you're welcome!","anytime!"])

        # Try and talk
        elif ai.text != '** awkward silence **':
            chat = nlp(transformers.Conversation(ai.text), pad_token_id=50256)
            res = str(chat)
            res = "I'm afraid I don't understand your question in relation to my area of expertise. Please rephrase - but if you just want to chat, then: " + res[res.find("bot >> ")+6:].strip()

        # saying goodbye
        if any([goodbye in ai.text for goodbye in goodbyes]):
            res = 'It was nice talking to you. Goodbye!'
            end = True
        
        ai.text_to_speech(res)