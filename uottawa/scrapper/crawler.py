# run the three spider python files in the spiders folder

import os
import subprocess

def main():
    # get the current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # get the spiders directory
    spiders_dir = os.path.join(current_dir, 'spiders')
    # get the python files in the spiders directory
    spiders = [f for f in os.listdir(spiders_dir) if f.endswith('.py') and f != '__init__.py']
    # run the python files in the spiders directory from
    for spider in spiders:
        subprocess.run(['python', os.path.join(spiders_dir, spider)])

if __name__ == '__main__':
    main()