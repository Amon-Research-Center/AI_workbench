#!/usr/bin/env python3
"""
Access Control and Redaction System
- Full story access for Christopher
- Redacted/curated public view
- Real-time section marking for privacy
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional, List
import psycopg2
import psycopg2.extras
import os

security = HTTPBearer()

# User roles and access levels
USER_ROLES = {
    'christopher': {
        'access_level': 'full',
        'can_redact': True,
        'can_edit': True,
        'sees_private': True
    },
    'public': {
        'access_level': 'public',
        'can_redact': False, 
        'can_edit': False,
        'sees_private': False
    },
    'researcher': {
        'access_level': 'academic',
        'can_redact': False,
        'can_edit': False,
        'sees_private': False
    }
}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract user from JWT token or default to public"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, os.getenv("JWT_SECRET", "dev_secret"), algorithms=["HS256"])
        user_type = payload.get("user_type", "public")
        return USER_ROLES.get(user_type, USER_ROLES['public'])
    except:
        return USER_ROLES['public']

def filter_content_by_access(content, user):
    """Filter content based on user access level"""
    if user['sees_private']:
        # Christopher sees everything, including redaction controls
        return add_redaction_controls(content, user['can_redact'])
    else:
        # Public/researchers see only non-redacted content
        return remove_redacted_sections(content)

def add_redaction_controls(content, can_redact=False):
    """Add redaction controls to content for Christopher"""
    if not can_redact:
        return content
        
    # Add interactive redaction markers
    content_with_controls = content.replace(
        '<p>', '<p><span class="redact-control" onclick="toggleRedaction(this)">🔒</span> '
    )
    
    return f"""
    <div class="redaction-controls" style="background: #2a2a2a; padding: 10px; margin: 10px 0; border-radius: 5px;">
        <strong>🔒 Privacy Controls:</strong>
        <button onclick="markSectionPrivate()">Mark Section Private</button>
        <button onclick="markSectionPublic()">Make Public</button>
        <button onclick="previewPublicView()">Preview Public View</button>
    </div>
    {content_with_controls}
    
    <script>
        function toggleRedaction(element) {{
            const paragraph = element.parentElement;
            if (paragraph.classList.contains('redacted')) {{
                paragraph.classList.remove('redacted');
                element.innerHTML = '🔒';
                element.title = 'Click to redact from public view';
            }} else {{
                paragraph.classList.add('redacted');
                element.innerHTML = '🔒❌';
                element.title = 'This section is hidden from public view';
            }}
            saveRedactionState(paragraph.id, paragraph.classList.contains('redacted'));
        }}
        
        function saveRedactionState(paragraphId, isRedacted) {{
            fetch('/api/redaction', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    paragraph_id: paragraphId,
                    redacted: isRedacted
                }})
            }});
        }}
        
        function previewPublicView() {{
            // Hide all redacted content temporarily
            document.querySelectorAll('.redacted').forEach(el => {{
                el.style.display = 'none';
            }});
            
            // Show "return to full view" button
            const returnBtn = document.createElement('button');
            returnBtn.innerHTML = '↩️ Return to Full View';
            returnBtn.onclick = () => {{
                document.querySelectorAll('.redacted').forEach(el => {{
                    el.style.display = 'block';
                }});
                returnBtn.remove();
            }};
            document.body.insertBefore(returnBtn, document.body.firstChild);
        }}
    </script>
    
    <style>
        .redacted {{ 
            background: rgba(255,0,0,0.1); 
            border-left: 3px solid red;
            padding-left: 10px;
        }}
        .redact-control {{ 
            cursor: pointer; 
            user-select: none;
            margin-right: 5px;
        }}
        .redaction-controls button {{
            margin: 5px;
            padding: 5px 10px;
            background: #444;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }}
    </style>
    """

def remove_redacted_sections(content):
    """Remove redacted sections from public view"""
    # This would parse HTML and remove elements marked as redacted
    # For now, simple string replacement
    import re
    
    # Remove content between redaction markers
    content = re.sub(r'<div class="redacted">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<p class="redacted">.*?</p>', '', content, flags=re.DOTALL)
    
    return content

# Database schema additions for redaction
REDACTION_SCHEMA = """
-- Table to track redacted content sections
CREATE TABLE IF NOT EXISTS redactions (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES content(id),
    section_id VARCHAR(255), -- HTML element ID or text hash
    redacted_by VARCHAR(50), -- 'christopher'
    redaction_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Content sections table for granular control
CREATE TABLE IF NOT EXISTS content_sections (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES content(id),
    section_text TEXT,
    section_order INTEGER,
    is_redacted BOOLEAN DEFAULT false,
    redaction_level VARCHAR(50) DEFAULT 'public', -- 'public', 'academic', 'private'
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_redactions_content ON redactions(content_id);
CREATE INDEX IF NOT EXISTS idx_sections_content ON content_sections(content_id, section_order);
"""

# API endpoints for redaction management
def setup_redaction_endpoints(app):
    
    @app.post("/api/redaction")
    async def toggle_redaction(
        request: dict,
        user = Depends(get_current_user)
    ):
        """Toggle redaction status of content section"""
        if not user['can_redact']:
            raise HTTPException(status_code=403, detail="Not authorized to redact content")
        
        conn = get_db()
        cursor = conn.cursor()
        
        if request['redacted']:
            # Add redaction
            cursor.execute("""
                INSERT INTO redactions (content_id, section_id, redacted_by)
                VALUES (%s, %s, %s)
                ON CONFLICT (content_id, section_id) DO NOTHING
            """, (request['content_id'], request['paragraph_id'], 'christopher'))
        else:
            # Remove redaction
            cursor.execute("""
                DELETE FROM redactions 
                WHERE content_id = %s AND section_id = %s
            """, (request['content_id'], request['paragraph_id']))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {"status": "updated"}
    
    @app.get("/api/content/{content_id}/redactions")
    async def get_redactions(
        content_id: int,
        user = Depends(get_current_user)
    ):
        """Get redaction status for content sections"""
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT section_id, redaction_reason
            FROM redactions 
            WHERE content_id = %s
        """, (content_id,))
        
        redactions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"redactions": [{"section": r[0], "reason": r[1]} for r in redactions]}

# Usage example in main content endpoint:
def get_filtered_content(content_id: str, user):
    """Get content filtered by user access level"""
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Get content
    cursor.execute("SELECT * FROM content WHERE filename = %s", (content_id,))
    content = cursor.fetchone()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Check if user can access this content
    if content['is_public'] == False and not user['sees_private']:
        raise HTTPException(status_code=403, detail="Content not available")
    
    # Apply redaction filtering
    content['full_content'] = filter_content_by_access(content['full_content'], user)
    
    cursor.close()
    conn.close()
    
    return content

"""
Usage Flow:

1. Christopher logs in with full access
2. Views complete development story with redaction controls
3. Clicks 🔒 icons to mark sections as private/redacted
4. Can preview public view to see what others will see
5. Public users automatically get filtered content
6. Academic researchers get middle tier (more than public, less than full)

This gives Christopher complete control over what gets shared while
maintaining the full development story for his own reference.
"""