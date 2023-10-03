from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in employee_checkin_location/__init__.py
from employee_checkin_location import __version__ as version

setup(
	name="employee_checkin_location",
	version=version,
	description="Employee Checkin Location",
	author="Ganu Reddy",
	author_email="ganu.b@caratred.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
