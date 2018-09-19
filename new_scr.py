import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import MySQLdb
# import datetime
import requests

import pdftotext
from six.moves.urllib.request import urlopen
import io
import re
import json


from datetime import datetime
from dateutil.relativedelta import relativedelta
current_date = datetime.today()

after_one_month = current_date+ relativedelta(months=1)

# current_date = datetime.datetime.now()
after_one_month = after_one_month.strftime("%d/%m/%Y")
created_date = current_date.strftime("%Y-%m-%d")
try:
	db = MySQLdb.connect('localhost','root','root@123','railway')
	cursor = db.cursor()
except Exception as e:
	print("ERRORRRRRRR ----- -----")
	print(e)
search_parames = ['anbond','adhcsive','loctite','dow cornind','molykote','grease','lubricant','silicone','sealants','chemicals','paints','polyurethane','sikaflex','cleaners','tapes']
# search_parames = ['adhesive','loctite']

def save_pdf(tender_id,url):
	
	url = url
	r = requests.get(url, stream=True)
	chunk_size = 2000
	with open('/Users/sakthivel/Desktop/scrapy/pdf/viewNitPdf_'+tender_id+'.pdf', 'wb') as fd:
	    for chunk in r.iter_content(chunk_size):
	        fd.write(chunk)

def get_details():
	# requests.post('http://localhost:8000/post-tender/', data = {'key':'value'})
	print("*********** Newww")
	sql = """ select * from tender where created_date='%s' """%(created_date)
	# sql = """ select * from tender """ 
	cursor.execute(sql)
	datas = cursor.fetchall()
	# print(datas)
	for data in datas:
		print(data)
		print("-------")
		driver = webdriver.Chrome()
		driver.implicitly_wait(10)
		driver.get(data[8])
		
		closing_date = driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[1]/td/table[1]/tbody/tr[1]/td[6]')
		closing_date = closing_date.text
		tender_type = driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[1]/td/table[1]/tbody/tr[3]/td[4]')
		tender_type = tender_type.text
		table = driver.find_element_by_xpath('//*[@id="attach_docs"]')
		rows = table.find_elements_by_tag_name("tr")
		i =0
		number_documents_attached = 0
		for row in rows:
			if i >0:
				number_documents_attached+=1
			i+=1
		print("closing_date: "+str(closing_date))
		print("tender_type: "+str(tender_type))
		print("number_documents_attached: "+str(number_documents_attached))
		
		# num = driver.execute_script('return downloadtenderDoc()')
		num = driver.execute_script("return downloadtenderDoc()")
		driver.switch_to_window(driver.window_handles[-1])
		# save_pdf(data[1],driver.current_url)
		# print(driver.current_url)

		remote_file = urlopen(driver.current_url).read()
		memory_file = io.BytesIO(remote_file)
		pdf = pdftotext.PDF(memory_file)
		total_contant = "".join(pdf)
		result = re.findall('(2. ITEM)(.+)((?:\n.+)+)(T AND C)',total_contant)
		con_str = ""
		if result:
			con_str = ''.join(result[0])
		data = {
		"tender_id":data[1],
		"deptt_rly_unit":data[2],
		"tender_title":data[3],
		"status":data[4],
		"work_area":data[5],
		"due_date_time":data[6],
		"due_days":data[7],
		"detail_url":data[8],
		"tender_type":tender_type,
		"number_documents_attached":number_documents_attached,
		"item_description":con_str,
		"pdf_url":driver.current_url
		}
		headers = {
	        'Content-Type': 'application/json',
	    }
		response = requests.post('http://localhost:8000/post-tender/',data=data)

		time.sleep(20)
		driver.quit()
