from graphviz import Digraph
from fpdf import FPDF

# Create conceptual map with Graphviz
dot = Digraph(comment="Morphogenesis Models Map", format='pdf')
dot.attr(rankdir='LR', size='10')

# Main categories
dot.node('B', 'Biophysical Models', shape='box', style='filled', color='lightblue')
dot.node('G', 'Genetic Models', shape='box', style='filled', color='lightgreen')
dot.node('C', 'Computational Models', shape='box', style='filled', color='lightyellow')

# Subtopics for Biophysical
dot.node('B1', 'Mechanical forces & tissue elasticity')
dot.node('B2', 'Actomyosin contractility')
dot.node('B3', 'Finite element tissue modeling')

# Subtopics for Genetic
dot.node('G1', 'Gene regulatory networks (GRNs)')
dot.node('G2', 'Signaling pathways in morphogenesis')
dot.node('G3', 'Single-cell omics integration')

# Subtopics for Computational
dot.node('C1', 'Reaction-diffusion systems')
dot.node('C2', 'Cellular Potts models')
dot.node('C3', 'Growth tensor simulations')

# Hybrid intersections
dot.node('BG', 'Mechanochemical models\n(Gene-mechanics coupling)', shape='ellipse', color='pink', style='filled')
dot.node('BC', 'Biomechanical simulation\nintegrated with PDE solvers', shape='ellipse', color='orange', style='filled')
dot.node('GC', 'GRN-driven computational\npattern formation', shape='ellipse', color='violet', style='filled')

# Connect categories to subtopics
dot.edges([('B', 'B1'), ('B', 'B2'), ('B', 'B3')])
dot.edges([('G', 'G1'), ('G', 'G2'), ('G', 'G3')])
dot.edges([('C', 'C1'), ('C', 'C2'), ('C', 'C3')])

# Connect hybrid models
dot.edge('B', 'BG')
dot.edge('G', 'BG')
dot.edge('B', 'BC')
dot.edge('C', 'BC')
dot.edge('G', 'GC')
dot.edge('C', 'GC')

# Render conceptual map to PDF
map_pdf_path = '/mnt/data/morphogenesis_models_map.pdf'
dot.render(map_pdf_path, cleanup=True)

map_pdf_path
