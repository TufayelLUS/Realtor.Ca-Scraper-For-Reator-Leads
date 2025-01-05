import requests
from bs4 import BeautifulSoup as bs
import json
import csv
import os
from time import sleep

'''
Libraries to install
pip install requests bs4


To hire me for projects related to web scraping or any python automation related tasks,
please reach out to https://www.fiverr.com/thechoyon
Your request must adhere the terms of use guidelines of your target website
'''

# get it from your browser if it stops working or increase check_delay value below
# if 
page_cookie = 'Language=1; app_mode=1; Currency=CAD; GUID=62137c76-c7e4-4663-a5d8-546607e0660f; gig_bootstrap_3_mrQiIl6ov44s2X3j6NGWVZ9SDDtplqV7WgdcyEpGYnYxl7ygDWPQHqQqtpSiUfko=gigya-pr_ver4; __AntiXsrfToken=eb577fbef9b8443cac82e294c094bfa8; visid_incap_2269415=//ash/hBRWuKkwgYTzCRIiGsemcAAAAAQUIPAAAAAACsCUKPChcjGjVyOeaf0bz9; nlbi_2269415=jqdpbQkMd2X3DVwACcuCgwAAAABvzj9STA4a+tNGTPMBq/RQ; visid_incap_3157676=pXVOsCX3TAagDSn3obvLqCKsemcAAAAAQUIPAAAAAACMmwtBqFT5RXebOyR3Bvff; incap_ses_33_3157676=SlbhF+IaNRZMtrEoiT11ACKsemcAAAAAJ93YRR1akVqfi8ETD7W0Kg==; TermsOfUseAgreement=2018-06-07; incap_ses_33_2269415=L447RKygpUcqD/AoiT11ACfCemcAAAAAycUinLHHkkgqsGX+aFPdIg==; reese84=3:C9JntuATiZEFa747mNfBCA==:NRo22LW5mIAv2BBZptqfhY1zvV4fSHRMUqBroPw6J1L66ee++usqs/u4p4fFTcYeNJsMeirsHz2vy6q6+i5mRtGQR+hJ9B6Xca/DE+tc8BLRAPAQmXVEkXqGvRwCHeNNjPjafoSgtGXXTG8Ps9Tlv3l9ZGHLPKtAdvr4LHYNaVNz0pUBTUsHjuZaW3sWz42Z6Vgx+jTrVNsl8aN/VPeFL2PxMuyI9hrtKqsFNGn2/HpMMHtizqKA88lFYOnj8Y1CFWfcFgQyAjcdbxAU0Rhwg1LxXH63I8x0sXfrR9oC03gig86sxYpv272DdvvKYQZv7pjHn+f1LXEDJaVDX2j0I/j5/1aWVEDZ5Ki/1bcsln/Yubc04RhuNxNNXUZUpywXpuqJ19ihNrCHTzC1aTMrAJmFRnKBasNNOx+Q8155PLTgPiEfC29cvqrmB4lDvkP5ipgQ3HvD7QKiAA21zSLdzA==:DdyDf4mRaof2fxDi+ARZMBXIs4rUkt6YgXbf0W9jleI=; nlbi_2269415_2147483392=J1rvWnS8EVdPmcsoCcuCgwAAAABT3wam9AhO3vePJjebpjpt'
# place the name of the city for which you want to get the realtor list
city_name = "ottawa"
# number of seconds to wait before checking for next results
check_delay = 5
s = requests.Session()


class RealtorScraper:
    def __init__(self):
        self.url = 'https://www.realtor.ca/Services/ControlFetcher.asmx/GetRealtorResults'
        self.csv_name = f'{city_name}.csv'

    def paginateResults(self):
        headers = {
            'content-type': 'application/json',
            'cookie': page_cookie,
            'referer': 'https://www.realtor.ca/realtor-search-results',
            'dnt': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        page_no = 1
        while True:
            # here you can apply more filters but this is just a showcasing project, hence lacking functionalities for now
            data = {
                "firstName": "",
                "lastName": "",
                "addressLine1": "",
                "city": city_name,
                "companyName": "",
                "designations": "",
                "languages": "",
                "postalCode": "",
                "provinceIds": "",
                "specialties": "",
                "isCCCMember": "",
                "currentPage": str(page_no),
                "sortBy": "11",
                "sortOrder": "A",
                "organizationId": "",
                "recordsPerPage": 50,
                "maxRecords": None,
                "showOfficeDetails": None,
                "disablePhoneNumberDisplay": None,
                "disableFaxNumberDisplay": False,
                "isForSEOLandingPage": False
            }

            try:
                resp = s.post(
                    self.url, headers=headers, data=json.dumps(data)).json()
            except:
                print("Failed to open {}".format(self.url))
                print("Please access realtor website from your browser again to recover cookies")
                sleep(check_delay)
                continue
            page_html = resp.get('d')
            if page_html.startswith('Error:'):
                print("Please update cookies again!")
                return
            soup = bs(page_html, 'html.parser')
            cards = soup.find_all(
                'div', {'class': 'realtorSearchResultCardCon'})
            print("Page {} has {} records".format(page_no, len(cards)))
            if len(cards) == 0:
                break
            for card in cards:
                try:
                    realtor_name = card.find(
                        'span', {'class': 'realtorCardName'}).text.strip()
                except:
                    continue
                try:
                    position = card.find(
                        'div', {'class': 'realtorCardTitle'}).text.strip()
                except:
                    position = ""
                try:
                    company = card.find(
                        'div', {'class': 'realtorCardOfficeName'}).text.strip()
                except:
                    company = ""
                try:
                    office_type = card.find(
                        'div', {'class': 'realtorCardOfficeDesignation'}).text.strip()
                except:
                    office_type = ""
                try:
                    address = card.find(
                        'div', {'class': 'realtorCardOfficeAddress'}).text.strip()
                except:
                    address = ""
                try:
                    phone = card.find(
                        'span', {'class': 'realtorCardContactNumber'}).text.strip()
                except:
                    phone = ""
                print("Realtor: {}".format(realtor_name))
                print("Position: {}".format(position))
                print("Company: {}".format(company))
                print("Office Type: {}".format(office_type))
                print("Address: {}".format(address))
                print("Phone: {}".format(phone))
                dataset = [
                    realtor_name,
                    position,
                    company,
                    office_type,
                    address,
                    phone
                ]
                self.saveData(dataset)
            page_no += 1
            sleep(check_delay)

    def saveData(self, dataset):
        with open(self.csv_name, mode='a+', encoding='utf-8-sig', newline='') as csvFile:
            fieldnames = ["City", "Realtor Name", "Position",
                          "Company", "Office Type", "Address", "Phone"]
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames,
                                    delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if os.stat(self.csv_name).st_size == 0:
                writer.writeheader()
            writer.writerow({
                "City": city_name,
                "Realtor Name": dataset[0],
                "Position": dataset[1],
                "Company": dataset[2],
                "Office Type": dataset[3],
                "Address": dataset[4],
                "Phone": dataset[5]
            })


if __name__ == "__main__":
    client = RealtorScraper()
    client.paginateResults()
