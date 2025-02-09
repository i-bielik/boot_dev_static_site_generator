import shutil

from blocks import generate_page, generate_pages_recursive


def copy_file_to_public_dir():
    # delete all content from public dir
    shutil.rmtree("./public")
    # copy all files from static dir into clean public dir
    shutil.copytree("./static", "./public")


def main():
    copy_file_to_public_dir()
    # generate a html page from template and md file
    generate_pages_recursive("content", "./template.html", "public")


if __name__ == "__main__":
    main()
