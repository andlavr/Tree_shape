import json
import random

import requests
from faker import Faker

fake = Faker('ru_RU')


def create_employer():
    """
    Создает фейкового работника
    :return: dict
    """

    fullname = fake.name()
    return {
        "surname": fullname.split()[0],
        "name": fullname.split()[1],
        "patronymic": fullname.split()[2],
        "position": fake.job(),
        "start_work_date": fake.date(),
        "salary": random.randint(10000, 100000),
    }


def add_employer(user):
    """
    Добавляет работника в БД

    :param user:
    :return: id
    """

    res = requests.post('http://localhost:5000/employer', json={"user": user})
    res = res.json()
    message, id_ = res["message"], res["id"]
    print(message)
    return id_


def add_links(user1, user2):
    """
    Объединяет работника и босса

    :param user1: id
    :param user2: id
    :return: None
    """

    res = requests.post('http://localhost:5000/subordination_links', json={"ids": [user1, user2]})
    res = res.json()
    message = res["message"]
    print(message)


class TreeNode:
    def __init__(self, value, depth=0, parent=None):
        self.value = value
        self.depth = depth
        self.parent = parent
        self.children = list()

    def add_child(self, child_node):
        """
        Добавляет новую ноду в дерево
        :param child_node:
        :return: None
        """
        if self.depth < 4:
            child_node.depth = self.depth + 1
            child_node.parent = self
            self.children.append(child_node)
        else:
            raise Exception("Max depth exceeded")

    def to_dict(self):
        """
        Конвертирует ноду и её детей в словарь
        :return: dict
        """
        return {
            'value': self.value,
            'depth': self.depth,
            'children': [child.to_dict() for child in self.children]
        }

    @classmethod
    def from_dict(cls, data, parent=None):
        """
        Создаёт ноду из словаря
        :param data: dict
        :param parent: TreeNode
        :return: TreeNode
        """
        node = cls(data['value'], data['depth'], parent)
        node.children = [cls.from_dict(child, node) for child in data['children']]
        return node

    def __repr__(self):
        return f"TreeNode({self.value}, depth={self.depth})"


class Tree:
    def __init__(self, root_value):
        self.root = TreeNode(root_value)
        self._iter_nodes = []

    def __repr__(self):
        nodes = []
        self._moving(self.root, nodes, level=0)
        return "\n".join(nodes)

    def _moving(self, node, nodes, level):
        nodes.append(" " * (level * 4) + repr(node))
        for child in node.children:
            self._moving(child, nodes, level + 1)

    def get_all_nodes(self):
        """
        Полный список нод
        :return: list
        """
        nodes = []
        self._collect_nodes(self.root, nodes)
        return nodes

    def _collect_nodes(self, node, nodes):
        """
        Получение всех нод текущей ноды

        :param node:  TreeNode
        :param nodes: list
        :return: None
        """
        nodes.append(node)
        for child in node.children:
            self._collect_nodes(child, nodes)

    def get_random_node(self) -> TreeNode:
        """
        Выбирает случайную ноду из дерева

        :return: TreeNode
        """
        all_nodes = self.get_all_nodes()
        return random.choice(all_nodes)

    def to_json(self):
        """
        Сериализует дерево в JSON строку
        :return: str
        """
        return json.dumps(self.root.to_dict(), ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls, json_str):
        """
        Десериализует дерево из JSON строки
        :param json_str: str
        :return: Tree
        """
        data = json.loads(json_str)
        root_node = TreeNode.from_dict(data)
        tree = cls(root_node.value)
        tree.root = root_node
        return tree

    def get_nodes_at_depth(self, depth):
        """
        Возвращает все ноды на указанной глубине
        :param depth: int
        :return: list of TreeNode
        """
        nodes_at_depth = []
        self._collect_nodes_at_depth(self.root, depth, nodes_at_depth)
        return nodes_at_depth

    def _collect_nodes_at_depth(self, node, depth, nodes_at_depth):
        """
        Рекурсивно собирает ноды на указанной глубине
        :param node: TreeNode
        :param depth: int
        :param nodes_at_depth: list
        :return: None
        """
        if node.depth == depth:
            nodes_at_depth.append(node)
        for child in node.children:
            self._collect_nodes_at_depth(child, depth, nodes_at_depth)

    def __iter__(self):
        """
        Возвращает итератор для дерева
        :return: self
        """
        self._iter_nodes = self.get_all_nodes()
        self._index = 0
        return self

    def __next__(self):
        """
        Возвращает следующий элемент при итерации
        :return: TreeNode
        """
        if self._index < len(self._iter_nodes):
            node = self._iter_nodes[self._index]
            self._index += 1
            return node
        else:
            raise StopIteration


if __name__ == '__main__':

    m_dir = Tree(create_employer())
    # m_dir_id = add_employer(m_dir.root.value)

    for _ in range(5):
        d = TreeNode(create_employer())
        # d_id = add_employer(d.value)

        m_dir.root.add_child(d)
        # add_links(m_dir_id, d_id)

        for _ in range(10):
            s_d = TreeNode(create_employer())
            # s_d_id = add_employer(s_d.value)

            d.add_child(s_d)
            # add_links(d_id, s_d_id)

            for _ in range(10):
                s_s_d = TreeNode(create_employer())
                # s_s_d_id = add_employer(s_s_d.value)

                s_d.add_child(s_s_d)
                # add_links(s_d_id, s_s_d_id)

                for _ in range(100):
                    s_s_s_d = TreeNode(create_employer())
                    # s_s_s_d_id = add_employer(s_s_s_d.value)

                    s_s_d.add_child(s_s_s_d)
                    # add_links(s_s_d_id, s_s_s_d_id)

    tree = m_dir.to_json()
    res = requests.post('http://localhost:5000/fill_db', json={"tree": tree})
    res = res.json()
    message = res["message"]
    print(message)
