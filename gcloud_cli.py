#!/usr/bin/env python3
"""
Google Cloud Authentication CLI for Genomic Twin Platform
Usage: python gcloud_cli.py [command] [options]
"""
import argparse
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.gcloud_auth import gcloud_login, is_authenticated, get_project_id, setup_authentication_instructions


def main():
    parser = argparse.ArgumentParser(description='Google Cloud Authentication for Genomic Twin Platform')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Login command
    login_parser = subparsers.add_parser('login', help='Authenticate with Google Cloud')
    login_parser.add_argument('--method', choices=['default', 'service_account'], 
                            default='default', help='Authentication method')
    login_parser.add_argument('--project', help='Google Cloud project ID')
    
    # Status command
    subparsers.add_parser('status', help='Check authentication status')
    
    # Setup command
    subparsers.add_parser('setup', help='Show setup instructions')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configure Google Cloud settings')
    config_parser.add_argument('--project', help='Set Google Cloud project ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'login':
        print("🔐 Authenticating with Google Cloud...")
        success = gcloud_login(method=args.method, project_id=args.project)
        if success:
            project = get_project_id()
            print(f"✅ Successfully authenticated with Google Cloud")
            if project:
                print(f"📋 Project: {project}")
        else:
            print("❌ Authentication failed")
            print("💡 Run 'python gcloud_cli.py setup' for setup instructions")
            sys.exit(1)
    
    elif args.command == 'status':
        authenticated = is_authenticated()
        project = get_project_id()
        
        print(f"Authentication Status: {'✅ Authenticated' if authenticated else '❌ Not authenticated'}")
        if project:
            print(f"Project: {project}")
        
        if not authenticated:
            print("\n💡 Run 'python gcloud_cli.py login' to authenticate")
    
    elif args.command == 'setup':
        print("📋 Google Cloud Authentication Setup Instructions:")
        print()
        setup_authentication_instructions()
    
    elif args.command == 'config':
        if args.project:
            os.environ['GOOGLE_CLOUD_PROJECT'] = args.project
            print(f"✅ Project set to: {args.project}")
            print("💡 To make this permanent, add to your environment variables:")
            print(f"export GOOGLE_CLOUD_PROJECT={args.project}")
        else:
            current_project = get_project_id() or os.getenv('GOOGLE_CLOUD_PROJECT', 'Not set')
            print(f"Current project: {current_project}")


if __name__ == '__main__':
    main()