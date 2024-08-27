from typing import List

from hanzipy.dictionary import HanziDictionary
from hsk_1 import hsk_1
from hsk_2 import hsk_2
from hsk_3 import hsk_3
from hsk_4 import hsk_4
from hsk_5 import hsk_5
from hsk_6 import hsk_6

dictionary = HanziDictionary()
surname_definition_count = 0
surname_definitions = []
real_definitions_to_save = []
not_found_characters = []
copied_definition_count = 0
copied_definitions = []
hsks = [hsk_1, hsk_2, hsk_3, hsk_4, hsk_5, hsk_6]
for hsk in hsks:
    for char_data in hsk:
        hanzi = char_data['hanzi']
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
            not_found_characters.append(hanzi)

print('surname definition count:', surname_definition_count)
print('real_definitions_count:', len(real_definitions_to_save))
print('not found characters:', len(not_found_characters), not_found_characters)
print('Copied definition: ', copied_definition_count)
# print('Copied definitions: ', copied_definitions)
