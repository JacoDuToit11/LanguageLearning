from openai import OpenAI
import os

difficulty_level = 'beginner'
# difficulty_level = 'intermediate'

language = 'German'
# language = 'Afrikaans'

text_lessons_path = f'../data/{language}/text/{difficulty_level}/'
speech_lessons_path = f'../data/{language}/speech/{difficulty_level}/'

openai_client = OpenAI(api_key=os.environ['JACO_OPENAI_API_KEY'])
speech_model = 'tts-1'

def main():
    text_to_speech()

def text_to_speech():
    # TODO redo this
    lessons_text_files = sorted(os.listdir(text_lessons_path))
    lessons_text_files.remove('combined_lessons.txt')

    for text_file in lessons_text_files:
        with open(f'{text_lessons_path}{text_file}', 'r') as file:
            text = file.read()
        
        text = text[:1000]
        print(text)
        exit()
        response = openai_client.audio.speech.create(
            model=speech_model,
            voice='onyx',
            input=text
        )
        response.stream_to_file(f'{speech_lessons_path}{text_file[:-3]}mp3')
        break

if __name__ == '__main__':
    main()