""" Contains functions relating to the Anemone Build Configuration file format """
import os.path

#TODO: consider iterators
# pylint: disable=C0200
def parse(filepath):
    """ Loads a file (expecting it to be of the abc format) and returns abc-object """
    if not os.path.isfile(filepath):
        return None

    file = open(filepath, "r", -1, "utf-8")
    line = file.readline()
    current_node = root = ABCNode("root")

    while line is not "": #end of file
        if line.find("#") is not -1:
            line = line.split("#", 1)[0]
        if line.strip() == "":
            line = file.readline()
            continue
        if line[0] != '\t':
            current_node = root

        for char_index in range(len(line)):
            if line[char_index] == '=':
                if char_index == 0: #no key
                    break
                key = line[:char_index].strip()
                if len(key) is 0:
                    break
                value = line[char_index+1:].strip()
                if len(value) is 0:
                    value = None
                current_node.set(line[:char_index].strip(), value)
            elif line[char_index] == ':':
                if char_index == 0: #no key
                    return
                key = line[:char_index].strip()
                current_node = ABCNode(key, current_node)
        line = file.readline()
    return root
#pylint: enable=C0200

class ABCNode(object):
    """ABCNode containing the values and subnodes for parsed abc file"""
    def __init__(self, key, parent=None):
        super(ABCNode, self).__init__()
        self.m_values = dict()
        self.m_nodes = dict()
        self.m_key = key
        self.m_parent = parent
        if parent is not None:
            parent.set_subnode(key, self)

    def __getitem__(self, key):
        return self.m_nodes[key]

    def __setitem__(self, key, value):
        if isinstance(ABCNode, value):
            self.set_subnode(key, value)

    def __delitem__(self, key):
        node = self[key]
        if node is not None:
            del node.m_key, node.m_values, node.m_nodes

    def __repr__(self):
        return "{}({})[{}]".format(self.m_key, len(self.m_values), len(self.m_nodes))

    def get(self, key):
        """ gets a value out of the nodes internal dictionary,
            returns NoneType if value was not found """
        value = self.m_values.get(key, None)
        if value is None:
            if self.m_parent is not None:
                return self.m_parent.get(key)
        return value

    def set(self, key, value):
        """ Sets setting in internal value dictionary """
        self.m_values[key] = value

    def set_subnode(self, key, node):
        """ Creates a new node in this nodes internal dict of nodes.
            Overrides subnode if already defined. """
        self.m_nodes[key] = node
        node.m_parent = self
        return node
