import re
import sys
from track_torrent import IknowYourDownload


def main():

	#By default, it will return the torrent tracker of your own ISP IP 
	#if there is no IP address.
	#
	#If you do $Terminal>python main.py aaa.bbb.ccc.ddd
	#It will return the torrent details of the given IP address.

	ip_address = None
	
	if len(sys.argv) > 2:

		if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", sys.argv[1]):
	
			ip_address = sys.argv[1]
			
	H = IknowYourDownload(ip_address)
	H.get_torrent_data()


if __name__ == "__main__":

	main()
