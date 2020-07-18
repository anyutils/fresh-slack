# Not currently used; in case I ever turn this into a formal package
import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements-dev.txt') as f:
    requirements_dev = f.read().split('\n')
    requirements_dev = [x for x in requirements_dev if x != '']

setuptools.setup(
    name = 'fresh-slack',
    version = '0.1.0',
    author = ['Ryan J. Price'],
    author_email = ['ryapric@gmail.com'],
    description = 'Like destalinator, but active',
    long_description = long_description,
    url = 'https://github.com/anyutils/fresh-slack',
    packages = setuptools.find_packages(),
    python_requires = '>= 3.6.*',
    # install_requires = [
    #     'pkg >= 0.1.0'
    # ],
    extras_require = {
        'dev': requirements_dev
    },
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: MIT'
    ],
    entry_points = {
        'console_scripts': [
            'freshen-slack = fresh_slack.main:main'
        ]
    },
    include_package_data = True
)
