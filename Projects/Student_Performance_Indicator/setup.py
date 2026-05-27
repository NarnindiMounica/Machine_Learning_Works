from setuptools import find_packages, setup
from typing import List

def get_requirements(filepath:str)->List[str]:
    
    """this function will return the list of requirements"""
    requirements=[]
    with open(filepath, 'r') as file_obj:
        requirements = file_obj.readlines()
    requirements = [req.replace("\n", "") for req in requirements if req != "-e ."]
    return requirements

setup(
    name="student_performance",
    version=0.1,
    author="mounica",
    author_email="mounica.narnindi12@gmail.com",
    description="end to end project implementation",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)