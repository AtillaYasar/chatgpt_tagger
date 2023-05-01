import requests, json, os
from secrets import openai_key

def col(ft, s):
    """For printing text with colors.
    
    Uses ansi escape sequences. (ft is "first two", s is "string")"""
    # black-30, red-31, green-32, yellow-33, blue-34, magenta-35, cyan-36, white-37
    u = '\u001b'
    numbers = dict([(string,30+n) for n, string in enumerate(('bl','re','gr','ye','blu','ma','cy','wh'))])
    n = numbers[ft]
    return f'{u}[{n}m{s}{u}[0m'

def chatgpt_call(messages):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_key}"
    }
    data = {
        "model":"gpt-3.5-turbo",
        'messages':messages,
        'n':1,
        'temperature':0,
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']

def create_messages(tuples):
    messages = []
    for tup in tuples:
        role = tup[0]
        content = tup[1]
        assert role in ['user','assistant', 'system']

        messages.append(
            {
                'role':tup[0],
                'content':tup[1],
            }
        )
    return messages

def stringify(messages):
    return '\n'.join([f'{col("cy",m["role"])}\n{m["content"]}' for m in messages])

def chatgpt_tagger(background_info, title, text):
    tuples = [
        (
            'user',  # the actual prompt used for chatgpt.
            'Hey, can you help me analyze this text? Take on the persona of AnalysisBot.'
        ),
        (
            'assistant',
            'Sure! I am now AnalysisBot. Anything else you want me to know before I get to work?.'
        ),
        (
            'user',
            f'Yes. Here is some background info:\n```background.txt\n{background_info}\n```\n\nAnd here is the text I want you to analyze:\n```{title}\n{text}\n```\n\nExplain it in relation to the background info. Do it in 3 steps:\n1) "General description of the background info"\n2) "General description of the text"\n3) "Bulletpoint breakdown of the text"'
        ),
    ]
    messages = create_messages(tuples)
    response = chatgpt_call(messages)
    messages.append({'role':'assistant', 'content':response})
    return messages

with open('all_text.json', 'r') as f:
    all_text = json.load(f)
with open('bg_info.txt') as f:
    background_info = f.read()

auto_mode = True
for n, item in enumerate(all_text):
    title = item['title']
    text = item['text']
    print(col('gr', f'Title:'), title)
    if 'messages' in item:
        print(col('cy', 'Messages exists.'))
        print(stringify(item['messages']))
    else:
        print(col('cy', 'No analysis exists.'))
    print()

    while True:
        if not auto_mode:
            i = input(f'do analysis? {col("cy", "(y/n) ")}')
        else:
            i = 'y'
        if i == 'n':
            skip = True
            break
        elif i == 'y':
            skip = False
            break
        else:
            print(col('re', 'Invalid input.'))
            continue
    if skip or (auto_mode and 'messages' in item):
        continue

    # use api
    messages = chatgpt_tagger(background_info, title, text)
    all_text[n]['messages'] = messages
    print(stringify(messages))
    print('-'*20)
    with open('all_text.json', 'w') as f:
        json.dump(all_text, f, indent=4)

    # followup question
    followup_q = 'Which endpoints are used?'
    messages.append(
        {
            'role':'user',
            'content':followup_q
        }
    )
    response = chatgpt_call(messages)
    messages.append(
        {
            'role':'assistant',
            'content':response
        }
    )
    all_text[n]['messages'] = messages
    print(stringify(messages))
    print('-'*20)
    with open('all_text.json', 'w') as f:
        json.dump(all_text, f, indent=4)

    if n < len(all_text)-1:
        nxt = all_text[n+1]['title']
        if not auto_mode:
            i = input(f'Press enter to continue to {col("cy", nxt)}.')
    else:
        print(col('gr', 'Done!'))
        break

# collect info into a single document
collection = []
for item in all_text:
    title = item['title']
    text = item['text']
    messages = item['messages']
    
    collection.append(f'Title: {title}')
    collection.append('Conversation:')

    conversation_length = 2
    for item in messages[-(conversation_length*2-1):]:
        collection.append(f'{item["role"]}:\n{item["content"]}\n')
    collection.append('='*50)
    collection.append('='*50)
    collection.append('='*50)

with open('collection.txt', 'w') as f:
    f.write('\n'.join(collection))