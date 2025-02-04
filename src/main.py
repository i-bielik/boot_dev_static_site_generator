import shutil


def copy_file_to_public_dir():
    # delete all content from public dir
    shutil.rmtree("./public")
    # copy all files from static dir into clean public dir
    shutil.copytree("./static", "./public")


def main():
    copy_file_to_public_dir()


if __name__ == "__main__":
    main()
