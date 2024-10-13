import pytest
from informed.astar import AStarLogic

class TestAStar:
    @pytest.fixture
    def astar_logic(self):
        # Create mock objects for the required arguments
        mock_canvas = type('MockCanvas', (), {'create_text': lambda *args, **kwargs: None})()
        
        def mock_update_node_color(*args):
            pass
        
        def mock_show_goal_message(*args):
            pass
        
        mock_node_lines = {}

        # Initialize AStarLogic with all required arguments
        astar = AStarLogic(
            canvas=mock_canvas,
            update_node_color=mock_update_node_color,
            show_goal_message=mock_show_goal_message,
            node_lines=mock_node_lines
        )

        # Set up a simple graph for testing
        astar.edges = [
            ('S', 'N'), ('S', 'Q'), ('S', 'T'), ('S', 'E'),
            ('N', 'J'), ('J', 'I'), ('I', 'U'), ('U', 'A'), ('U', 'L'),
            ('Q', 'U'), ('T', 'Q'), ('T', 'L'), ('L', 'B'), ('B', 'H'),
            ('H', 'D'), ('D', 'R'), ('R', 'E'), ('E', 'G'), ('E', 'F'), ('E', 'K'),
            ('F', 'M'), ('F', 'O'), ('M', 'P'), ('K', 'O'), ('P', 'C'), ('O', 'C')
        ]

        astar.SURIGAO_DEL_NORTE_DISTANCE = {
            'A': 46.3, 'B': 38.7, 'C': 104, 'D': 55.1, 'E': 65.2, 
            'F': 87.3, 'G': 80.4, 'H': 52.7, 'I': 36.1, 'J': 30.9, 
            'K': 90.70, 'L': 31.8, 'M': 94.2, 'N': 10.6, 'O': 93.5, 
            'P': 102, 'Q': 19.3, 'R': 95.7, 'S': 0, 'T': 23.5, 'U': 35.2
        }

        astar.SURIGAO_DEL_NORTE_COST = {
            'A': 37.57, 'B': 25.95, 'C': 68.45, 'D': 35.67, 'E': 61.45, 
            'F': 54.70, 'G': 72.12, 'H': 21.20, 'I': 28.06, 'J': 21.70, 
            'K': 67.00, 'L': 19.16, 'M': 59.33, 'N': 7.98, 'O': 67.00, 
            'P': 64.70, 'Q': 15.30, 'R': 52.22, 'S': 0, 'T': 14.35, 'U': 27.67
        }
        return astar

    def test_astar_simple_path(self, astar_logic):
        path = astar_logic.astar('A', 'E')
        assert path == ['A', 'U', 'Q', 'S', 'E']

    def test_astar_no_path(self, astar_logic):
        # Remove all edges to E
        astar_logic.edges = [edge for edge in astar_logic.edges if 'E' not in edge]
        path = astar_logic.astar('A', 'E')
        assert path is None

    def test_astar_goal_not_in_graph(self, astar_logic):
        path = astar_logic.astar('A', 'Z')
        assert path is None

    def test_astar_start_is_goal(self, astar_logic):
        path = astar_logic.astar('A', 'A')
        assert path == ['A']

    def test_astar_heuristic(self, astar_logic):
        assert astar_logic.heuristic('A', 'E') == 46.3
        assert astar_logic.heuristic('C', 'E') == 104
        assert astar_logic.heuristic('E', 'E') == 65.2

    def test_astar_get_neighbors(self, astar_logic):
        neighbors = astar_logic.get_neighbors('E')
        assert set(neighbors) == {'F', 'G', 'K', 'R', 'S'}

    def test_astar_reconstruct_path(self, astar_logic):
        came_from = {'E': 'D', 'D': 'C', 'C': 'A', 'A': None}
        path = astar_logic.reconstruct_path(came_from, 'A', 'E')
        assert path == ['A', 'C', 'D', 'E']
