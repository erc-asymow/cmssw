import FWCore.ParameterSet.Config as cms

muonvtxagniso04 = cms.EDProducer("MuonVtxAgnosticIsoProducer",
    muonInputTag = cms.InputTag("linkedObjects","muons"),
    pfCandidateInputTag = cms.InputTag("packedPFCandidates"),
    maxdr = cms.double(0.4),
    mindrchg = cms.double(1e-4),
    mindrrest = cms.double(0.01),
    maxdeltaz = cms.double(0.2),
    minptchg = cms.double(0.0),
    minptneu = cms.double(0.5),
    minptpho = cms.double(0.5),
    minptpu = cms.double(0.5),
    calculateNeutralPhoton = cms.int32(0)
)

muonvtxagniso03 = muonvtxagniso04.clone()
muonvtxagniso03.maxdr = cms.double(0.3)
