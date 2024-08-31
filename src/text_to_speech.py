from openai import OpenAI
import os, json
from pydub import AudioSegment
silence_duration1 = 2000 # milliseconds
silence_duration2 = 3000 # milliseconds

difficulty_level = 'beginner'
# difficulty_level = 'intermediate'

language = 'German'
# language = 'Afrikaans'

text_lessons_path = f'../data/{language}/text/{difficulty_level}/'
speech_lessons_path = f'../data/{language}/speech/{difficulty_level}/'

openai_client = OpenAI(api_key=os.environ['JACO_OPENAI_API_KEY'])
speech_model = 'tts-1'

def main():
    with open(f'{text_lessons_path}combined_lessons.json', 'r') as file:
        lessons_dict = json.load(file)
    
    for lesson_num, lesson_content in lessons_dict.items():
        text_to_speech(lesson_num, lesson_content)
        exit()

def text_to_speech(lesson_num, lesson_content):
    final_audio = AudioSegment.silent(duration=0)
    silence_segment1 = AudioSegment.silent(duration=silence_duration1)
    silence_segment2 = AudioSegment.silent(duration=silence_duration2)

    for i in range(0, len(lesson_content), 2):

        response1 = openai_client.audio.speech.create(
            model=speech_model,
            voice="onyx", 
            input=lesson_content[i],
        )

        # Save and load each segment
        temp_audio_file1 = f"tmp1.mp3"
        with open(temp_audio_file1, "wb") as f:
            f.write(response1.content) 

        response2 = openai_client.audio.speech.create(
            model=speech_model,
            voice="onyx", 
            input=lesson_content[i+1],
        )

        temp_audio_file2 = f"tmp2.mp3"
        with open(temp_audio_file2, "wb") as f:
            f.write(response2.content) 

        segment1_audio = AudioSegment.from_file(temp_audio_file1)
        segment2_audio = AudioSegment.from_file(temp_audio_file2)

        final_audio += segment1_audio
        final_audio += silence_segment1
        final_audio += segment2_audio

        if i > 0:
            final_audio += silence_segment1
            final_audio += segment1_audio
            final_audio += silence_segment2
            final_audio += segment2_audio
        final_audio += silence_segment1

        # Clean up the temporary file
        os.remove(temp_audio_file1)
        os.remove(temp_audio_file2)
    final_audio.export(f"{speech_lessons_path}lesson_{lesson_num}.mp3", format="mp3")

if __name__ == '__main__':
    main()