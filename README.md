# Modular Engine

## 📚 Project Overview  
This Django project allows dynamic installation, uninstallation, and upgrading of modules. The core example is a `sample_module` (Product Management) that can be installed and managed from a modular engine UI.  

## ✅ Features  
- Modular system with install, uninstall, and upgrade functions  
- Automatic migrations on module installation and upgrades  
- Role-based permissions (Manager, User, Public) for CRUD operations  
- Confirmation popup before deletion  
- Seamless redirection to module landing pages  

## 📁 Project Structure  
- modular_engine
    - models.py (InstalledModule model)
    - views.py (install, uninstall, upgrade, module list views)
    - templates/
- sample_module
    - models.py (Product model)
    - apps.py (SampleModuleConfig with metadata & post-migrate hook)


## 🛠 Installation  
1. Unzip folder 
2. source env/bin/activate
3. Install dependencies pip install -r requirements.txt
4. Run python manage.py install_modular_engine
5. go to /base_url/admin to create user. You can add group(manager, user, public) to that user. It is used for permission CRUD of product.

## ▶️ Usage
- Visit /module/ to see available modules
- Install a module by clicking "Install"
- After install, you'll be redirected to the landing page (e.g., /products/)
- Role-based permissions are set automatically:
    - Manager: Full CRUD
    - User: Create, Read, Update
    - Public: Read only

## 🔁 Upgrade Flow
- Click "Upgrade" to re-run migrations for the module and redirect to the landing page

## ❌ Uninstall Flow
- Clicking "Uninstall" removes the module entry and redirects to module list

## 👩‍💻 Running Tests
- coverage run manage.py test
- coverage report
- coverage html
