import requests
from bs4 import BeautifulSoup
import os 

content_of_courses_url = 'https://wish.wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main'
class_schedule_url = 'https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main'
exam_timetable_url = 'https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.main'

# scrape content of courses 
res = requests.get(content_of_courses_url)
soup = BeautifulSoup(res.text.replace('\n', ''), 'lxml')

# get select tag for acadsem
acadsem_select_tag = soup.find(name='select', attrs={'name': 'acadsem'})

# get all options for acadsem and store in a dictionary
# key: option, value: name for that option
acadsem_options_dict = {}
for option in acadsem_select_tag.children:
	acadsem_options_dict[option['value']] = option.text


for acadsem_option in acadsem_options_dict.keys():
	url = 'https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SUBJ_CONT.main_display'
	form_data = {
		'acadsem': acadsem_option,
		'r_course_yr': '',
		'r_subj_code': '',
		'boption': 'CLoad',
		'acad': '',
		'semester': '',
	}
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded',
	}

	res = requests.post(url, data=form_data)
	soup = BeautifulSoup(res.text.replace('\n', ''), 'lxml')

	r_course_yr_select_tag = soup.find('select', attrs={'name': 'r_course_yr'})
	r_course_yr_options = [option for option in r_course_yr_select_tag.children if option['value'] != '']

	for r_course_yr_option_tag in r_course_yr_options:
		url = 'https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SUBJ_CONT.main_display1'
		acad_yr = acadsem_option.split('_')[0]
		semester = acadsem_option.split('_')[1]
		form_data = {
			'acadsem': acadsem_option,
			'r_course_yr': r_course_yr_option_tag['value'],
			'r_subj_code': '',
			'boption': 'CLoad',
			'acad': acad_yr,
			'semester': semester,
		}
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded',
		}

		res = requests.post(url, data=form_data)

		filename = f'Content of Courses/{acadsem_options_dict[acadsem_option]}/{r_course_yr_option_tag.text}.html'
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		with open(filename, 'w') as f:
			f.write(res.text)
			f.close()









