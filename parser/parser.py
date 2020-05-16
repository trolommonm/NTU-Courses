from bs4 import BeautifulSoup
import os
import json

year = 2020
term = 1
encoding_fmt = 'utf-8'

parser_directory = os.path.dirname(__file__)
main_directory = parser_directory[:-7]
deg = "Accountancy (GA) Year 1"

# Relative Paths
html_files = "scraper\\Content of Courses"
parsed_files = "parser\\data"
desired_html_folder = f"Acad Yr {year} {term}"
desired_html_file = f"{deg}.html"
desired_storage_file = "data_file.json"


# Absolute Paths
storage_location = os.path.join(main_directory,parsed_files,desired_storage_file)
file_loc = os.path.join(main_directory, html_files, desired_html_folder,desired_html_file)


template = {
    "name": None,
    "au": None,
    "mutually_exclusive":None,
    "not_available":None,
    "grade_type": "graded",
    "not_available_spec":None,
    "description":None,
}

file_temp = {
    "code" : {None:None},
}

# Using lxml for speed
# Need to pip3 install lxml
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
with open(file_loc) as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

# Finds all content with <b> tags and stores them in a list
mods = soup.body.find_all('table')
storage = {}
for mod in mods:
    mod_data = mod.find_all("td")
    code = mod_data[0].string
    name = mod_data[1].string
    au = mod_data[2].string
    mutually_exclusive = None
    not_available = None
    not_available_spec = None
    grade_type = "Graded"
    description = None

    # Skip 3 and 4 as they will return None
    for i in range(5, len(mod_data)):
        line = mod_data[i]
        if line.string == "Mutually exclusive with: ":
            i += 1
            mutually_exclusive = mod_data[i].string
            continue

        elif line.string == "Not available to Programme: ":
            i += 1
            not_available = mod_data[i].string
            continue

        elif line.string == "Not available to all Programme with: ":
            i += 1
            not_available_spec = mod_data[i].string
            continue

        elif line.string == "Grade Type: ":
            i += 1
            grade_type = mod_data[i].string
            continue
        
        # Assume it is a description
        else:
            description = line.string
            continue
    temp = {
        "name": str(name),
        "au": str(au),
        "mutually_exclusive": str(mutually_exclusive),
        "not_available": str(not_available),
        "grade_type": str(grade_type),
        "not_available_spec": str(not_available_spec),
        "description": str(description),
    }
    storage[code] = temp

print(type(""))
with open(storage_location, "w") as write_file:
    s = json.dump(storage, write_file)