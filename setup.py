from setuptools import setup, find_packages

setup(
    name='framework',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Werkzeug',
        'Jinja2',
        'SQLAlchemy',
        'itsdangerous',
    ],
)
