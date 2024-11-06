from setuptools import setup,find_packages

from typing import List


HYPEN_E_DOT = '-e .'
def get_requirements(path):
    requirements = []
    with open(path) as fileobj:
        requirements = fileobj.readlines()
        requirements = [require.replace('\n','') for require in requirements ]
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name = 'Medical_insurence_claim_prediction',
    version='0.0.1',
    author='M Gnana Chaithanya',
    author_email='m.gnanachaithanya12@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('Requirements.txt')
)

