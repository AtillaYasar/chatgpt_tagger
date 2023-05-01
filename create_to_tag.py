import os, json

result_path = 'all_text.json'
input_path = 'create_to_tag.txt'

if result_path in os.listdir():
    with open(result_path, 'r') as f:
        all_text = json.load(f)
else:
    all_text = []

while True:
    # set title
    i = input('Write the title of the file you want to tag:\n')
    title = i

    # get text
    i = input('Put the text in create_to_tag.txt\nPress enter when done.')
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    all_text.append({'title':title, 'text':text})

    # save
    with open(result_path, 'w') as f:
        json.dump(all_text, f, indent=4)
    
    print('Done!')
    print('-'*20)

