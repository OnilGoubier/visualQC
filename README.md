# visualQC
visualQC is an application package allowing data dan metadata quality control for instrument and technical managers, and seismologists. It's based on obspy (https://github.com/obspy/obspy/wiki).

The package contains the scripts to generate plots for a map of stations, data availability, instrument response by station or by channel, time waveforms by station or by channel and probabilistic power spectral densities (PPSD) by station, or only by channel. 

To install the package via the TestPyPi using pip, use the following command :

pip install --index-url https://test.pypi.org/simple visualQC

To test the scripts, use the following commands :

plotStationsMap -h
plotDataAvailability -h
plotInstrumentResponseS -h
plotInstrumentResponseC -h
plotTimeWaveformsS -h
plotTimeWaveformsC -h
plotPPSDSC -h
plotPPSDC -h
