from distutils.core import setup

setup(
    name='python-wrike',
    version='0.1.0',
    packages=['wrike'],
    url='https://github.com/adalekin/python-wrike.git',
    license='MIT',
    author='Aleksey Dalekin',
    author_email='adalekin@gmail.com',
    description='',
    install_requires=[
        'requests',
        'requests_oauth2',
        'six'
    ],
)
