class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list['HTMLNode']=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        formatted = ""
        for key in self.props:
            formatted += f' {key}="{self.props[key]}"'
        return formatted
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value.")
        
        if not self.tag:
            return self.value
        
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag: 
            raise ValueError("All parent nodes must have a tag.")
        
        if not self.children:
            raise ValueError("All parent nodes must have children.")

        formatted = f'<{self.tag}{self.props_to_html()}>'
        
        for child in self.children:
            formatted += f'{child.to_html()}'

        formatted += f'</{self.tag}>'
        return formatted

        