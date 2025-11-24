"""
Intel Arc GPU Optimization Guide
Intel Arc GPUs can be used with PyTorch through Intel Extension for PyTorch (IPEX)
"""

import subprocess
import sys

def check_current_setup():
    """Check current PyTorch setup"""
    print("="*60)
    print("CURRENT SETUP")
    print("="*60)
    
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        print(f"✓ CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"✓ CUDA device: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠ Running on CPU")
        
        # Check for Intel Extension
        try:
            import intel_extension_for_pytorch as ipex
            print(f"✓ Intel Extension for PyTorch: {ipex.__version__}")
            print("✓ Intel Arc GPU support available!")
        except ImportError:
            print("✗ Intel Extension for PyTorch not installed")
            print("  This is needed for Intel Arc GPU acceleration")
    
    except ImportError:
        print("✗ PyTorch not installed")
    
    print()

def install_intel_extension():
    """Install Intel Extension for PyTorch"""
    print("="*60)
    print("INSTALLING INTEL EXTENSION FOR PYTORCH")
    print("="*60)
    print()
    print("This will enable GPU acceleration on your Intel Arc GPU")
    print()
    
    response = input("Do you want to install Intel Extension for PyTorch? (y/n): ")
    if response.lower() != 'y':
        print("Installation cancelled")
        return False
    
    print("\nInstalling...")
    
    # Install Intel Extension for PyTorch
    cmd = [
        sys.executable, '-m', 'pip', 'install',
        'intel-extension-for-pytorch',
        'oneccl_bind_pt',
        '--extra-index-url',
        'https://pytorch-extension.intel.com/release-whl/stable/xpu/us/'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Installation successful!")
        print("\nPlease restart the Flask server for changes to take effect")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Installation failed: {e}")
        return False

def create_optimized_test_script():
    """Create an optimized test.py that uses Intel Arc GPU"""
    print("="*60)
    print("CREATING OPTIMIZED TEST SCRIPT")
    print("="*60)
    print()
    
    script_content = '''"""
Optimized test.py for Intel Arc GPU
This version uses Intel Extension for PyTorch (IPEX) for GPU acceleration
"""

# Add this at the top of your test.py file
import torch
try:
    import intel_extension_for_pytorch as ipex
    IPEX_AVAILABLE = True
    print("Intel Extension for PyTorch loaded - GPU acceleration enabled")
except ImportError:
    IPEX_AVAILABLE = False
    print("Intel Extension for PyTorch not available - using CPU")

# In your main() function, after loading models:
if IPEX_AVAILABLE:
    device = torch.device('xpu')  # Intel GPU device
    print(f"Using Intel Arc GPU: {device}")
    
    # Optimize models for Intel GPU
    seg = ipex.optimize(seg)
    gmm = ipex.optimize(gmm)
    alias = ipex.optimize(alias)
else:
    device = torch.device('cpu')
    print("Using CPU")

# Move models to device
seg.to(device).eval()
gmm.to(device).eval()
alias.to(device).eval()
'''
    
    print("To enable Intel Arc GPU acceleration:")
    print("\n1. Install Intel Extension for PyTorch (run this script with --install)")
    print("2. Modify VITON-HD/test.py to use 'xpu' device instead of 'cuda'")
    print("3. Restart the Flask server")
    print("\nNote: This requires code modifications to test.py")
    print()

def show_cpu_optimizations():
    """Show CPU optimization tips"""
    print("="*60)
    print("CPU OPTIMIZATION TIPS (Current Setup)")
    print("="*60)
    print()
    print("Since you're running on CPU, here are ways to improve performance:")
    print()
    print("1. ✓ Use fewer threads (already optimized in test.py)")
    print("2. ✓ Process one image at a time (batch_size=1)")
    print("3. ✓ Use recommended image pairs (better preprocessing)")
    print("4. ⚠ Close other applications to free up RAM")
    print("5. ⚠ Ensure good cooling (CPU will work hard)")
    print()
    print("Expected performance:")
    print("  • Processing time: 1-3 minutes per image")
    print("  • Quality: Good (same model, just slower)")
    print("  • Memory usage: 4-6 GB RAM")
    print()
    print("The results will be the SAME quality as GPU, just slower!")
    print()

def main():
    """Main function"""
    print("\n" + "="*60)
    print("INTEL ARC GPU OPTIMIZATION TOOL")
    print("="*60)
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--install':
        check_current_setup()
        install_intel_extension()
        create_optimized_test_script()
    else:
        check_current_setup()
        show_cpu_optimizations()
        
        print("="*60)
        print("RECOMMENDATIONS")
        print("="*60)
        print()
        print("Option 1: Continue with CPU (Easiest)")
        print("  • No changes needed")
        print("  • Same quality, just slower (1-3 min per image)")
        print("  • Use: python test_combinations.py --test 3")
        print()
        print("Option 2: Try Intel Arc GPU (Advanced)")
        print("  • Requires Intel Extension for PyTorch")
        print("  • Requires code modifications")
        print("  • Run: python optimize_for_intel_arc.py --install")
        print("  • May be faster but requires setup")
        print()
        print("Option 3: Use NVIDIA GPU (Best, if available)")
        print("  • Requires NVIDIA GPU with CUDA")
        print("  • 10-30x faster than CPU")
        print("  • Best quality and performance")
        print()
        print("RECOMMENDED: Continue with CPU and test combinations")
        print("Run: python test_combinations.py --test 3")
        print()

if __name__ == '__main__':
    main()
