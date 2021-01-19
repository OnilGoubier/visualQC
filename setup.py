import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visualQC", 
    version="0.0.1.3",
    #scripts=[ 
    #    'visualQC/graphicGenerator.py', 
    #    'visualQC/dirAndFiles.py'],
    #    'visualQC/plotStationsMap.py',
    #    'visualQC/plotDataAvailability.py'],
    author="IPGP",   
    author_email="goubier@ipgp.fr",
    description="Scripts used to generate data plots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OnilGoubier/visualQC",
    packages=setuptools.find_packages(),
    package_dir={"visualQC": 'visualQC'},
    # package_data and include_package_data = True are necessary to include config in .whl
    package_data={"visualQC": ['visualQC/config/config.ini']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'plotStationsMap = visualQC.plotStationsMap:main',
            'plotDataAvailability = visualQC.plotDataAvailability:main',
    ],
},

)
