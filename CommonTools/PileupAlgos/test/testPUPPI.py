import FWCore.ParameterSet.Config as cms
process = cms.Process('TestPUPPIs')

process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")

#process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.load('CommonTools/PileupAlgos/Puppi_cff')
#from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.source.inputCommands = cms.untracked.vstring("keep *",
#                                                     "drop *_MEtoEDMConverter_*_*")
# Input source
process.source = cms.Source("PoolSource",
                            secondaryFileNames=cms.untracked.vstring(),
                            fileNames=cms.untracked.vstring(
                                #'/store/mc/RunIIAutumn18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/9E5D0032-E9FB-6646-B1AB-67EA8B95FCCD.root'
                                'file:/uscms_data/d3/yfeng/WMass/CMSSW_10_6_26/src/RecoMET/METPUSubtraction/test/0845F5F1-BEAA-2D42-AEA7-6B0E424FF356.root'
                            ),
                            skipEvents=cms.untracked.uint32(0)
                            )

#process.options = cms.untracked.PSet(
#  wantSummary = cms.untracked.bool(True),
#  Rethrow     = cms.untracked.vstring('ProductNotFound'),
#  fileMode    = cms.untracked.string('NOMERGE')
#)

process.sequence = cms.Sequence(process.puppiPVRobust)
process.p = cms.Path(process.sequence)
process.output = cms.OutputModule("PoolOutputModule",
                                  outputCommands = cms.untracked.vstring('keep *'),
                                  fileName       = cms.untracked.string ("Output.root")
)
# schedule definition                                                                                                       
process.outpath  = cms.EndPath(process.output) 
