#!/usr/bin/env python3
"""
Quick fix for the status filter issue in admin_dashboard_v2.py
"""
import re

def apply_status_filter_fix():
    # Path to the file
    file_path = 'admin_dashboard_v2.py'
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Fix for search logs status filter
        search_pattern = r"(# Status filter\s+if status_filter != 'all':\s+success_value = status_filter == 'success'\s+if 'success' in log and log\['success'\] != success_value:)"
        search_replacement = """# Status filter
                    if status_filter != 'all':
                        success_value = status_filter == 'success'
                        if 'success' in log:
                            # Convert to boolean if it's a string 'true'/'false'
                            if isinstance(log['success'], str):
                                log_success = log['success'].lower() == 'true'
                            else:
                                log_success = bool(log['success'])
                                
                            if log_success != success_value:"""
        
        # Replace both occurrences
        new_content = re.sub(search_pattern, search_replacement, content)
        
        # Write the modified content back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"✅ Successfully updated {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating file: {str(e)}")
        return False

if __name__ == "__main__":
    apply_status_filter_fix()
