from playwright.sync_api import sync_playwright
import os

def capture_session(start_url="https://www.xing.com/"):
    """
    Launches a visible browser for the initial login. 
    Saves all cookies and session state to the .browser_data folder.
    """
    # Get the absolute path to your .browser_data directory
    user_data_dir = os.path.join(os.getcwd(), '.browser_data')

    with sync_playwright() as p:
        print(f"Launching persistent browser context at: {user_data_dir}")
        
        # Launch Chromium with the persistent data directory
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,  # Set to False so you can see the window and log in
            args=["--disable-blink-features=AutomationControlled"] # Helps evade basic bot detection
        )
        
        # Use the default open page or create a new one
        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        
        print(f"Navigating to {start_url}...")
        page.goto(start_url)
        
        print("\n--- ACTION REQUIRED ---")
        print("1. Please log in to your account manually in the browser window.")
        print("2. Solve any CAPTCHAs or 2FA prompts.")
        print("3. Once you are fully logged in and see your feed, simply close the browser window.")
        print("-----------------------\n")
        
        # This pauses the script and opens the Playwright Inspector. 
        # Click the "Resume" play button in the inspector ONLY AFTER you have logged in.
        page.pause()
        
        browser_context.close()
        print("Session data successfully saved to .browser_data/")

if __name__ == "__main__":
    # You can change this to https://www.linkedin.com/ to capture that session too!
    capture_session(start_url="https://www.xing.com/")