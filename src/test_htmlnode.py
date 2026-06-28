import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_none(self):
        # Test 1: When props is None or empty, it should return an empty string
        node = HTMLNode("p", "Hello world", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        # Test 2: A single property should format correctly with a leading space and quotes
        node = HTMLNode("a", "Boot.dev", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_props_to_html_multiple(self):
        # Test 3: Multiple properties should be separated by spaces
        node = HTMLNode("a", "Boot.dev", None, {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')


class TestLeafNode(unittest.TestCase):
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_without_tag(self):
        node = ParentNode(None, [LeafNode("b", "text")])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a tag.")

    def test_to_html_deep_nesting(self):
        leaf = LeafNode("code", "print('Hello World!')")
        mid_parent = ParentNode("span", [leaf], {"class": "code-block"})
        top_parent = ParentNode("div", [mid_parent], {"id": "main"})
        self.assertEqual(
            top_parent.to_html(),
            '<div id="main"><span class="code-block"><code>print(\'Hello World!\')</code></span></div>'
        )


if __name__ == "__main__":
    unittest.main()