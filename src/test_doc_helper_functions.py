import unittest
from doc_helper_functions import *

class TestDocHelperFunctions(unittest.TestCase):
    # 
    # Tests for markdown_to_html function
    # 
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
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        )
    
    def test_blockquote(self):
        md = """
> This is a blockquote
> with multiple lines
> and _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote<br/>with multiple lines<br/>and <i>italic</i> text</blockquote></div>"
        )
    
    def test_unordered_list(self):
        md = """
- This is an unordered list
- with multiple items
- and _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list</li><li>with multiple items</li><li>and <i>italic</i> text</li></ul></div>"
        )

    def test_unordered_list_of_links(self):
        md = """
- [This is a link](http://example.com)
- [This is another link](http://example.com)
- [This is a third link](http://example.com)
"""
        node = markdown_to_html_node(md)
        # print("\n\n///\n")
        # print(node.__repr__())
        # print("\n///\n\n")
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><a href=\"http://example.com\" target=\"_blank\">This is a link</a></li><li><a href=\"http://example.com\" target=\"_blank\">This is another link</a></li><li><a href=\"http://example.com\" target=\"_blank\">This is a third link</a></li></ul></div>"
        )
    
    def test_ordered_list(self):
        md = """
1. This is an ordered list
2. with multiple items
3. and **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>with multiple items</li><li>and <b>bold</b> text</li></ol></div>"
        )

    def test_headings(self):
        md = """
# This is an h1 heading

## This is an h2 heading

### This is an h3 heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an h1 heading</h1><h2>This is an h2 heading</h2><h3>This is an h3 heading</h3></div>"
        )
    
    def test_mixed_content(self):
        md = """
# This is an h1 heading

## This is an h2 heading

This is a paragraph that follows the headings

```
This is text that _should_ remain
the **same** even with inline stuff
1. Potato
2. Tomato
3. A cat?!
```

> This is a blockquote
> with multiple lines
> and _italic_ text

- This is an unordered list
- with multiple items
- and _italic_ text

1. This is an ordered list
2. with multiple items
3. and **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is an h1 heading</h1><h2>This is an h2 heading</h2><p>This is a paragraph that follows the headings</p><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n1. Potato\n2. Tomato\n3. A cat?!\n</code></pre><blockquote>This is a blockquote<br/>with multiple lines<br/>and <i>italic</i> text</blockquote><ul><li>This is an unordered list</li><li>with multiple items</li><li>and <i>italic</i> text</li></ul><ol><li>This is an ordered list</li><li>with multiple items</li><li>and <b>bold</b> text</li></ol></div>"
        )
    
    def test_blockquotes_again(self):
        md = """
> This is a blockquote
> with multiple lines
> of text
> 
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote<br/>with multiple lines<br/>of text<br/><br/>\"I am in fact a Hobbit in all but size.\"<br/><br/>-- J.R.R. Tolkien</blockquote></div>"
        )