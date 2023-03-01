import sys
import logging

logging.basicConfig(level=logging.DEBUG, filename="/var/www/html/crm.abcbbr.org/logs/crm.abcbbr.org.log", format="%(asctime)s %(message)s")
sys.path.insert(0, "/var/www/html/crm.abcbbr.org")
sys.path.insert(0, "/var/www/html/crm.abcbbr.org/env/lib/python3.8/site-packages")
from app import app as application