from setuptools import setup, find_packages

setup(
    name='personal-assistant',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'assistant-bot=assistant.main:main',
        ],
    },
)