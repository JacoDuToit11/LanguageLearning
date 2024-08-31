from openai import OpenAI
import os
import textwrap
import json

openai_client = OpenAI(api_key=os.environ['JACO_OPENAI_API_KEY'])
model = "gpt-4o-mini"
num_lessons = 10
phrases_per_lesson = 25

difficulty_level = 'beginner'
# difficulty_level = 'intermediate'

language = 'German'
# language = 'Afrikaans'

with open('../data/language_examples.json', 'r') as file:
    data = json.load(file)
example_phrases = data['languages'][language]

def main():
    gen_lessons_text()

def gen_lessons_text():
    system_instruction = 'You are a language teacher creating a podcast to help people learn a language.'

    prompt = textwrap.dedent(f'''
    Provide {num_lessons} lessons for people learning {language}. You should give a phrase in English, 
    and then the translation in {language}. Each lesson should contain {phrases_per_lesson} phrases. 
    These lessons should be at a {difficulty_level} level. You can make up details like names and years.
    The format should look like this: 
    
    ### Lesson 1: title...
    Summary of what we will be learning in this lesson...
    {example_phrases}
    ...
    ---
    ### Lesson 2: title...
    ...
    ''')
    
    messages = [{'role':'system', 'content':system_instruction},
                {'role':'user', 'content':prompt}]
    
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
    ).choices[0].message.content

    with open(f'../data/{language}/text/{difficulty_level}/combined_lessons.txt', 'w') as file:
        file.write(response)

if __name__ == '__main__':
    main()