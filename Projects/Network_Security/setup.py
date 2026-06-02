from setuptools import find_packages, setup

def get_requirements(filepath)->list:
    with open(filepath, 'r') as fileobj:
        requirements = fileobj.readlines()
        requirements = [req.strip() for req in requirements if req!="- e." ]
        return requirements


setup(
    name="network_security_project",
    version=1.0,
    install_requires=get_requirements(filepath='requirements.txt'),
    packages=find_packages())