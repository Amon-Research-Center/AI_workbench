# CMCI Calibration Checklist

- Bench signals
  - [ ] Loopback test: split one generator to two channels; expect near-1 coherence at tone frequency
  - [ ] Multi-tone test: verify multiple peaks and linearity
  - [ ] Broadband noise: check flat PSD and low spurious coherence
- Synchronization
  - [ ] Verify shared clock/timing reference; measure drift over 1h
  - [ ] Cross-channel delay estimation and compensation
- Shielding/Grounding
  - [ ] Inspect cabling and grounding; measure cross-talk/isolation
  - [ ] Record with terminated inputs; quantify baseline noise floor
- Processing
  - [ ] Confirm `coherence_metrics.py` reproduces tone frequency and high MSC
  - [ ] Parameter sweep of `nperseg`; stability of coherence estimates
- Documentation
  - [ ] Save raw data, configs, and analysis outputs with checksums
  - [ ] Record environment (fs, gain, temperature, date)
