import re

difficulty_level = 'beginner'
# difficulty_level = 'intermediate'
language = 'German'

def main():
    extract_individual_lessons()

def extract_individual_lessons():
     
    with open(f'../data/{language}/text/{difficulty_level}/combined_lessons.txt', 'r') as file:
        combined_lessons = file.read()
    
    # print(combined_lessons)

    # lesson_pattern = re.compile(r'(### Lesson ([\w]+):[\S]+---)')
    lesson_pattern = re.compile(r'### (Lesson ([\w]+):[\S\s]+?)---')
    lessons = re.findall(lesson_pattern, combined_lessons)
    print(lessons[0][0])

    for lesson in lessons:
        with open(f'../data/{language}/text/{difficulty_level}/lesson_{lesson[1]}.txt', 'w') as file:
            file.write(lesson[0])

if __name__ == '__main__':
    main()