'''
Check status of flight arriving at Zurich Airport. Sounds a beep if status changes.
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time
import winsound

frequeny = 2000  # Hz
duration = 2000  # 1000 = 1sec

driver = webdriver.Firefox()

driver.get("https://www.zurich-airport.com/passengers-and-visitors/arrivals-and-departures/arrivals")

input("You have to manually give cookie consent and then press 'Enter'.")
airport_dep = str(input("Departing Airport: "))
flight_no = str(input("Flight Number: "))

scroll = input("Flight is on next page? [y/n]")
if scroll in ["y", "yes", "Y", "Yes"]:
    later_button = driver.find_element_by_id("later2")
    later_button.click()

print("searching for flight from '%s' with flight number '%s'" % (airport_dep, flight_no))

first = True
status = ""
while True:
    table_rows = driver.find_elements(By.TAG_NAME, "tr")

    # print(len(table_rows))

    counter = 0  # iteration counter for location on table row list
    save_loc = []  # save location of city in table row list
    for row in table_rows:
        counter += 1
        td_text = row.text
        # print(td_text)
        if airport_dep in td_text and flight_no in td_text:
            save_loc.append(counter-1)

    if len(save_loc) == 0:
        print("Your flight has not been found")
    else:
        table_row = []
        # title_row = ["Time: ", "| Expected: ", "| From: ", "| Airport: ", "| Flight: ", "| Arrival: ",
        #  "| Baggage Claim: ", "| Status: "]
        for item in save_loc:
            table_row = table_rows[item].text.split("\n")
            len_row = len(table_row)
            print(table_row)
            # out_list = []
            # for i in range(len_row):
            #     out_list.append(title_row[i])
            #     out_list.append(str(table_row[i]))
            # print("".join(out_list))
            # print(len(table_row), "length table row")
            # print(type(table_row), "type table row")

        new_status = table_row[-1]
        if new_status != status:
            winsound.Beep(frequeny, duration)
            status = new_status

    time.sleep(60)
