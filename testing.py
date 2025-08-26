from imports import *

SYSTEM = platform.system().lower()

def get_pictures_path():
    # Check if OneDrive is managing Pictures
    user_profile = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    onedrive_path = os.environ.get("OneDrive")
    print(onedrive_path)
    # Default Pictures path
    default_pictures = os.path.join(user_profile, "Pictures")
    onedrive_pictures = os.path.join(onedrive_path, "Pictures") if onedrive_path else None
    print(os.path.exists(onedrive_pictures))
    # Use OneDrive path if it exists and is valid
    if onedrive_pictures and os.path.exists(onedrive_pictures):
        return os.path.join(onedrive_pictures, "SEOLookup")
    else:
        return os.path.join(default_pictures, "SEOLookup")

try:
    print("Trying to create Pictures\\SEOLookup Directory")
    path = get_pictures_path()

    if SYSTEM == "windows":
        #os.makedirs(path, exist_ok=True)
        pass
    elif SYSTEM == "linux":
        #os.makedirs(path.replace('\\', '/'), exist_ok=True)
        pass
    print(f"Directory created at: {path}")
except Exception as e:
    print(f"Error creating directory: {e}")
