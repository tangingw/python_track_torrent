import re
import sys
from track_torrent import IknowYourDownload


def main():

	ip_address = None
	
	if len(sys.argv) > 2:

		if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", sys.argv[1]):
	
			ip_address = sys.argv[1]
			
	H = IknowYourDownload(ip_address)
	H.get_torrent_data()


if __name__ == "__main__":

	main()
