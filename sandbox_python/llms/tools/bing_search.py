from os import getenv

from langchain_community.tools.bing_search import BingSearchResults
from langchain_community.utilities import BingSearchAPIWrapper


def get_bing_search_tool(k: int = 1):
    return BingSearchResults(
        api_wrapper=BingSearchAPIWrapper(
            bing_search_url=getenv("BING_SEARCH_URL"),
            bing_subscription_key=getenv("BING_SUBSCRIPTION_KEY"),
            k=k,
        ),
        num_results=k,
    )
