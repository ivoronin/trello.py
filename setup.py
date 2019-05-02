from setuptools import setup, find_packages

version = '0.0.1'

requirements = []
with open('requirements.txt') as f:
	requirements = f.read().splitlines()

readme = ''
with open('README.md') as f:
	readme = f.read()

setup(
	name='trello.py',
	author='Ilya Voronin',
	url='https://github.com/ivoronin/trello.py',
	project_urls={
		'Documentation': 'https://trello-py.readthedocs.io/en/latest/',
		'Issue tracker': 'https://github.com/ivoronin/trello.py/issues'
	},
	version=version,
	packages=['trello'],
	license='Unlicense',
	description='Python Trello API client',
	long_description=readme,
	long_description_content_type="text/x-rst",
	install_requires=requirements,
	python_requires='>=3.5',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: Freely Distributable',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Topic :: Internet',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Utilities'
		]
	)
