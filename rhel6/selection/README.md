I will need to clean this up but you have to change out the code in the loop to decide what events you want to keep.  

Usage:
`python bsub_Sklimming.py -i <abspath/to/input/dir> --subdir <ouput/root/dir> --swdir <your/ldmx/build>`

Example command:
`python bsub_Sklimming.py -i /u/ey/ntran/ldmx/centralSamples/4pt0_gev_e_target_gamMuConv_v1_fieldmap/prod0_1e9_Feb26_SimToRecon --subdir  tmpSklim_prod0 --swdir /u/ey/ntran/ldmx/gammaMuConversion/master/ldmx-sw`