# basic description
```
Feed pairs of title and text to ChatGPT, get analysis.
```

# 2 program parts
1. `create_to_tag.py` --> create `all_text.json`
2. `main.py` --> use ChatGPT API to analyze data in json

# Intended workflow
- use `create_to_tag.py`, a commandline interaction that helps you create pairs of title and text, and create `all_text.json`
- then use `main.py` to create analysis of the text, using `bg_info.txt`, the title, the text, and a pre-written prompt for ChatGPT (using the OpenAI API)
    + in this case `bg_info.txt` has API docs for ElevenLabs
    + in this case each `text` is stuff copypasted from a github repo (as you can see in the Youtube video)
    + it also does a followup question (for a second ChatGPT API call), that's specific to this repo. it asks, "which endpoint does it use?".
        - since the `bg_info.txt` is basically a collection of the ElevenLabs endpoints, this is a useful question.

# recording of me using `create_to_tag.py` and `main.py`
https://www.youtube.com/watch?v=41e3OA_0RdY&ab_channel=AtillaCodesStuff

# note
put your openai key in `secrets.py`