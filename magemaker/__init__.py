import os

import pkg_resources
import subprocess

def pre_flight():
    print('running preflight checks')


    scripts_dir = pkg_resources.resource_filename('magemaker', 'scripts')
    setup_script = os.path.join(scripts_dir, 'preflight.sh')
    setup_role_script = os.path.join(scripts_dir, 'setup_role.sh')
    
    # Make scripts executable
    os.chmod(setup_script, 0o755)
    os.chmod(setup_role_script, 0o755)
    
    
    # Use subprocess instead of os.system for better error handling
    try:
        subprocess.run(['bash', setup_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing setup.sh: {e}")
        return 1
    except FileNotFoundError:
        print("Could not find setup.sh in the installed package")
        return 1

    import dotenv
    dotenv.load_dotenv('.env')
    # Rest of your main function code
    return 0

pre_flight()
# print('sometihng', os.getpwd())
# if (not os.path.exists(os.path.expanduser('~/.aws')) or not os.path.exists('.env')):
#     os.system("bash setup.sh")