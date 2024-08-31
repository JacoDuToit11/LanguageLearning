import re
import json

difficulty_level = 'beginner'
# difficulty_level = 'intermediate'
language = 'German'
# language = 'Afrikaans'

def main():
    extract_individual_lessons()

def extract_individual_lessons():
    with open(f'../data/{language}/text/{difficulty_level}/combined_lessons.txt', 'r') as file:
        combined_lessons = file.read()
    
    lesson_pattern = re.compile(r'### (Lesson ([\w]+):[\S\s]+?)---')
    lessons = re.findall(lesson_pattern, combined_lessons)

    lessons_dict = {}
    for lesson in lessons:
        lesson_output = process_lesson_text(lesson[0])
        lessons_dict[lesson[1]] = lesson_output

    with open(f'../data/{language}/text/{difficulty_level}/combined_lessons.json', 'w') as file:
        json.dump(lessons_dict, file, indent=4)


def process_lesson_text(text):
    pattern = r"([0-9]+[.])\s"
    text = re.sub(pattern, r"", text)

    pattern = r"([.]{3})"
    text = re.sub(pattern, r".", text)

    output = []
    text_lines = text.splitlines()
    text_lines.remove('')
    for i, line in enumerate(text_lines):
        if i < 2:
            output.append(line)
        else:
            pattern = re.compile(r'\s*([^.!?]*[.!?])')
            sentences = pattern.findall(line)
            output.extend(sentences)
    return output

if __name__ == '__main__':
    main()