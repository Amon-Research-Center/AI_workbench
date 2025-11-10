# BMF Theory Development Environment Setup
# For broke genius mode scientific computing ($0.00 budget)
# Target: Complete scientific toolkit for Nobel Prize-worthy physics research

project_name: "Base Morphogenic Field Theory Development Environment"
budget: "$0.00"
target_os: ["linux"]

# Core development tools
development_tools:
  version_control:
    - name: "git"
      description: "Version control system"
      install_methods:
        ubuntu: "sudo apt install git"
        centos: "sudo yum install git"
        windows: "Download from https://git-scm.com/download/windows"
        macos: "brew install git"
      post_install:
        - "git config --global user.name 'BMF Researcher'"
        - "git config --global user.email 'vectortrust@protonmail.com'"

  python_ecosystem:
    - name: "python3"
      description: "Core programming language for simulations"
      install_methods:
        ubuntu: "sudo apt install python3 python3-pip python3-venv"
        centos: "sudo yum install python3 python3-pip"
        windows: "Download from https://python.org/downloads/"
        macos: "brew install python"
      
    - name: "python_packages"
      description: "Scientific computing packages"
      install_method: "pip3 install"
      packages:
        - "numpy"           # Mathematical operations
        - "scipy"           # Scientific computing
        - "matplotlib"      # Plotting and visualization
        - "sympy"           # Symbolic mathematics
        - "pandas"          # Data manipulation
        - "jupyter"         # Interactive notebooks
        - "plotly"          # Interactive visualizations
        - "seaborn"         # Statistical visualizations
        - "opencv-python"   # Image processing for experiments
        - "scikit-learn"    # Machine learning tools

# 3D modeling and visualization
graphics_tools:
  - name: "blender"
    description: "3D modeling for morphogenic field visualization"
    install_methods:
      ubuntu: "sudo snap install blender --classic"
      windows: "Download from https://www.blender.org/download/"
      macos: "brew install --cask blender"
    
  - name: "krita"
    description: "Digital art for scientific illustrations"
    install_methods:
      ubuntu: "sudo apt install krita"
      windows: "Download from https://krita.org/en/download/krita-desktop/"
      macos: "brew install --cask krita"
      
  - name: "gimp"
    description: "Image editing for publication graphics"
    install_methods:
      ubuntu: "sudo apt install gimp"
      windows: "Download from https://www.gimp.org/downloads/"
      macos: "brew install --cask gimp"
      
  - name: "inkscape"
    description: "Vector graphics for technical diagrams"
    install_methods:
      ubuntu: "sudo apt install inkscape"
      windows: "Download from https://inkscape.org/release/"
      macos: "brew install --cask inkscape"

# Scientific computation alternatives
alternatives:
  - name: "octave"
    description: "Free MATLAB alternative"
    install_methods:
      ubuntu: "sudo apt install octave"
      windows: "Download from https://www.gnu.org/software/octave/download.html"
      macos: "brew install octave"

# Documentation and publishing
documentation:
  - name: "texlive"
    description: "LaTeX distribution for scientific papers"
    install_methods:
      ubuntu: "sudo apt install texlive-full"
      windows: "Download MiKTeX from https://miktex.org/download"
      macos: "brew install --cask mactex"
      
  - name: "zotero"
    description: "Reference management"
    install_methods:
      ubuntu: "Download from https://www.zotero.org/download/"
      windows: "Download from https://www.zotero.org/download/"
      macos: "brew install --cask zotero"

# Experimental tools
experimental:
  - name: "arduino-ide"
    description: "Hardware experiment programming"
    install_methods:
      ubuntu: "sudo apt install arduino"
      windows: "Download from https://www.arduino.cc/en/software"
      macos: "brew install --cask arduino"
      
  - name: "audacity"
    description: "Audio analysis for cymatics experiments"
    install_methods:
      ubuntu: "sudo apt install audacity"
      windows: "Download from https://www.audacityteam.org/download/"
      macos: "brew install --cask audacity"

# Cloud-based alternatives (privacy-conscious)
cloud_alternatives:
  compute_platforms:
    - name: "AWS EC2 Free Tier"
      url: "https://aws.amazon.com/free/"
      description: "12 months free Linux instance, full control"
      privacy_note: "Acceptable - you control the instance"
      
    - name: "Google Colab"
      url: "https://colab.research.google.com/"
      description: "Free Jupyter with GPU - USE SPARINGLY"
      privacy_note: "Only for non-sensitive computations, avoid uploading core theory files"
      
  documentation:
    - name: "Overleaf"
      url: "https://www.overleaf.com/"
      description: "Online LaTeX editor"
      
  version_control:
    - name: "GitHub"
      url: "https://github.com/"
      description: "Free public repositories"
    - name: "GitLab"
      url: "https://gitlab.com/"
      description: "Alternative to GitHub with private repos"
    - name: "Codeberg"
      url: "https://codeberg.org/"
      description: "Privacy-focused Git hosting"

