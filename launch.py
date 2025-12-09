#!/usr/bin/env python3
"""
Smart launcher for PriceSpy Lite
Automatically chooses the best interface based on platform and available libraries
"""
import sys
import platform


def check_tkinter():
    """Check if Tkinter is available and working"""
    try:
        import tkinter
        # Try to create a test window
        root = tkinter.Tk()
        root.withdraw()
        root.destroy()
        return True
    except Exception as e:
        print(f"Tkinter not available: {e}")
        return False


def main():
    print("="*60)
    print("🔍 PriceSpy Lite - Smart Launcher")
    print("="*60)
    print(f"\nDetected Platform: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version.split()[0]}\n")
    
    # Check if tkinter is available
    if check_tkinter():
        print("✓ Tkinter is available!")
        print("\nLaunching Desktop GUI...\n")
        print("="*60)
        
        try:
            import main_gui
            main_gui.main()
        except Exception as e:
            print(f"\n✗ Desktop GUI failed: {e}")
            print("\nFalling back to Web Interface...")
            launch_web_interface()
    else:
        print("✗ Tkinter is not available or not working properly")
        print("\nLaunching Web Interface instead...\n")
        launch_web_interface()


def launch_web_interface():
    """Launch the web-based interface"""
    try:
        print("="*60)
        print("Starting Web Interface...")
        print("="*60 + "\n")
        
        import web_gui
        # web_gui will handle the rest
        
    except ImportError as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease install Flask:")
        print("  pip install flask")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error launching web interface: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
