import datetime
import tweepy


def get_usable_api(apis: list[tweepy.api], api_exceptions: dict[int, datetime], api_index: int) -> int:
    """
    Get the usable api.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        api_exceptions (dict[int, datetime]): The list of api exceptions.
        api_index (int): The index of the api to use.

    Returns:
        int: The index of the usable api.
    """
    print(f'    INFO: The api {api_index} has been used up. Search to use another api...')
    if not (api_index in api_exceptions and
            api_exceptions[api_index] + datetime.timedelta(minutes=15) > datetime.datetime.now()):
        api_exceptions[api_index] = datetime.datetime.now()

    api_index = (api_index + 1) % len(apis)

    while api_index in api_exceptions and \
            api_exceptions[api_index] + datetime.timedelta(minutes=15) > datetime.datetime.now():
        api_index = (api_index + 1) % len(apis)

    print(f'    INFO: Using api {api_index}.')

    return api_index


def fetch_user_data(apis: list[tweepy.api], user_id: int, **kwargs):
    """
    Fetch the data of a user.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        user_id (int): The user id to fetch the data of.

    Returns:
        dict: The data of the user.
    """
    api_index = kwargs.get('api_index', 0)
    api_exceptions = kwargs.get('api_exceptions', {})

    try:
        user = apis[api_index].get_user(user_id=user_id)
    except tweepy.errors.TooManyRequests:
        api_index = get_usable_api(apis, api_exceptions, api_index)
        return fetch_user_data(apis, user_id, api_index=api_index, api_exceptions=api_exceptions)

    return user


def fetch_followers(apis: list[tweepy.api], user_id: int, **kwargs) -> list:
    """
    Fetch the followers of a user.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        user_id (int): The user id to fetch the followers of.

    Returns:
        list[int]: The list of followers of the user.
    """
    api_index = kwargs.get('api_index', 0)
    api_exceptions = kwargs.get('api_exceptions', {})
    followers: list = kwargs.get('followers', [])

    try:
        for user in tweepy.Cursor(apis[api_index].get_followers, user_id=user_id).items():
            followers.append(user)
    except tweepy.errors.TooManyRequests:
        api_index = get_usable_api(apis, api_exceptions, api_index)
        return fetch_followers(apis, user_id, api_index=api_index, followers=followers, api_exceptions=api_exceptions)

    return followers


def fetch_following(apis: list[tweepy.api], user_id: int, **kwargs) -> list:
    """
    Fetch the following of a user.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        user_id (int): The user id to fetch the following of.

    Returns:
        list[int]: The list of following of the user.
    """
    api_index = kwargs.get('api_index', 0)
    api_exceptions = kwargs.get('api_exceptions', {})
    following: list = kwargs.get('following', [])

    try:
        for user in tweepy.Cursor(apis[api_index].get_friends, user_id=user_id).items():
            following.append(user)
    except tweepy.errors.TooManyRequests:
        api_index = get_usable_api(apis, api_exceptions, api_index)
        return fetch_following(apis, user_id, api_index=api_index, following=following, api_exceptions=api_exceptions)

    return following


def fetch_relationship(apis: list[tweepy.api], source_user_id: int, target_user_id: int, **kwargs) -> dict:
    """
    Fetch the relationships of a list of users.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        source_user_id (int): The source user id to fetch the relationships of.
        target_user_id (int): The target user id to fetch the relationships of.

    Returns:
        dict: The relationships of the users.
    """
    api_index = kwargs.get('api_index', 0)
    api_exceptions = kwargs.get('api_exceptions', {})

    try:
        relationship = apis[api_index].get_friendship(source_id=source_user_id, target_id=target_user_id)
    except tweepy.errors.TooManyRequests:
        api_index = get_usable_api(apis, api_exceptions, api_index)
        return fetch_relationship(apis, source_user_id, target_user_id, api_index=api_index,
                                  api_exceptions=api_exceptions)

    return relationship


def fetch_mutuals(apis: list[tweepy.api], user_id: int) -> list:
    """
    Fetch the mutuals of a user.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        user_id (int): The user id to fetch the mutuals of.

    Returns:
        list[int]: The list of mutuals of the user.
    """
    print('    > Fetching user info...')
    user = fetch_user_data(apis, user_id)
    print('    > User info fetched!')

    relations_to_check: list = []

    if user.friends_count < user.followers_count:
        print('    > Fetching following...')
        following = fetch_following(apis, user_id)
        print('    > Following fetched!')
        relations_to_check.extend(following)
    else:
        print('    > Fetching followers...')
        followers = fetch_followers(apis, user_id)
        print('    > Followers fetched!')
        relations_to_check.extend(followers)

    mutuals: list[int] = []

    print('    > Fetching relationships...')
    for relation_to_check in relations_to_check:
        relationship = fetch_relationship(apis, user_id, relation_to_check.id)
        if relationship[0].following and relationship[1].following:
            mutuals.append(relation_to_check.id)
    print('    > Relationships fetched!')

    return mutuals


