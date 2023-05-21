#!/bin/python
import re
import codecs
import argparse
import os
import sys
    
ENCRYPTION_KEY = "QWERTY"
match_brackets = re.compile(r'([^\[]*)\]')
match_inner_quote = re.compile(r'"(.*)"')


def encryption(input_text, encrypt):
    output = []
    KEY_MAX_INDEX = len(ENCRYPTION_KEY)
    
    for index, c in enumerate(input_text):
        CodePointInput = ord(c)
        codePointKey = ord(ENCRYPTION_KEY[index % KEY_MAX_INDEX])
        
        if encrypt:
            output_char = chr(CodePointInput + codePointKey)
        else:
            output_char = chr(CodePointInput - codePointKey)
        
        output.append(output_char)
    
    return ''.join(output)

def save_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)

def convert_line(line, encrypt):
    if len(line) == 0:
        print("null line found")
        return None

    if line[0] == "\0":
        print("null line found")
        return None
    
    if line[0] == " ":
        return None
    
    match = match_brackets.search(line)
    if match:
        changed_text = encryption(match.group(1), encrypt)
        return f'[{changed_text}]\n'
    else:
        key, value = line.split("=")
        changed_key = encryption(key, encrypt)
        
        if not changed_key:
            return None
        
        match = match_inner_quote.search(value)
        if match:
            changed_val = encryption(match.group(1), encrypt)
        else:
            changed_val = ""
        
        return f'{changed_key}="{changed_val}"\n'

def read_save(text, encrypt):
    output = []
    
    for line in text:
        converted = convert_line(line, encrypt)
        if converted is None:
            continue
        
        output.append(converted)
    
    return ''.join(output)

def handle_decryption_of_file(filename, encrypt):
    try:
        with codecs.open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        text = text.split('\n')
            
        changed_text = read_save(text, encrypt)
        
        if encrypt:
            filename = f'{filename}.sav'
        else:
            filename = f'{filename}.decoded.txt'
        
        save_file(changed_text, filename)
        print(f'Save location is -> {filename}')
        
    except IOError:
        print("Error reading file")


def summon_add(id, summon_array) -> None:
    id = int(id)
    summon_array = summon_array.split(',')
    summon_array[id] = '100'
    summon_array = ','.join(summon_array)
    print(f'Summon={summon_array}')


def knowledge_add(id, arr) -> int:
    arr = arr.split(',')
    id = str(id)
    find = 0
    for i, v in enumerate(arr[::2]):
        if v == id:
            find = 1
            break
    if not find:
        return -1
    
    i *= 2
    arr[i+1] = '10000'
    arr = ','.join(arr)
    print(f'Array={arr}')
    return 0


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        help="file to use",
        required=False,
    )
    parser.add_argument(
        "-m", "--mode", 
        choices=['enc', 'dec', 'knowledge', 'mana'],
        help="Encrypt or decrypt a save file.", 
        required=False
    )
    parser.add_argument(
        "-i", "--id",
        help="Creature's ID", 
        required=False
    )
    parser.add_argument(
        "-",
        dest='stdin',
        action='store_true',
        help="Read stdin. For pipe like usage", 
        required=False
    )
    args = parser.parse_args()
    
    if args.stdin:
        stdin_input = sys.stdin.read()
        
        if args.mode == "mana":
            summon_add(args.id, stdin_input)
        elif args.mode == "knowledge":
            knowledge_add(args.id, stdin_input)
    
    else:
        if '~' in args.file:
            expanded_path = os.path.expanduser(args.file)
        else:
            expanded_path = args.file

        if args.mode == 'enc':
            encrypt = True
        else:
            encrypt = False

        handle_decryption_of_file(
            filename=expanded_path,
            encrypt=encrypt
        )