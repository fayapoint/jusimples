#!/usr/bin/env python3
"""
Fix for the status filter in admin_dashboard_v2.py
"""
import os

def fix_status_filter():
    # Read the file
    filepath = "admin_dashboard_v2.py"
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Create the replacement for status filter handling
    old_filter = """                    # Status filter
                    if status_filter != 'all':
                        success_value = status_filter == 'success'
                        if 'success' in log and log['success'] != success_value:
                            should_include = False"""
    
    new_filter = """                    # Status filter
                    if status_filter != 'all':
                        success_value = status_filter == 'success'
                        if 'success' in log:
                            # Convert to boolean if it's a string
                            if isinstance(log['success'], str):
                                log_success = log['success'].lower() == 'true'
                            else:
                                log_success = bool(log['success'])
                                
                            if log_success != success_value:
                                should_include = False"""
    
    # Replace all occurrences
    updated_content = content.replace(old_filter, new_filter)
    
    # Write the updated content back
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print(f"✅ Updated status filter handling in {filepath}")
    
    return True

if __name__ == "__main__":
    fix_status_filter()
