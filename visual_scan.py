from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_screenshot(url):
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1280, 720)
        driver.get(url)
        driver.save_screenshot("screenshot.png")
        print("[+] Screenshot saved as screenshot.png")
        driver.quit()
    except Exception as e:
        print("[-] Screenshot error:", e)
