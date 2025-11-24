#!/usr/bin/env python3
"""
Script to help access the VITON-HD presentation files
"""

import os
import sys

def main():
    # Define the project directory
    project_dir = r"c:\Users\Prasad\OneDrive\Desktop\vton github"
    
    # List of presentation files
    files = [
        "VITON-HD_Virtual_TryOn_Presentation.pdf",
        "VITON-HD_Virtual_TryOn_Presentation.pptx.txt",
        "PROJECT_SUMMARY.md",
        "PRESENTATION_README.md"
    ]
    
    print("VITON-HD Virtual Try-On System - Presentation Files")
    print("=" * 50)
    
    # Check which files exist
    existing_files = []
    for file in files:
        file_path = os.path.join(project_dir, file)
        if os.path.exists(file_path):
            existing_files.append((file, file_path))
            print(f"✓ Found: {file}")
        else:
            print(f"✗ Missing: {file}")
    
    print("\n" + "=" * 50)
    
    if existing_files:
        print("\nTo access these files:")
        for file, path in existing_files:
            print(f"\n{file}:")
            print(f"  Path: {path}")
            if file.endswith('.txt'):
                print("  This is a text outline for PowerPoint slides.")
                print("  You can open it in any text editor and copy the content to create slides.")
            elif file.endswith('.pdf'):
                print("  This is a complete PDF presentation.")
                print("  You can open it directly with any PDF reader.")
            elif file.endswith('.md'):
                print("  This is a markdown document with additional information.")
    
    else:
        print("No presentation files found. Please check the project directory.")
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    main()