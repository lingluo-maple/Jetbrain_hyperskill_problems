import os
import sys
import hashlib
import string


def get_files(ext: str, mode: int):
    files_map = {}
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file = os.path.join(root, name)
            with open(file, "rb") as f:
                content = f.read()
                md5 = hashlib.md5(content).hexdigest()
            size = os.path.getsize(file)
            if file.endswith(ext):
                if files_map.get((size, md5)):
                    files_map[(size, md5)] = files_map[(size, md5)] + [file]
                else:
                    files_map[(size, md5)] = [file]
    new_dict = {}

    for i in sorted(files_map)[::mode]:
        new_dict[i] = files_map[i]

    last_size = None
    for size, files in new_dict.items():
        if size[0] != last_size:
            print(f"{size[0]} bytes")
            last_size = size[0]
        for file in files:
            print(file)
    print("Check for duplicates?\n")
    while True:
        choice = input()
        if choice == "yes":
            with_hash(new_dict)
        elif choice == "no":
            break
        else:
            continue


def with_hash(elements: dict):
    last_size = None
    last_hash = None
    number = 1
    duplications = {}
    for data, files in elements.items():
        if len(files) > 1:
            if data[0] != last_size:
                last_size = data[0]
                print(f"{data[0]} bytes")
            if data[1] != last_hash:
                last_hash = data[1]
                print(f"Hash: {data[1]}")
            for file in files:
                print(f"{number}: {file}")
                duplications[number] = file
                number += 1
    while True:
        print("Delete files?")
        choice = input()
        if choice == "yes":
            delete_files(duplications, number)
            break
        elif choice == "no":
            break
        else:
            continue


def delete_files(duplications: dict[int: str], max_number: int):
    while True:
        print("Enter file numbers to delete:")
        numbers = input()
        if numbers == "" or str(max_number) in numbers:
            print("Wrong format")
            continue
        else:
            numbers = numbers.split()
            for num in numbers:
                wrong = False
                for letter in string.ascii_letters:
                    if letter in num:
                        print("Wrong format")
                        wrong = True
                        break
                if wrong:
                    exit()
                if float(int(float(num))) != float(num):
                    print("Wrong format")
            break
    size = 0
    for i in numbers:
        idx = int(i)
        file = duplications.get(idx)
        try:
            size += os.path.getsize(file)
            os.remove(file)
        except FileNotFoundError:
            pass
    print(f"Total freed up space: {size} bytes")


def main():
    print("Enter file format")
    file_format = input()
    print("Size sorting options:")
    print("1. Descending")
    print("2. Ascending")
    while True:
        print("Enter a sorting option:")
        sorting = input()
        if sorting == "1":
            mode = -1
            break
        elif sorting == "2":
            mode = 1
            break
        else:
            print("Wrong option")
            continue
    get_files(file_format, mode)


try:
    path = sys.argv[1]
    main()
except IndexError:
    print("Directory is not specified")
