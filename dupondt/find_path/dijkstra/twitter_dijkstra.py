import math
from tqdm import tqdm

from dupondt.find_path.dijkstra.dijkstra import dijkstra
from dupondt.fetch_tw_data import FetchTwitterData


class Id:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)


class TwitterDijkstra:
    def __init__(self, apis: list, direction: str = 'from_user', verbose: bool = False):
        """
        Args:
            direction ('from_user' | 'from_mutual'): The direction to fetch the data from.
        """
        self.fetcher = FetchTwitterData(apis, verbose)
        self.direction = direction

        self.scores = {}

        if verbose:
            self.pbar = tqdm()
        else:
            self.pbar = None

    def get_children_nodes(self, user: Id) -> list[Id]:
        """
        Get the mutuals of a user.

        Args:
            user: The user.
        """
        mutuals = self.fetcher.fetch_mutuals(user.id)

        if self.pbar is not None:
            self.pbar.reset()
            self.pbar.total = len(mutuals)

        self.fetch_score(user)

        return [Id(mutual) for mutual in mutuals]

    def fetch_score(self, user: Id):
        """
        Args:
            user: The user.
        """
        score = self.fetcher.get_scores(user.id)

        self.scores[user.id] = {k: v['retweets'] * 1.1 + v['favorites'] * 1 + v['replies'] * 1.3
                                for k, v in score.items()}

        if self.pbar is not None:
            self.pbar.update(1)

    def get_score(self, user: Id, mutual: Id) -> float:
        """
        Get the score between two users.

        Args:
            user: The user.
            mutual: The mutual.
        """
        if user.id not in self.scores or mutual.id not in self.scores[user.id]:
            return math.inf

        return 1 / self.scores[user.id][mutual.id]

    def run(self, source_id: int, target_id: int):
        """
        Get the shortest path between two users.

        Args:
            source_id (int): The source user id.
            target_id (int): The target user id.
        """
        return dijkstra(Id(source_id), Id(target_id),
                        self.get_children_nodes, self.get_score)
