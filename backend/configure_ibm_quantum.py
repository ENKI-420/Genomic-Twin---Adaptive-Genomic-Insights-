#!/usr/bin/env python3
"""
IBM Quantum Configuration Helper
Assists with setting up and validating IBM Quantum credentials.
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional


def load_token_from_json(json_path: str) -> Optional[str]:
    """Load IBM Quantum token from JSON file."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data.get('apikey') or data.get('token')
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None


def save_token_to_env(token: str, env_file: str = '.env'):
    """Save token to .env file."""
    env_path = Path(env_file)

    # Read existing content
    existing_content = ""
    if env_path.exists():
        with open(env_path, 'r') as f:
            existing_content = f.read()

    # Check if token already exists
    if 'QISKIT_IBM_TOKEN' in existing_content:
        print("⚠️  QISKIT_IBM_TOKEN already exists in .env file.")
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Aborted.")
            return False

        # Remove old token line
        lines = existing_content.split('\n')
        lines = [l for l in lines if not l.startswith('QISKIT_IBM_TOKEN')]
        existing_content = '\n'.join(lines)

    # Append new token
    with open(env_path, 'w') as f:
        if existing_content and not existing_content.endswith('\n'):
            existing_content += '\n'
        f.write(existing_content)
        f.write(f"QISKIT_IBM_TOKEN={token}\n")

    print(f"✓ Token saved to {env_path}")
    return True


def validate_token(token: str) -> bool:
    """Validate IBM Quantum token."""
    print("\n🔍 Validating token...")

    try:
        from qiskit_ibm_runtime import QiskitRuntimeService

        service = QiskitRuntimeService(
            channel='ibm_quantum',
            token=token
        )

        backends = service.backends()
        print(f"✓ Authentication successful!")
        print(f"✓ Found {len(backends)} available backends")

        print("\n📋 Hardware backends:")
        for backend in list(backends)[:10]:
            status = backend.status()
            print(f"   • {backend.name:20s} - {status.status_msg}")

        return True

    except ImportError:
        print("❌ qiskit-ibm-runtime not installed")
        print("   Install with: pip install qiskit-ibm-runtime")
        return False

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False


def interactive_setup():
    """Interactive setup wizard."""
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║   IBM Quantum Configuration Wizard                            ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")

    print("How would you like to provide your IBM Quantum token?\n")
    print("  1. Enter token manually")
    print("  2. Load from JSON file")
    print("  3. Load from environment variable")
    print("  4. Exit\n")

    choice = input("Select option (1-4): ").strip()

    token = None

    if choice == '1':
        print("\n📌 Get your token from: https://quantum.ibm.com/account\n")
        token = input("Enter your IBM Quantum token: ").strip()

    elif choice == '2':
        json_path = input("Enter path to JSON file: ").strip()
        token = load_token_from_json(json_path)
        if not token:
            print("❌ Could not load token from JSON file")
            return False

    elif choice == '3':
        token = os.getenv('QISKIT_IBM_TOKEN')
        if not token:
            print("❌ QISKIT_IBM_TOKEN environment variable not set")
            return False
        print(f"✓ Loaded token from environment")

    elif choice == '4':
        print("Exiting...")
        return True

    else:
        print("Invalid choice")
        return False

    if not token:
        print("❌ No token provided")
        return False

    # Validate token
    if not validate_token(token):
        return False

    # Offer to save to .env
    print("\n💾 Save token to .env file?")
    save_response = input("This will allow automatic loading in future runs (y/N): ").strip().lower()

    if save_response == 'y':
        project_root = Path(__file__).parent.parent
        env_file = project_root / '.env'
        save_token_to_env(token, str(env_file))

        # Add to .gitignore
        gitignore_path = project_root / '.gitignore'
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            if '.env' not in gitignore_content:
                with open(gitignore_path, 'a') as f:
                    f.write('\n.env\n')
                print("✓ Added .env to .gitignore")

    print("\n" + "="*65)
    print("✅ Configuration complete!")
    print("="*65)
    print("\nYou can now run quantum experiments with hardware backends.")
    print("\nExample:")
    print("  python3 backend/quantum_swarm.py --backend ibm_torino")
    print("\nOr run the full demo:")
    print("  ./demo_quantum_swarm.sh")
    print("="*65)

    return True


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Non-interactive mode
        if sys.argv[1] == '--validate':
            token = os.getenv('QISKIT_IBM_TOKEN')
            if not token:
                print("❌ QISKIT_IBM_TOKEN not set")
                sys.exit(1)
            success = validate_token(token)
            sys.exit(0 if success else 1)

        elif sys.argv[1] == '--from-json':
            if len(sys.argv) < 3:
                print("Usage: configure_ibm_quantum.py --from-json <path>")
                sys.exit(1)
            token = load_token_from_json(sys.argv[2])
            if token:
                if validate_token(token):
                    save_token_to_env(token)
                    sys.exit(0)
            sys.exit(1)

        else:
            print(f"Unknown option: {sys.argv[1]}")
            print("Usage:")
            print("  configure_ibm_quantum.py              # Interactive mode")
            print("  configure_ibm_quantum.py --validate   # Validate existing token")
            print("  configure_ibm_quantum.py --from-json <path>  # Load from JSON")
            sys.exit(1)
    else:
        # Interactive mode
        success = interactive_setup()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
