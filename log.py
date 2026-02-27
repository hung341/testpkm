from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os

def start_auto():

    file_path = "sdt.txt"
    
    if not os.path.exists(file_path):
        print(f"Lỗi: Không tìm thấy file {file_path} trong cùng thư mục!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
       
        accounts = [line.strip() for line in f if '|' in line]

    if not accounts:
        print("Danh sách tài khoản trống hoặc sai định dạng (user|pass)")
        return
    
    print(f"Đã nạp {len(accounts)} tài khoản từ file {file_path}")


    options = webdriver.ChromeOptions()
    options.add_argument("--incognito") 
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
   
    driver.get("http://127.0.0.1:5500/index.html")
    print("Đang đợi mở Form đăng nhập...")

    current_idx = 0

    try:
        while current_idx < len(accounts):
            try:
                driver.switch_to.default_content()
                iframe = driver.find_element(By.ID, "gameIframe")
                driver.switch_to.frame(iframe)
            except:
                time.sleep(1) 
                continue

            try:
                wait_fast = WebDriverWait(driver, 1)
                u_input = wait_fast.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'e-mail')]")))
                
                if u_input.is_displayed() and u_input.get_attribute("value") == "":
                    user, pwd = accounts[current_idx].split('|')
                    print(f" Thấy Form! Đang điền Acc {current_idx + 1}: {user}")

                    p_input = driver.find_element(By.XPATH, "//input[@type='password']")
                    u_input.send_keys(user)
                    p_input.send_keys(pwd)
                    
                    login_red = driver.find_element(By.XPATH, "//button[contains(., 'Log in')] | //div[contains(., 'Log in')]")
                    driver.execute_script("arguments[0].click();", login_red)
                    
                    print(f" Đã xong nick {user}. Đợi form tiếp theo...")
                    current_idx += 1
                    time.sleep(1) 
            except:
                pass
            
            time.sleep(1)

        print(" Đã điền hết danh sách tài khoản!")

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        print("Dừng tool.")

if __name__ == "__main__":
    start_auto()