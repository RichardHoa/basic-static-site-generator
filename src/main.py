from textnode import TextNode
import os
import shutil
from htmlnode import markdown_to_html_node, extract_title


def main():

    copy_folder("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_pages_recursive("./content", "./template.html", "./public")


def copy_folder(source, destination):
    # print(f"source: {source} | destination: {destination}")
    if os.path.exists(destination):
        # If the destination exists, delete it
        shutil.rmtree(destination)

    if os.path.exists(source):
        # If the source exists, make the destination folder and copy all the files from source to destination
        os.mkdir(destination)
        helper_copy_folder(source, destination)


def helper_copy_folder(path, destination):

    source_folder = os.listdir(path)
    for file in source_folder:
        current_path_with_file = os.path.join(path, file)
        destination_path_with_file = os.path.join(destination, file)

        if os.path.isdir(current_path_with_file):
            os.mkdir(destination_path_with_file)
            helper_copy_folder(current_path_with_file, destination_path_with_file)
        else:
            # print(f"file:{file} |{current_path_with_file} | {destination_path_with_file}")
            shutil.copy(current_path_with_file, f"{destination}")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read and create new file
    markdown_file = open(from_path, "r").read()
    html_file = open(template_path, "r").read()
    destination_file = open(dest_path, "w")

    # Convert markdown to html file
    html_converted = markdown_to_html_node(markdown_file).to_html()
    # Extract title of the file
    title = extract_title(markdown_file)
    # Write the full html file based on the template
    full_html = html_file.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_converted
    )
    # Write the file to the new destination
    destination_file.write(full_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    source_folder = os.listdir(dir_path_content)
    # print(f"dest_dir_path: {dest_dir_path}")
    for file in source_folder:
        current_path_with_file = os.path.join(dir_path_content, file)
        destination_path_with_file = os.path.join(
            dest_dir_path, file
        ).replace(".md", ".html")

        # print(
        #     f"{file} | current_path_with_file: {current_path_with_file} | destination_path_with_file: {destination_path_with_file}"
        # )
        if os.path.isfile(current_path_with_file):
            generate_page(
                current_path_with_file, template_path, destination_path_with_file
            )
        else:
            os.mkdir(destination_path_with_file)
            generate_pages_recursive(current_path_with_file, template_path, destination_path_with_file)


if __name__ == "__main__":
    main()
