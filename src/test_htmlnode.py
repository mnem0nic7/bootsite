import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_no_implementation(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "my-class"})
        expected = ' class="my-class"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        node = HTMLNode("div", "Hello, world!", None, {"class": "greeting"})
        expected = "HTMLNode(div, Hello, world!, children: None, {'class': 'greeting'})"
        self.assertEqual(repr(node), expected)

    def test_values_defaults_to_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Main Title")
        self.assertEqual(node.to_html(), "<h1>Main Title</h1>")

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("img", "alt text", {"src": "image.jpg", "alt": "A picture", "class": "responsive"})
        expected = '<img src="image.jpg" alt="A picture" class="responsive">alt text</img>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_empty_props(self):
        node = LeafNode("span", "Some text", {})
        self.assertEqual(node.to_html(), "<span>Some text</span>")


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

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("tag", str(context.exception))

    def test_to_html_no_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertIn("children", str(context.exception))

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        expected = '<div class="container" id="main"><span>child</span></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_nested_parents(self):
        innermost = LeafNode("span", "text")
        middle = ParentNode("p", [innermost])
        outer = ParentNode("div", [middle])
        expected = "<div><p><span>text</span></p></div>"
        self.assertEqual(outer.to_html(), expected)

    def test_to_html_complex_nesting(self):
        # Create a complex nested structure
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode(None, " and ")
        leaf3 = LeafNode("i", "italic")
        para = ParentNode("p", [leaf1, leaf2, leaf3])
        
        leaf4 = LeafNode("a", "Link", {"href": "test.com"})
        div = ParentNode("div", [para, leaf4], {"class": "content"})
        
        expected = '<div class="content"><p><b>Bold</b> and <i>italic</i></p><a href="test.com">Link</a></div>'
        self.assertEqual(div.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
