# Changes needed in src/sustainability/panel_bridge.py

# CHANGE 1: Update Panel extension configuration (line ~13)
# OLD:
# pn.extension('tabulator', 'modal')

# NEW:
pn.extension()  # Minimal extensions - app.py handles main config

# CHANGE 2: Remove outputs directory creation and file saving (replace entire download method)
# OLD: download_markdown_report method around line 380
# NEW: Web-only download method

def download_markdown_report(self, event):
    """Download the training report as markdown - Web optimized"""
    if not self.latest_results:
        self.chat_interface.send("No results available for download.", user="System", respond=False)
        return
    
    try:
        # Get the structured data
        if hasattr(self.latest_results, 'tasks_output') and self.latest_results.tasks_output:
            final_task = self.latest_results.tasks_output[-1]
            if hasattr(final_task, 'pydantic') and final_task.pydantic:
                data = final_task.pydantic.model_dump()
                markdown_content = self.format_results_as_markdown(data)
                
                # Create download filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sustainability_training_report_{timestamp}.md"
                
                # Web-only download using JavaScript
                import urllib.parse
                
                # Encode content safely for JavaScript
                encoded_content = urllib.parse.quote(markdown_content)
                
                download_html = f"""
                <div style="margin: 20px 0; padding: 20px; border: 2px solid #28a745; border-radius: 10px; background-color: #f8f9fa; text-align: center;">
                    <h3 style="color: #28a745; margin-bottom: 15px;">📄 Training Report Ready!</h3>
                    <p style="margin-bottom: 20px;">Click the button below to download your comprehensive sustainability training report.</p>
                    <button onclick="downloadReport()" 
                            style="background-color: #28a745; color: white; padding: 15px 30px; 
                                   border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold;
                                   box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: background-color 0.3s;">
                        📄 Download {filename}
                    </button>
                    <p style="margin-top: 15px; font-size: 14px; color: #666;">
                        File size: ~{len(markdown_content):,} characters | Format: Markdown (.md)
                    </p>
                </div>
                <script>
                function downloadReport() {{
                    try {{
                        const content = decodeURIComponent(`{encoded_content}`);
                        const blob = new Blob([content], {{ type: 'text/markdown;charset=utf-8' }});
                        const url = window.URL.createObjectURL(blob);
                        const link = document.createElement('a');
                        link.href = url;
                        link.download = '{filename}';
                        link.style.display = 'none';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        window.URL.revokeObjectURL(url);
                        
                        // Show success message
                        alert('✅ Download started! Check your Downloads folder for {filename}');
                    }} catch (error) {{
                        console.error('Download error:', error);
                        alert('❌ Download failed. Please try again or contact support.');
                    }}
                }}
                </script>
                """
                
                download_widget = pn.pane.HTML(download_html, sizing_mode="stretch_width")
                
                self.chat_interface.send("📄 **Training Report Generated Successfully!**", user="System", respond=False)
                self.chat_interface.send(download_widget, user="Download", respond=False)
                
    except Exception as e:
        self.chat_interface.send(f"Error preparing download: {str(e)}", user="System", respond=False)

# CHANGE 3: Update PDF download method (replace entire method)
# OLD: download_pdf_report method
# NEW: Web-friendly PDF instructions

def download_pdf_report(self, event):
    """Download instructions for PDF conversion - Web optimized"""
    self.chat_interface.send(
        """📑 **PDF Conversion Instructions:**

**Step 1:** First download the Markdown report using the button above

**Step 2:** Convert to PDF using any of these methods:

🌐 **Online Conversion (Easiest):**
• Go to **pandoc.org/try**
• Upload your .md file  
• Select "PDF" as output format
• Download the converted PDF

💻 **Local Conversion:**
• Install Pandoc: `brew install pandoc` (Mac) or `apt install pandoc` (Linux)
• Run: `pandoc your_report.md -o report.pdf`

📝 **Alternative Tools:**
• **Typora** - Markdown editor with PDF export
• **Mark Text** - Free markdown editor  
• **VS Code** - With "Markdown PDF" extension

Your report contains professional formatting that will look great as a PDF! 🎯""", 
        user="PDF Help", 
        respond=False
    )

# CHANGE 4: Remove any file system operations (check for these patterns and remove)
# Remove any lines containing:
# - os.makedirs('outputs')
# - open(file_path, 'w')
# - with open(f'outputs/...
# - file system saving operations

# CHANGE 5: Update environment detection (add after imports)
import os

def is_web_environment():
    """Detect if running in web deployment vs local development"""
    return bool(os.environ.get('PORT'))  # Render sets PORT env var

# CHANGE 6: Add web-specific optimizations to __init__ method
# In the SustainabilityPanelApp.__init__ method, add after pn.extension():

if self.is_web_environment():
    # Web deployment optimizations
    pn.config.autoreload = False
    pn.config.dev = False
else:
    # Local development settings  
    pn.config.autoreload = True

# CHANGE 7: Update the servable method to be web-friendly
# Replace the servable method:

def servable(self):
    """Return the servable Panel application - Web optimized"""
    return self.layout

def is_web_environment(self):
    """Helper method to detect web deployment"""
    return bool(os.environ.get('PORT'))