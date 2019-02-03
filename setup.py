from setuptools import setup

setup(
    name='web_log_parser',
    version='1.0.0',
    packages=['web_log_parser'],
    install_requires=['user_agents>=1.1.0'],
    entry_points={
        'console_scripts': [
            'web_log_parser = web_log_parser.__main__:main'
        ]
    },
    test_suite='tests'
)
