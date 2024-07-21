import datetime
import random

import requests

from app.app import app, db
from app.models import Employees
# from crud.

from crud.fake_data import create_employer
from crud.tree_data_test import test_ids_list


class TreeNode:
    def __init__(self, value, depth=0):
        self.value = value
        self.depth = depth
        self.children = list()

    def add_child(self, child_node):
        """
        Добавляет нового работника в дерево
        :param child_node:
        :return: None
        """
        if self.depth < 4:
            child_node.depth = self.depth + 1
            self.children.append(child_node)
        else:
            raise Exception("Max depth exceeded")

    def __repr__(self):
        return f"Tree Node({self.value}, depth={self.depth})"


class Tree:
    def __init__(self, root_node):
        self.root = TreeNode(root_node)

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
        Полгый список работников
        :return: list
        """
        nodes = []
        self._collect_nodes(self.root, nodes)
        return nodes

    def _collect_nodes(self, node, nodes):
        """
        Добавляет нового работника в список ранее добалвенных работников
        :param node:  dict
        :param nodes: dict
        :return: None
        """
        nodes.append(node)
        for child in node.children:
            self._collect_nodes(child, nodes)

    def get_random_node(self) -> TreeNode:
        """
        Выбирает рандомных работников из списка
        :return:
        """
        all_nodes = self.get_all_nodes()
        return random.choice(all_nodes)


if __name__ == '__main__':
    def add_db_user(user):
        """
        Добавляет работника d <L
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
        res = requests.post('http://localhost:5000/bosses', json={"ids": [user1, user2]})
        res = res.json()
        message = res["message"]
        print(message)


    m_dir = Tree(create_employer())
    m_dir_id = add_db_user(m_dir.root.value)

    for i in range(5):
        d = TreeNode(create_employer())
        d_id = add_db_user(d.value)

        m_dir.root.add_child(d)
        add_links(m_dir_id, d_id)

        for j in range(10):
            s_d = TreeNode(create_employer())
            s_d_id = add_db_user(s_d.value)

            d.add_child(s_d)
            add_links(d_id, s_d_id)
    #
    # К 10 ВЫШЕ ДОБАВЛЕННЫМ ДОБАВЛЯЕМ ЕЩЕ 10  ПОДЧИНЕННЫХ
            for k in range(10):
                s_s_d = TreeNode(create_employer())
                s_s_d_id = add_db_user(s_s_d.value)
    #
                d.add_child(s_s_d)
                add_links(d_id, s_s_d_id)


                for l in range(100):
                    s_s_s_d = TreeNode(create_employer())
                    s_s_s_d_id = add_db_user(s_s_s_d.value)


                    s_s_d.add_child(s_s_s_d)
                    add_links(d_id, s_s_s_d_id)
    #
    # print(m_dir)
