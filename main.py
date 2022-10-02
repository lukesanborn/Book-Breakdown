import datetime

import configargparse
import numpy as np
import pandas as pd
from dotenv import load_dotenv

from todoist_manager import TodoistManager

load_dotenv()

p = configargparse.ArgParser()
p.add_argument('--api_key', help='Todoist API key', env_var='API_KEY')
p.add_argument('--title', help='Title of the book', required=True, type=str)
p.add_argument('--pages', help='Number of pages', required=True, type=int)
p.add_argument('--project_id', help='Todoist project id for tasks', required=True, type=int)
p.add_argument('--section_id', help='Todoist section id for tasks', required=True, type=int)
p.add_argument('--start', help='start date (YYYY-MM-DD) or current day', required=False,
               type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'),
               default=datetime.date.today())
p.add_argument('--end', help='due date (YYYY-MM-DD) - exclusive', required=True,
               type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'))
options = p.parse_args()

drange = pd.date_range(options.start, options.end, inclusive='left')
pages = np.arange(1, options.pages + 1)
pages_per_day = [f"{x[0]}-{x[-1]}" for x in np.array_split(pages, len(drange), axis=0)]
work = pd.DataFrame(pages_per_day, index=drange, columns=["Pages"])

td = TodoistManager(api_key=options.api_key, section_id=options.section_id, project_id=options.project_id)
td.add_tasks(work, options.title)
