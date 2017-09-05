import sys

from LDMX.Framework import ldmxcfg

p=ldmxcfg.Process("recon")

p.libraries.append("libEventProc.so")

ecalDigis = ldmxcfg.Producer("ecalDigis","ldmx::EcalDigiProducer")
ecalDigis.parameters["meanNoise"] = 0.015
ecalDigis.parameters["readoutThreshold"] = ecalDigis.parameters["meanNoise"]*3

hcalDigis = ldmxcfg.Producer("hcalDigis", "ldmx::HcalDigiProducer")
hcalDigis.parameters["meanNoise"] = 1.5

ecalVeto = ldmxcfg.Producer("ecalVeto", "ldmx::EcalVetoProcessor")
ecalVeto.parameters["num_ecal_layers"] = 50
ecalVeto.parameters["back_ecal_starting_layer"] = 22
ecalVeto.parameters["do_bdt"] = 0
ecalVeto.parameters["bdt_file"] = "bdt_data_train_FALSE.pkl"
ecalVeto.parameters["disc_cut"] = 0.995

hcalVeto = ldmxcfg.Producer("hcalVeto", "ldmx::HcalVetoProcessor")
hcalVeto.parameters["pe_threshold"] = 8.0

trigger = ldmxcfg.Producer("trigger", "ldmx::TriggerProcessor")
trigger.parameters["threshold"] = 12.0
trigger.parameters["mode"] = 0
trigger.parameters["start_layer"] = 1
trigger.parameters["end_layer"] = 16

findable_track = ldmxcfg.Producer("findable", "ldmx::FindableTrackProcessor")

p.histogramFile = "histo.root"

p.sequence=[ecalDigis, hcalDigis, ecalVeto, hcalVeto, trigger, findable_track]

p.inputFiles=["$input"]
p.outputFiles=["$output"]

p.printMe()