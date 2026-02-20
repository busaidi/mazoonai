from setuptools import setup, find_packages

setup(
    name='mazoonai-django',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'Django>=5.0,<6.0',
        'transformers',
        'torch',
    ],
)
