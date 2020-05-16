from bs4 import BeautifulSoup
import os
import json

year = 2020
term = 1
encoding_fmt = 'utf-8'
nbsp = u'\xa0'



# File directories
parser_directory = os.path.dirname(__file__)
main_directory = parser_directory[:-7]
scraper_directory = os.path.join(main_directory, "scraper")

# Relative Paths
data_files_relative = "Content of Courses"
raw_data_relative = os.path.join(data_files_relative, "raw")
parsed_files_relative = os.path.join(data_files_relative, "parsed")
desired_storage_file_relative = "data_file.json"
ay_term_file_relative = f"Acad Yr {year} {term}.html"


# Absolute Paths
storage_location = os.path.join(scraper_directory,parsed_files_relative,desired_storage_file_relative)
raw_data_loc = os.path.join(scraper_directory, raw_data_relative, ay_term_file_relative)


template = {
    "name": "",
    "au": "",
    "pre-requisite": "",
    "mutually_exclusive": "",
    "not_available": "",
    "grade_type": "graded",
    "not_available_spec": "",
    "non_core_to": "",
    "description": "" 
}

file_temp = {
    "code" : {None:None},
}

# print(raw_data_loc)

# Using lxml for speed
# Need to pip3 install lxml
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
with open(raw_data_loc) as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

# Finds all content with <b> tags and stores them in a list
mods = soup.body.find_all('td')
'''
Ignore the first 4 lines of the header which is written as td

|Course Code|Title|AU |Programme/(DEPT MAINTAIN)*|
|-----------|-----|---|--------------------------|

'''
mods = mods[4:1000]

'''
JSON file will be following this template
{
    "department":{
        "code":{
            "name":None
            "au":None,
            "pre-requisite":None,
            "mutually_exclusive":None,
            "not_available":None,
            "grade_type": "graded",
            "not_available_spec":None,
            "description":None   
        }
    }
}
'''
storage = {}

idx = 0
current_mod = {}
start = True
prev = None
# s = mods[13:20]
# for line in s:
#     print(line.string)


while (idx < len(mods)):
    try:
        line = mods[idx]
    except:
        print("Error!")

    if start:
        try:
            text = line.string
            while text == "None" or text == nbsp or text == None:
                idx += 1
                text = mods[idx].string
            code = str(text)
            name = str(mods[idx+1].string)
            au = str(mods[idx+2].string)
            department = str(mods[idx+3].string)
            if department != prev:
                print(code, name, au, department, idx)
                prev = department
        except IndexError:
            print("There's an IndexError at the start, most likely missed testcase below.")
            break
        # Declare the value in the key as a dictionary
        if department not in storage:
            storage[department] = {}
        
        storage[department][code] = template.copy()
        current_mod = storage[department][code]
        current_mod['name'] = name
        current_mod['au'] = au

        start = False
        idx += 4
        continue

    else:
        text = line.string
        if text == "Prerequisite:":
            req_string = ""
            idx += 1
            text = mods[idx].string
            while "OR" in text:
                req_string = req_string + text
                idx += 2
                text = mods[idx].string

            req_string = req_string + text
            req_string = req_string.replace("OR", "")
            current_mod['pre-requisite'] += str(req_string)

        elif text == "None" or text == nbsp or text == None:
            pass

        elif text == "Mutually exclusive with: ":
            idx += 1
            current_mod['mutually_exclusive'] += str(mods[idx].string)

        elif text == "Not available to Programme: ":
            idx += 1
            current_mod['not_available'] += str(mods[idx].string)
            
        elif text == "Grade Type: ":
            idx += 1
            current_mod['grade_type'] += str(mods[idx].string)

        elif text == "Not available to all Programme with: ":
            idx += 1
            current_mod['not_available_spec'] += str(mods[idx].string)
            
        elif text == "Not available as Core to Programme: ":
            idx += 1
            current_mod['non_core_to'] += str(mods[idx].string)

        # Description
        else:
            current_mod['description'] += str(mods[idx].string)
            start = True

        idx += 1


with open(storage_location, "w+") as write_file:
    json.dump(storage, write_file)
    print("Done!")