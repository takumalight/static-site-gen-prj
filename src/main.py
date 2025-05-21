import os
import shutil
from doc_helper_functions import markdown_to_html_node

# Empty /public directory and recursively add everything from /static
# Also logs the path of each file copied
def copy_static_files():
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    public_dir = os.path.join(os.path.dirname(__file__), '..', 'public')

    # If public directory exists, remmove it
    if os.path.exists(public_dir):
        print(f"Removing existing public directory")
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

def extract_title(markdown_file):
    f = open(markdown_file, 'r')
    markdown_text = f.read()
    f.close()
    for line in markdown_text.splitlines():
        if line.startswith('# '):
            title = line[1:].strip()
            if title:
                return title
    raise Exception("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"\nGenerating page from {from_path} to {dest_path} using template {template_path}\n")
    md = open(from_path, 'r')
    markdown_text = md.read()
    md.close()

    tp = open(template_path, 'r')
    template_text = tp.read()
    tp.close()

    html_text = markdown_to_html_node(markdown_text).to_html()
    title = extract_title(from_path)

    template_text = template_text.replace("{{ Title }}", title)
    template_text = template_text.replace("{{ Content }}", html_text)

    with open(dest_path, 'w') as f:
        f.write(template_text)

    

def main():
    copy_static_files()
    generate_page(
        os.path.join(os.path.dirname(__file__), '..', 'content', 'index.md'),
        os.path.join(os.path.dirname(__file__), '..', 'template.html'),
        os.path.join(os.path.dirname(__file__), '..', 'public', 'index.html')
    )

main()