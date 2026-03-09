"""Fixtures nbforager/foragers/joiner.py."""
import pytest

from nbforager import nb_tree
from nbforager.foragers.joiner import Joiner
from nbforager.nb_tree import NbTree
from tests import functions as func


@pytest.fixture
def joiner() -> Joiner:
    """Initialize Joiner with root data."""
    tree: NbTree = func.full_tree()
    tree = nb_tree.join_tree(tree)
    joiner_ = Joiner(tree=tree)
    joiner_.init_extra_keys()
    return joiner_
