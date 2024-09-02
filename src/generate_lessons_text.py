from openai import OpenAI
import os
import textwrap
import json
import re
import yaml

openai_client = OpenAI(api_key=os.environ['JACO_OPENAI_API_KEY'])

# model = "gpt-4o-mini"
model = "gpt-4o-2024-08-06"

num_lessons = 10
phrases_per_lesson = 25

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

language = config['settings']['language']
difficulty_level = config['settings']['difficulty_level']

output_path = f'../data/{language}/{difficulty_level}/'
if not os.path.exists(output_path):
    os.makedirs(output_path)

with open('../data/language_examples.json', 'r') as file:
    data = json.load(file)
example_phrases = data['languages'][language]

def main():
    gen_lessons_text()

def gen_lessons_text():
    system_instruction = 'You are a language teacher creating a podcast to help people learn a language.'

    prompt = textwrap.dedent(f'''
    Provide exactly {num_lessons} different lessons for people learning {language}. You should give a phrase in English, 
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
    
    lessons = openai_client.chat.completions.create(
        model=model,
        messages=messages
    ).choices[0].message.content

    lesson_pattern = re.compile(r'### (Lesson ([\w]+):[\S\s]+?)---')
    lessons = re.findall(lesson_pattern, lessons)

    lessons_dict = {}
    for lesson in lessons:
        lesson_output = process_lesson_text(lesson[0])
        lessons_dict[lesson[1]] = lesson_output

    with open(f'{output_path}lessons.json', 'w') as file:
        json.dump(lessons_dict, file, indent=4)

def process_lesson_text(text):
    # Remove number at start of line
    pattern = r"([0-9]+[.])\s"
    text = re.sub(pattern, r"", text)

    pattern = r"([.]{3})"
    text = re.sub(pattern, r"", text)

    text_lines = text.splitlines()
    if '' in text_lines:
        text_lines.remove('')
    
    output = []
    for i, line in enumerate(text_lines):
        if i < 2:
            output.append(line)
        else:
            # Split sentences
            pattern = re.compile(r'\s*([^.!?]*[.!?])')
            sentences = pattern.findall(line)
            output.extend(sentences)
    return output

if __name__ == '__main__':
    main()