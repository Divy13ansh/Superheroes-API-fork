#!/usr/bin/env python3
"""
Simple Dagger test script to verify installation and basic functionality.
"""

import sys
import asyncio


async def test_dagger_installation():
    """Test if Dagger is properly installed and working."""
    try:
        import dagger
        print("✅ Dagger imported successfully")
        
        # Test basic Dagger functionality
        config = dagger.Config(log_output=sys.stderr)
        async with dagger.Connection(config) as client:
            # Simple container test
            result = await (
                client.container()
                .from_("alpine:latest")
                .with_exec(["echo", "Hello from Dagger!"])
                .stdout()
            )
            
            print(f"✅ Dagger container test successful: {result.strip()}")
            
            # Test Python container
            python_result = await (
                client.container()
                .from_("python:3.10-slim")
                .with_exec(["python", "--version"])
                .stdout()
            )
            
            print(f"✅ Python container test successful: {python_result.strip()}")
            
        print("🎉 All Dagger tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Dagger import failed: {e}")
        print("💡 Install with: pip install -r requirements-dagger.txt")
        return False
        
    except Exception as e:
        print(f"❌ Dagger test failed: {e}")
        print("💡 Make sure Docker is running")
        return False


if __name__ == "__main__":
    print("🧪 Testing Dagger installation and functionality...")
    print("=" * 50)
    
    success = asyncio.run(test_dagger_installation())
    
    if success:
        print("\n🚀 Ready to run the full CI pipeline!")
        print("Run: ./scripts/run-dagger-ci.sh")
        sys.exit(0)
    else:
        print("\n❌ Dagger setup needs attention")
        sys.exit(1)
