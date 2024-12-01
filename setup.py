from setuptools import setup

setup(
    name='aoc_import',
    version='0.1',
    py_modules=['aoc_import'],
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points='''
        [console_scripts]
        aoc-import=aoc_import:main
    ''',
)
