import os
import shutil

# Empty /public directory and recursively add everything from /static
# Also logs the path of each file copied
def copy_static_files():
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    public_dir = os.path.join(os.path.dirname(__file__), '..', 'public')

    # If public directory exists, remmove it
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    # Create new public directory
    os.mkdir(public_dir)

    # Recursively copies all files and directories from static to public
    print(f"Beginning file copy process")
    copy_recursively(static_dir, public_dir)

def copy_recursively(src, dst):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            print(f"Copying directory: {src_path} to {dst_path}")
            os.mkdir(dst_path)
            copy_recursively(src_path, dst_path)
        else:
            print(f"Copying file: {item}")
            shutil.copy(src_path, dst_path)

    

def main():
    copy_static_files()

main()