# get_details()
for search in search_parames:
	# driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
	driver = webdriver.Chrome()
	driver.implicitly_wait(10)
	driver.get("https://www.ireps.gov.in/")
	#time.sleep(5)
	#driver.maximize_window()
	driver.find_element_by_link_text("Search E-Tenders").click()
	driver.find_element_by_id("custumSearchId").click()
	Select(driver.find_element_by_name("searchOption")).select_by_visible_text("Item Description")
	time.sleep(5)
	driver.find_element_by_id("searchtext").send_keys(search)
	# Select(driver.find_element_by_id("division")).select_by_visible_text("Stores")
	# driver.find_element_by_name("dateFrom").__setattr__("value","03/10/2018")
	# 
	print("AFTERRRRRRRRR ONE MONNNN::")
	print(after_one_month)
	dateto=driver.find_element_by_name("dateTo")
	driver.execute_script('arguments[0].setAttribute("value","'+after_one_month+'");', dateto)
	# driver.execute_script('arguments[0].setAttribute("value","31/12/2018");', dateto)
	
	# driver.execute_script("document.find_element_by_name('dateTo').value = '03/10/2018';")
	print(driver.find_element_by_name("dateTo").get_attribute("value"))
	# driver.find_element_by_name("dateTo").send_keys("03/10/2018")
	# time.sleep(5)
	element1=driver.find_element_by_xpath("//*[@id='searchButtonBlock']/td/input[1]")
	hoverover =ActionChains(driver).move_to_element(element1).click().perform()
	time.sleep(10)
	# driver.back()
	# WebDriverWait(driver, 30).until(expected_conditions.title_contains("XML"))
	# driver.find_element_by_xpath("//*[@id='searchButtonBlock']/td/input[1]").click
	# print(driver.find_element_by_xpath("//*[@id='searchButtonBlock']/td/input[1]").get_attribute("value"))
	# driver.find_element_by_xpath("//*[@id='searchButtonBlock']/td/input[1]").click
	#for da in driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[7]/td/table/tr"):
	#    print("test ---------------------------- *****************************")
	try:
		search_results = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[6]/td/table/tbody/tr/td/b[2]")
		search_results = int(search_results.text)
		if search_results:
			pages = search_results/25
			reminder = search_results%25
			if reminder > 0:
				pages = pages+1
	except Exception as e:
		pages = 0
		# raise e
	
	if pages > 1:
		next_page_url = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[9]/td[2]/a[1]")
		next_page_url = next_page_url.get_attribute('href')
		parameters = next_page_url.split("&")
		j=1
		for parameter in parameters:
			parameter_name = parameter.split("=")
			if parameter_name[0] != 'pageNo':
				if j == 1:
					url = parameter
				else:
					url = url+'&'+parameter
				j+=1
		url = url+'&pageNo='
	for i in range(1, pages+1):
		if i !=1:
			driver.get(url+str(i))
		table = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[7]/td/table")
		rows = table.find_elements_by_tag_name("tr") # get all of the rows in the table
		total_tenders = []
		i =0
		for row in rows:
			tenders = {}
			if i >0:
			    deptt_rly_unit = row.find_element_by_xpath("td[1]") 
			    tenders['deptt_rly_unit'] = deptt_rly_unit.text
			    tender_id = row.find_element_by_xpath("td[2]/span") 
			    tenders['tender_id'] = tender_id.text
			    try:
			    	tender_title = row.find_element_by_xpath("td[3]/span/img").get_attribute("title")
			    	tenders['tender_title'] = tender_title
			    except Exception as e:
			    	tender_title = row.find_element_by_xpath("td[3]/span")
			    	tenders['tender_title'] = tender_title.text
			    status = row.find_element_by_xpath("td[4]")
			    tenders['status'] = status.text
			    work_area = row.find_element_by_xpath("td[5]")
			    tenders['work_area'] = work_area.text
			    due_date_time = row.find_element_by_xpath("td[6]")
			    tenders['due_date_time'] = due_date_time.text
			    due_days = row.find_element_by_xpath("td[7]")
			    tenders['due_days'] = due_days.text
			    detail_url = row.find_element_by_xpath("td[8]/a")
			    detail_url = detail_url.get_attribute("onclick")
			    detail_url = detail_url.replace("window.open('", '')
			    detail_url = detail_url.replace("')", '')
			    detail_url = detail_url.split(",")
			    tenders['detail_url'] = detail_url[0]
			    total_tenders.append(tenders)

			    # tds = table.find_elements_by_tag_name("td") 
			i+=1
		    # for t in tds:
		    #     print("--------------------")
		    # print(row.find_element_by_xpath("td[0]").get_attribute("value"))
		        # print(t.get_attribute('innerHTML'))
		#for tender in driver.css('td.boxStyle form table.advSearch tr:nth-child(7) td table tr'):
		#    print("------------------------------")
		# print(total_tenders)
	
		for ten in total_tenders:
			tender_id = ten['tender_id']
			detail_url = ten['detail_url']
			detail_url = 'https://www.ireps.gov.in'+detail_url

			deptt_rly_unit = ten['deptt_rly_unit']
			tender_title = ten['tender_title']
			status = ten['status']
			work_area = ten['work_area']
			due_date_time = ten['due_date_time'].strip()
			due_days = ten['due_days']
			tender_id = ten['tender_id']
			print("******")
			print(due_date_time+"::")
			due_date_time = datetime.strptime(str(due_date_time), '%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
			print(due_date_time)
			sql = """ select * from tender where tender_id='%s' """%(tender_id)
			cursor.execute(sql)
			datas = cursor.fetchall()
			if not datas:
				sql = """ insert into tender (tender_id,detail_url,deptt_rly_unit,tender_title,status,work_area,due_date_time,due_days,created_date) values ('%s',"%s",'%s','%s',"%s",'%s','%s',"%s",'%s')"""%(tender_id,detail_url,deptt_rly_unit,tender_title,status,work_area,due_date_time,due_days,created_date)
				cursor.execute(sql)
				print("New tender")
			else:
				print("Old tender")
		db.commit()
	time.sleep(10)
	driver.quit()

	if search == 'tapes':
		time.sleep(10)
		get_details()

db.close()



