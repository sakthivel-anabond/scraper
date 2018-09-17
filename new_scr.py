import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import MySQLdb
import datetime
current_date = datetime.datetime.now()
after_one_month = current_date.strftime("%d/%m/%Y")
created_date = current_date.strftime("%Y-%m-%d")
try:
	db = MySQLdb.connect('localhost','root','root@123','railway')
	cursor = db.cursor()
except Exception as e:
	print("ERRORRRRRRR ----- -----")
	print(e)
# search_parames = ['anbond','adhcsive','loctite','dow cornind','molykote','grease','lubricant','silicone','sealants','chemicals','paints','polyurethane','sikaflex','cleaners','tapes']
search_parames = ['adhesive','loctite']



def get_details():
	print("***********")
	sql = """ select * from tenders where created_date='%s' """%(created_date)
	cursor.execute(sql)
	datas = cursor.fetchall()
	for data in datas:
		print(data[2])
		print("-------")
		driver = webdriver.Chrome()
		driver.implicitly_wait(10)
		driver.get(data[2])
		# num = driver.execute_script('return downloadtenderDoc()')
		num = driver.execute_script("return downloadtenderDoc()")
		
		print("**********@@@@@@@@")
		print(num);
		print(driver.current_url)
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
	dateto=driver.find_element_by_name("dateTo")
	# driver.execute_script('arguments[0].setAttribute("value","'+after_one_month+'");', dateto)
	driver.execute_script('arguments[0].setAttribute("value","31/12/2018");', dateto)
	
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
	search_results = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[6]/td/table/tbody/tr/td/b[2]")
	search_results = int(search_results.text)
	if search_results:
		pages = search_results/25
		reminder = search_results%25
		if reminder > 0:
			pages = pages+1
	print(pages)
	print("TOTAL PAGESSSSS ***********")
	if pages > 1:
		next_page_url = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[9]/td[2]/a[1]")
		next_page_url = next_page_url.get_attribute('href')
		parameters = next_page_url.split("&")
		print(next_page_url)
		print("################################")
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
			print("URLLLLLLLLLLLL ******** !!!!!!")
			print(url)
			print("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[9]/td[2]/a[%s]" % i)
			print('///////////////')
			# driver = webdriver.Chrome()
			# driver.implicitly_wait(10)
			# driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[9]/td[2]/a[%s]" % i).click()

			# driver.find_element_by_link_text(str(i)).click()
			driver.get(url+str(i))

		table = driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[7]/td/table")
		# print(table.get_attribute('innerHTML'))
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
		print(total_tenders)
	
		for ten in total_tenders:
			tender_id = ten['tender_id']
			detail_url = ten['detail_url']
			detail_url = 'https://www.ireps.gov.in'+detail_url
			sql = """ select * from tenders where tender_id='%s' """%(tender_id)
			cursor.execute(sql)
			datas = cursor.fetchall()
			if not datas:
				sql = """ insert into tenders (tender_id,detail_url,created_date) values ('%s',"%s",'%s')"""%(tender_id,detail_url,created_date)
				cursor.execute(sql)
				print("New tender")
			else:
				print("Old tender")
		
	time.sleep(10)
	driver.quit()

	if search == 'loctite':
		get_details()
db.commit()
db.close()



