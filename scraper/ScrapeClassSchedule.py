import requests
from bs4 import BeautifulSoup
import os

class_schedule_url = 'https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main'

print('Scraping class schedule...')

# scrape class schedule
res = requests.get(class_schedule_url)
soup = BeautifulSoup(res.text.replace('\n', ''), 'lxml')

# get select tag for acadsem
acadsem_select_tag = soup.find(name='select', attrs={'name': 'acadsem'})

# get all options for acadsem and store in a dictionary
# key: option, value: name for that option
acadsem_options_dict = {}
for option in acadsem_select_tag.children:
	acadsem_options_dict[option['value']] = option.text

for acadsem_option in acadsem_options_dict.keys():
	url = 'https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1'
	form_data = {
		'acadsem': acadsem_option,
		'r_course_yr': '',
		'r_subj_code': '',
		'r_search_type': 'F',
		'boption': 'Search',
		'staff_access': 'false',
	}

	res = requests.post(url, data=form_data)
	
	filename = f'Class Schedule/raw/{acadsem_options_dict[acadsem_option]}.html'
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, 'w') as f:
		f.write(res.text)
		f.close()

