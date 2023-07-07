#!/bin/bash
cd `dirname $0`

input_dir="docs"
output_file="docs.pdf"
title="My Docs"
homepage="index.md"
cover_image="docs/cover.png"

../md-to-pdf.py "$input_dir" "$output_file" "$title" "$homepage" "$cover_image"
