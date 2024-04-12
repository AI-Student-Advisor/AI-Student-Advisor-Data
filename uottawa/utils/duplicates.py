import json

def combine_files(input_files, output_file):
    seen_texts = set()
    with open(output_file, 'w') as outfile:
        for filename in input_files:
            with open(filename, 'r') as infile:
                for line in infile:
                    data = json.loads(line)
                    text = data['text']
                    if text not in seen_texts:
                        seen_texts.add(text)
                        outfile.write(json.dumps(data) + '\n')

data_dir = '../data'
input_files = [
    f'{data_dir}/uottawa_catalog_data.jsonl', 
    f'{data_dir}/uottawa_current_students_data.jsonl', 
    f'{data_dir}/uottawa_faculty_staff_data.jsonl'
]
output_file = f'{data_dir}/uottawa_data.jsonl'
combine_files(input_files, output_file)
