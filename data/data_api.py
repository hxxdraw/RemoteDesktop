from requests import get
from platform import platform


class Api(object):
    def __init__(self):
        """
        :service: https://ipdata.co
        """
        self.service_url = "https://api.ipdata.co?api-key="
        self.api_key = "e80f5e887499facfa70f182e3e28f389f645ad8554e63c6d152f9658"

    def GetLog(self):
        """
        Getting json log using api
        :return: str <data>
        """
        log_json = get(self.service_url + self.api_key).json()  # getting data from server
        ip = "IP: " + log_json['ip']  # IP
        provider = "Provider: " + log_json['asn']['name']  # PROVIDER
        domain = "Domain: " + log_json['asn']['domain']  # DOMAIN
        city = "City: " + log_json['city']  # CITY
        country = "Country: " + log_json['country_name']  # COUNTRY
        region = "Region: " + log_json['region']  # REGION
        sys = "Platform: " + platform()  # OS NAME
        return f'{ip}\n{provider}\n{domain}\n{city}\n{country}\n{region}\n{sys}'


