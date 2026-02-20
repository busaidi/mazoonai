from setuptools import setup, find_packages

setup(
    name='framework',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Werkzeug',
        'Jinja2',
        'SQLAlchemy',
        'itsdangerous',
        'transformers',
        'torch',
    ],
)
