import os
import sys
import glob
import json

argv = [x.lower() for x in sys.argv]

def prompt_with_default(prompt, default):
    value = (input(prompt) or str(default))
    return value.strip().lower()

def should_prettify_file(file_path):
    response = 'empty'
    while response not in ['y', 'n']:
        if response is not 'empty':
            print('Invalid response, please try again\n')
        response = prompt_with_default('Do you want to prettify ' + file_path + ' (y/n)? [y] ', 'y')

    return response == 'y'

use_ascii_escaping = (False if '-no-ascii' in argv
                        else '-ascii' in argv or
                            prompt_with_default('Do you want to ASCII-escape Unicode characters (y/n)? [n] ', 'n') == 'y')
def prettify_file(file_path):
    print('Prettifying ' + file_path)
    print('Reading project file')
    with open(file_path, mode='r', encoding='UTF-8') as file:
        data = json.load(file,
                        object_hook=None) # Python 3.7 ensures dict iterates over insertion order
    print('Done reading, now formatting')
    with open(file_path, mode='w', encoding='UTF-8', newline='\n') as file:
        json.dump(data,
                file,
                ensure_ascii=use_ascii_escaping, # SynthV can read the file either way
                check_circular=False, # Disable because we know there won't be any problem
                indent=2,
                separators=(',', ': '),
                sort_keys=False) # We want insertion order
        file.write('\n')
    print('Done prettifying ' + file_path + '\n')

# Assuming project dir is where the script is located
project_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
print('Project directory: ' + project_dir)
project_files = list(map(os.path.realpath, glob.iglob(os.path.join(project_dir, './**/*.s5p'), recursive=True)))

if '-y' not in argv and not prompt_with_default('Do you want to prettify all files found by this script (y/n)? [y] ', 'y') == 'y':
    project_files = [file_path for file_path in project_files if should_prettify_file(file_path)]
print('Will prettify ' + str(len(project_files)) + ' files...\n')
project_files = [prettify_file(file_path) for file_path in project_files]
