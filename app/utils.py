import os
import geoip2.database
from user_agents import parse

GEOIP_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'geoip', 'GeoLite2-City.mmdb')

def get_geo_info(ip):
    if not os.path.exists(GEOIP_DB_PATH):
        return {'country': None, 'city': None, 'isp': None}
    try:
        with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
            response = reader.city(ip)
            return {
                'country': response.country.name,
                'city': response.city.name,
                'isp': None  # MaxMind GeoLite2 gratuite ne contient pas ISP
            }
    except Exception:
        return {'country': None, 'city': None, 'isp': None}

def parse_user_agent(user_agent_string):
    user_agent = parse(user_agent_string)
    device_type = 'Other'
    if user_agent.is_mobile:
        device_type = 'Mobile'
    elif user_agent.is_tablet:
        device_type = 'Tablet'
    elif user_agent.is_pc:
        device_type = 'PC'

    return {
        'os_type': user_agent.os.family,
        'browser': user_agent.browser.family,
        'device_type': device_type,
    }
