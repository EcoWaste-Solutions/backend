import pathlib
import textwrap


import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import markdown





def getAnswer(question):
    def to_markdown(text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

    genai.configure(api_key="AIzaSyAh5oI0O_peNbi-W56i2Cv00Jty1Y42aq8")

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(question)

    return response.text

model = genai.GenerativeModel('gemini-1.0-pro-latest')

convo = model.start_chat()

while True:
    question = input('You: ')
    if question == 'exit':
        break
    response = convo.send_message(question)
    print('AI:', response.text)
    



    

