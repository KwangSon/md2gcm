#!/usr/bin/env python3

import textwrap
import re

def convert_code_block(a):
    print(a)
    exit()

def remove_pattern_line(orig_string, pattern):
    return re.sub(".*"+pattern+".*\n?","",orig_string)

# open git msg file
with open('git-msg.md', 'r') as f:
    content = f.read()

HEAD_TAG = '## head'
BODY_TAG = '## body'
FOTTER_TAG = '## footer'
CODE_BLOCK_TAG = '```'

head_pattern = re.findall(HEAD_TAG, content)
body_pattern = re.findall(BODY_TAG, content)
fotter_pattern = re.findall(FOTTER_TAG, content)

assert(len(head_pattern) == 1)
assert(len(body_pattern) == 1)
assert(len(fotter_pattern) == 1)

headtag_end = re.search(HEAD_TAG, content).end()
bodytag_start = re.search(BODY_TAG, content).start()

filtered_content = content[headtag_end:bodytag_start]
clear_head = remove_pattern_line(filtered_content, '###').strip()

wrong_head = False
# check capital letter
if clear_head[0].islower():
    print('Change with captial letter: ' + clear_head[0].upper() + clear_head[1:])
    wrong_head = True

if '.' in clear_head:
    print('Head should not contain dot(.)')
    wrong_head = True

if len(clear_head) > 50:
    print('Head is too long, make it less than 50 letter')
    wrong_head = True

assert(wrong_head == False)

bodytag_end = re.search(BODY_TAG, content).end()
fottertag_start = re.search(FOTTER_TAG, content).start()
filtered_content = content[bodytag_end:fottertag_start].strip()
clear_body = remove_pattern_line(filtered_content, '###')

# 1. check code block (if exist code block, skip)
# 2. wrap 72 line
# 3. append code block with '---'

num_code_block = len(re.findall(CODE_BLOCK_TAG, clear_body))
assert(num_code_block == 0 or num_code_block == 2)

normal_body = clear_body
if num_code_block == 2:
    normal_body = clear_body[:re.search(CODE_BLOCK_TAG, clear_body).start()]
    code_block = re.findall(CODE_BLOCK_TAG + '(.*?)' + CODE_BLOCK_TAG, clear_body, flags=re.S)[0].strip()

# normal_body = normal_body.strip()
body_paragraph = normal_body.strip().split('\n')

with open('git-commit.msg', 'w') as f:
    f.write(clear_head + '\n\n')
    for line in body_paragraph:
        f.writelines(textwrap.fill(line, 72) + '\n\n')
    if num_code_block > 0:
        f.write('---\n')
        f.write(code_block)
