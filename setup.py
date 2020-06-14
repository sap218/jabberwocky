import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='jabberwocky',
      version='0.5.1.1',
      description='tool for ontologies',
      url='https://github.com/sap218/jabberwocky',
      author='Samantha C Pendleton',
      author_email='samanfapc@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
      zip_safe=False,
      entry_points = {'console_scripts': ['catch=catch.catch:main','bite=bite.bite:main','arise=arise.arise:main']},
      include_package_data = True
)
