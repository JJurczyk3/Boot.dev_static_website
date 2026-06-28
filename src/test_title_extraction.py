import unittest
from parse_md_blocks import extract_title


class TestTitleExtraction(unittest.TestCase):

    def test_title_generation_case1(self):
        markdown = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
"""
        expected = "Tolkien Fan Club"
        actual = extract_title(markdown)
        self.assertEqual(expected, actual)


    def test_title_generation_case2(self):
        markdown = """## Tolkien Fan Club

# Spider-Man 3
"""
        expected = "Tolkien Fan Club"
        actual = extract_title(markdown)
        self.assertNotEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()