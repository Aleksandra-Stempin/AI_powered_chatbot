import subprocess
import pkg_resources
import sys

def install_modules(modules):
    err_msg = ""
    success_msg_1 = ""
    success_msg_2 = ""
    success_msg = ""
    installed_modules = ""
    new_installed_modules = ""
    for module in modules:
        try:
            # Check if the module is already installed
            dist = pkg_resources.get_distribution(module)
            installed_modules = installed_modules + module + ", "
        except pkg_resources.DistributionNotFound:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                new_installed_modules = new_installed_modules + ", " + module
            except subprocess.CalledProcessError as e:
                module_failed_to_install = f'''Failed to install {module}.
Error: {e}
'''
                err_msg = err_msg + module_failed_to_install
            err_msg = err_msg.strip()
    if (len(err_msg)>0):
        print(err_msg)
    else:
        installed_modules = installed_modules.strip()
        installed_modules = installed_modules.strip(",")
        new_installed_modules = new_installed_modules.strip()
        new_installed_modules = new_installed_modules.strip(",")
        if (len(new_installed_modules)>3):
            success_msg_1 = f'Modules {new_installed_modules} were added.'
        if(len(installed_modules)>3):
            success_msg_2 = f'''Modules {installed_modules} have already been installed.'''
        success_msg = success_msg_1 +"\n" + success_msg_2
        print(success_msg)

# List of modules to be installed
modules_list = ["tkinter", "time", "pyperclip", "google.generativeai"]

# Install the modules
install_modules(modules_list)