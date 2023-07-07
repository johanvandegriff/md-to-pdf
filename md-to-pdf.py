#!/usr/bin/env python3
import os
import sys
import re
import shutil

input_dir = sys.argv[1]
output_file = sys.argv[2]
title = sys.argv[3]
homepage = sys.argv[4]
cover_image = sys.argv[5]

cover_image = os.path.abspath(cover_image)
tmpdir = os.path.join(os.path.dirname(input_dir), os.path.basename(input_dir) + '-tmp-md-to-pdf')

# sudo apt install pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils texlive-latex-extra texlive-xetex

files = [homepage]
#search the homepage for links to get the order of the files correct
with open(os.path.join(input_dir, homepage), 'r') as f:
    files.extend(re.findall('\[[^\]]*\]\(([^#^)]*)#?[^\)]*\)', f.read()))

[files.append(item) for item in sorted(os.listdir(input_dir)) if item not in files]

os.mkdir(tmpdir)

def slug_str(s):
    return '-'.join(''.join([c for c in s.lower() if c.isalnum() or c == ' ']).strip().split())

def heading_lookup_callback(match):
    desc, url = match.groups()
    try:
        with open(os.path.join(input_dir, url), 'r') as f:
            heading_slug = slug_str(re.search(r'^(#+) (.*)$', f.read(), re.M).groups()[1])
        return f'[{desc}](#{heading_slug})'
    except:
        return f'[{desc}]({url})'

md_files = []
for file in files:
    if '.md' in file:
        md_files.append(file)
        with open(os.path.join(input_dir, file), 'r') as f:
            lines = f.readlines()
        
        with open(os.path.join(tmpdir, file), 'w') as f:
            is_in_code_block = False
            for line in lines:
                if '```' in line:
                    is_in_code_block = not is_in_code_block
                if not is_in_code_block:
                    # before: [link text](my-file.md#my-heading)
                    # after: [link text](#my-heading)
                    line = re.sub('\[([^\]]*)\]\([^)]*(#[^\)]*)\)', r'[\1](\2)', line)

                    # before: [link text](my-file.md)
                    # after: [link text](#first-heading-from-my-file)
                    line = re.sub('\[([^\]]*)\]\(([^#][^\)]*)\)', heading_lookup_callback, line)

                    # handle markdown todo lists
                    # before: - [ ] todo item
                    # after: - ☐ todo item
                    line = re.sub('([-\*]) \[ \]', r'\1 ☐ ', line)
                    # before: - [x] todo item
                    # after: - ☒ todo item
                    line = re.sub('([-\*]) \[x\]', r'\1 ☒ ', line)
                f.write(line)
            f.write('\n') # write an extra newline at the end of each file to separate them
    else:
        shutil.copyfile(os.path.join(input_dir, file), os.path.join(tmpdir, file))

with open(os.path.join(tmpdir, 'cover.tex'), 'w') as f:
    f.write(r'''
\vspace*{\stretch{1.0}}
\begin{center}
    \Huge\textbf{''' + title + r'''}\\
\end{center}
\vspace*{\stretch{2.0}}

\includegraphics{''' + cover_image + r'''}

\thispagestyle{empty}
''')

with open(os.path.join(tmpdir, 'quote.tex'), 'w') as f:
    f.write(r'''
% change style of quote, see also https://tex.stackexchange.com/a/436253/114857
\usepackage[most]{tcolorbox}

\definecolor{linequote}{RGB}{224,224,224}
\definecolor{backquote}{RGB}{224,224,224}
\definecolor{bordercolor}{RGB}{128,128,128}

% change left border: https://tex.stackexchange.com/a/475716/114857
% change left margin: https://tex.stackexchange.com/a/457936/114857
\newtcolorbox{myquote}[1][]{%
    enhanced,
    breakable,
    size=minimal,
    left=10pt,
    top=5pt,
    bottom=5pt,
    frame hidden,
    boxrule=0pt,
    sharp corners=all,
    colback=backquote,
    borderline west={2pt}{0pt}{bordercolor},
    #1
}

% redefine quote environment to use the myquote environment, see https://tex.stackexchange.com/a/337587/114857
\renewenvironment{quote}{\begin{myquote}}{\end{myquote}}
''')

#xelatex leaves out some unicode but can process internal links, as long as you use the heading anchor text instead of the filename
os.system('''cd "''' + tmpdir + '''"; pandoc \
    --pdf-engine=xelatex \
    --table-of-contents \
    --number-sections \
    -V colorlinks \
    -H quote.tex \
    --include-before-body cover.tex \
    -V geometry:margin=2.5cm \
    -V mainfont="DejaVu Serif" \
    -V monofont="DejaVu Sans Mono" \
    ''' + ' '.join(md_files) + ''' \
    -o result.pdf''')

os.rename(os.path.join(tmpdir, 'result.pdf'), output_file)
shutil.rmtree(tmpdir)
