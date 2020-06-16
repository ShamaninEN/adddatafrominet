from getnewsfromlenta import pars_lenta
from pprint import pprint
from datetime import datetime
date_now = datetime.now()

lenta_report = pars_lenta(date_now)
pprint(f'update lenta: {lenta_report}')
