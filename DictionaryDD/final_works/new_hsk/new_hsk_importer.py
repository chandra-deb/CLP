with open('new_hsk_1.txt', 'r', encoding='utf-8') as f:
    word_list = [line.strip() for line in f.readlines()]

for word in word_list:
    print(word)
print(len(word_list))