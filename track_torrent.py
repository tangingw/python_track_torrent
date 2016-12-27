import requests
from bs4 import BeautifulSoup
import json


URL = "http://iknowwhatyoudownload.com"


def fetch_data(ip=None):

	params = {}

	if not ip is None:

		params={"ip": ip}

	req = requests.get(URL + "/en/peer/", params=params)
	
	if req.status_code == 200:
	
		return req.text
	
	error_page = """<html>
			<body>
				data not found
			<body>
			</html>
		     """
	return error_page


class IknowYourDownload(BeautifulSoup):

	def __init__(self, ip=None):

		self.ip = ip
		self.data = fetch_data(ip=self.ip)
		BeautifulSoup.__init__(self, self.data, 'lxml')

	def get_yourdata(self):

		data = dict()
		data["IP_Address"] = self.find("h3", {"itemprop": "about"}).text.split(" ")[-1]

		isp_data = tuple([item.text for item in self.find_all("span", {"class": "label label-primary"})])
		data["Country"] = isp_data[0]
		data["ISP_Name"] = isp_data[-1]	

		return data

	def get_torrent_data(self):

		header = tuple([item.text for item in self.find("thead", "header-torrents").find_all("th")] + ["Torrent_Link"])
		
		body_data = self.find("table", {"class": "table table-condensed table-striped"}).find("tbody")
		
		td_attribute_list = ["date-column", "category-column", "name-column", "size-column"]
		td_list = list()

		for td in td_attribute_list:

			td_list.append(body_data.find_all("td", {"class": td}))

		date_list = [(td_list[0][2*i].text, td_list[0][2*i + 1].text) for i in range(len(td_list[0])/2)]
		movie_title_list = [item.text.strip("'\n\r\n                ") for item in td_list[2]]	
		size_list = [item.text for item in td_list[3]]
		torrent_link_list = [URL + item.a["href"] for item in td_list[2]]
		category_list = [item.text for item in td_list[1]]

		result = dict()
		result["Result"] = list()

		for i in range(len(date_list)):

			result["Result"].append({"Entry_" + str(i + 1) :{
										header[0]: date_list[i][0], 
										header[1]: date_list[i][1], 
										header[2]: category_list[i], 
										header[3]: movie_title_list[i], 
										header[4]: size_list[i], 
										header[5]: torrent_link_list[i]
									}
						})

		result.update(self.get_yourdata())

		print json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True, separators=(",", ":"))


