#!/usr/bin/env python3
import os
import sys
import re
import shutil

contents = '''

some stuff

# Heading 1
## Heading 2

asdf [link text](my-file-1.md#anchor-123) blah blah
asdf [link text2](my-file-2.md) blah blah
asdf [link text3](#anchor456) blah blah

asdf [link text](my-file-1.html#anchor-123) blah blah
asdf [link text2](my-file-2.html) blah blah
asdf [link text3](#anchor456) blah blah
'''

# contents = re.sub('\]\([a-zA-Z0-9\-]*\.md', '](', contents)
contents = re.sub('\[([^\]]*)\]\(.*(#.*)\)', r'[\1](\2)', contents)



def callback(match):
    desc, url = match.groups()
    return f'TEST({desc} {url})'

contents = re.sub('\[([^\]]*)\]\(([^#].*)\)', callback, contents)

print(re.search(r'^(#+) (.*)$', contents, re.M).groups()[1])


print(contents)