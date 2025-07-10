import setuptools
from distutils.core import setup

setup(
    name="task-tracker",
    version="0.0.0",
    description="CLI task tracker used to track and manage tasks",
    author="Jakub Stankiewicz",
    author_email="jakubstankiewicz024@gmail.com",
    packages=["task_tracker"],
    entry_points={
        "console_scripts":["tasktracker=task_tracker.entry:cli_entry_point"]
    }
)