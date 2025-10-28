	Contents

Abstract . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
Acknowledgements . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
1 Introduction and Motivation 14
1.1 Galaxies in the Universe . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
1.1.1 The Big Bang Theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
1.2 Dark Matter in the Universe . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
1.2.1 Evidence for Dark Matter . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
1.2.2 The Fundamental Nature of Dark Matter . . . . . . . . . . . . . . . . . . . . 23
1.3 Outstanding Galactic-scale Challenges to ΛCDM . . . . . . . . . . . . . . . . . . . . 27
1.3.1 The Hierarchical Structure Formation of Galaxies . . . . . . . . . . . . . . . . 27
1.3.2 Astrophysical Evidence for Hierarchical Structure Formation . . . . . . . . . 28
1.3.3 Simulations and Galactic-Scale Challenges to ΛCDM . . . . . . . . . . . . . . 29
1.4 Harnessing Disrupting Galaxies and their Tidal Debris . . . . . . . . . . . . . . . . 31
1.4.1 Tidal Debris as Records of Galaxy Formation . . . . . . . . . . . . . . . . . . 31
1.4.2 Tidal Debris as Probes of Dark Matter . . . . . . . . . . . . . . . . . . . . . . 32
1.4.3 Motivating Population Studies of Tidal Debris . . . . . . . . . . . . . . . . . 32
1.5 Thesis Outline . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33

2 Machine Learning the 6th Dimension: Stellar Radial Velocities from 5D Phase-
space Correlations 34

2.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
2.2 Methodology . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36
2.2.1 Mock Data Catalog . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36
2.2.2 Neural Network Architecture & Training . . . . . . . . . . . . . . . . . . . . . 37

11

2.3 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
2.4 Conclusions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43
3 Revealing the Milky Way’s Most Recent Major Merger with a Machine-learned
Catalog of Radial Velocities 46
3.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 47
3.2 Network Testing and Validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 49
3.2.1 Network Architecture and Error Sampling . . . . . . . . . . . . . . . . . . . . 51
3.2.2 High-Eccentricity Stars in the Test-Set Catalog . . . . . . . . . . . . . . . . . 54
3.3 Introducing the ML-RV Catalog . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 59
3.4 Features of GSE in the ML-RV Catalog . . . . . . . . . . . . . . . . . . . . . . . . . 59
3.4.1 Dynamics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 59
3.4.2 Metallicity Distribution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 61
3.4.3 Spatial Distribution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 63
3.5 Conclusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 65
4 StreamGen: Connecting Populations of Tidal Debris to their Host Galaxies 70
4.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 71
4.2 Simulations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 74
4.2.1 SatGen . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 74
4.2.2 Morphology Metric . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 77
4.2.3 StreamGen . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 79
4.2.4 Sample StreamGen Runs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 83
4.2.5 StreamGen Validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 85
4.3 Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 86
4.3.1 Fiducial Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 88
4.3.2 Variations of Host Properties and Feedback . . . . . . . . . . . . . . . . . . . 93
4.4 Discussion and Conclusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 98
5 The Galactic Sidekick: LMC-Induced Perturbations of Stellar Streams in FIRE102
5.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 103
5.2 Simulations and Modeling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 106
5.2.1 FIRE Simulations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 106
5.2.2 Stream Identification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 107

12

5.2.3 Potential Modeling with Basis Function Expansions . . . . . . . . . . . . . . 109
5.2.4 Modeling Direct Perturbations . . . . . . . . . . . . . . . . . . . . . . . . . . 111
5.3 LMC-Stream Interactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 113
5.3.1 Streams in Energy-Angular Momentum Space . . . . . . . . . . . . . . . . . . 113
5.3.2 Stream Orbits . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 114
5.3.3 Towards a Statistical Understanding of the LMC Analog’s Perturbations of
Stellar Streams . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 120
6 Conclusion and Outlook 121
6.1 Conclusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 121
6.2 Outlook . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 122
A Machine Learning the 6

th Dimension Supplementary Material 124
A.1 Network information . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 124
A.1.1 Tested Network Architectures . . . . . . . . . . . . . . . . . . . . . . . . . . . 124
A.1.2 Network Diagnostics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 126
A.2 Transforming Velocities and Uncertainties . . . . . . . . . . . . . . . . . . . . . . . . 129
A.3 Supplementary Figures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 131
B StreamGen Supplementary Material 134
B.1 Morphology Metric Uncertainty Analysis . . . . . . . . . . . . . . . . . . . . . . . . . 134
B.2 Additional Plots . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 136
C The Galactic Sidekick Supplementary Material 137
C.1 Supplemental Figures . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 137
Bibliography