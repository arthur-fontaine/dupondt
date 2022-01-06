import tweepy


def get_tw_api_instance(consumer_key: str, consumer_secret: str,
                        access_token: str, access_token_secret: str) -> tweepy.API:
    """
    Get an API instance.

    Args:
        consumer_key (str): The consumer key.
        consumer_secret (str): The consumer secret.
        access_token (str): The access token.
        access_token_secret (str): The access token secret.

    Returns:
        tweepy.API: The API instance.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)
