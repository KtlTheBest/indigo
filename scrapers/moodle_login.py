import requests
import time
from bs4 import BeautifulSoup

CURRENT_YEAR = '2020'
CURRENT_SEMESTER = 'spring'

def login_to_moodle(username, password):
  url = "https://moodle.nu.edu.kz/login/index.php"
  session = requests.Session()
  payload = {
    'username': username,
    'password': password,
    'remeberusername': 0
  }
  session.post(url, data=payload)
  return session

def get_grades(username, password):
  r = login_to_moodle(username, password)
  html_doc = r.get('https://moodle.nu.edu.kz/grade/report/overview/index.php').text
  soup = BeautifulSoup(html_doc, 'html.parser')
  overview_grade = soup.find(id='overview-grade')
      
  if overview_grade is None:
    r.close()
    return {}

  grades_table = overview_grade.tbody
  trs_grades = grades_table.find_all('tr', class_="")

  courses = {}

  for tr_grade in trs_grades:
    course_link = tr_grade.td.a
    course_name = course_link.text

    if not CURRENT_YEAR in course_name.lower() or not CURRENT_SEMESTER in course_name.lower():
      continue

    if 'internship' in course_name.lower():
      continue

    course_href = course_link.get('href')
    html_doc = r.get(course_href).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    tr_itemnames = soup.find_all('tr')
    courses[course_name] = []
    for item_tr in tr_itemnames:
      column_itemname = item_tr.find('th', class_='column-itemname')
      column_grade = item_tr.find('td', class_='column-grade')
      column_range = item_tr.find('td', class_='column-range')
      column_percentage = item_tr.find('td', class_='column-percentage')
      
      if column_grade is None or column_itemname is None:
        continue

      if len(column_grade.text) < 2: # case when '-' or ''
        continue

      not_allowed_entries = [
        'mean of grades',
        'среднее взвешенное',
        'course total',
        'attendance',
        'қатыс'
      ]  

      item_name = column_itemname.text.lower()
      invalid = False

      for entry in not_allowed_entries:
        if entry in item_name:
          invalid = True

      if invalid:
        continue

      grade_item = {
        'name': column_itemname.text,
        'grade': column_grade.text
      }

      if not column_range is None and len(column_range.text) > 1:
        grade_item['range'] = column_range.text
      if not column_percentage is None and len(column_percentage.text) > 1:
        grade_item['percentage'] = column_percentage.text
      courses[course_name].append(grade_item)

  r.close()
  return courses

def parse_for_deadlines(soup):
  s = soup.findAll('div', {
    "class":"event",
    "data-region":"event-item"
  })

  deadlines = []
  for deadline in s:
    deadlines.append({
      'deadline_name': deadline.a.text,
      'deadline_date': deadline.div.text
    })

  return deadlines

def get_deadlines(username, password):
  r = login_to_moodle(username, password)

  try:
    html_doc = r.get("https://moodle.nu.edu.kz/my").text
  except:
    print ("Catched an error when trying to connect to moodle")
  r.close()

  soup = BeautifulSoup(html_doc, 'html.parser')
  deadlines = parse_for_deadlines(soup)
  return deadlines