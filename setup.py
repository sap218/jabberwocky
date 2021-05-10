import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='jabberwocky',
      version='2.0.0.0',
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
      entry_points = {'console_scripts': ['jab-bandersnatch=bandersnatch.bandersnatch:main','jab-catch=catch.catch:main','jab-bite=bite.bite:main','jab-arise=arise.arise:main']},
      include_package_data = True
)
