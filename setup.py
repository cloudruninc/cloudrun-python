from setuptools import setup

setup(
    name='cloudrun',
    version='0.1.0',
    description='Python interface to Cloudrun API',
    author='Cloudrun Inc.',
    author_email='hello@cloudrun.co',
    url='https://github.com/cloudruninc/cloudrun-python',
    packages=['cloudrun'],
    install_requires=['pytest', 'requests', 'requests-toolbelt', 'responses'],
    test_suite='cloudrun.tests',
    license='MIT'
)
