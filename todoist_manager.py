from dataclasses import dataclass

import pandas as pd
from todoist_api_python.api import TodoistAPI


@dataclass
class TaskLocation:
    """Class for keeping track of where a todoist item should be"""
    section_name: str
    section_id: float
    project_name: str
    project_id: float


class TodoistManager:
    def __init__(self, api_key: str, section_id: int, project_id: int):
        """
        Adds tasks to Todoist
        :param api_key: Todoist api key
        :param section_id: section to add task
        :param project_id:  project to add task
        """
        self.api = TodoistAPI(api_key)
        self._task_location = self._format_task_location(section_id, project_id)

    def _format_task_location(self, section_id: int, project_id: int) -> TaskLocation:
        """
        Check task location and return a TaskLocation object
        :param section_id: section to add task
        :param project_id: project to add task
        :return:
        """
        try:
            project = self.api.get_project(project_id=project_id)
        except Exception:
            raise Exception(f"Todoist project id not found: {project_id}")
        try:
            section = self.api.get_section(section_id=section_id)
        except Exception:
            raise Exception(f"Todoist section id not found: {section_id}")
        return TaskLocation(project_name=project.name, project_id=project.id, section_name=section.name,
                            section_id=section.id)

    def check_tasks(self, num_tasks: int) -> bool:
        """
        Ask user permission before adding tasks
        :param num_tasks: number of tasks to add
        :return: bool if user permission was granted
        """
        msg = f"Do you wish to add {num_tasks} tasks to {self._task_location.project_name} under {self._task_location.section_name}"
        if TodoistManager.yes_or_no(msg):
            return True
        else:
            raise Exception("Error in tasks to add")

    @staticmethod
    def yes_or_no(question) -> bool:
        """
        Ask and validate user permission
        :param question:
        :return: user input answer
        """
        reply = str(input(question + ' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
        else:
            return TodoistManager.yes_or_no("Please enter ")

    def add_tasks(self, tasks: pd.DataFrame, title: str) -> None:
        """

        :param tasks: mapping of dates and tasks
        :param title: title of book
        """
        self.check_tasks(len(tasks))
        for date, task in tasks.iterrows():
            try:
                self.api.add_task(
                    content=f"Read {title} pages {task['Pages']}",
                    description=f"Take notes and read {title} before due date",
                    due_date=date.strftime('%Y-%m-%d'),
                    section_id=self._task_location.section_id,
                    project_id=self._task_location.project_id
                )
            except Exception as error:
                print(error)
        print("Tasks successfully added")
