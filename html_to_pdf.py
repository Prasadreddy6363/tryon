"""
Convert HTML to PDF using pdfkit (wkhtmltopdf wrapper)
"""
import sys
from pathlib import Path

try:
    import pdfkit
    
    # Configure paths
    workspace = Path(r"c:\Users\Prasad\OneDrive\Desktop\vton github")
    html_file = workspace / "VITON_HD_Research_Paper.html"
    pdf_file = workspace / "VITON_HD_Research_Paper.pdf"
    
    # PDF options for academic paper
    options = {
        'page-size': 'A4',
        'margin-top': '1in',
        'margin-right': '1in',
        'margin-bottom': '1in',
        'margin-left': '1in',
        'encoding': 'UTF-8',
        'enable-local-file-access': None,
        'print-media-type': None,
        'no-outline': None,
    }
    
    print("📄 Converting HTML to PDF...")
    pdfkit.from_file(str(html_file), str(pdf_file), options=options)
    
    print(f"✅ PDF created successfully!")
    print(f"📍 Location: {pdf_file}")
    print(f"📊 Size: {pdf_file.stat().st_size / 1024:.2f} KB")
    
except ImportError:
    print("❌ pdfkit not installed. Installing now...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pdfkit"], check=True)
    print("\n⚠️  Also need wkhtmltopdf binary:")
    print("   Download from: https://wkhtmltopdf.org/downloads.html")
    print("   Or run: winget install wkhtmltopdf")
    print("\n   Then run this script again.")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Alternative: Open VITON_HD_Research_Paper.html in browser")
    print("   Then Print → Save as PDF")
