#!/usr/bin/env python3
import os
import sys
import re

BUF_SIZE = 4096

def read_all(path: str) -> str:
    fd = os.open(path, os.O_RDONLY)
    try:
        chunks = []
        while True:
            data = os.read(fd, BUF_SIZE)
            if not data:
                break
            chunks.append(data) #storing all the data from the file into chunks
        raw = b"".join(chunks) # now we are combining those chunks into one big chunk to later decode for use
        return raw.decode("utf-8", errors="ignore") #Now decoding the big chunk so that python can understand it
    finally:
        os.close(fd)

def write_all(path: str, content: str) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        b = content.encode("utf-8") #converting content into bytes
        total = 0 #storing how many bytes we've stored in total
        while total < len(b):
            written = os.write(fd, b[total:]) # writing all the bytes in b and the b[total:] meanse that it'll write all the bytes that os can't write becasue it can only write 600 bytes
            total += written
    finally:
        os.close(fd)

def main():
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    text = read_all(input_path)

    # tokenizing the words to all lowercase and no weird characters
    tokens = re.findall(r"[A-Za-z0-9']+", text.lower())

    #simply counting how many words are being repeated using a dictionary
    counts = {}
    for word in tokens:
        counts[word] = counts.get(word, 0) + 1 # if there is no word already in the list then add a 1 to it

    # sort by count descending order
    items = sorted(counts.items())

    lines = []
    for word, ct in items:
        lines.append(f"{word} {ct}")
    out_text = "\n".join(lines) + ("\n" if lines else "")#this makes the text look like word count\nword count

    write_all(output_path, out_text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
