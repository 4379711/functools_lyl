# -*- coding: utf-8 -*-
import datetime
import json
from requests import api as request_api
from .ad_config import *


# docs :https://advertising.amazon.com/API/docs/en-us
class BaseMethods:

    @staticmethod
    def remove_empty(dict_):
        """
        Returns dict_ with all empty values removed.
        """
        return {k: v for k, v in dict_.items() if v}


class Client(BaseMethods):
    """
    Base advertising API .
    """

    def __init__(self, client_id, client_secret, access_token, refresh_token, region, profile_id=None, sandbox=True):
        """
        :param client_id: client id
        :param client_secret: client password
        :param access_token: token,it will be expired .(1 hour)
        :param refresh_token:use it to get a new token .
        :param region:region
        :param profile_id:profiled id ,must be None except <Profiles.list_profiles> .
        :param sandbox:start sandbox model .
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self._access_token = access_token
        self.refresh_token = refresh_token
        self._profile_id = profile_id
        self.sandbox = sandbox
        self.region = region.upper()
        self._host = ENDPOINTS[MARKETPLACES[self.region]] if not sandbox else ENDPOINTS['sandbox']

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def profile_id(self):
        return self._profile_id

    @profile_id.setter
    def profile_id(self, value):
        self._profile_id = value

    def do_refresh_token(self):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        resp = request_api.post(OAUTH_URL,
                                headers=headers,
                                data=json.dumps(data))
        self._access_token = dict(resp.json()).get('access_token')

    def _request(self, interface, method='GET', payload=None):
        headers = {
            'Content-Type': 'application/json',
            'Amazon-Advertising-API-ClientId': self.client_id,
            'Authorization': 'Bearer {}'.format(self._access_token)
        }

        url = 'https://{host}{version}/{interface}'.format(
            host=self._host,
            version=api_version,
            interface=interface
        )

        if self.profile_id:
            headers['Amazon-Advertising-API-Scope'] = self._profile_id

        extra_data = payload if payload else {}
        assert isinstance(extra_data, dict)

        extra_data = self.remove_empty(extra_data)

        # convert all Python date/time objects to isoformat
        for key, value in extra_data.items():
            if isinstance(value, (datetime.datetime, datetime.date)):
                extra_data[key] = value.isoformat()

        # some params needs json type .
        data = json.dumps(extra_data)
        resp = request_api.request(method=method, url=url, headers=headers, data=data)

        # try ... except block ,just for refreshing token .
        try:
            result = resp.json()
            if result.get('code') == 'UNAUTHORIZED':
                self.do_refresh_token()
                headers['Authorization'] = 'Bearer {}'.format(self.access_token)
                resp = request_api.request(method=method, url=url, headers=headers, data=data)
                return resp
        except (TypeError, AttributeError):
            pass
        return resp


class Profiles(Client):
    """
    Profiles are associated with a unique Profile identifier.
    A management scope is required in the header for all API calls.
    Use your Profile identifier as the value for the management scope
    (Amazon-Advertising-API-Scope) in the header.
    To retrieve your profile identifer,
    call the listProfiles operation including a valid authorization token in the header.
    """

    def get_profile(self, profile_id):
        """
        Retrieves a single profile specified by identifier.
        :param profile_id:The profile identifier.
        :return:
        """
        interface = 'profiles/{profile_id}'.format(
            profile_id=profile_id
        )
        return self._request(interface)

    def list_profiles(self):
        """
        Retrieves one or more profiles associated with the authorization passed in the request header.
        :return:
        """
        interface = 'profiles'
        return self._request(interface)

    def update_profiles(self):
        """Updates one or more profiles."""
        interface = 'profiles'
        return self._request(interface, method='PUT')

    def register_profiles(self):
        """
        Registers a profile in the sandbox environment.
        If this call is made to a production endpoint an error is returned.
        """
        interface = 'profiles/register'
        data = {'countryCode': self.region}
        assert self.sandbox is True
        return self._request(interface, method='PUT', payload=data)

    def register_brand(self):
        interface = 'profiles/registerBrand'
        assert self.sandbox is True
        return self._request(interface, method='PUT')


class Portfolios(Client):

    def list_portfolios(self, **params):
        """
        portfolioId	:Retrieve the portfolios with the specified IDs .
        """
        interface = 'portfolios'
        payload = {
            'portfolioIdFilter': params.get('portfolioIdFilter'),
            'portfolioNameFilter': params.get('portfolioNameFilter'),
            'portfolioStateFilter': params.get('portfolioStateFilter')
        }
        return self._request(interface, payload=payload)

    def list_portfolios_ex(self, **params):
        interface = 'portfolios/extended'
        payload = {
            'portfolioIdFilter': params.get('portfolioIdFilter'),
            'portfolioNameFilter': params.get('portfolioNameFilter'),
            'portfolioStateFilter': params.get('portfolioStateFilter')
        }
        return self._request(interface, payload=payload)

    def get_portfolio(self, portfolio_id):
        interface = 'portfolios/{}'.format(portfolio_id)
        return self._request(interface)

    def get_portfolio_ex(self, portfolio_id):
        interface = 'portfolios/extended/{}'.format(portfolio_id)
        return self._request(interface)

    def create_portfolios(self, **params):
        interface = 'portfolios'

        return self._request(interface, method='POST', payload=params)

    def update_portfolios(self, **params):
        interface = 'portfolios'

        return self._request(interface, method='PUT', payload=params)


class AdGroups(Client):

    def get_ad_group(self, ad_group_id):
        interface = 'sp/adGroups/{}'.format(ad_group_id)
        return self._request(interface)

    def get_ad_group_ex(self, ad_group_id):
        interface = 'sp/adGroups/extended/{}'.format(ad_group_id)
        return self._request(interface)

    def create_ad_groups(self, **params):
        interface = 'sp/adGroups'

        return self._request(interface, method='POST', payload=params)

    def update_ad_groups(self, **params):
        interface = 'sp/adGroups'

        return self._request(interface, method='PUT', payload=params)

    def delete_ad_group(self, ad_group_id):
        interface = 'sp/adGroups/{}'.format(ad_group_id)
        return self._request(interface, method='DELETE')

    def list_ad_groups(self, **params):
        interface = 'sp/adGroups'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'name': params.get('name'),
            'adGroupIdFilter': params.get('adGroupIdFilter'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self._request(interface, payload=payload)

    def list_ad_groups_ex(self, **params):
        interface = 'sp/adGroups/extended'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'name': params.get('name'),
            'adGroupIdFilter': params.get('adGroupIdFilter'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self._request(interface, payload=payload)


class Bid(Client):

    def get_bid_recommendations_for_ad_groups(self, ad_group_id):
        interface = 'adGroups/{}/bidRecommendations'.format(ad_group_id)
        return self._request(interface)

    def get_bid_recommendations_for_keywords(self, keyword_id):
        interface = 'keywords/{}/bidRecommendations'.format(keyword_id)
        return self._request(interface)

    def create_keywords_bid_recommendations(self, **params):
        interface = 'keywords/bidRecommendations'
        payload = {
            'adGroupId': params.get('adGroupId'),
            'keywords': params.get('keywords')
        }
        return self._request(interface, method='POST', payload=payload)

    def update_campaign_ad_group(self, **params):
        interface = 'hsa/campaigns'
        payload = {
            'startIndex': params.get('startIndex', 0),
            'count': params.get('count', 0),
            'bidMultiplier': params.get('bidMultiplier'),
            'placementGroupId': params.get('placementGroupId'),
            'primaryAdGroupId': params.get('primaryAdGroupId')
        }
        return self._request(interface, method='PUT', payload=payload)


class Campaigns(Client):

    def get_campaign(self, campaign_id, **params):
        interface = '{spon}/campaigns/{campaign_id}'.format(
            spon=params.get('spon'),
            campaign_id=campaign_id
        )
        return self._request(interface)

    def get_campaign_ex(self, campaign_id, **params):
        interface = '{spon}/campaigns/extended/{campaign_id}'.format(
            spon=params.get('spon'),
            campaign_id=campaign_id
        )
        return self._request(interface)

    def create_campaigns(self, **params):
        interface = 'sp/campaigns'

        return self._request(interface, method='POST', payload=params)

    def update_campaigns(self, **params):
        interface = '{}/campaigns'.format(params.get('spon'))

        return self._request(interface, method='PUT', payload=params)

    def delete_campaign(self, campaign_id, **params):
        interface = '{spon}/campaigns/{campaign_id}'.format(
            spon=params.get('spon'),
            campaign_id=campaign_id
        )
        return self._request(interface, method='DELETE')

    def list_campaigns(self, **params):
        interface = '{}/campaigns'.format(params.get('spon'))
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'name': params.get('name'),
            'portfolioIdFilter': params.get('portfolioIdFilter'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self._request(interface, payload=payload)

    def list_campaigns_ex(self, **params):
        interface = '{}/campaigns/extended'.format(params.get('spon'))
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'name': params.get('name'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self._request(interface, payload=payload)


class Keywords(Client):

    def get_biddable_keyword(self, keyword_id, **params):
        interface = '{spon}/keywords/{kid}'.format(
            spon=params.get('spon'),
            kid=keyword_id
        )
        return self._request(interface)

    def get_biddable_keyword_ex(self, keyword_id, **params):
        interface = '{spon}/keywords/extended/{kid}'.format(
            spon=params.get('spon'),
            kid=keyword_id
        )
        return self._request(interface)

    def create_biddable_keywords(self, **params):
        interface = '{}/keywords'.format(params.get('spon'))

        return self._request(interface, method='POST', payload=params)

    def update_biddable_keywords(self, **params):
        interface = '{}/keywords'.format(params.get('spon'))

        return self._request(interface, method='PUT', payload=params)

    def delete_biddable_keyword(self, keyword_id, **params):
        interface = '{spon}/keywords/{kid}'.format(
            spon=params.get('spon'),
            kid=keyword_id
        )
        return self._request(interface, method='DELETE')

    def list_biddable_keywords(self, **params):
        interface = 'sp/keywords'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'matchTypeFilter': params.get('matchTypeFilter'),
            'keywordText': params.get('keywordText'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter')
        }
        return self._request(interface, payload=payload)

    def list_biddable_keywords_ex(self, **params):
        interface = 'sp/keywords/extended'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'campaignType': params.get('campaignType'),
            'matchTypeFilter': params.get('matchTypeFilter'),
            'keywordText': params.get('keywordText'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter'),
            'keywordIdFilter': params.get('keywordIdFilter')
        }
        return self._request(interface, payload=payload)

    def get_negative_keyword(self, keyword_id):
        interface = 'sp/negativeKeywords/{}'.format(keyword_id)
        return self._request(interface)

    def get_negative_keyword_ex(self, keyword_id):
        interface = 'sp/negativeKeywords/extended/{}'.format(keyword_id)
        return self._request(interface)

    def create_negative_keywords(self, **params):
        interface = 'sp/negativeKeywords'

        return self._request(interface, method='POST', payload=params)

    def update_negative_keywords(self, **params):
        interface = 'sp/negativeKeywords'

        return self._request(interface, method='PUT', payload=params)

    def delete_negative_keyword(self, keyword_id):
        interface = 'sp/negativeKeywords/{}'.format(keyword_id)
        return self._request(interface, method='DELETE')

    def list_negative_keywords(self, **params):
        interface = 'sp/negativeKeywords'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'matchTypeFilter': params.get('matchTypeFilter'),
            'keywordText': params.get('keywordText'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter')
        }
        return self._request(interface, payload=payload)

    def list_negative_keywords_ex(self, **params):
        interface = 'sp/negativeKeywords/extended'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'matchTypeFilter': params.get('matchTypeFilter'),
            'keywordText': params.get('keywordText'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter')
        }
        return self._request(interface, payload=payload)

    def get_campaign_negative_keyword(self, keyword_id):
        interface = 'sp/campaignNegativeKeywords/{}'.format(keyword_id)
        return self._request(interface)

    def get_campaign_negative_keyword_ex(self, keyword_id):
        interface = 'sp/campaignNegativeKeywords/extended/{}'.format(keyword_id)
        return self._request(interface)

    def create_campaign_negative_keywords(self, **params):
        interface = 'sp/campaignNegativeKeywords'

        return self._request(interface, method='POST', payload=params)

    def update_campaign_negative_keywords(self, **params):
        interface = 'sp/campaignNegativeKeywords'

        return self._request(interface, method='PUT', payload=params)

    def delete_campaign_negative_keyword(self, keyword_id):
        interface = 'sp/campaignNegativeKeywords{}'.format(keyword_id)
        return self._request(interface, method='DELETE')

    def list_campaign_negative_keywords(self, **params):
        interface = 'sp/campaignNegativeKeywords/'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'matchTypeFilter': params.get('matchTypeFilter'),
            'keywordText': params.get('keywordText'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self._request(interface, payload=payload)

    def list_campaign_negative_keywords_ex(self, **params):
        interface = 'sp/campaignNegativeKeywords/extended'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'matchTypeFilter': params.get('matchTypeFilter'),
            'keywordText': params.get('keywordText'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self._request(interface, payload=payload)

    def get_ad_group_suggested_keywords(self, ad_group_id, **params):
        interface = 'adGroups/{}/suggested/keywords'.format(ad_group_id)
        payload = {
            'maxNumSuggestions': params.get('maxNumSuggestions'),
            'adStateFilter': params.get('adStateFilter')
        }
        return self._request(interface, payload=payload)

    def get_ad_group_suggested_keywords_ex(self, ad_group_id, **params):
        interface = 'adGroups/{}/suggested/keywords/extended'.format(ad_group_id)
        payload = {
            'maxNumSuggestions': params.get('maxNumSuggestions'),
            'adStateFilter': params.get('adStateFilter'),
            'suggestBids': params.get('suggestBids')
        }
        return self._request(interface, payload=payload)

    def get_asin_suggested_keywords(self, asin, **params):
        interface = 'asins/{}/suggested/keywords'.format(asin)
        payload = {
            'maxNumSuggestions': params.get('maxNumSuggestions')
        }
        return self._request(interface, payload=payload)

    def bulk_get_asin_suggested_keywords(self, **params):
        interface = 'asins/suggested/keywords'
        payload = {
            'maxNumSuggestions': params.get('maxNumSuggestions')
        }
        return self._request(interface, method='POST', payload=payload)


class ProductAds(Client):

    def get_productad(self, adid):
        interface = 'sp/productAds/{}'.format(adid)
        return self._request(interface)

    def get_productad_ex(self, adid):
        interface = 'sp/productAds/extended/{}'.format(adid)
        return self._request(interface)

    def create_productad(self, **params):
        interface = 'sp/productAds'

        return self._request(interface, method='POST', payload=params)

    def update_productad(self, **params):
        interface = 'sp/productAds'

        return self._request(interface, method='PUT', payload=params)

    def delete_productad(self, adid):
        interface = 'sp/productAds/{}'.format(adid)
        return self._request(interface, method='DELETE')

    def list_productads(self, **params):
        interface = 'sp/productAds'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'sku': params.get('sku'),
            'asin': params.get('asin'),
            'stateFilter': params.get('stateFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self._request(interface, payload=payload)

    def list_productads_ex(self, **params):
        interface = 'sp/productAds/extended'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'adGroupId': params.get('adGroupId'),
            'sku': params.get('sku'),
            'asin': params.get('asin'),
            'stateFilter': params.get('stateFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self._request(interface, payload=payload)


class Reports(Client):

    def create_report(self, **params):
        spon = params.get('spon')
        record_type = params.get('record_type')
        if spon == 'asin':
            interface = 'asins/report'
        else:
            interface = '{spon}/{record_type}/report'.format(
                spon=spon,
                record_type=record_type
            )

        rp_common = '{}_common'.format(spon)
        metrics_list = report_type.get(record_type) + report_type.get(rp_common)
        payload = {
            'reportDate': params.get('reportDate'),
            'metrics': ','.join(metrics_list)
        }
        if ('sp/keywords' or 'targets') in interface:
            payload['segment'] = 'query'
        if 'asins' in interface:
            payload['campaignType'] = 'sponsoredProducts'
        return self._request(interface, method='POST', payload=payload)

    def get_report(self, report_id):
        interface = 'reports/{}/download'.format(report_id)
        return self._request(interface)

    def create_snapshot(self, **params):
        interface = '{spon}/{record_type}/snapshot'.format(
            spon=params.get('spon'),
            record_type=params.get('record_type')
        )

        return self._request(interface, method='POST', payload=params)

    def get_snapshot(self, snapshot_id):
        interface = 'snapshots/{}/download'.format(snapshot_id)
        return self._request(interface)


class Stores(Client):

    def get_store(self, brand_entity_id):
        interface = 'stores/{brand_entity_id}'.format(
            brand_entity_id=brand_entity_id
        )
        return self._request(interface)

    def list_stores(self, **params):
        interface = 'stores'
        return self._request(interface)


class Targets(Client):

    def get_targeting_clause(self, target_id):
        interface = 'sp/targets/{}'.format(target_id)
        return self._request(interface)

    def get_targeting_clause_ex(self, target_id):
        interface = 'sp/targets/extended/{}'.format(target_id)
        return self._request(interface)

    def list_targeting_clause(self, **params):
        interface = 'sp/targets'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter')
        }
        return self._request(interface, payload=payload)

    def list_targeting_clause_ex(self, **params):
        interface = 'sp/targets/extended'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'campaignType': params.get('campaignType'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter')
        }
        return self._request(interface, payload=payload)

    def create_targeting_clause(self, **params):
        interface = 'sp/targets'

        return self._request(interface, method='POST', payload=params)

    def update_targeting_clause(self, **params):
        interface = 'sp/targets'

        return self._request(interface, method='PUT', payload=params)

    def delete_targeting_clause(self, target_id):
        interface = 'sp/targets/{}'.format(target_id)
        return self._request(interface, method='DELETE')

    def create_target_recommendations(self, **params):
        interface = 'sp/targets/productRecommendations'

        return self._request(interface, method='POST', payload=params)

    def get_targeting_categories(self, **params):
        interface = 'sp/targets/categories'
        payload = {
            'asins': params.get('asins')
        }
        return self._request(interface, payload=payload)

    def get_brand_recommendations(self, **params):
        interface = 'sp/targets/brands'
        payload = {
            'keyword': params.get('keyword'),
            'categoryId': params.get('categoryId')
        }
        return self._request(interface, payload=payload)

    def get_negative_targeting_clause(self, target_id):
        interface = 'sp/negativeTargets/{}'.format(target_id)
        return self._request(interface)

    def get_negative_targeting_clause_ex(self, target_id):
        interface = 'sp/negativeTargets/extended/{}'.format(target_id)
        return self._request(interface)

    def create_negative_targeting_clauses(self, **params):
        interface = 'sp/negativeTargets'

        return self._request(interface, method='POST', payload=params)

    def update_negative_targeting_clauses(self, **params):
        interface = 'sp/negativeTargets'

        return self._request(interface, method='PUT', payload=params)

    def list_negative_targeting_clauses(self, **params):
        interface = 'sp/negativeTargets'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter')
        }
        return self._request(interface, payload=payload)

    def list_negative_targeting_clauses_ex(self, **params):
        interface = 'sp/negativeTargets/extended'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'campaignType': params.get('campaignType'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter')
        }
        return self._request(interface, payload=payload)

    def delete_negative_targeting_clause(self, target_id):
        interface = 'sp/negativeTargets/{}'.format(target_id)
        return self._request(interface)
