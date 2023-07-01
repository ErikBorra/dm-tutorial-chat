import os
import re

# Define your directory here
dir_path = './audio_transcription'

# Loop over every file in the directory
for filename in os.listdir(dir_path):
    # Only process text files
    if filename.endswith('.txt'):
        with open(os.path.join(dir_path, filename), 'r') as file:
            lines = file.readlines()

        # Loop over each line in the file
        for i, line in enumerate(lines):
            # Use regex to remove everything from the URL between '&list' and '&t'
            modified_line = re.sub(r'&list.*&t', '&t', line)
            line = modified_line
            modified_line = re.sub(r'Libmanian', 'Lippmannian', line)
            lines[i] = modified_line

        # Write the modified lines back to the file
        with open(os.path.join(dir_path, filename), 'w') as file:
            file.writelines(lines)
