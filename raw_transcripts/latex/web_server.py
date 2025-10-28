#!/usr/bin/env python3
"""
Amon Field Theory Interactive Database Server
Serves both personal transcript exploration and public theory website
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles  
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import psycopg2.extras
from typing import List, Optional
import os
import json
from datetime import datetime

app = FastAPI(title="Amon Field Theory Explorer")

# CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "amon_field_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "password")
    )

@app.get("/")
async def root():
    """Main landing page - timeline view"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Amon Field Theory - Interactive Development Story</title>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            body { font-family: 'Segoe UI', sans-serif; margin: 0; background: #0a0a0a; color: #fff; }
            .timeline { width: 100%; height: 200px; margin: 20px 0; }
            .content-grid { display: grid; grid-template-columns: 1fr 2fr 1fr; gap: 20px; padding: 20px; }
            .card { background: #1a1a2e; border-radius: 10px; padding: 20px; cursor: pointer; }
            .card:hover { background: #16213e; transform: translateY(-2px); }
            .breakthrough { border-left: 4px solid #00ff88; }
            .development { border-left: 4px solid #ffd700; }
            .application { border-left: 4px solid #ff6b6b; }
            .nav-link { color: #00ff88; text-decoration: none; }
            .nav-link:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div style="text-align: center; padding: 40px;">
            <h1>🌌 Amon Field Theory</h1>
            <p><em>The Interactive Development Story</em></p>
        </div>
        
        <div id="timeline" class="timeline"></div>
        
        <div class="content-grid">
            <div class="card breakthrough" onclick="loadContent('20250619-original-spark')">
                <h3>🌟 Original Spark</h3>
                <p>June 19, 2025</p>
                <p>"Morphological equations can define the essence of the penultimate creator"</p>
            </div>
            
            <div class="card development" onclick="loadContent('20250713-foundation')">
                <h3>🏗️ Foundation Conversations</h3>
                <p>July 13-14, 2025</p>
                <p>Extended framework development and strategic planning</p>
            </div>
            
            <div class="card breakthrough" onclick="loadContent('20250811-mathematical')">
                <h3>📐 Mathematical Breakthrough</h3>
                <p>August 11, 2025</p>
                <p>Five fundamental operators formalized with rigorous mathematics</p>
            </div>
        </div>
        
        <div id="content-detail" style="padding: 20px; display: none;">
            <div id="detail-content"></div>
        </div>

        <script>
            async function loadContent(contentId) {
                const response = await fetch(`/content/${contentId}`);
                const content = await response.json();
                
                document.getElementById('content-detail').style.display = 'block';
                document.getElementById('detail-content').innerHTML = `
                    <div style="background: #1a1a2e; border-radius: 10px; padding: 30px; margin: 20px 0;">
                        <h2>${content.title}</h2>
                        <p><strong>Date:</strong> ${content.date}</p>
                        <div>${content.summary}</div>
                        <hr style="border-color: #333; margin: 20px 0;">
                        <div>${content.full_content}</div>
                        
                        <div style="margin-top: 30px;">
                            <h4>🔗 Related Insights:</h4>
                            ${content.connections.map(conn => 
                                `<a href="#" onclick="loadContent('${conn.id}')" class="nav-link">${conn.title}</a><br>`
                            ).join('')}
                        </div>
                        
                        ${content.equations.length > 0 ? `
                            <div style="margin-top: 30px;">
                                <h4>📊 Mathematics:</h4>
                                ${content.equations.map(eq => `
                                    <div style="background: #0d1117; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                        <pre>${eq.latex}</pre>
                                        <p>${eq.description}</p>
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}
                        
                        ${content.implementations.length > 0 ? `
                            <div style="margin-top: 30px;">
                                <h4>💻 Implementations:</h4>
                                ${content.implementations.map(impl => `
                                    <div style="background: #0d1117; padding: 15px; border-radius: 5px; margin: 10px 0;">
                                        <h5>${impl.title}</h5>
                                        <p>${impl.description}</p>
                                        <a href="/notebook/${impl.id}" class="nav-link">🚀 Run Interactive Notebook</a>
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}
                    </div>
                `;
            }
            
            // Timeline visualization with D3
            const timeline = d3.select("#timeline");
            // TODO: Implement interactive timeline
        </script>
    </body>
    </html>
    """)

@app.get("/content/{content_id}")
async def get_content(content_id: str):
    """Get detailed content with connections, equations, implementations"""
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Get main content
    cursor.execute("SELECT * FROM content WHERE filename = %s", (content_id,))
    content = cursor.fetchone()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Get connected insights
    cursor.execute("""
        SELECT c.*, conn.relationship_type 
        FROM connections conn
        JOIN content c ON conn.to_content_id = c.id
        WHERE conn.from_content_id = %s
    """, (content['id'],))
    connections = cursor.fetchall()
    
    # Get equations
    cursor.execute("SELECT * FROM equations WHERE content_id = %s", (content['id'],))
    equations = cursor.fetchall()
    
    # Get implementations  
    cursor.execute("SELECT * FROM implementations WHERE content_id = %s", (content['id'],))
    implementations = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {
        **dict(content),
        'connections': [dict(c) for c in connections],
        'equations': [dict(e) for e in equations],
        'implementations': [dict(i) for i in implementations]
    }

@app.get("/timeline")
async def get_timeline():
    """Get chronological timeline data for visualization"""
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute("""
        SELECT date, title, filename, significance, theory_tags, summary
        FROM content 
        WHERE is_public = true OR %s = 'christopher'
        ORDER BY date
    """, ('christopher',))  # TODO: Get user type from auth
    
    timeline_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [dict(item) for item in timeline_data]

@app.get("/search")
async def search_content(q: str = Query(..., description="Search query")):
    """Full-text search across all content"""
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute("""
        SELECT *, ts_rank(to_tsvector('english', title || ' ' || summary || ' ' || full_content), 
                         plainto_tsquery('english', %s)) as rank
        FROM content 
        WHERE to_tsvector('english', title || ' ' || summary || ' ' || full_content) @@ plainto_tsquery('english', %s)
        ORDER BY rank DESC, significance DESC
    """, (q, q))
    
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [dict(item) for item in results]

@app.get("/notebook/{implementation_id}")
async def get_notebook(implementation_id: int):
    """Serve interactive Jupyter/SageMath notebook"""
    # TODO: Integrate with JupyterHub or similar for live notebooks
    return {"message": "Notebook integration coming soon", "id": implementation_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)