"""
Test Virtual Try-On Combinations
This script helps you test different person-cloth combinations to find the best results
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import json

WORKSPACE = Path(__file__).parent
VITON_DIR = WORKSPACE / 'VITON-HD'
DATASETS_DIR = VITON_DIR / 'datasets'
TEST_DIR = DATASETS_DIR / 'test'
IMG_DIR = TEST_DIR / 'image'
CLOTH_DIR = TEST_DIR / 'cloth'
RESULTS_DIR = VITON_DIR / 'results'
CHECKPOINTS_DIR = VITON_DIR / 'checkpoints'

def get_recommended_people():
    """Get list of people with good poses for try-on"""
    # These are known good images from VITON-HD dataset
    recommended = [
        '00008_00.jpg',  # Good front pose
        '00013_00.jpg',  # Clear shoulders
        '00034_00.jpg',  # Arms visible
        '00044_00.jpg',  # Good lighting
        '00055_00.jpg',  # Standard pose
        '00069_00.jpg',  # Well-lit
        '00077_00.jpg',  # Clear pose
        '00091_00.jpg',  # Good alignment
        '00101_00.jpg',  # Front-facing
        '00126_00.jpg',  # Standard pose
    ]
    
    # Filter to only existing files
    existing = [p for p in recommended if (IMG_DIR / p).exists()]
    return existing

def get_recommended_clothes():
    """Get list of clothes that work well"""
    recommended = [
        '00008_00.jpg',  # Simple shirt
        '00013_00.jpg',  # Plain design
        '00034_00.jpg',  # Clean pattern
        '00044_00.jpg',  # Standard shirt
        '00055_00.jpg',  # Simple style
        '00067_00.jpg',  # Good quality
        '00077_00.jpg',  # Clear design
        '00091_00.jpg',  # Standard shirt
        '00101_00.jpg',  # Simple pattern
        '00126_00.jpg',  # Clean style
    ]
    
    existing = [c for c in recommended if (CLOTH_DIR / c).exists()]
    return existing

def run_tryon(person, cloth, job_name=None):
    """Run virtual try-on for a person-cloth pair"""
    if job_name is None:
        job_name = f"test_{int(time.time())}"
    
    print(f"\n{'='*60}")
    print(f"Testing: {person} + {cloth}")
    print(f"{'='*60}")
    
    # Create pairs file
    pairs_path = DATASETS_DIR / 'test_pairs.txt'
    with open(pairs_path, 'w', encoding='utf-8') as f:
        f.write(f"{person} {cloth}\n")
    
    # Ensure result directory exists
    result_dir = RESULTS_DIR / job_name
    result_dir.mkdir(parents=True, exist_ok=True)
    
    # Run test.py
    cmd = [
        sys.executable,
        str(VITON_DIR / 'test.py'),
        '--name', job_name,
        '--dataset_dir', str(DATASETS_DIR),
        '--checkpoint_dir', str(CHECKPOINTS_DIR),
        '--save_dir', str(RESULTS_DIR)
    ]
    
    print("Running inference...")
    start_time = time.time()
    
    proc = subprocess.run(cmd, cwd=str(VITON_DIR), capture_output=True, text=True)
    
    elapsed = time.time() - start_time
    
    if proc.returncode != 0:
        print(f"❌ FAILED (took {elapsed:.1f}s)")
        print(f"Error: {proc.stderr}")
        return None
    
    # Find result
    results = list(result_dir.glob('*.jpg'))
    if results:
        result_file = results[0]
        print(f"✅ SUCCESS (took {elapsed:.1f}s)")
        print(f"Result saved: {result_file}")
        return result_file
    else:
        print(f"❌ No result generated")
        return None

def test_single_pair(person, cloth):
    """Test a single person-cloth combination"""
    if not (IMG_DIR / person).exists():
        print(f"❌ Person not found: {person}")
        return False
    
    if not (CLOTH_DIR / cloth).exists():
        print(f"❌ Cloth not found: {cloth}")
        return False
    
    result = run_tryon(person, cloth)
    return result is not None

def test_recommended_pairs(num_tests=3):
    """Test several recommended combinations"""
    print("\n" + "="*60)
    print("TESTING RECOMMENDED COMBINATIONS")
    print("="*60)
    
    people = get_recommended_people()
    clothes = get_recommended_clothes()
    
    if not people:
        print("❌ No recommended people found")
        return
    
    if not clothes:
        print("❌ No recommended clothes found")
        return
    
    print(f"\nFound {len(people)} recommended people")
    print(f"Found {len(clothes)} recommended clothes")
    print(f"\nTesting {num_tests} combinations...\n")
    
    results = []
    
    for i in range(min(num_tests, len(people), len(clothes))):
        person = people[i]
        cloth = clothes[i]
        
        result = run_tryon(person, cloth, f"recommended_{i+1}")
        
        results.append({
            'person': person,
            'cloth': cloth,
            'success': result is not None,
            'result': str(result) if result else None
        })
        
        # Small delay between tests
        time.sleep(1)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    successful = sum(1 for r in results if r['success'])
    print(f"\nSuccessful: {successful}/{len(results)}")
    
    for i, r in enumerate(results, 1):
        status = "✅" if r['success'] else "❌"
        print(f"{status} Test {i}: {r['person']} + {r['cloth']}")
    
    if successful > 0:
        print(f"\n✅ Results saved in: {RESULTS_DIR}")
        print("\nView results in the web interface at http://127.0.0.1:5000")
    
    return results

def interactive_test():
    """Interactive mode to test custom combinations"""
    print("\n" + "="*60)
    print("INTERACTIVE TESTING MODE")
    print("="*60)
    
    # List available people
    people = sorted([f for f in os.listdir(IMG_DIR) if f.endswith('.jpg')])
    print(f"\nAvailable people: {len(people)}")
    print("First 10:", people[:10])
    
    # List available clothes
    clothes = sorted([f for f in os.listdir(CLOTH_DIR) if f.endswith('.jpg')])
    print(f"\nAvailable clothes: {len(clothes)}")
    print("First 10:", clothes[:10])
    
    print("\n" + "-"*60)
    person = input("Enter person filename (or press Enter for recommended): ").strip()
    if not person:
        person = get_recommended_people()[0]
        print(f"Using recommended: {person}")
    
    cloth = input("Enter cloth filename (or press Enter for recommended): ").strip()
    if not cloth:
        cloth = get_recommended_clothes()[0]
        print(f"Using recommended: {cloth}")
    
    test_single_pair(person, cloth)

def main():
    """Main function"""
    print("\n" + "="*60)
    print("VIRTUAL TRY-ON COMBINATION TESTER")
    print("="*60)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == '--test' or mode == '-t':
            # Test recommended combinations
            num_tests = int(sys.argv[2]) if len(sys.argv) > 2 else 3
            test_recommended_pairs(num_tests)
        
        elif mode == '--single' or mode == '-s':
            # Test single combination
            if len(sys.argv) < 4:
                print("Usage: python test_combinations.py --single <person> <cloth>")
                return
            person = sys.argv[2]
            cloth = sys.argv[3]
            test_single_pair(person, cloth)
        
        elif mode == '--interactive' or mode == '-i':
            # Interactive mode
            interactive_test()
        
        elif mode == '--help' or mode == '-h':
            print("\nUsage:")
            print("  python test_combinations.py --test [num]        # Test N recommended pairs (default: 3)")
            print("  python test_combinations.py --single <p> <c>    # Test specific person + cloth")
            print("  python test_combinations.py --interactive       # Interactive mode")
            print("  python test_combinations.py --help              # Show this help")
            print("\nExamples:")
            print("  python test_combinations.py --test 5")
            print("  python test_combinations.py --single 00069_00.jpg 00067_00.jpg")
            print("  python test_combinations.py --interactive")
    else:
        # Default: test 3 recommended pairs
        print("\nNo arguments provided. Testing 3 recommended combinations...")
        print("Use --help to see all options\n")
        test_recommended_pairs(3)

if __name__ == '__main__':
    main()
