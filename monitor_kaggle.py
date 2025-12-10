"""
Kaggle Notebook Monitor - Automatically checks run status
"""
from kaggle import api
import time
from datetime import datetime

KERNEL_SLUG = "hemanthreganti/winner-trajectory-reward-grpo-training-gemm"
CHECK_INTERVAL = 60  # seconds

def get_status():
    """Get current kernel status"""
    try:
        api.authenticate()
        status = api.kernels_status(KERNEL_SLUG)
        return status._status.name, status._failure_message
    except Exception as e:
        return "ERROR", str(e)

def monitor():
    """Monitor the kernel and report status changes"""
    print(f"🔍 Monitoring: {KERNEL_SLUG}")
    print(f"⏱️  Checking every {CHECK_INTERVAL} seconds")
    print("=" * 60)
    
    last_status = None
    start_time = datetime.now()
    
    while True:
        current_status, failure_msg = get_status()
        timestamp = datetime.now().strftime("%H:%M:%S")
        elapsed = (datetime.now() - start_time).seconds // 60
        
        # Status changed
        if current_status != last_status:
            print(f"\n[{timestamp}] Status changed: {last_status} → {current_status}")
            
            if current_status == "COMPLETE":
                print("\n" + "=" * 60)
                print("✅ SUCCESS! Notebook completed successfully!")
                print("=" * 60)
                print(f"📊 View results: https://www.kaggle.com/code/{KERNEL_SLUG}")
                break
            
            elif current_status == "ERROR":
                print("\n" + "=" * 60)
                print("❌ FAILED! Notebook encountered an error")
                if failure_msg:
                    print(f"Error message: {failure_msg}")
                print("=" * 60)
                print(f"📋 View logs: https://www.kaggle.com/code/{KERNEL_SLUG}/log")
                break
            
            elif current_status == "RUNNING":
                print(f"🏃 Notebook is running... ({elapsed}m elapsed)")
            
            elif current_status == "QUEUED":
                print(f"⏳ Notebook is queued...")
            
            last_status = current_status
        else:
            # Still same status, print a heartbeat
            if current_status == "RUNNING":
                print(f"[{timestamp}] Still running... ({elapsed}m elapsed)", end="\r")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("\n🚀 Kaggle Notebook Monitor")
    print("Press Ctrl+C to stop monitoring\n")
    
    try:
        monitor()
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
