import openai
from time import time,sleep
import textwrap
import os

def open_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()
    else:
        raise FileNotFoundError(f"File '{filepath}' not found. Please check the file path.")
    
def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

absolute_path = "openaiapikey.txt"

openai.api_key = open_file(absolute_path)

userContent = ""

if __name__ == '__main__':
    alltext = open_file('input.txt')
    if len(alltext) < 17000:
      userContent = alltext
      # submit to GPT3
      completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "You are a helpful assistant that summarizes text."},
          {"role": "assistant", "content": "I will summarize any text you give me. "},
          {"role": "user", "content": userContent}
        ],
        temperature=0.5
      )
      summary = completion.choices[0].message
          # pull out "content" from the response and turn it into a string
      summary = summary.content.split('"content":')[0]
      save_file(summary, 'output.txt')
      save_file('\n\n'.join(result), f'output_{time()}.txt')
    else:
      chunks = textwrap.wrap(alltext, 17000)
      result = list()
      count = 0
      for chunk in chunks:
          count = count + 1
          userContent = open_file('prompt.txt').replace('<<SUMMARY>>', chunk)
          userContent = userContent.encode(encoding='ASCII',errors='ignore').decode()
          # submit to GPT3
          completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
              {"role": "system", "content": "You are a helpful assistant that summarizes text."},
              {"role": "assistant", "content": "I will summarize any text you give me. "},
              {"role": "user", "content": userContent}
            ],
            temperature=0.5
          )
          summary = completion.choices[0].message
          # pull out "content" from the response and turn it into a string
          summary = summary.content.split('"content":')[0]
          print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
          result.append(summary)
      save_file('\n\n'.join(result), 'output.txt')
      # save a file that joins result with a new line between each item the file name should be output followed by the date and time
      save_file('\n\n'.join(result), f'output_{time()}.txt')

