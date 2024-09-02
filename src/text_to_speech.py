from openai import OpenAI
import os, json
from pydub import AudioSegment
import yaml
silence_duration1 = 2000 # milliseconds
silence_duration2 = 3000 # milliseconds

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

language = config['settings']['language']
difficulty_level = config['settings']['difficulty_level']

text_lessons_path = f'../data/{language}/{difficulty_level}/lessons.json'
speech_lessons_path = f'../data/{language}/{difficulty_level}/'

openai_client = OpenAI(api_key=os.environ['JACO_OPENAI_API_KEY'])
speech_model = 'tts-1'

def main():
    with open(text_lessons_path, 'r') as file:
        lessons_dict = json.load(file)
    
    for lesson_content in lessons_dict.values():
        text_to_speech(lesson_content)

def text_to_speech(lesson_content):
    final_audio = AudioSegment.silent(duration=0)
    # Silence segments with different lengths
    silence_segment1 = AudioSegment.silent(duration=silence_duration1)
    silence_segment2 = AudioSegment.silent(duration=silence_duration2)

    for i in range(0, len(lesson_content), 2):
        # Generate first phrase (English)
        response1 = openai_client.audio.speech.create(
            model=speech_model,
            voice="onyx", 
            input=lesson_content[i],
        )

        temp_audio_file1 = f"tmp1.mp3"
        with open(temp_audio_file1, "wb") as f:
            f.write(response1.content) 

        # Generate second phrase (Translation)
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
        
        # Adding phrase and translation 
        final_audio += segment1_audio
        final_audio += silence_segment1
        final_audio += segment2_audio

        if i > 0:
            # Repeating phrase and translation 
            final_audio += silence_segment1
            final_audio += segment1_audio
            final_audio += silence_segment2
            final_audio += segment2_audio
        final_audio += silence_segment1

        # Clean up the temporary files
        os.remove(temp_audio_file1)
        os.remove(temp_audio_file2)
    final_audio.export(f"{speech_lessons_path}{lesson_content[0]}.mp3", format="mp3")

if __name__ == '__main__':
    main()