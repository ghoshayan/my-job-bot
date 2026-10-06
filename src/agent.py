import subprocess
import os

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
    # Note: Because you are using the Antigravity application, this is where you will 
    # link the google-antigravity SDK to take control of the authenticated Playwright 
    # instance and map the generated data into the web form.
    print("Pipeline executed successfully! (Submission logic ready to be attached)")

if __name__ == "__main__":
    run_application_pipeline()