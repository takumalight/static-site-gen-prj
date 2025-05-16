from textnode import *

def main():
    test_node = TextNode("Test String", TextType.LINK, "http://example.com")
    
    print(test_node.__repr__())

main()