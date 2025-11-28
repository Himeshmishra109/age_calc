#!/usr/bin/env python
"""
Quick test script to verify the Flask app is working correctly
Run this before deploying to Vercel
"""

import sys
import json
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        from flask import Flask, render_template, request, jsonify, Response
        from datetime import datetime, timedelta
        import math
        import random
        import json
        import os
        from collections import Counter
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_creation():
    """Test that the Flask app can be created"""
    print("\nTesting app creation...")
    try:
        from app import app
        print("✓ Flask app created successfully")
        return True, app
    except Exception as e:
        print(f"✗ App creation error: {e}")
        return False, None

def test_routes(app):
    """Test that all routes are registered"""
    print("\nTesting routes...")
    try:
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/calculator/<slug>', '/calculate', '/about', 
                          '/contact', '/privacy-policy', '/terms-and-conditions',
                          '/sitemap.xml', '/robots.txt']
        
        print(f"  Total routes registered: {len(routes)}")
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"  ✓ {route}")
            else:
                print(f"  ✗ {route} - NOT FOUND")
        return True
    except Exception as e:
        print(f"✗ Route testing error: {e}")
        return False

def test_data_files():
    """Test that required data files exist"""
    print("\nTesting data files...")
    try:
        with open('data/calculators.json', 'r', encoding='utf-8') as f:
            calculators = json.load(f)
        print(f"✓ calculators.json loaded ({len(calculators)} calculators)")
        return True
    except Exception as e:
        print(f"✗ Data file error: {e}")
        return False

def test_templates():
    """Test that all required templates exist"""
    print("\nTesting templates...")
    templates = ['index.html', 'calculator_page.html', 'about.html', 
                'contact.html', 'privacy.html', 'terms.html', '404.html']
    
    import os
    all_exist = True
    for template in templates:
        path = f'templates/{template}'
        if os.path.exists(path):
            print(f"  ✓ {template}")
        else:
            print(f"  ✗ {template} - NOT FOUND")
            all_exist = False
    return all_exist

def test_static_files():
    """Test that static files exist"""
    print("\nTesting static files...")
    static_files = ['calculator-forms.js', 'style.css']
    
    import os
    all_exist = True
    for file in static_files:
        path = f'static/{file}'
        if os.path.exists(path):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - NOT FOUND")
            all_exist = False
    return all_exist

def test_calculation():
    """Test a sample calculation"""
    print("\nTesting calculation function...")
    try:
        from app import calculate
        
        # Test age calculator
        test_data = {"dob": "1990-01-01"}
        result = calculate("age", test_data)
        if "Age:" in result:
            print(f"  ✓ Age calculation: {result}")
        else:
            print(f"  ✗ Age calculation failed: {result}")
            return False
        
        # Test BMI calculator
        test_data = {"weight": "70", "height": "175"}
        result = calculate("bmi", test_data)
        if "BMI:" in result:
            print(f"  ✓ BMI calculation: {result}")
        else:
            print(f"  ✗ BMI calculation failed: {result}")
            return False
        
        # Test percentage calculator
        test_data = {"value": "100", "percent": "25"}
        result = calculate("percentage", test_data)
        if "25" in result:
            print(f"  ✓ Percentage calculation: {result}")
        else:
            print(f"  ✗ Percentage calculation failed: {result}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Calculation error: {e}")
        return False

def test_app_context(app):
    """Test app in request context"""
    print("\nTesting app context...")
    try:
        with app.test_client() as client:
            # Test homepage
            response = client.get('/')
            if response.status_code == 200:
                print("  ✓ Homepage loads (200 OK)")
            else:
                print(f"  ✗ Homepage failed ({response.status_code})")
                return False
            
            # Test sitemap
            response = client.get('/sitemap.xml')
            if response.status_code == 200:
                print("  ✓ Sitemap loads (200 OK)")
            else:
                print(f"  ✗ Sitemap failed ({response.status_code})")
                return False
            
            # Test robots.txt
            response = client.get('/robots.txt')
            if response.status_code == 200:
                print("  ✓ Robots.txt loads (200 OK)")
            else:
                print(f"  ✗ Robots.txt failed ({response.status_code})")
                return False
            
            # Test 404
            response = client.get('/nonexistent-page')
            if response.status_code == 404:
                print("  ✓ 404 page works correctly")
            else:
                print(f"  ✗ 404 handling failed ({response.status_code})")
                return False
            
        return True
    except Exception as e:
        print(f"✗ App context error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("FLASK APP VERIFICATION TEST")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    
    success, app = test_app_creation()
    results.append(("App Creation", success))
    
    if app:
        results.append(("Routes", test_routes(app)))
        results.append(("App Context", test_app_context(app)))
    
    results.append(("Data Files", test_data_files()))
    results.append(("Templates", test_templates()))
    results.append(("Static Files", test_static_files()))
    results.append(("Calculations", test_calculation()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:20s} {status}")
    
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your app is ready for deployment!")
        print("\nNext steps:")
        print("1. Review DEPLOYMENT_CHECKLIST.md")
        print("2. Push to GitHub")
        print("3. Deploy to Vercel")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
