"""
Provides linkedin api-related code
"""

import datetime
import json
import logging
import random
from time import sleep
import demoji
import slack
from linkedin_slack_bot.client import Client

logger = logging.getLogger(__name__)


def default_evade():
#     """
#     A catch-all method to try and evade suspension from Linkedin.
#     Currenly, just delays the request by a random (bounded) time
#     """
    sleep(random.randint(2, 5))
    # sleep(30)

class API_Linkedin(object):
    """
    Class for accessing the LinkedIn API.

    :param username: Username of LinkedIn account.
    :type username: str
    :param password: Password of LinkedIn account.
    :type password: str
    """

    _MAX_POST_COUNT = 100  # max seems to be 100 posts per page
    _MAX_UPDATE_COUNT = 100  # max seems to be 100
    _MAX_SEARCH_COUNT = 49  # max seems to be 49, and min seems to be 2
    _MAX_REPEATED_REQUESTS = (
        200  # VERY conservative max requests count to avoid rate-limit
    )

    def __init__(
        self,
        username,
        password,
        *,
        authenticate=True,
        refresh_cookies=False,
        debug=False,
        proxies={},
        cookies=None,
        cookies_dir=None,
    ):
        """Constructor method"""
        self.client = Client(
            refresh_cookies=refresh_cookies,
            debug=debug,
            proxies=proxies,
            cookies_dir=cookies_dir,
        )
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self.logger = logger

        if authenticate:
            if cookies:
                # If the cookies are expired, the API won't work anymore since
                # `username` and `password` are not used at all in this case.
                self.client._set_session_cookies(cookies)
            else:
                self.client.authenticate(username, password)

    def _fetch(self, uri, evade=default_evade, base_request=False, **kwargs):
        """GET request to Linkedin API"""
        evade()

        url = f"{self.client.API_BASE_URL if not base_request else self.client.LINKEDIN_BASE_URL}{uri}"
        return self.client.session.get(url, **kwargs)

    def _post(self, uri, evade=default_evade, base_request=False, **kwargs):
        """POST request to Linkedin API"""
        evade()

        url = f"{self.client.API_BASE_URL if not base_request else self.client.LINKEDIN_BASE_URL}{uri}"
        return self.client.session.post(url, **kwargs)


    def get_conversations(self , start , count):
        """Fetch list of conversations the user is in.

        :return: List of conversations
        :rtype: list
        """
        params = {
            "keyVersion": "LEGACY_INBOX",
            "start": start,
            "count": count
        }

        res = self._fetch(f"/messaging/conversations", params=params)
        
        return res.json()
    
    def get_conversation(self, conversation_urn_id):
        """Fetch data about a given conversation.

        :param conversation_urn_id: LinkedIn URN ID for a conversation
        :type conversation_urn_id: str

        :return: Conversation data
        :rtype: dict
        """
        res = self._fetch(f"/messaging/conversations/{conversation_urn_id}/events")

        return res.json()

