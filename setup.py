import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

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
        'dev': [
            'coverage',
            'pytest',
            'pytest-cov',
            'mypy'
        ]
    },
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: MIT'
    ],
    entry_points = {
        'console_scripts': [
            'freshen-slack = fresh-slack.main:main'
        ]
    },
    include_package_data = True
)
