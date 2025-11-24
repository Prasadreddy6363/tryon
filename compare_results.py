"""
Compare Virtual Try-On Results
View and compare multiple try-on results side by side
"""

import os
from pathlib import Path
from PIL import Image
import sys

WORKSPACE = Path(__file__).parent
VITON_DIR = WORKSPACE / 'VITON-HD'
RESULTS_DIR = VITON_DIR / 'results'
DATASETS_DIR = VITON_DIR / 'datasets'
TEST_DIR = DATASETS_DIR / 'test'

def list_recent_results(limit=10):
    """List recent try-on results"""
    print("="*60)
    print("RECENT TRY-ON RESULTS")
    print("="*60)
    print()
    
    # Get all result directories
    result_dirs = [d for d in RESULTS_DIR.iterdir() if d.is_dir()]
    result_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not result_dirs:
        print("No results found. Run some try-ons first!")
        return []
    
    results = []
    for i, result_dir in enumerate(result_dirs[:limit], 1):
        result_files = list(result_dir.glob('*.jpg'))
        if result_files:
            result_file = result_files[0]
            # Parse filename to get person and cloth
            name = result_file.stem
            parts = name.split('_')
            if len(parts) >= 2:
                person = f"{parts[0]}_{parts[1]}.jpg"
                cloth = f"{parts[2]}_{parts[3]}.jpg" if len(parts) >= 4 else "unknown"
            else:
                person = "unknown"
                cloth = "unknown"
            
            results.append({
                'index': i,
                'dir': result_dir.name,
                'file': result_file,
                'person': person,
                'cloth': cloth,
                'time': result_dir.stat().st_mtime
            })
            
            print(f"{i}. {result_dir.name}")
            print(f"   Person: {person}")
            print(f"   Cloth: {cloth}")
            print(f"   Result: {result_file.name}")
            print()
    
    return results

def create_comparison_image(result_info):
    """Create a side-by-side comparison image"""
    print("="*60)
    print("CREATING COMPARISON IMAGE")
    print("="*60)
    print()
    
    try:
        # Load images
        person_path = TEST_DIR / 'image' / result_info['person']
        cloth_path = TEST_DIR / 'cloth' / result_info['cloth']
        result_path = result_info['file']
        
        if not person_path.exists():
            print(f"❌ Person image not found: {person_path}")
            return None
        
        if not cloth_path.exists():
            print(f"❌ Cloth image not found: {cloth_path}")
            return None
        
        if not result_path.exists():
            print(f"❌ Result image not found: {result_path}")
            return None
        
        person_img = Image.open(person_path)
        cloth_img = Image.open(cloth_path)
        result_img = Image.open(result_path)
        
        # Resize to same height
        height = 600
        
        person_aspect = person_img.width / person_img.height
        cloth_aspect = cloth_img.width / cloth_img.height
        result_aspect = result_img.width / result_img.height
        
        person_resized = person_img.resize((int(height * person_aspect), height), Image.Resampling.LANCZOS)
        cloth_resized = cloth_img.resize((int(height * cloth_aspect), height), Image.Resampling.LANCZOS)
        result_resized = result_img.resize((int(height * result_aspect), height), Image.Resampling.LANCZOS)
        
        # Create comparison
        padding = 20
        total_width = person_resized.width + cloth_resized.width + result_resized.width + (padding * 4)
        total_height = height + (padding * 2) + 60  # Extra space for labels
        
        comparison = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
        
        # Paste images
        x_offset = padding
        comparison.paste(person_resized, (x_offset, padding + 30))
        
        x_offset += person_resized.width + padding
        comparison.paste(cloth_resized, (x_offset, padding + 30))
        
        x_offset += cloth_resized.width + padding
        comparison.paste(result_resized, (x_offset, padding + 30))
        
        # Add labels (simple text overlay would require PIL ImageDraw)
        # For now, just save the comparison
        
        # Save comparison
        comparison_dir = WORKSPACE / 'comparisons'
        comparison_dir.mkdir(exist_ok=True)
        
        comparison_file = comparison_dir / f"comparison_{result_info['dir']}.jpg"
        comparison.save(comparison_file, 'JPEG', quality=95)
        
        print(f"✅ Comparison saved: {comparison_file}")
        print()
        print("Layout: [Original Person] [Clothing] [Try-On Result]")
        print()
        
        return comparison_file
        
    except Exception as e:
        print(f"❌ Error creating comparison: {e}")
        return None

def compare_multiple_results(indices):
    """Compare multiple results"""
    results = list_recent_results(20)
    
    if not results:
        return
    
    print("="*60)
    print("CREATING COMPARISONS")
    print("="*60)
    print()
    
    for idx in indices:
        if 1 <= idx <= len(results):
            result_info = results[idx - 1]
            create_comparison_image(result_info)
        else:
            print(f"❌ Invalid index: {idx}")

def main():
    """Main function"""
    print("\n" + "="*60)
    print("VIRTUAL TRY-ON RESULT COMPARISON TOOL")
    print("="*60)
    print()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--list' or sys.argv[1] == '-l':
            # List results
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            list_recent_results(limit)
        
        elif sys.argv[1] == '--compare' or sys.argv[1] == '-c':
            # Compare specific results
            if len(sys.argv) < 3:
                print("Usage: python compare_results.py --compare <index1> [index2] [index3] ...")
                print("First run: python compare_results.py --list")
                return
            
            indices = [int(x) for x in sys.argv[2:]]
            compare_multiple_results(indices)
        
        elif sys.argv[1] == '--all' or sys.argv[1] == '-a':
            # Compare all recent results
            results = list_recent_results(20)
            if results:
                indices = [r['index'] for r in results[:5]]  # Compare first 5
                compare_multiple_results(indices)
        
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("Usage:")
            print("  python compare_results.py --list [num]           # List recent results")
            print("  python compare_results.py --compare <idx> ...    # Compare specific results")
            print("  python compare_results.py --all                  # Compare all recent results")
            print("  python compare_results.py --help                 # Show this help")
            print("\nExamples:")
            print("  python compare_results.py --list 10")
            print("  python compare_results.py --compare 1 2 3")
            print("  python compare_results.py --all")
    else:
        # Default: list and compare most recent
        results = list_recent_results(10)
        if results:
            print("Creating comparison for most recent result...")
            create_comparison_image(results[0])
            print("\nTo compare more results:")
            print("  python compare_results.py --compare 1 2 3")

if __name__ == '__main__':
    main()
