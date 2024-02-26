#!/usr/bin/env python
# Purpose: Convert ITK-Snap formatted labels file to a FreeSurfer LUT labels file.
# Usage: ./itksnap2freesurfer.py < input.txt > output.txt

import sys


def main():
    without_comments = map(remove_comment, sys.stdin)
    stripped = map(str.strip, without_comments)
    non_blanks = filter(not_blank, stripped)
    transformed = map(transform, non_blanks)

    for line in transformed:
        print(line)


def remove_comment(s: str) -> str:
    return s.split('#', maxsplit=1)[0]


def not_blank(s: str) -> bool:
    return s != ''


def transform(s: str) -> str:
    i, r, g, b, a, _v0, _v1, *label_quoted = s.split()
    label = '_'.join(label_quoted)[1:-1]
    return f'{i:4s} {label:30s} {r:4s} {g:4s} {b:4s} {a:4s}'


if __name__ == '__main__':
    main()
