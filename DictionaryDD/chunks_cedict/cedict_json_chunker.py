import json

def split_json(file_path, chunk_size):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        items = list(data.items())  # Convert dictionary to list of items
        for i in range(0, len(items), chunk_size):
            chunk = dict(items[i:i + chunk_size])  # Convert slice back to dictionary
            with open(f'chunk_{i//chunk_size}.json', 'w', encoding='utf-8') as chunk_file:
                json.dump(chunk, chunk_file, ensure_ascii=False, indent=4)

split_json('all_cedict.json', 10000)  # Adjust chunk_size as needed
