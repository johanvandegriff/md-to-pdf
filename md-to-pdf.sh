#!/bin/bash
input_dir="$1"
output_file="$2"
title="$3"
homepage="$4"
cover_image="$5"

cd $input_dir
input_dir=`pwd`

# sudo apt install pandoc texlive-latex-base texlive-fonts-recommended texlive-extra-utils texlive-latex-extra texlive-xetex

#search the homepage for links to get the order of the files correct
files="$homepage
"`cat "$homepage" | tr '[' '\n' | grep '](' | cut -f2 -d '(' | cut -f1 -d'#' | cut -f1 -d')'`
for file in *.md; do
    if ! echo "$files" | grep "^${file}$" > /dev/null; then
        files="$files
$file"
    fi
done

tmpdir=${input_dir}-tmp-$RANDOM
mkdir $tmpdir

for file in $files; do
    # before: ](my-file.md#my-heading)
    # after: ](#my-heading)
    cat $file | sed 's,]([a-zA-Z\-]*\.md,](,g' > $tmpdir/$file

    # before: ](my-file.md)
    # after: ](#first-heading-from-my-file)
    #TODO
done


cd $tmpdir

echo "
\vspace*{\stretch{1.0}}
\begin{center}
    \Huge\textbf{$title}\\
\end{center}
\vspace*{\stretch{2.0}}

\includegraphics{$cover_image}

\thispagestyle{empty}
" > cover.tex

echo '% change style of quote, see also https://tex.stackexchange.com/a/436253/114857
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
' > quote.tex


#xelatex leaves out some unicode but can process internal links, as long as you use the heading anchor text instead of the filename
pandoc \
    --pdf-engine=xelatex \
    --table-of-contents \
    --number-sections \
    -V colorlinks \
    -H quote.tex \
    --include-before-body cover.tex \
    -V geometry:margin=2.5cm \
    -V mainfont="DejaVu Serif" \
    -V monofont="DejaVu Sans Mono" \
    $files \
    -o result.pdf


cd $input_dir
mv $tmpdir/result.pdf "$output_file"
rm -r "$tmpdir"
