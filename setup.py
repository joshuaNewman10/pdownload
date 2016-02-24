from setuptools import setup

setup(name='jdownload',
      version='0.1',
      description='Parallel file downloader',
      author='Ben Harris',
      author_email='benharris247@gmail.com',
      license='Apache',
      packages=['jdownload'],
      entry_points={
          'console_scripts': [
              'jdownload = pdownload.__main__:main'
          ]
      },
      zip_safe=False)