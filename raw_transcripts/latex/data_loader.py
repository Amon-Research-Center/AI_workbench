#!/usr/bin/env python3
"""
Load transcript data into the database
"""

import psycopg2
import psycopg2.extras
import os
from datetime import datetime

def load_initial_data():
    """Load the key breakthrough transcripts into database"""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "amon_field_db"),
        user=os.getenv("DB_USER", "postgres"), 
        password=os.getenv("DB_PASS", "password")
    )
    cursor = conn.cursor()
    
    # Initial content entries
    content_entries = [
        {
            'date': '2025-06-19',
            'title': 'The Original Spark',
            'filename': '20250619-original-spark',
            'summary': 'THE FOUNDATIONAL BREAKTHROUGH - First Turing-morphogenesis insight. "Substrate that all creation dances to."',
            'full_content': '''
            <div class="breakthrough-content">
                <h3>The Setting</h3>
                <p>Christopher was dealing with router issues, thinking about capacitors and electrical engineering...</p>
                
                <h3>The Breakthrough Moment</h3>
                <blockquote>
                "I have this crazy notion that Turing was on to something, that morphological equations 
                should be able to define the essence of the penultimate creator."
                </blockquote>
                
                <h3>The Full Vision</h3>
                <blockquote>
                "The substrate that all creation dances to and the only thing that's left when you take 
                away all created matter is God so in a sense everything is created in God image and from 
                Gods perspective all he needs is a little seed matter and it take form in a way patterned 
                after God morphogentically"
                </blockquote>
                
                <h3>What This Revealed</h3>
                <ul>
                    <li><strong>Substrate Reality:</strong> There's a fundamental substrate underlying all existence</li>
                    <li><strong>Pattern Formation:</strong> Reality emerges through morphogenic patterns</li>
                    <li><strong>Mathematical Framework:</strong> Turing's equations can describe ultimate reality</li>
                    <li><strong>Creative Abundance:</strong> Infinite potential from minimal "seed matter"</li>
                </ul>
            </div>
            ''',
            'content_type': 'transcript',
            'theory_tags': ['BMF', 'Substrate', 'Morphogenesis', 'Foundation'],
            'significance': 5,
            'is_public': True
        },
        {
            'date': '2025-07-13',
            'title': 'Foundation Conversations', 
            'filename': '20250713-foundation',
            'summary': 'Extended ChatGPT conversations building strategic framework and expanding core concepts.',
            'full_content': '''
            <div class="development-content">
                <h3>The Context</h3>
                <p>Weekend conversations while doing system maintenance, starting with Eric Weinstein research.</p>
                
                <h3>Key Developments</h3>
                <ul>
                    <li><strong>Academic Suppression:</strong> Understanding how revolutionary physics gets buried</li>
                    <li><strong>Strategic Planning:</strong> Sheldrake collaboration, George Knapp exclusive</li>
                    <li><strong>Framework Expansion:</strong> Building out the original substrate insight</li>
                    <li><strong>Economic Implications:</strong> Abundance vs artificial scarcity systems</li>
                </ul>
                
                <h3>The Strategic Shift</h3>
                <p>This conversation changed the approach from traditional academic channels to:</p>
                <ul>
                    <li>Collaborative partnerships with established researchers</li>
                    <li>Media platforms for credible public presentation</li>
                    <li>Defensive applications before offensive ones</li>
                    <li>Opt-out systems rather than confrontational approaches</li>
                </ul>
            </div>
            ''',
            'content_type': 'transcript',
            'theory_tags': ['Strategy', 'Framework', 'Development'],
            'significance': 4,
            'is_public': True
        },
        {
            'date': '2025-08-11',
            'title': 'Mathematical Breakthrough',
            'filename': '20250811-mathematical',
            'summary': 'DeepSeek collaboration formalizes theory into rigorous mathematics. Five fundamental operators emerge.',
            'full_content': '''
            <div class="mathematical-content">
                <h3>The Challenge</h3>
                <p>Converting brilliant insights into academically rigorous mathematics while preserving the original vision.</p>
                
                <h3>DeepSeek Collaboration</h3>
                <p>First systematic mathematical formalization of the morphogenic field theory:</p>
                
                <h4>Five Fundamental Operators Defined:</h4>
                <ul>
                    <li><strong>Point Operator (P̂):</strong> Localization and existence</li>
                    <li><strong>Line Operator (L̂):</strong> Connection and direction</li>
                    <li><strong>Curve Operator (Ĉ):</strong> Curvature and acceleration</li>
                    <li><strong>Movement Operator (M̂):</strong> Dynamics and evolution</li>
                    <li><strong>Resistance Operator (R̂):</strong> Constraint and stability</li>
                </ul>
                
                <h4>Master Equation:</h4>
                <div class="equation">
                    ∂²P/∂t² = C(L(P)) + M(P,t) + R(M(P,t)) + Λ
                </div>
                
                <h3>The Validation</h3>
                <p>Mathematics confirmed the intuitive insights were correct. Reality does operate on these principles, 
                and they can be precisely described and predicted.</p>
            </div>
            ''',
            'content_type': 'transcript',
            'theory_tags': ['Five_Operators', 'Mathematics', 'Formalization'],
            'significance': 5,
            'is_public': True
        }
    ]
    
    # Insert content entries
    for entry in content_entries:
        cursor.execute("""
            INSERT INTO content (date, title, filename, summary, full_content, content_type, theory_tags, significance, is_public)
            VALUES (%(date)s, %(title)s, %(filename)s, %(summary)s, %(full_content)s, %(content_type)s, %(theory_tags)s, %(significance)s, %(is_public)s)
        """, entry)
    
    # Add some sample equations
    cursor.execute("SELECT id FROM content WHERE filename = '20250811-mathematical'")
    math_content_id = cursor.fetchone()[0]
    
    equations = [
        {
            'content_id': math_content_id,
            'equation_latex': r'\frac{\partial^2 P}{\partial t^2} = C(L(P)) + M(P,t) + R(M(P,t)) + \Lambda',
            'description': 'Master equation showing how all physical phenomena emerge from five fundamental operators',
            'significance': 5
        },
        {
            'content_id': math_content_id, 
            'equation_latex': r'\hat{P} = \int \delta(r - r\') dr\'',
            'description': 'Point operator representing localization and existence',
            'significance': 4
        }
    ]
    
    for eq in equations:
        cursor.execute("""
            INSERT INTO equations (content_id, equation_latex, description, significance)
            VALUES (%(content_id)s, %(equation_latex)s, %(description)s, %(significance)s)
        """, eq)
    
    # Add connections between insights
    cursor.execute("SELECT id FROM content WHERE filename = '20250619-original-spark'")
    spark_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM content WHERE filename = '20250713-foundation'")
    foundation_id = cursor.fetchone()[0]
    
    cursor.execute("""
        INSERT INTO connections (from_content_id, to_content_id, relationship_type, description)
        VALUES (%s, %s, 'led_to', 'Original insight inspired extended framework development')
    """, (spark_id, foundation_id))
    
    cursor.execute("""
        INSERT INTO connections (from_content_id, to_content_id, relationship_type, description)  
        VALUES (%s, %s, 'led_to', 'Foundation conversations enabled mathematical formalization')
    """, (foundation_id, math_content_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ Initial data loaded successfully!")

if __name__ == "__main__":
    load_initial_data()