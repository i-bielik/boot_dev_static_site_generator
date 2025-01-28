class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == {} or self.props is None:
            return ""
        htext = [f' {k}="{v}"' for k, v in self.props.items()]
        return "".join(htext)

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}) -> None:
        super().__init__(tag, value, [], props)
        if self.value is None:
            raise ValueError("Leaf node has to have value.")

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}) -> None:
        super().__init__(tag, None, children, props)
        if self.tag is None:
            raise ValueError("Object has to have a tag.")
        if self.children is None:
            raise ValueError("HTML children missing from constructor.")

    def to_html(self):
        html_tag = f"<{self.tag}"
        if self.props:
            html_tag += f"{self.props_to_html()}"
        html_tag += f">{self.children_to_html()}</{self.tag}>"
        return html_tag

    def children_to_html(self):
        html_str = ""
        for child in self.children:
            html_str += child.to_html()
        return html_str

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
