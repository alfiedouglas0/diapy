from setuptools import setup

setup(
    name='diapy',
    version='0.1.0',
    packages=['diapy'],
    entry_points={
        'console_scripts': [
            'diapy = diapy.__main__:main'
        ]
    },
    install_requires=[
        'npyscreen',
        'pysqlcipher3'
    ])
