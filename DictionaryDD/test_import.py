import sqlite3
from hanzipy.dictionary import HanziDictionary
from processed.processed_chars import word_list

# Create a new SQLite database or connect to an existing one
conn = sqlite3.connect('wow.db')
cursor = conn.cursor()



# Create a table to store the character definitions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY,
        simplified TEXT,
        traditional TEXT,
        pinyin TEXT,
        definition TEXT
    )
''')

cursor.execute('''
    CREATE INDEX IF NOT EXISTS idx_simplified_traditional_pinyin_definition ON characters (simplified, traditional, pinyin, definition)
''')

# Initialize the Hanzi dictionary
dictionary = HanziDictionary()

# Get all characters and their definitions
i = 0
for character in word_list:  # Unicode range for CJK characters
    try:
        definitions = dictionary.definition_lookup(character)
        for definition in definitions:
            simplified = definition['simplified']
            traditional = definition['traditional']
            pinyin = definition['pinyin']
            definition = definition['definition']
            cursor.execute('''
                INSERT INTO characters (simplified, traditional, pinyin, definition)
                VALUES (?, ?, ?, ?);
            ''', (simplified, traditional, pinyin, definition))

    except KeyError:
        pass

# Commit the changes and close the database connection
conn.commit()
conn.close()
