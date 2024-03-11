import FWCore.ParameterSet.Config as cms
from RecoMET.METPUSubtraction.deepMETProducer_cfi import deepMETProducer
from RecoMET.METPUSubtraction.deepMETPVRobustProducer_cfi import deepMETPVRobustProducer

process = cms.Process('DeepMET')

process.task = cms.Task()

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load(
    'Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(200)
)

# Input source
process.source = cms.Source("PoolSource",
                            secondaryFileNames=cms.untracked.vstring(),
                            fileNames=cms.untracked.vstring(
                                #'/store/mc/RunIIAutumn18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/9E5D0032-E9FB-6646-B1AB-67EA8B95FCCD.root'
                                'file:/uscms_data/d3/yfeng/WMass/CMSSW_10_6_26/src/RecoMET/METPUSubtraction/test/0845F5F1-BEAA-2D42-AEA7-6B0E424FF356.root'
                            ),
                            skipEvents=cms.untracked.uint32(0)
                            )

process.deepMETPVRobustProducer = deepMETPVRobustProducer.clone(
    do_print=cms.bool(True), 
    ignore_leptons = cms.bool(True)
)

process.deepMETPVRobustNoPUPPIProducer = deepMETPVRobustProducer.clone(
    do_print=cms.bool(True), 
    ignore_leptons = cms.bool(True), 
    usePUPPI = cms.bool(False),
    graph_path = cms.string('RecoMET/METPUSubtraction/data/deepmet_pvrobust/deepmet_pvrobust_nopuppi.pb')
)

process.deepMETProducer = deepMETProducer.clone(
    do_print=cms.bool(True), 
    ignore_leptons = cms.bool(True)
)

process.load('CommonTools/PileupAlgos/Puppi_cff')
#process.deepMETPVRobustProducer.pf_src = cms.InputTag("puppiPVRobust")
#process.deepMETPVRobustNoPUPPIProducer.pf_src = cms.InputTag("puppiPVRobust")
process.sequence = cms.Sequence(process.puppiPVRobust + process.deepMETPVRobustProducer + process.deepMETPVRobustNoPUPPIProducer + process.deepMETProducer)

#process.sequence = cms.Sequence(process.deepMETPVRobustProducer + process.deepMETPVRobustNoPUPPIProducer + process.deepMETProducer)

process.p = cms.Path(process.sequence)
process.output = cms.OutputModule("PoolOutputModule",
                                  outputCommands=cms.untracked.vstring(
                                      'keep *'),
                                  fileName=cms.untracked.string(
                                      "DeepMETTest.root")
                                  )
process.outpath  = cms.EndPath(process.output)
