#ifndef TrackSplittingMonitor_H
#define TrackSplittingMonitor_H
// -*- C++ -*-
//
// Package:    TrackSplittingMonitor
// Class:      TrackSplittingMonitor
//
/**\class TrackSplittingMonitor TrackSplittingMonitor.cc DQM/TrackingMonitor/src/TrackSplittingMonitor.cc
 Monitoring source for general quantities related to tracks.
 */
// Original Author:  Nhan Tran
//         Created:  Thu 28 22:45:30 CEST 2008

#include <fstream>
#include <memory>
#include "DQMServices/Core/interface/DQMEDAnalyzer.h"
#include "DQMServices/Core/interface/DQMStore.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "Geometry/CSCGeometry/interface/CSCGeometry.h"
#include "Geometry/DTGeometry/interface/DTGeometry.h"
#include "Geometry/RPCGeometry/interface/RPCGeometry.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "TrackingTools/TransientTrackingRecHit/interface/TransientTrackingRecHitBuilder.h"

class TProfile;

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"

class TrackSplittingMonitor : public DQMEDAnalyzer {
public:
  explicit TrackSplittingMonitor(const edm::ParameterSet&);
  ~TrackSplittingMonitor() override;

  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void bookHistograms(DQMStore::IBooker&, edm::Run const&, edm::EventSetup const&) override;

private:
  void doProfileX(TH2* th2, MonitorElement* me);
  void doProfileX(MonitorElement* th2m, MonitorElement* me);

  // ----------member data ---------------------------

  //  unsigned int minTracks_;

  std::string histname;  //for naming the histograms according to algorithm used

  DQMStore* dqmStore_;
  edm::ParameterSet conf_;

  const edm::ESGetToken<MagneticField, IdealMagneticFieldRecord> mfToken_;
  const edm::ESGetToken<TrackerGeometry, TrackerDigiGeometryRecord> tkGeomToken_;
  const edm::ESGetToken<DTGeometry, MuonGeometryRecord> dtGeomToken_;
  const edm::ESGetToken<CSCGeometry, MuonGeometryRecord> cscGeomToken_;
  const edm::ESGetToken<RPCGeometry, MuonGeometryRecord> rpcGeomToken_;

  const TrackerGeometry* theGeometry;
  const MagneticField* theMagField;
  const DTGeometry* dtGeometry;
  const CSCGeometry* cscGeometry;
  const RPCGeometry* rpcGeometry;

  edm::InputTag splitTracks_;
  edm::InputTag splitMuons_;
  edm::EDGetTokenT<std::vector<reco::Track> > splitTracksToken_;
  edm::EDGetTokenT<std::vector<reco::Muon> > splitMuonsToken_;

  bool plotMuons_;
  int pixelHitsPerLeg_;
  int totalHitsPerLeg_;
  double d0Cut_;
  double dzCut_;
  double ptCut_;
  double norchiCut_;

  // histograms
  MonitorElement* ddxyAbsoluteResiduals_tracker_;
  MonitorElement* ddzAbsoluteResiduals_tracker_;
  MonitorElement* dphiAbsoluteResiduals_tracker_;
  MonitorElement* dthetaAbsoluteResiduals_tracker_;
  MonitorElement* dptAbsoluteResiduals_tracker_;
  MonitorElement* dcurvAbsoluteResiduals_tracker_;

  MonitorElement* ddxyNormalizedResiduals_tracker_;
  MonitorElement* ddzNormalizedResiduals_tracker_;
  MonitorElement* dphiNormalizedResiduals_tracker_;
  MonitorElement* dthetaNormalizedResiduals_tracker_;
  MonitorElement* dptNormalizedResiduals_tracker_;
  MonitorElement* dcurvNormalizedResiduals_tracker_;

  MonitorElement* ddxyAbsoluteResiduals_global_;
  MonitorElement* ddzAbsoluteResiduals_global_;
  MonitorElement* dphiAbsoluteResiduals_global_;
  MonitorElement* dthetaAbsoluteResiduals_global_;
  MonitorElement* dptAbsoluteResiduals_global_;
  MonitorElement* dcurvAbsoluteResiduals_global_;

  MonitorElement* ddxyNormalizedResiduals_global_;
  MonitorElement* ddzNormalizedResiduals_global_;
  MonitorElement* dphiNormalizedResiduals_global_;
  MonitorElement* dthetaNormalizedResiduals_global_;
  MonitorElement* dptNormalizedResiduals_global_;
  MonitorElement* dcurvNormalizedResiduals_global_;
};
#endif
