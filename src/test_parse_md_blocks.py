import unittest
from parse_md_blocks import markdown_to_blocks, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_to_blocks_no_leading_or_trailing_blank_lines(self):
            md = """This is paragraph one

This is paragraph two

This is paragraph three"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is paragraph one",
                    "This is paragraph two",
                    "This is paragraph three",
                ],
            )

        def test_markdown_to_blocks_extra_blank_lines(self):
            md = """

This is paragraph one



This is paragraph two


This is paragraph three

"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is paragraph one",
                    "This is paragraph two",
                    "This is paragraph three",
                ],
            )


class TestMarkdownToHTML(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_heading(self):
        md = "# Hello"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>Hello</h1></div>")

    def test_markdown_to_html_paragraph(self):
        md = "Hello world"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>Hello world</p></div>")

    def test_markdown_to_html_bold(self):
        md = "This is **bold** text"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>This is <b>bold</b> text</p></div>")

    def test_markdown_to_html_italic(self):
        md = "This is _italic_ text"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>This is <i>italic</i> text</p></div>")

    def test_markdown_to_html_image(self):
        md = "![Alt text](/path/to/image.png)"
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<img", html)
        self.assertIn("src", html)
        self.assertIn("alt", html)

    def test_markdown_to_html_link(self):
        md = "[Boot.dev](https://www.boot.dev)"
        html = markdown_to_html_node(md).to_html()
        self.assertIn('<a href="https://www.boot.dev">Boot.dev</a>', html)

if __name__ == "__main__":
    unittest.main()