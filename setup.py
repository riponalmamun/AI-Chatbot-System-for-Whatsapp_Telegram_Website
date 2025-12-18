"""
Quick setup script for database and Redis
"""
import subprocess
import sys
import time

def check_docker():
    """Check if Docker is installed"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Docker is installed")
            return True
        else:
            print("❌ Docker is not installed")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed")
        return False


def start_services():
    """Start PostgreSQL and Redis using Docker Compose"""
    print("\n🚀 Starting PostgreSQL and Redis...")
    
    try:
        # Start services
        subprocess.run(
            ["docker-compose", "up", "-d", "db", "redis"],
            check=True
        )
        
        print("⏳ Waiting for services to start (10 seconds)...")
        time.sleep(10)
        
        # Check status
        subprocess.run(["docker", "ps"])
        
        print("\n✅ Services started successfully!")
        print("\n📊 Connection details:")
        print("PostgreSQL: postgresql://postgres:postgres@localhost:5432/chatbot_db")
        print("Redis: redis://localhost:6379/0")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting services: {e}")
        return False
    except FileNotFoundError:
        print("❌ docker-compose not found. Please install Docker Desktop.")
        return False


def main():
    print("=" * 60)
    print("AI Chatbot System - Quick Setup")
    print("=" * 60)
    
    # Check Docker
    if not check_docker():
        print("\n💡 Please install Docker Desktop:")
        print("   https://www.docker.com/products/docker-desktop/")
        sys.exit(1)
    
    # Start services
    if start_services():
        print("\n✅ Setup complete!")
        print("\n🚀 Now run: uvicorn main:app --reload")
    else:
        print("\n❌ Setup failed")
        sys.exit(1)


if __name__ == "__main__":
    main()