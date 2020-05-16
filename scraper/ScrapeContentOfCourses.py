import requests
from bs4 import BeautifulSoup
import os

content_of_courses_url = 'https://wish.wis.ntu.edu.sg/webexe/owa/aus_subj_cont.main'

print('Scraping content of courses...')

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
	acad_yr = acadsem_option.split('_')[0]
	semester = acadsem_option.split('_')[1]
	url = 'https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SUBJ_CONT.main_display1'
	form_data = {
		'acadsem': acadsem_option,
		'r_course_yr': '',
		'r_subj_code': '',
		'boption': 'Search',
		'acad': acad_yr,
		'semester': semester,
	}

	res = requests.post(url, data=form_data)
	
	filename = f'Content of Courses/raw/{acadsem_options_dict[acadsem_option]}.html'
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, 'w') as f:
		f.write(res.text)
		f.close()
