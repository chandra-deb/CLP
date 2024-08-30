from typing import List

from hanzipy.dictionary import HanziDictionary
from hsk_1 import hsk_1
from hsk_2 import hsk_2
from hsk_3 import hsk_3
from hsk_4 import hsk_4
from hsk_5 import hsk_5
from hsk_6 import hsk_6
from all_hsk import all_hsk

dictionary = HanziDictionary()
surname_definition_count = 0
surname_definitions = []
real_definitions_to_save = []
# not_found_characters = []
copied_definition_count = 0
copied_definitions = []
# hsks = [hsk_1, hsk_2, hsk_3, hsk_4, hsk_5, hsk_6]
hsks = [all_hsk]
all_characters = [char_data['hanzi'] for char_data in all_hsk]


def parse_new_hsk(filename: str):
    with open(filename, 'r', encoding='utf-8') as f:
        word_list = [line.strip() for line in f.readlines()]
        return word_list


word_list = parse_new_hsk('new_hsk_1.txt')
all_characters.extend(word_list)


def gather_all_chars(filenames: List[str]):
    chars = []
    for filename in filenames:
        chars.extend(parse_new_hsk(filename))
    return chars


filenames = ['new_hsk_1.txt', 'new_hsk_2.txt', 'new_hsk_3.txt',
             'new_hsk_4.txt', 'new_hsk_5.txt', 'new_hsk_6.txt',
             'new_hsk_7.txt', ]
new_hsk_chars = gather_all_chars(filenames)
print('newhskchars:', len(new_hsk_chars))
all_characters.extend(new_hsk_chars)
print(len(all_characters))



real_characters = []
not_found_characters = []
for char in all_characters:
    # hanzi = char_data['hanzi']
    if char not in real_characters:
        real_characters.append(char)
    hanzi = char
    try:
        definitions = dictionary.definition_lookup(hanzi)
        for definition in definitions:
            if definition not in real_definitions_to_save:
                english: str = definition['definition']
                if english.startswith('surname'):
                    surname_definitions.append(definition)
                    surname_definition_count += 1
                else:
                    real_definitions_to_save.append(definition)
            else:
                copied_definition_count += 1
                copied_definitions.append(definition)

    except KeyError:
        if hanzi not in not_found_characters:
            not_found_characters.append(hanzi)

print('surname definition count:', surname_definition_count)
print('real_definitions_count:', len(real_definitions_to_save))
print('real_character_count', len(real_characters))
print('not found characters:', len(not_found_characters), not_found_characters)
print('Copied definition: ', copied_definition_count)
# print('Copied definitions: ', copied_definitions)
print()

with open('../processed/processed_chars.py', 'w', encoding='utf-8') as f:
    f.write("word_list = {}\n".format(real_characters))


with open('../processed/not_found_processed_chars.py', 'w', encoding='utf-8') as f:
    f.write("not_found_word_list = {}\n".format(not_found_characters))
