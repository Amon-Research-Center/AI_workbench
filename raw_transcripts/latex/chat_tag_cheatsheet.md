# 🧠 Symbolic Chat Tag Cheat Sheet
Use these minimal `%x` tags during chat (or in notes) to auto-structure your symbolic research pipeline. They map directly to sections in Jupyter notebooks, LaTeX, markdown files, or todo lists.
---
## ✨ Tags
| Tag  | Meaning                     | Maps To              |
|------|------------------------------|-----------------------|
| `%t` | Text / prose                  | Markdown cell         |
| `%e` | Equation (LaTeX)              | Markdown `$$...$$`    |
| `%c` | Code (Python, Sage, etc.)     | Code cell             |
| `%d` | Directive / To-do             | Markdown checklist    |
| `%n` | Note / comment                | Markdown blockquote   |
| `%i` | Idea / hypothesis             | Markdown callout      |
| `%q` | Question                      | Markdown Q line       |
| `%a` | Answer                        | Markdown A line       |
| `%r` | Reference / citation          | `.bib` or markdown    |
---
## ✅ Usage Examples
```
%t Symbolic resonance is the condition of stabilized form.
e% \Psi = \hat{R}(\hat{M}(\Phi_0)) + \epsilon
%c
def resonance(phi, alpha, epsilon):
    return alpha * morphic_memory(phi) + epsilon
%d Implement operator simulation for \hat{R}
i% Form is resonance crystallized in symbolic structure.
%q What does \hat{M} represent?
a It retrieves memory from the morphic field.
%r Sheldrake, R. (1981). *A New Science of Life*
```
---
Keep this visible while working/chatting. Every tag you use is a future code block, paper paragraph, or symbolic glossary entry.
→ Works beautifully with Jupyter, `nbconvert`, Pandoc, and regex extractors.
Symbolic cognition starts with symbolic discipline. 🌀
