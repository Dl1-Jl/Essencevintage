
import requests
import sys
import time
import json
from datetime import datetime

class TikTokPromoAPITester:
    def __init__(self, base_url="https://73e02b98-cd67-4b21-b9e6-5820e21a911d.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"Response: {response.text}")
                except:
                    pass
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )
        if success:
            print(f"Response: {response}")
        return success

    def test_promo_content(self):
        """Test the promo content endpoint"""
        success, response = self.run_test(
            "Promo Content Endpoint",
            "GET",
            "promo-content",
            200
        )
        if success:
            # Verify the content structure
            required_fields = ["title", "subtitle", "description", "call_to_action", "target_url", "benefits", "testimonials"]
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                print(f"❌ Missing required fields: {', '.join(missing_fields)}")
                return False
            
            # Verify specific content values
            if response["title"] != "💰 Make Money From Your PC! 💰":
                print(f"❌ Incorrect title: {response['title']}")
                return False
                
            if response["subtitle"] != "Discover the Secret to Earning $100+ Daily":
                print(f"❌ Incorrect subtitle: {response['subtitle']}")
                return False
                
            if "beacons.ai/junior47620" not in response["target_url"]:
                print(f"❌ Incorrect target URL: {response['target_url']}")
                return False
                
            if len(response["testimonials"]) < 3:
                print(f"❌ Not enough testimonials: {len(response['testimonials'])}")
                return False
                
            print("✅ All promo content fields verified")
            return True
        return False

    def test_track_click(self):
        """Test the click tracking endpoint"""
        click_types = ["beacons_link", "share", "view"]
        all_success = True
        
        for click_type in click_types:
            success, response = self.run_test(
                f"Track Click - {click_type}",
                "POST",
                "track-click",
                200,
                data={
                    "click_type": click_type,
                    "user_agent": "Mozilla/5.0 (Test Agent)",
                    "ip_address": "127.0.0.1"
                }
            )
            if not success:
                all_success = False
            else:
                if response.get("click_type") != click_type:
                    print(f"❌ Response click_type mismatch: {response.get('click_type')} != {click_type}")
                    all_success = False
        
        return all_success

    def test_analytics(self):
        """Test the analytics endpoint"""
        success, response = self.run_test(
            "Analytics Endpoint",
            "GET",
            "analytics",
            200
        )
        if success:
            # Verify the analytics structure
            required_fields = ["total_views", "total_clicks", "beacons_clicks", "share_clicks"]
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                print(f"❌ Missing required fields: {', '.join(missing_fields)}")
                return False
                
            print("✅ All analytics fields verified")
            return True
        return False

def main():
    # Setup
    tester = TikTokPromoAPITester()
    
    # Run tests
    root_success = tester.test_root_endpoint()
    promo_success = tester.test_promo_content()
    track_success = tester.test_track_click()
    analytics_success = tester.test_analytics()
    
    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    
    # Overall success
    all_success = root_success and promo_success and track_success and analytics_success
    print(f"\n{'✅ All tests passed!' if all_success else '❌ Some tests failed!'}")
    
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())
