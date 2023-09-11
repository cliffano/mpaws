import os
import setuptools
from setuptools import sic
import yaml

info_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conf/info.yaml')
with open(info_file, 'r', encoding='utf8') as info_fh:
    info = yaml.load(info_fh, Loader=yaml.FullLoader)

readme_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.md')
with open(readme_file, 'r', encoding='utf8') as readme_fh:
    readme = readme_fh.read()

setuptools.setup(
    name='mpaws',
    description='Execute AWS CLI across multiple profiles in one go',
    version=sic(info['version']),
    author='Cliffano Subagio',
    author_email='cliffano@gmail.com',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/cliffano/mpaws',
    keywords=['mpaws', 'aws', 'cli', 'multi', 'multiple', 'profiles'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    py_modules=['mpaws'],
    entry_points={
        'console_scripts': [
            'mpaws = mpaws:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'boto3==1.28.44',
        'click==8.1.3',
        'conflog==1.5.1'
    ],
)
