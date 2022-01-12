import datetime
import tweepy


class FetchTwitterData:
    def __init__(self, apis: list, verbose: bool = False):
        self.apis: list[tweepy.api] = apis
        self.api_index = 0
        self.api_exceptions: dict[int, datetime] = {}

        self.verbose: bool = verbose

    def update_usable_api(self):
        """
        Get the usable api.
    
        Returns:
            tuple[int, dict[int, datetime]]: The index of the usable api and the api exceptions.
        """
        # if self.verbose:
        #     print(f'    INFO: The api {self.api_index} has been used up. Search to use another api...')

        if not (self.api_index in self.api_exceptions and
                self.api_exceptions[self.api_index] + datetime.timedelta(minutes=15) > datetime.datetime.now()):
            self.api_exceptions[self.api_index] = datetime.datetime.now()

        self.api_index = (self.api_index + 1) % len(self.apis)

        while self.api_index in self.api_exceptions and \
                self.api_exceptions[self.api_index] + datetime.timedelta(minutes=15) > datetime.datetime.now():
            self.api_index = (self.api_index + 1) % len(self.apis)

        # if self.verbose:
        #     print(f'    INFO: Using api {self.api_index}.')

    def fetch_user_data(self, user_id: int):
        """
        Fetch the data of a user.
    
        Args:
            user_id (int): The user id to fetch the data of.
    
        Returns:
            tweepy.models.User: The data of the user.
        """
        try:
            return self.apis[self.api_index].get_user(user_id=user_id)
        except tweepy.errors.TooManyRequests:
            self.update_usable_api()
            return self.fetch_user_data(user_id)

    def fetch_followers(self, user_id: int, private_accounts=False, **kwargs) -> list:
        """
        Fetch the followers of a user.
    
        Args:
            self.apis (list[tweepy.api]): The list of self.apis to use.
            user_id (int): The user id to fetch the followers of.
            private_accounts (bool): Whether to include private accounts.
    
        Returns:
            list[int]: The list of followers of the user.
        """
        followers: list = kwargs.get('followers', [])
        cursor = tweepy.Cursor(self.apis[self.api_index].get_followers, user_id=user_id,
                               cursor=kwargs.get('cursor', None))

        try:
            for user in cursor.items():
                followers.append(user)
        except tweepy.errors.TooManyRequests:
            self.update_usable_api()
            return self.fetch_followers(user_id, followers=followers, cursor=cursor.iterator.next_cursor)

        if not private_accounts:
            followers = [user for user in followers if not user.protected]

        return followers

    def fetch_following(self, user_id: int, private_accounts=False, **kwargs) -> list:
        """
        Fetch the following of a user.
    
        Args:
            self.apis (list[tweepy.api]): The list of self.apis to use.
            user_id (int): The user id to fetch the following of.
            private_accounts (bool): Whether to include private accounts.
    
        Returns:
            list[int]: The list of following of the user.
        """
        following: list = kwargs.get('following', [])
        cursor = tweepy.Cursor(self.apis[self.api_index].get_friends, user_id=user_id,
                               cursor=kwargs.get('cursor', None))

        try:
            for user in cursor.items():
                following.append(user)
        except tweepy.errors.TooManyRequests:
            self.update_usable_api()
            return self.fetch_following(user_id, following=following, cursor=cursor.iterator.next_cursor)

        if not private_accounts:
            following = [user for user in following if not user.protected]

        return following

    def fetch_relationship(self, source_user_id: int, target_user_id: int):
        """
        Fetch the relationships of a list of users.
    
        Args:
            self.apis (list[tweepy.api]): The list of self.apis to use.
            source_user_id (int): The source user id to fetch the relationships of.
            target_user_id (int): The target user id to fetch the relationships of.
    
        Returns:
            dict: The relationships of the users.
        """
        try:
            return self.apis[self.api_index].get_friendship(source_id=source_user_id, target_id=target_user_id)
        except tweepy.errors.TooManyRequests:
            self.update_usable_api()
            return self.fetch_relationship(source_user_id, target_user_id)

    def fetch_mutuals(self, user_id: int) -> list[int]:
        """
        Fetch the mutuals of a user.
    
        Args:
            self.apis (list[tweepy.api]): The list of self.apis to use.
            user_id (int): The user id to fetch the mutuals of.
    
        Returns:
            list[int]: The list of mutuals of the user.
        """

        user = self.fetch_user_data(user_id)

        relations_to_check: list = []

        if user.friends_count < user.followers_count:

            following = self.fetch_following(user_id)

            relations_to_check.extend(following)
        else:

            followers = self.fetch_followers(user_id)

            relations_to_check.extend(followers)

        mutuals: list[int] = []

        for relation_to_check in relations_to_check:
            relationship = self.fetch_relationship(user_id, relation_to_check.id)
            if relationship[0].following and relationship[1].following:
                mutuals.append(relation_to_check.id)

        return mutuals

    def fetch_timeline(self, user_id: int, count=1000, **kwargs) -> list:
        """
        Fetch the timeline of a user.
    
        Args:
            self.apis (list[tweepy.api]): The list of self.apis to use.
            user_id (int): The user id to fetch the timeline of.
            count (int): The number of tweets to fetch.
    
        Returns:
            list[int]: The list of timeline of the user.
        """
        timeline: list = kwargs.get('timeline', [])
        cursor = tweepy.Cursor(self.apis[self.api_index].user_timeline, user_id=user_id, count=count,
                               cursor=kwargs.get('cursor', None))

        try:
            for tweet in cursor.items():
                timeline.append(tweet)
        except tweepy.errors.TooManyRequests:
            self.update_usable_api()
            return self.fetch_timeline(user_id, timeline=timeline, count=count, cursor=cursor.iterator.next_cursor)

        return timeline

    def fetch_favorites(self, user_id: int, count=1000, **kwargs) -> list:
        """
        Fetch the favorites of a user.
    
        Args:
            self.apis (list[tweepy.api]): The list of self.apis to use.
            user_id (int): The user id to fetch the favorites of.
            count (int): The number of favorites to fetch.
    
        Returns:
            list[int]: The list of favorites of the user.
        """
        favorites: list = kwargs.get('favorites', [])
        cursor = tweepy.Cursor(self.apis[self.api_index].get_favorites, user_id=user_id, count=count,
                               cursor=kwargs.get('cursor', None))

        try:
            for tweet in cursor.items():
                favorites.append(tweet)
        except tweepy.errors.TooManyRequests:
            self.update_usable_api()
            return self.fetch_favorites(user_id, favorites=favorites, count=count, cursor=cursor.iterator.next_cursor)

        return favorites

    @staticmethod
    def add_record(scores: dict[int, dict[str, int]], user_id: int, field: str) -> dict[int, dict[str, int]]:
        """
        Add a record to the scores.

        Args:
            scores (dict[str, dict[str, int]]): The scores to add the record to.
            user_id (int): The user id to add the record to.
            field ('retweets' | 'favorites' | 'replies'): The field to add the record to.

        Returns:
            dict[str, dict[str, int]]: The scores with the record added.
        """
        if user_id not in scores:
            scores[user_id] = {
                'retweets': 0,
                'favorites': 0,
                'replies': 0
            }

        scores[user_id][field] += 1

        return scores

    def get_scores(self, user_id: int) -> dict[int, dict[str, int]]:
        """
        Get the scores of a user.
    
        Args:
            self.apis (list[tweepy.api]): The list of self.apis to use.
            user_id (int): The user id to fetch the scores of.
    
        Returns:
            dict: The scores of the user.
        """
        scores: dict[int, dict[str, int]] = {}

        tweets = self.fetch_timeline(user_id, count=200)

        for tweet in tweets:
            if hasattr(tweet, 'retweeted_status') and tweet.retweeted_status.user.id != user_id:
                if tweet.retweeted_status.user.id is not None:
                    scores = self.add_record(scores, tweet.retweeted_status.user.id, 'retweets')
            if hasattr(tweet, 'in_reply_to_status_id') and tweet.in_reply_to_status_id != user_id:
                if tweet.in_reply_to_status_id is not None:
                    scores = self.add_record(scores, tweet.in_reply_to_status_id, 'replies')

        favorites = self.fetch_favorites(user_id, count=200)

        for tweet in favorites:
            if tweet.user.id != user_id:
                scores = self.add_record(scores, tweet.user.id, 'favorites')

        return scores

    def fetch_data(self, user_id: int, direction: str = 'from_user') -> dict[int, dict]:
        """
        Fetch the data of a user.
    
        Args:
            self.apis (list[tweepy.api]): The list of self.apis to use.
            user_id (int): The user id to fetch the data of.
            direction ('from_user' | 'from_mutual'): The direction to fetch the data from.
    
        Returns:
            dict: The data of the user.
        """

        mutuals = self.fetch_mutuals(user_id)

        if direction == 'from_user':

            scores = self.get_scores(user_id)

            filtered_scores = {k: v for k, v in scores.items() if k in mutuals}

            return filtered_scores
        elif direction == 'from_mutual':
            scores = {}

            for mutual in mutuals:
                mutual_scores = self.get_scores(mutual)

                filtered_mutual_scores = {k: v for k, v in mutual_scores.items() if k == user_id}
                scores[mutual.id] = filtered_mutual_scores

            return scores
        else:
            raise ValueError(f'Invalid direction: {direction}')
