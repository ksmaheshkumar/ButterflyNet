from setuptools import setup
import sys, os

if not os.environ.get("CIRCLE_USERNAME", None):
    if not sys.version_info >= (3, 4, 0):
        sys.exit("Sorry, this library requires Python 3.4 or higher.")


setup(
    name='ButterflyNet',
    version='0.0.1',
    packages=['bfnet'],
    url='https://butterflynet.veriny.tf',
    license='AGPLv3',
    author='Isaac Dickinson',
    author_email='eyesismine@gmail.com',
    description='A better networking library.',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries"
    ],
    tests_require=["pytest", "tox", "tox-pyenv"],
    setup_requires=['pytest-runner'],
)
