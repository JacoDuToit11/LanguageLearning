# Language Learning Audio Generation

This project generates audio files that can assist in language learning.

## Scripts:

- **`generate_lessons_text.py`**: 
  - Generates the language learning texts, i.e., translations from English to any other language.

- **`text_to_speech.py`**: 
  - Generates audio files for each lesson.

## To Run:

1. Set the language and difficulty level in `config.yaml`.
2. Run the following commands:

    ```bash
    $ python generate_lessons_text.py
    $ python text_to_speech.py
    ```

<!-- Sample lesson:
<audio controls>
  <source src="/data/German/beginner/Lesson 2: Introducing Oneself and Others.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio> -->
