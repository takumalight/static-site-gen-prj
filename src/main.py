import sys
import os
import shutil
from doc_helper_functions import markdown_to_html_node

# Empty /docs directory and recursively add everything from /static
# Also logs the path of each file copied
def copy_static_files():
    static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'docs')

    # If docs directory exists, remove it
    if os.path.exists(docs_dir):
        print(f"Removing existing docs directory")
        shutil.rmtree(docs_dir)
    
    # Create new docs directory
    os.mkdir(docs_dir)

    # Recursively copies all files and directories from static to docs
    print(f"Beginning file copy process")
    copy_recursively(static_dir, docs_dir)

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

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith('# '):
            title = line[1:].strip()
            if title:
                return title
    raise Exception("No title found in markdown")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"\nGenerating page from {from_path} to {dest_path} using template {template_path}\n")
    md = open(from_path, 'r')
    markdown_text = md.read()
    md.close()

    tp = open(template_path, 'r')
    template_text = tp.read()
    tp.close()

    title = extract_title(markdown_text)
    html_text = markdown_to_html_node(markdown_text).to_html()

    template_text = template_text.replace("{{ Title }}", title)
    template_text = template_text.replace("{{ Content }}", html_text)
    template_text = template_text.replace('href="/', f'href="{basepath}')
    template_text = template_text.replace('src="/', f'src="{basepath}')

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w') as f:
        f.write(template_text)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            if not os.path.exists(new_dest_dir):
                os.makedirs(new_dest_dir)
            generate_pages_recursive(item_path, template_path, new_dest_dir, basepath)
        elif item.endswith('.md'):
            dest_file = os.path.splitext(item)[0] + '.html'
            dest_path = os.path.join(dest_dir_path, dest_file)
            generate_page(item_path, template_path, dest_path, basepath)

    

def main():
    basepath = "/" 
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    copy_static_files()

    generate_pages_recursive(
        os.path.join(os.path.dirname(__file__), '..', 'content'),
        os.path.join(os.path.dirname(__file__), '..', 'template.html'),
        os.path.join(os.path.dirname(__file__), '..', 'docs'),
        basepath
    )


main()