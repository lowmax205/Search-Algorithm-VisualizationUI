import pytest
from uninformed.bfs import BFSLogic

class TestBFS:
    @pytest.fixture
    def bfs_logic(self):
        # Create a mock canvas and other necessary objects
        mock_canvas = type('MockCanvas', (), {'create_text': lambda *args, **kwargs: None})()
        return BFSLogic(mock_canvas, lambda *args: None, lambda *args: None)

    def test_bfs_simple_path(self, bfs_logic):
        # Define a simple graph
        bfs_logic.graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F', 'G'],
            'D': ['H', 'I'],
            'E': [],
            'F': ['J', 'K'],
            'G': [],
            'H': ['L'],
            'I': ['M'],
            'J': ['N'],
            'K': [],
            'L': [],
            'M': [],
            'N': []
        }

        # Run BFS
        path = bfs_logic.bfs('A', 'F')

        # Assert the correct path is found
        assert path == ['A', 'C', 'F']

    def test_bfs_no_path(self, bfs_logic):
        # Define a graph with no path to the goal
        bfs_logic.graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F', 'G'],
            'D': ['H', 'I'],
            'E': [],
            'F': ['J', 'K'],
            'G': [],
            'H': ['L'],
            'I': ['M'],
            'J': ['N'],
            'K': [],
            'L': [],
            'M': [],
            'N': []
        }

        # Run BFS
        path = bfs_logic.bfs('A', 'F')

        # Assert that no path is found
        assert path is None

    def test_bfs_goal_not_in_graph(self, bfs_logic):
        # Define a graph where the goal is not present
        bfs_logic.graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F', 'G'],
            'D': ['H', 'I'],
            'E': [],
            'F': ['J', 'K'],
            'G': [],
            'H': ['L'],
            'I': ['M'],
            'J': ['N'],
            'K': [],
            'L': [],
            'M': [],
            'N': []
        }
        # Run BFS
        path = bfs_logic.bfs('A', 'Z')

        # Assert that no path is found
        assert path is None

    # Add more test cases as needed
