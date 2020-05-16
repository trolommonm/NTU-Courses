import requests
from bs4 import BeautifulSoup
import os

exam_timetable_url = 'https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.MainSubmit'

print('Scraping exam timetable...')

form_data = {
	'p_opt': '1',
	'p_type': 'UE',
	'bOption': 'Next',
}

res = requests.post(exam_timetable_url, data=form_data)
soup = BeautifulSoup(res.text.replace('\n', ''), 'lxml')

p_plan_no_tags = soup.find_all('input', attrs={'name': 'p_plan_no'})

p_plan_no_dict = {}
for p_plan_no_tag in p_plan_no_tags:
	p_plan_no_dict[p_plan_no_tag['value']] = p_plan_no_tag.next_sibling

for p_plan_no_value in p_plan_no_dict.keys():
	url = 'https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.query_page'
	form_data = {
		'p_plan_no': p_plan_no_value,
		'p1': '',
		'p2': '',
		'p_type': 'UE',
		'bOption': 'Next',
	}

	res = requests.post(url, data=form_data)
	soup = BeautifulSoup(res.text.replace('\n', ''), 'lxml')

	acad_session = soup.find('input', attrs={'name': 'academic_session'})['value']
	p_plan_no = soup.find('input', attrs={'name': 'p_plan_no'})['value']
	p_exam_yr = soup.find('input', attrs={'name': 'p_exam_yr'})['value']
	p_semester = soup.find('input', attrs={'name': 'p_semester'})['value']

	url = 'https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.Get_detail'
	form_data = {
		'p_exam_dt': '',
		'p_start_time': '',
		'p_dept': '',
		'p_subj': '',
		'p_venue': '',
		'p_matric': '',
		'academic_session': acad_session,
		'p_plan_no': p_plan_no,
		'p_exam_yr': p_exam_yr,
		'p_semester': p_semester,
		'p_type': 'UE',
		'bOption': 'Next',
	}

	res = requests.post(url, data=form_data)

	filename = f'Exam Timetable/raw/{p_plan_no_dict[p_plan_no_value]}.html'
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, 'w') as f:
		f.write(res.text)
		f.close()

