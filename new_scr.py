import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import MySQLdb
try:
	db = MySQLdb.connect('localhost','root','root@123','railway')
except Exception as e:
	print("ERRORRRRRRR ----- -----")
	print(e)
search_parames = ['anbond','adhcsive','loctite','dow cornind','molykote','grease','lubricant','silicone','sealants','chemicals','paints','polyurethane','sikaflex','cleaners','tapes']
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
	driver.execute_script('arguments[0].setAttribute("value","03/10/2018");', dateto)
	# driver.execute_script("document.find_element_by_name('dateTo').value = '03/10/2018';")
	print(driver.find_element_by_name("dateTo").get_attribute("value"))
	# driver.find_element_by_name("dateTo").send_keys("03/10/2018")
	# time.sleep(5)
	element1=driver.find_element_by_xpath("//*[@id='searchButtonBlock']/td/input[1]")
	hoverover =ActionChains(driver).move_to_element(element1).click().perform()
	time.sleep(20)
	# driver.back()
	# WebDriverWait(driver, 30).until(expected_conditions.title_contains("XML"))
	# driver.find_element_by_xpath("//*[@id='searchButtonBlock']/td/input[1]").click
	# print(driver.find_element_by_xpath("//*[@id='searchButtonBlock']/td/input[1]").get_attribute("value"))
	# driver.find_element_by_xpath("//*[@id='searchButtonBlock']/td/input[1]").click
	#for da in driver.find_element_by_xpath("/html/body/table/tbody/tr[4]/td[2]/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table[3]/tbody/tr[7]/td/table/tr"):
	#    print("test ---------------------------- *****************************")
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
	cursor = db.cursor()
	for ten in total_tenders:
		tender_id = ten['tender_id']
		sql = """ select * from tenders where tender_id='%s' """%(tender_id)
		cursor.execute(sql)
		datas = cursor.fetchall()
		if not datas:
			sql = """ insert into tenders (tender_id) values ('%s')"""%(tender_id)
			cursor.execute(sql)
			print("New tender")
		else:
			print("Old tender")
	
	time.sleep(10)
	driver.quit()
db.commit()
db.close()

