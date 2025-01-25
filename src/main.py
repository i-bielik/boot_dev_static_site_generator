from textnode import TextNode, TextType


def main():
    dummy = TextNode("This is example", TextType.BOLD, "https://www.boot.dev")
    print(dummy)


if __name__ == "__main__":
    main()
