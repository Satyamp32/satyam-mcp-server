#!/usr/bin/env python3
"""
Railway Deployment Validation Script
Tests the deployment configuration before actual deployment
"""

import os
import json
import sys
from pathlib import Path

def validate_files():
    """Check if all required files exist"""
    required_files = [
        'server.py',
        'auth.py',
        'requirements.txt',
        'railway.toml',
        'Dockerfile',
        '.dockerignore'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def validate_railway_config():
    """Validate railway.toml configuration"""
    try:
        with open('railway.toml', 'r') as f:
            content = f.read()
        
        required_sections = ['[build]', '[deploy]', '[env]']
        for section in required_sections:
            if section not in content:
                print(f"❌ Missing section {section} in railway.toml")
                return False
        
        print("✅ railway.toml configuration valid")
        return True
    except Exception as e:
        print(f"❌ Error validating railway.toml: {e}")
        return False

def validate_dockerfile():
    """Validate Dockerfile"""
    try:
        with open('Dockerfile', 'r') as f:
            content = f.read()
        
        required_instructions = ['FROM', 'WORKDIR', 'COPY', 'RUN', 'EXPOSE', 'CMD']
        for instruction in required_instructions:
            if instruction not in content:
                print(f"❌ Missing Docker instruction {instruction}")
                return False
        
        print("✅ Dockerfile valid")
        return True
    except Exception as e:
        print(f"❌ Error validating Dockerfile: {e}")
        return False

def validate_python_syntax():
    """Validate Python files syntax"""
    python_files = ['server.py', 'auth.py', 'docs_tool.py', 'gmail_tool.py']
    
    for file in python_files:
        try:
            with open(file, 'r') as f:
                content = f.read()
            compile(content, file, 'exec')
            print(f"✅ {file} syntax valid")
        except SyntaxError as e:
            print(f"❌ Syntax error in {file}: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ File {file} not found")
            return False
    
    return True

def validate_requirements():
    """Validate requirements.txt"""
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        if not requirements or requirements == ['']:
            print("❌ requirements.txt is empty")
            return False
        
        essential_packages = ['fastapi', 'uvicorn', 'google-auth', 'google-api-python-client']
        missing_packages = []
        
        for package in essential_packages:
            if not any(package in req for req in requirements):
                missing_packages.append(package)
        
        if missing_packages:
            print(f"❌ Missing essential packages: {missing_packages}")
            return False
        
        print("✅ requirements.txt valid")
        return True
    except Exception as e:
        print(f"❌ Error validating requirements.txt: {e}")
        return False

def validate_railway_env_compatibility():
    """Check if code supports Railway environment variables"""
    try:
        with open('auth.py', 'r') as f:
            auth_content = f.read()
        
        railway_vars = ['RAILWAY_ENVIRONMENT', 'RAILWAY_SERVICE_NAME', 'RAILWAY_PROJECT_NAME']
        missing_vars = []
        
        for var in railway_vars:
            if var not in auth_content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ auth.py missing Railway environment variables: {missing_vars}")
            return False
        
        with open('server.py', 'r') as f:
            server_content = f.read()
        
        if not any('RAILWAY' in server_content for var in railway_vars):
            print("❌ server.py missing Railway environment detection")
            return False
        
        print("✅ Railway environment compatibility valid")
        return True
    except Exception as e:
        print(f"❌ Error validating Railway compatibility: {e}")
        return False

def main():
    """Run all validation checks"""
    print("🚀 Railway Deployment Validation")
    print("=" * 40)
    
    checks = [
        ("Files", validate_files),
        ("Railway Config", validate_railway_config),
        ("Dockerfile", validate_dockerfile),
        ("Python Syntax", validate_python_syntax),
        ("Requirements", validate_requirements),
        ("Railway Compatibility", validate_railway_env_compatibility)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error in {name} check: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 40)
    print("📊 Validation Summary:")
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All validation checks passed! Ready for Railway deployment.")
        return 0
    else:
        print("⚠️  Some validation checks failed. Please fix issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
