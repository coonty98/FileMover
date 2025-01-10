#!/usr/bin/env python3
import os, shutil
from sys import exit
from prettytable import PrettyTable as pt
import re
from collections import defaultdict

print('''Welcome to FileMover!
          This program allows the user to quickly move files.
          Simply identify your SOURCE and/or DESTINATION folders when prompted and
            enter or scan your case numbers.
          A table will display indicating what shade folder each file was placed in.
          Be sure to check that files were assigned the correct shade.
          If a case entered does not have any files, this will display in the table.\n''')
input('Press enter to continue--->\n')
term_size = os.get_terminal_size()
print('=' * term_size.columns)
print()

while True:

    def startquestion():
        while True:
            sourcequestion = input("""What is your source?
    1. Milling Folder
    2. New CAM Files - NDX Standard FCZ
    3. Other
                                   
Enter number--->""")
            print()
            if not re.match(r"[123]", sourcequestion):
                print("Error! Invalid input. Enter number 1-3.")
            else:
                return sourcequestion
    sourcequestion = startquestion()


    def sourceanswer():
        print('=' * term_size.columns)
        print()
        if sourcequestion == '1':
            while True:
                dtinput = input("Enter date of milling folder: ")
                print()
                if not re.match(r"\b([1-9]|1[0-2])\b-\b([1-9]|[12][0-9]|3[01])\b-\d\d", dtinput):
                    print ("Error! Date format should be m-d-yy or mm-dd-yy")
                else:
                    if os.path.exists('Y:\\ManufactDir\\' + dtinput + '\\NDX Standard FCZ'):
                        source = ('Y:\\ManufactDir\\' + dtinput + '\\NDX Standard FCZ')
                        destination = ('Y:\\ManufactDir\\' + dtinput + '\\NDX Standard FCZ')
                        return source, destination
                    else:
                        print('ERROR Invalid Source--->' + 'Y:\\ManufactDir\\' + dtinput + '\\NDX Standard FCZ')
        elif sourcequestion == '2':
            while True:
                dtinput = input("Enter date of milling folder for destination: ")
                print()
                if not re.match(r"\b([1-9]|1[0-2])\b-\b([1-9]|[12][0-9]|3[01])\b-\d\d", dtinput):
                    print ("Error! Date format should be m-d-yy or mm-dd-yy")
                else:
                    if os.path.exists('Y:\\ManufactDir\\' + dtinput + '\\NDX Standard FCZ'):
                        source = ('Y:\\ManufactDir\\New CAM Files\\NDX Standard FCZ')
                        destination = ('Y:\\ManufactDir\\' + dtinput + '\\NDX Standard FCZ')
                        return source, destination
                    else:
                        print('ERROR Invalid Destination--->' + 'Y:\\ManufactDir\\' + dtinput + '\\NDX Standard FCZ')
        elif sourcequestion == '3':
            print()
            sources = input('Enter source path: ')
            destinations = input('Enter destination path: ')
            sources1 = sources.split('"')
            source = str(sources1[1])
            destinations1 = destinations.split('"')
            destination = str(destinations1[1])
            return source, destination
    source, destination = sourceanswer()




    shadeguide = {
    'A1': ('A1' ,'1M2', '2L1.5', '2M1', '2R1.5'),
    'A2': ('A2', '2M2'),
    'A3.5': ('A3.5', '3L2.5', '3M3', '3R2.5', '4L2.5', '4M2'),
    'A3': ('A3', '2L2.5', '2M3', '2R2.5'),
    'A4': ('A4', '4M3', '4R2.5', '5M2', '5M3'),
    'B1': ('B1', '1M1'),
    'B2': ('B2'),
    'B3': ('B3'),
    'B4': ('B4'),
    'C1': ('C1', '3M1'),
    'C2': ('C2'),
    'C3': ('C3', '4L1.5'),
    'C4': ('C4', '5M1'),
    'D2': ('D2'),
    'D3': ('D3', '3L1.5', '3M2', '3R1.5', '4M1', '4R1.5'),
    'D4': ('D4'),
    'OM1': ('OM1'),
    'OM2': ('OM2'),
    'OM3': ('OM3'),
    }

    def actions():
        print('=' * term_size.columns)
        print()
        cases = []
        print('Enter or Scan Cases. Enter "X" to submit--->\n')
        while True:
            case = input('Enter Case #: ')
            if case == 'x':
                break
            cases.append(case)
        print()
        print('=' * term_size.columns)
        print()
        export = pt()
        export.title = ('Files Moved')
        export.field_names = ['Cases', 'Shade', 'File Name']
        exportnocase = pt()
        exportnocase.title = ('Cases w/ No Files Found')
        exportnocase.field_names = ['Cases', ' ']
        def file_manager(file_source_dir, file_destination_dir):
            source_dir = file_source_dir
            destination_dir = file_destination_dir
            file_names = os.listdir(source_dir)

            def pad_lines_vertically(lines, size):
                ''' List of lines of exactly `size` length.
                Extended with empty lines if needed.
                '''
                orig_lines = list(lines)
                assert size >= len(orig_lines)
                return orig_lines + [''] * (size - len(orig_lines))

            def pad_lines_horizontally(lines):
                ''' Pad lines to the lenght of the longest line.
                '''
                line_length = max(len(line) for line in lines)
                return [
                    line.ljust(line_length)
                    for line in lines
                ]

            def text_add(text1, text2, padding=' '):
                lines1 = text1.splitlines()
                lines2 = text2.splitlines()
                line_count = max(len(lines1), len(lines2))

                def pad_lines(lines):
                    return pad_lines_horizontally(
                        pad_lines_vertically(lines, line_count)
                    )

                return '\n'.join(
                    ''.join(line1 + padding + line2)
                    for line1, line2 in zip(pad_lines(lines1), pad_lines(lines2))
                )

            case_tuples = []
            for c in cases:
                for file_name in file_names:
                    if file_name.startswith(c):
                        tuple = (c, file_name)
                        case_tuples.append(tuple)
                else:
                    tuple = (c, 'error')
                    case_tuples.append(tuple)
            case_dict = defaultdict(list)
            for c, file_name in case_tuples:
                case_dict[c].append(file_name)

            for z, y in case_dict.items():
                for v in y:
                    regex = r"_[abcd][1234]\D[5]_|_[abcd][1234]_|_(?:om)[123]_|_[12345][m][123]_|_[234][lr][12]\D[5]_"
                    matches = re.finditer(regex, v, re.MULTILINE | re.IGNORECASE)
                    for match in matches:
                        shade = match.group(0).split('_')
                        shades = str(shade[1]).upper()
                        for key, value in shadeguide.items():
                            if shades in value:
                                x = key
                        if not os.path.isdir(os.path.join(destination_dir, x)):
                            os.mkdir(os.path.join(destination_dir, x))
                            shutil.move(os.path.join(source_dir, v), os.path.join(destination_dir, x))
                            export.add_row([z, x, v])
                        else:
                            shutil.move(os.path.join(source_dir, v), os.path.join(destination_dir, x))
                            export.add_row([z, x, v])
                else:
                    if z not in export.get_string(fields=['Cases']):
                        exportnocase.add_row([z, 'Case Not Found'])
            text1 = str(export)
            text2 = str(exportnocase)
            print (text_add(text1, text2, padding='\t'))
        file_manager(source, destination)
        continuetask()

    def continuetask():
        print('=' * term_size.columns)
        print()
        while True:
            again = input('''What would you like to do?
    1. Enter more cases
    2. Update Source/Destination
    3. Exit
    Enter "1" or "2" or "3"--->''')
            print()
            print('=' * term_size.columns)
            print()
            if again not in {"1","2","3"}:
                print("please enter valid input")               
            elif again == "3":
                exit()
            elif again == "2":
                break
            elif again == "1":
                return actions()
    actions()
    continue