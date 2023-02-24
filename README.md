# Target_scanner
QE target scanner for SLACube
example comand
python3 DBScan_tracks.py selftrigger_2022_08_05_00_04_09_PDT_evd.h5 3,6,8,78

This code will take the 3rd, 6th, 8th and 78th tracks, plot them in 2D with a colorbar of charge and then run a DBscan on the tracks and break the tracks into clusters, then colorcode and plot those clusters, with noise being plotted in black. The centers of clusters are found from a charge weighted average in x and y and that is also plotted in black.
