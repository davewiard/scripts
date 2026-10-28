#!/usr/bin/env python3

import os
from pathlib import Path


def generate_html_preview():
    # Target the Windows desktop through the WSL mount point
    desktop = Path("/mnt/c/Users/davew/Desktop")
    if not desktop.exists():
        desktop = Path.home() / "Downloads"
        desktop.mkdir(parents=True, exist_ok=True)
        
    output_path = desktop / "FontPreview.html"
    
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>System Fonts Preview</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #121212; color: #e0e0e0; padding: 20px; }
        .controls { position: sticky; top: 0; background: #1e1e1e; padding: 15px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); z-index: 100; }
        input { width: 100%; padding: 10px; font-size: 16px; background: #2a2a2a; color: #fff; border: 1px solid #444; border-radius: 4px; box-sizing: border-box; }
        button { background: #0078d4; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; margin-top: 10px; font-weight: bold; font-size: 14px; }
        button:hover { background: #005a9e; }
        .font-card { background: #1e1e1e; margin-bottom: 12px; padding: 12px 16px; border-radius: 6px; border-left: 4px solid #0078d4; }
        .font-name { font-size: 12px; color: #888; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }
        .sample { font-size: 30px; word-break: break-word; }
        #status { margin-top: 10px; font-size: 13px; color: #aaa; }
    </style>
</head>
<body>
    <div class="controls">
        <input type="text" id="textInput" value="The quick brown fox jumps over the lazy dog 1234567890" placeholder="Type demo text here..." oninput="updateText(this.value)">
        <br>
        <button onclick="loadFonts()">Load All Installed System Fonts</button>
        <div id="status">Click the button above to grant permission and render all system fonts.</div>
    </div>
    <div id="container"></div>

    <script>
        async function loadFonts() {
            const status = document.getElementById('status');
            const container = document.getElementById('container');
            
            if (!('queryLocalFonts' in window)) {
                status.textContent = "Local Font Access API is not supported in this browser. Please open this file in Google Chrome or Microsoft Edge.";
                return;
            }
            
            try {
                status.textContent = "Querying system fonts...";
                const availableFonts = await window.queryLocalFonts();
                status.textContent = `Loaded ${availableFonts.length} font variants successfully!`;
                
                // Extract and sort unique family names
                const families = [...new Set(availableFonts.map(f => f.family))].sort();
                
                container.innerHTML = '';
                const sampleText = document.getElementById('textInput').value;
                
                for (const family of families) {
                    const card = document.createElement('div');
                    card.className = 'font-card';
                    card.innerHTML = `
                        <div class="font-name">${family}</div>
                        <div class="sample" style="font-family: '${family}', sans-serif;">${sampleText}</div>
                    `;
                    container.appendChild(card);
                }
            } catch (err) {
                status.textContent = "Permission denied or error: " + err.message;
            }
        }

        function updateText(val) {
            document.querySelectorAll('.sample').forEach(el => el.textContent = val);
        }
    </script>
</body>
</html>
"""

    output_path.write_text(html, encoding="utf-8")
    print(f"Font preview generated at: {output_path}")


if __name__ == "__main__":
    generate_html_preview()

