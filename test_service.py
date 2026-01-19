"""
测试服务是否正常运行
"""
import requests
import time
import sys

def test_service():
    """测试服务"""
    url = "http://localhost:8080/api/health"
    
    print("等待服务启动...")
    time.sleep(5)
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("[OK] Service is running!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"[ERROR] Service returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("[ERROR] Cannot connect to service, please check if service is started")
        return False
    except Exception as e:
        print(f"[ERROR] Test failed: {str(e)}")
        return False

if __name__ == '__main__':
    test_service()
