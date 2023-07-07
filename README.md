# MD to PDF
This script takes a folder of markdown files, and converts it to a PDF. It automatically detects links between pages and makes them clickable in the PDF, and determines the order of pages automatically based on what is referenced first in the homepage.

## Running it (Ubuntu)
```bash
sudo apt install pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils texlive-latex-extra texlive-xetex
git clone https://github.com/johanvandegriff/md-to-pdf.git
cd md-to-pdf
#run the example:
examples/docs-to-pdf.sh
#open the generated file:
xdg-open example/docs.pdf

#run it on your own md files (replace the arguments below):
./md-to-pdf.py your/md/directory output.pdf "Your Title" homepage.md cover.png
xdg-open output.pdf
```
Right now, I only know the dependencies for ubuntu, but it should work in theory on any OS, if you can figure out how to install pandoc, texlive, and xelatex. I plan to package this as a docker image (and maybe even host it on a website) to make it easier to use, since the dependencies were the hardest part to get right.
