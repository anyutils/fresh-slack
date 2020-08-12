# Not currently used; in case I ever turn this into a formal package
import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = f.read().split('\n')
    install_requires = [x for x in install_requires if x != '']

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
    install_requires = install_requires,
    extras_require = {
        'dev': [
            'pytest >= 5.4.3',
            'pytest-cov >= 2.10.0',
            'coverage >= 5.2',
            'mypy >= 0.782'
        ]
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
