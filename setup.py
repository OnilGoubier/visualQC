import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visualQC", 
    version="0.0.1.4.7",
    author="IPGP",   
    author_email="goubier@ipgp.fr",
    description="Scripts used to generate data plots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OnilGoubier/visualQC",
    packages = ['visualQC'],
    package_data={"visualQC": ['visualQC/config/config.ini']},
    include_package_data=True,
    data_files=[('data', ['visualQC/data/noise_models.npz'])],

    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'plotStationsMap = visualQC.plotStationsMap:main',
            'plotDataAvailability = visualQC.plotDataAvailability:main',
            'plotInstrumentResponseS = visualQC.plotInstrumentResponseS:main',
            'plotInstrumentResponseC = visualQC.plotInstrumentResponseC:main',
            'plotTimeWaveformsS = visualQC.plotTimeWaveformsS:main',
            'plotTimeWaveformsC = visualQC.plotTimeWaveformsC:main',
            'plotPPSDSC = visualQC.plotPPSDSC:main',
            'plotPPSDC = visualQC.plotPPSDC:main',
            'PlotStationsMap = visualQC.graphicGenerator:PlotStationsMap',
            'PlotDataAvailability = visualQC.graphicGenerator:PlotDataAvailability',
            'PlotTimeWaveformsS = visualQC.graphicGenerator:PlotTimeWaveformsS',
            'PlotTimeWaveformsC = visualQC.graphicGenerator:PlotTimeWaveformsC',
            'PlotInstrumentResponseS = visualQC.graphicGenerator:PlotInstrumentResponseS',
            'PlotInstrumentResponseC = visualQC.graphicGenerator:PlotInstrumentResponseC',
            'PlotPPSDSC = visualQC.graphicGenerator:PlotPPSDSC',
            'PlotPPSDC = visualQC.graphicGenerator:PlotPPSDC',
            'listOfFilesWithAbsName = visualQC.dirAndFiles:listOfFilesWithAbsName'
            'ModuleName = visualQC.graphicGenerator:ModuleName', 

    ],
},

)
