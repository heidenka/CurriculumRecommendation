import json

ldjson_file_path = '/Users/kingaheidenthal/Downloads/marketing_sample_for_seek_au-seek_au_job__20210101_20210331__30k_data.ldjson'
output_json_file_path = '/Users/kingaheidenthal/Downloads/output2.json'

json_objects = []

with open(ldjson_file_path, 'r') as file:
    for line in file:
        # Parse each line as a JSON object
        json_object = json.loads(line.strip())
        json_objects.append(json_object)

# Save the list of JSON objects into a JSON file
with open(output_json_file_path, 'w') as output_file:
    json.dump(json_objects, output_file)

print(f'Data saved to {output_json_file_path}')