def fetch_timeline(apis: list[tweepy.api], user_id: int, **kwargs) -> list:
    """
    Fetch the timeline of a user.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        user_id (int): The user id to fetch the timeline of.

    Returns:
        list[int]: The list of timeline of the user.
    """
    api_index = kwargs.get('api_index', 0)
    api_exceptions = kwargs.get('api_exceptions', {})
    timeline: list = kwargs.get('timeline', [])

    try:
        for tweet in tweepy.Cursor(apis[api_index].user_timeline, user_id=user_id, count=1000).items():
            timeline.append(tweet)
    except tweepy.errors.TooManyRequests:
        api_index = get_usable_api(apis, api_exceptions, api_index)
        return fetch_timeline(apis, user_id, api_index=api_index, timeline=timeline, api_exceptions=api_exceptions)

    return timeline


def fetch_favorites(apis: list[tweepy.api], user_id: int, **kwargs) -> list:
    """
    Fetch the favorites of a user.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        user_id (int): The user id to fetch the favorites of.

    Returns:
        list[int]: The list of favorites of the user.
    """
    api_index = kwargs.get('api_index', 0)
    api_exceptions = kwargs.get('api_exceptions', {})
    favorites: list = kwargs.get('favorites', [])

    try:
        for tweet in tweepy.Cursor(apis[api_index].get_favorites, user_id=user_id, count=1000).items():
            favorites.append(tweet)
    except tweepy.errors.TooManyRequests:
        api_index = get_usable_api(apis, api_exceptions, api_index)
        return fetch_favorites(apis, user_id, api_index=api_index, favorites=favorites, api_exceptions=api_exceptions)

    return favorites


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


def get_scores(apis: list[tweepy.api], user_id: int) -> dict[int, dict[str, int]]:
    """
    Get the scores of a user.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        user_id (int): The user id to fetch the scores of.

    Returns:
        dict: The scores of the user.
    """
    scores: dict[int, dict[str, int]] = {}

    print('    > Fetching timeline...')
    tweets = fetch_timeline(apis, user_id)
    print('    > Timeline fetched!')

    for tweet in tweets:
        if hasattr(tweet, 'retweeted_status') and tweet.retweeted_status.user.id != user_id:
            scores = add_record(scores, tweet.retweeted_status.user.id, 'retweets')
        if hasattr(tweet, 'in_reply_to_status_id') and tweet.in_reply_to_status_id != user_id:
            scores = add_record(scores, tweet.in_reply_to_status_id, 'replies')

    print('    > Fetching favorites...')
    favorites = fetch_favorites(apis, user_id)
    print('    > Favorites fetched!')

    for tweet in favorites:
        if tweet.user.id != user_id:
            scores = add_record(scores, tweet.user.id, 'favorites')

    return scores


def fetch_data(apis: list[tweepy.api], user_id: int, direction: str = 'from_user') -> dict[int, int]:
    """
    Fetch the data of a user.

    Args:
        apis (list[tweepy.api]): The list of apis to use.
        user_id (int): The user id to fetch the data of.
        direction ('from_user' | 'from_mutual'): The direction to fetch the data from.

    Returns:
        dict: The data of the user.
    """
    print(f'Fetching data for user {user_id}...')

    print(f'Fetching mutuals...')
    mutuals = fetch_mutuals(apis, user_id)
    print(f'Mutuals fetched!')

    if direction == 'from_user':
        print(f'Fetching scores...')
        scores = get_scores(apis, user_id)
        print(f'Scores fetched!')

        filtered_scores = {k: v for k, v in scores.items() if k in mutuals}

        return filtered_scores
    elif direction == 'from_mutual':
        scores = {}

        for mutual in mutuals:
            print(f'Fetching scores...')
            mutual_scores = get_scores(apis, mutual)
            print(f'Scores fetched!')

            filtered_mutual_scores = {k: v for k, v in mutual_scores.items() if k == user_id}
            scores[mutual.id] = filtered_mutual_scores

        return scores
    else:
        raise ValueError(f'Invalid direction: {direction}')
