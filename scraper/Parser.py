from bs4 import BeautifulSoup
import os
import json

content_of_courses_raw_path = 'Content of Courses/raw/'

# to check for hidden files
if os.name == 'nt':
    import win32api, win32con

def file_is_hidden(p):
    if os.name== 'nt':
        attribute = win32api.GetFileAttributes(p)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return p.startswith('.') #linux-osx

file_list = [f for f in os.listdir(content_of_courses_raw_path) if not file_is_hidden(f)]

# currently implemented for Content of Courses only, todo for Class Schedule and Exam Timetable
for filename in file_list:
	html = open(os.path.join(content_of_courses_raw_path, filename), 'r').read()

	dict_of_courses = {}
	soup = BeautifulSoup(html.replace('\n', ''), 'lxml')

	tr_tags = soup.find_all('tr')

	for tr_tag in tr_tags:

		count = 0
		for tag in tr_tag.children:
			if count == 0:
				first_tag_text = tag.text
				if tag.text == 'COURSE CODE':
					break
				elif tag.text != 'Mutually exclusive with: ' and \
						tag.text != 'Not available to Programme: ' and \
						tag.text != 'Not available to all Programme with: ' and \
						tag.text != 'Not available as Core to Programme: ' and \
						tag.text != 'Not available as UE to Programme: ' and \
						tag.text != 'Not available as PE to Programme: ' and \
						tag.text != 'Prerequisite:' and \
						tag.text != 'Grade Type: ' and \
						tag.text != '\xa0' and \
						tag.text != '' and \
						tag.get('colspan') != '4':
					is_in_course_code = True
					course_code = tag.text 
					dict_of_courses[course_code] = {
						'name': None,
						'au': None,
						'program': None,
						'mutually_exclusive': None,
						'not_available_to_program': None,
						'not_available_to_all_program_with': None,
						'not_available_as_core_to_program': None,
						'not_available_as_UE_to_program': None,
						'not_available_as_PE_to_program': None,
						'prerequisite': None,
						'grade_type': None,
					}
				elif tag.get('colspan') == '4':
					dict_of_courses[course_code]['description'] = tr_tag.text

			else:
				if is_in_course_code:
					if count == 1:
						dict_of_courses[course_code]['name'] = tag.text
					elif count == 2:
						dict_of_courses[course_code]['au'] = tag.text
					elif count == 3:
						dict_of_courses[course_code]['program'] = tag.text
						is_in_course_code = False
				elif first_tag_text == 'Mutually exclusive with: ':
					dict_of_courses[course_code]['mutually_exclusive'] = tag.text
				elif first_tag_text == 'Not available to Programme: ':
					dict_of_courses[course_code]['not_available_to_program'] = tag.text
				elif first_tag_text == 'Not available to all Programme with: ':
					dict_of_courses[course_code]['not_available_to_all_program_with'] = tag.text
				elif first_tag_text == 'Not available as Core to Programme: ':
					dict_of_courses[course_code]['not_available_as_core_to_program'] = tag.text
				elif first_tag_text == 'Not available as UE to Programme: ':
					dict_of_courses[course_code]['not_available_as_UE_to_program'] = tag.text
				elif first_tag_text == 'Not available as PE to Programme: ':
					dict_of_courses[course_code]['not_available_as_PE_to_program'] = tag.text
				elif first_tag_text == 'Prerequisite:' or (first_tag_text == '' and tag.text != ''):
					if dict_of_courses[course_code].get('prerequisite'):
						dict_of_courses[course_code]['prerequisite'] += f' {tag.text}'
					else:
						dict_of_courses[course_code]['prerequisite'] = tag.text
				elif first_tag_text == 'Grade Type: ':
					dict_of_courses[course_code]['grade_type'] = tag.text
				elif first_tag_text == '\xa0':
					break


			count += 1

	json_filename = f'Content of Courses/parsed/{os.path.splitext(filename)[0]}.json'
	os.makedirs(os.path.dirname(json_filename), exist_ok=True)
	with open(json_filename, 'w') as file:
		file.write(json.dumps(dict_of_courses))
		file.close()