# Attribution and credit protection
attribution_strategy:
  copyright_notices:
    - "© 2025 Christopher Amon (Christopher M.)"
    - "Vector Trust Initiative"
    - "All rights reserved - Open source publication"
    
  timestamping:
    - name: "ArXiv preprint"
      description: "Establishes priority and timestamp"
    - name: "OSF preregistration"  
      description: "Academic timestamp service"
    - name: "Git commits"
      description: "Distributed timestamp proof"
      
  grant_eligibility:
    - name: "NSF EAGER grants"
      description: "Early-stage, untested ideas ($300K)"
    - name: "DOE Office of Science"
      description: "Fundamental physics research"
    - name: "Templeton Foundation"
      description: "Big questions in physics/consciousness"
    - name: "FQXi grants"
      description: "Foundational Questions Institute"
    - name: "Breakthrough Prize Foundation"
      description: "Fundamental physics breakthroughs"

# Project structure to create
project_structure:
  directories:
    - "bmf-theory/"
    - "bmf-theory/docs/"
    - "bmf-theory/src/"
    - "bmf-theory/simulations/"
    - "bmf-theory/experiments/"
    - "bmf-theory/visualizations/"
    - "bmf-theory/papers/"
    - "bmf-theory/data/"
    - "bmf-theory/tests/"

# Initial files to create
initial_files:
  - path: "bmf-theory/README.md"
    content: |
      # Base Morphogenic Field Theory
      ## Mathematical Framework for Foundational Reversion
      
      Author: Christopher Amon
      
      ### Abstract
      This repository contains the complete mathematical framework for the Base Morphogenic Field (BMF) theory, proposing that all reality consists of 5 fundamental operators acting on a base morphogenic field.
      
      ### Project Structure
      - `/docs/` - Theoretical documentation and papers
      - `/src/` - Python simulation code
      - `/simulations/` - Computational models
      - `/experiments/` - Laboratory experiment designs
      - `/visualizations/` - Blender and other visual models
      
  - path: "bmf-theory/requirements.txt"
    content: |
      numpy>=1.21.0
      scipy>=1.7.0
      matplotlib>=3.5.0
      sympy>=1.9.0
      pandas>=1.3.0
      jupyter>=1.0.0
      plotly>=5.0.0
      seaborn>=0.11.0
      opencv-python>=4.5.0
      scikit-learn>=1.0.0

# Installation script requirements
script_requirements:
  language: "python3 and bash"
  features:
    - "Cross-platform compatibility (Linux/Windows/MacOS)"
    - "Package manager detection (apt/yum/brew/chocolatey)"
    - "Error handling and logging"
    - "Progress indicators"
    - "Rollback capability on failures"
    - "Verification of successful installations"
    - "Creation of virtual environment for Python packages"
    - "Git repository initialization"
    - "Basic project structure setup"

# Success criteria
success_criteria:
  - "All tools install without errors"
  - "Python virtual environment created with all packages"
  - "Git repository initialized"
  - "Project structure created"
  - "All tools are accessible from command line"
  - "Jupyter notebook launches successfully"
  - "Blender opens and is functional"
  - "Basic test simulations run without errors"

# Post-installation tasks
post_installation:
  - "Initialize git repository in bmf-theory/"
  - "Create initial commit with project structure"
  - "Set up Python virtual environment"
  - "Install all Python packages in virtual environment"
  - "Create sample Jupyter notebook with BMF theory outline"
  - "Test all installations with simple commands"
  - "Generate installation report"

# Notes for AI assistant
ai_instructions: |
  Create a robust Python/Bash installation script that:
  1. Detects the operating system and package manager
  2. Installs all required tools in the correct order
  3. Handles dependencies and potential conflicts
  4. Creates the project structure
  5. Sets up a Python virtual environment
  6. Provides clear progress feedback
  7. Includes error handling and rollback
  8. Generates a final verification report
  
  The script should be idempotent (safe to run multiple times) and provide options for partial installation if some tools are already installed.
  
  Priority order: Git -> Python -> Python packages -> Graphics tools -> Optional tools
  
  Include a --dry-run option to show what would be installed without actually installing.