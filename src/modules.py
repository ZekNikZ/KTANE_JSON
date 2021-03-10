import json
import os
import os.path as path
import errno

# .env
import settings

# Paths
REPO_PATH = path.abspath(os.getenv('KTANE_CONTENT_REPO_PATH'))
OUTPUT_PATH = path.abspath(os.getenv('OUTPUT_PATH'))
JSON_PATH = path.join(REPO_PATH, 'JSON')

# Create output folder
if not os.path.exists(OUTPUT_PATH):
    try:
        os.makedirs(OUTPUT_PATH)
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

# Helper function to dump json to file
def dump_to_file(output_file_path, l):
    with open(path.join(OUTPUT_PATH, output_file_path), 'w') as file:
        json.dump(l, file, ensure_ascii=False)
        print(f"Dumped {len(l)} objects to '{output_file_path}'")

# Get item list
files = [f for f in os.listdir(JSON_PATH) if path.isfile(path.join(JSON_PATH, f))]
print(f'Found {len(files)} items.')

# Create caches
all_modules = []
regular_modules = []
needy_modules = []
widgets = []
holdables = []

# Read files
for json_path in files:
    try:
        with open(path.join(JSON_PATH, json_path)) as file:
            # Read data
            data = json.load(file)

            # Add fields for description and tags
            data['DescriptionText'] = data['Description'][:data['Description'].find(' Tags: ')]
            data['TagList'] = data['Description'][data['Description'].find(' Tags: ') + len(' Tags: '):].split(', ')

            # Put into the right bin
            item_type = data['Type']
            if item_type == 'Regular':
                all_modules.append(data)
                regular_modules.append(data)
            elif item_type == 'Needy':
                all_modules.append(data)
                needy_modules.append(data)
            elif item_type == 'Holdable':
                holdables.append(data)
            elif item_type == 'Widget':
                widgets.append(data)
            else:
                print(f"Invalid item type: {json_path}")
    except Exception as e:
        print(f"Error while reading file '{json_path}':")
        print(e)

# Output
dump_to_file('all_modules.json', all_modules)
dump_to_file('regular_modules.json', regular_modules)
dump_to_file('needy_modules.json', needy_modules)
dump_to_file('holdables.json', holdables)
dump_to_file('widgets.json', widgets)