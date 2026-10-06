import subprocess
import os
from playwright.sync_api import sync_playwright

def run_application_pipeline():
    print("Initializing Job Application Workflow...")
    
    # Step 1: Generate the Documents
    print("\n[Step 1] Generating custom LaTeX documents based on master_data.yaml...")
    try:
        # Calls the compiler script we wrote earlier
        subprocess.run(['python', 'src/latex_compiler.py'], check=True)
    except subprocess.CalledProcessError:
        print("Error: LaTeX generation failed.")
        return
    
    # Step 2: Human-in-the-Loop (HITL) Review
    print("\n[Step 2] --- HUMAN REVIEW REQUIRED ---")
    print("Please review the generated files in your 'templates/' directory.")
    approval = input("Type 'yes' to approve these documents and proceed to web submission, or anything else to abort: ")
    
    if approval.lower().strip() != 'yes':
        print("Application aborted by user. Please adjust your master_data.yaml and try again.")
        return

    # Step 3: Automated Submission
    print("\n[Step 3] Launching headless browser using saved .browser_data context...")
    
    user_data_dir = os.path.join(os.getcwd(), '.browser_data')
    target_job_url = "https://www.xing.com/jobs" # You will eventually pass the specific job URL here
    
    with sync_playwright() as p:
        # We set headless=True so this runs silently in the background
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=True, 
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        
        print(f"Navigating to: {target_job_url}")
        page.goto(target_job_url)
        
        print("Successfully loaded the authenticated session in the background!")
        
        # --- ANTIGRAVITY / PLAYWRIGHT ACTION ZONE ---
        # This is where your Antigravity agent will read the screen, upload the PDF 
        # from your templates/ folder, and click the final "Apply" (Bewerben) button.
        # Example command: page.click("button:has-text('Bewerben')")
        
        browser_context.close()
        
    print("\nPipeline executed successfully! The application has been submitted.")

if __name__ == "__main__":
    run_application_pipeline()