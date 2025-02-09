import shutil

from blocks import generate_page


def copy_file_to_public_dir():
    # delete all content from public dir
    shutil.rmtree("./public")
    # copy all files from static dir into clean public dir
    shutil.copytree("./static", "./public")


def main():
    copy_file_to_public_dir()
    # generate a html page from template and md file
    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
