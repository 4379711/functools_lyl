# -*- coding: utf-8 -*-
import gzip
import json

from ..Account import Client
from ..utils import MyTypeAssert


class Campaigns(Client):

    def get_campaign(self, campaign_id):
        interface = 'sp/campaigns/{}'.format(campaign_id)
        return self.make_request(interface)

    def get_campaign_ex(self, campaign_id):
        interface = 'sp/campaigns/extended/{campaign_id}'.format(campaign_id=campaign_id)
        return self.make_request(interface)

    def create_campaigns(self, name, targeting_type, state, daily_budget: (int, float),
                         start_date, campaign_type='sponsoredProducts',
                         all_data_list=None, **params):
        interface = 'sp/campaigns'
        if all_data_list is not None:
            return self.make_request(interface, method='POST', payload=all_data_list)
        MyTypeAssert.number_assert(daily_budget)
        assert len(start_date) == 8
        assert targeting_type in ["manual", "auto"]
        assert state in ["enabled", "paused", "archived"]

        data = [{
            'name': name,
            'targetingType': targeting_type,
            'state': state,
            'dailyBudget': daily_budget,
            'startDate': start_date,
            'campaignType': campaign_type

        }]
        data[0].update(params)

        return self.make_request(interface, method='POST', payload=data)

    def update_campaigns(self, campaign_id, all_data_list=None, **params):
        interface = 'sp/campaigns'
        if all_data_list is not None:
            return self.make_request(interface, method='PUT', payload=all_data_list)
        MyTypeAssert.number_assert(campaign_id)

        data = [{
            'campaignId': campaign_id
        }]
        data[0].update(params)

        return self.make_request(interface, method='PUT', payload=data)

    def archive_campaign(self, campaign_id):
        MyTypeAssert.number_assert(campaign_id)
        interface = 'sp/campaigns/{campaign_id}'.format(campaign_id=campaign_id)
        return self.make_request(interface, method='DELETE')

    def list_campaigns(self, **params):
        interface = 'sp/campaigns'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'name': params.get('name'),
            'portfolioIdFilter': params.get('portfolioIdFilter'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self.make_request(interface, payload=payload)

    def list_campaigns_ex(self, **params):
        interface = 'sp/campaigns/extended'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'name': params.get('name'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self.make_request(interface, payload=payload)


class AdGroups(Client):

    def get_ad_group(self, ad_group_id):
        MyTypeAssert.number_assert(ad_group_id)
        interface = 'sp/adGroups/{}'.format(ad_group_id)
        return self.make_request(interface)

    def get_ad_group_ex(self, ad_group_id):
        MyTypeAssert.number_assert(ad_group_id)
        interface = 'sp/adGroups/extended/{}'.format(ad_group_id)
        return self.make_request(interface)

    def create_ad_groups(self, campaign_id, name, state, default_bid, all_data_list=None, **params):
        interface = 'sp/adGroups'
        if all_data_list is not None:
            return self.make_request(interface, method='POST', payload=all_data_list)
        assert state in ["enabled", "paused", "archived"]
        MyTypeAssert.number_assert(campaign_id, default_bid)
        MyTypeAssert.str_assert(name, state)
        data = [{
            'campaignId': campaign_id,
            'name': name,
            'state': state,
            'defaultBid': default_bid
        }]
        data[0].update(params)

        return self.make_request(interface, method='POST', payload=data)

    def update_ad_groups(self, ad_group_id, state=None, all_data_list=None, **params):
        interface = 'sp/adGroups'
        if all_data_list is not None:
            return self.make_request(interface, method='PUT', payload=all_data_list)
        MyTypeAssert.number_assert(ad_group_id)
        if state is not None:
            assert state in ["enabled", "paused", "archived"]
        data = [{
            'adGroupId': ad_group_id,
            'state': state,
        }]
        data[0].update(params)
        return self.make_request(interface, method='PUT', payload=data)

    def archive_ad_group(self, ad_group_id):
        MyTypeAssert.number_assert(ad_group_id)
        interface = 'sp/adGroups/{}'.format(ad_group_id)
        return self.make_request(interface, method='DELETE')

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
        return self.make_request(interface, payload=payload)

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
        return self.make_request(interface, payload=payload)


class ProductAds(Client):
    """
    Used to create, read, update, or delete product ads for Sponsored Products.
    """

    def get_product_ad(self, ad_id):
        MyTypeAssert.number_assert(ad_id)
        interface = 'sp/productAds/{}'.format(ad_id)
        return self.make_request(interface)

    def get_product_ad_ex(self, ad_id):
        MyTypeAssert.str_assert(ad_id)
        interface = 'sp/productAds/extended/{}'.format(ad_id)
        return self.make_request(interface)

    def create_product_ad(self, campaign_id, ad_group_id, sku, state, all_data_list=None, **params):
        interface = 'sp/productAds'
        if all_data_list is not None:
            return self.make_request(interface, method='POST', payload=all_data_list)
        # Sellers use SKU, while vendors use ASIN.
        MyTypeAssert.number_assert(campaign_id, ad_group_id)
        MyTypeAssert.str_assert(sku)
        assert state in ["enabled", "paused", "archived"]

        data = [
            {'campaignId': campaign_id,
             'adGroupId': ad_group_id,
             'sku': sku,
             'state': state
             }
        ]
        data[0].update(params)
        return self.make_request(interface, method='POST', payload=data)

    def update_product_ad(self, ad_id, state, all_data_list=None):
        interface = 'sp/productAds'
        if all_data_list is not None:
            return self.make_request(interface, method='PUT', payload=all_data_list)
        MyTypeAssert.number_assert(ad_id)
        assert state in ["enabled", "paused", "archived"]
        data = [{
            'adId': ad_id,
            'state': state

        }]

        return self.make_request(interface, method='PUT', payload=data)

    def archive_product_ad(self, ad_id):
        MyTypeAssert.number_assert(ad_id)
        interface = 'sp/productAds/{}'.format(ad_id)
        return self.make_request(interface, method='DELETE')

    def list_product_ads(self, **params):
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
        return self.make_request(interface, payload=payload)

    def list_product_ads_ex(self, **params):
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
        return self.make_request(interface, payload=payload)


class Bid(Client):
    """
    Note: The workflow for auto-targeted campaigns is different from that of manually-targeted campaigns.
     Since auto-targeted campaigns do not have keywords, you must request bid recommendations at the ad group-level.
     The recommended workflow is as follows:

        Auto-targeted campaigns
            Create Campaign
            Create Ad Group
            Create Product Ad
            Call getAdGroupBidRecommendations
            Update Ad Group

        Manually-targeted campaigns
            Create Campaign
            Create Ad Group
            Create Product Ad
            Call getKeywordBidRecommendations
            Create Keywords
        Unsupported operations
            Manually-targeted campaigns:
                Cannot be made at the ad group-level if there are no product ads
            Auto-targeted Campaigns:
                Unsupported for auto-targeted campaigns if there are no product ads
            Negative match type and negative targets:
                Unsupported for bid recommendations
    """

    def __init__(self, *args, **kwargs):
        super(Bid, self).__init__(*args, **kwargs)
        self.sandbox_header = {'BIDDING_CONTROLS_ON': 'yes'} if self.sandbox else {}

    def get_bid_recommendations_for_ad_groups(self, ad_group_id):
        """
        Note:
            TargetingType  must set <auto>.
            How to create it ,see class <Campaigns> .
        """
        MyTypeAssert.number_assert(ad_group_id)
        interface = 'sp/adGroups/{}/bidRecommendations'.format(ad_group_id)
        return self.make_request(interface, headers=self.sandbox_header)

    def get_bid_recommendations_for_keywords(self, keyword_id):
        """
        Note:
           TargetingType  must set <manual>.
           How to create it ,see class <Campaigns> .
        """
        MyTypeAssert.number_assert(keyword_id)
        interface = 'keywords/{}/bidRecommendations'.format(keyword_id)
        return self.make_request(interface, headers=self.sandbox_header)

    def create_keywords_bid_recommendations(self, ad_group_id, match_type=None, keywords=None, all_keywords_list=None):
        interface = 'keywords/bidRecommendations'
        MyTypeAssert.number_assert(ad_group_id)
        if all_keywords_list is not None:
            keywords_list = all_keywords_list
        else:
            MyTypeAssert.str_assert(keywords)
            assert match_type in ['phrase', 'broad', 'exact']
            keywords_list = [{'keyword': keywords, 'matchType': match_type}]

        payload = {
            'adGroupId': ad_group_id,
            'keywords': keywords_list
        }

        return self.make_request(interface, method='POST', payload=payload)

    def get_bid_recommendations(self, ad_group, match_type, match_value):
        # This method requires the request to be of one targeting type
        # (expressions must be all keyword, product, or auto targets, and not a mix).
        interface = 'sp/targets/bidRecommendations'
        MyTypeAssert.number_assert(ad_group)
        assert match_type in ["queryBroadMatches", "queryPhraseMatches", "queryExactMatches"]
        payload = {
            'adGroupId': ad_group,
            'expressions': [[
                {
                    "type": match_type,
                    "value": match_value
                },
            ]
            ]

        }
        return self.make_request(interface, method='POST', payload=payload)


class Keywords(Client):
    """
    Ad group keyword limitations
        0.Keyword targeting and product targeting are mutually exclusive within an ad group.
          An ad group may include either keywords or product targets, but not both.

        1.If the ad group is associated with a campaign that has the targetingType field set to <auto>,
          it is not possible to create, read, update, or delete keywords.
          To use these operations, the associated campaign must have the targetingType field set to <manual>.

        2.The maximum number of keywords that can be associated with an ad group is 4000.
    """

    def get_biddable_keyword(self, keyword_id):
        MyTypeAssert.number_assert(keyword_id)
        interface = 'sp/keywords/{}'.format(keyword_id)

        return self.make_request(interface)

    def get_biddable_keyword_ex(self, keyword_id):
        MyTypeAssert.number_assert(keyword_id)
        interface = 'sp/keywords/extended/{}'.format(keyword_id)

        return self.make_request(interface)

    def create_biddable_keywords(self, ad_group_id, campaign_id,
                                 keyword_text, match_type,
                                 state, all_data_list=None,
                                 **params):
        interface = 'sp/keywords'

        if all_data_list is not None:
            return self.make_request(interface, method='POST', payload=all_data_list)
        MyTypeAssert.number_assert(ad_group_id, campaign_id)
        assert state in ["enabled", "paused", "archived"]
        assert match_type in ["exact", "phrase", "broad"]

        payload = [{
            'adGroupId': ad_group_id,
            'campaignId': campaign_id,
            'keywordText': keyword_text,
            'matchType': match_type,
            'state': state
        }]
        payload[0].update(params)
        return self.make_request(interface, method='POST', payload=payload)

    def update_biddable_keywords(self, keyword_id, all_data_list=None, **params):
        # While keywords are in a pending state
        # you can only update the bid amount, or archive them.
        # You cannot change the state from pending.

        interface = 'sp/keywords'
        if all_data_list is not None:
            return self.make_request(interface, method='PUT', payload=all_data_list)
        MyTypeAssert.number_assert(keyword_id)
        data = [{
            'keywordId': keyword_id
        }]
        data[0].update(params)

        return self.make_request(interface, method='PUT', payload=data)

    def archived_biddable_keyword(self, keyword_id):
        MyTypeAssert.number_assert(keyword_id)
        interface = 'sp/keywords/{}'.format(keyword_id)
        return self.make_request(interface, method='DELETE')

    def list_biddable_keywords(self, **params):
        # List keywords is not supported for SB.
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
        return self.make_request(interface, payload=payload)

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
        return self.make_request(interface, payload=payload)

    def get_negative_keyword(self, keyword_id):
        MyTypeAssert.number_assert(keyword_id)
        interface = 'sp/negativeKeywords/{}'.format(keyword_id)
        return self.make_request(interface)

    def get_negative_keyword_ex(self, keyword_id):
        MyTypeAssert.number_assert(keyword_id)
        interface = 'sp/negativeKeywords/extended/{}'.format(keyword_id)
        return self.make_request(interface)

    def create_negative_keywords(self, ad_group_id, campaign_id,
                                 keyword_text, match_type,
                                 state, all_data_list=None,
                                 **params):
        interface = 'sp/negativeKeywords'

        if all_data_list is not None:
            return self.make_request(interface, method='POST', payload=all_data_list)
        MyTypeAssert.number_assert(ad_group_id, campaign_id)

        assert state in ["enabled", "archived"]
        assert match_type in ["negativeExact", "negativePhrase"]

        payload = [{
            'adGroupId': ad_group_id,
            'campaignId': campaign_id,
            'keywordText': keyword_text,
            'matchType': match_type,
            'state': state
        }]
        payload[0].update(params)

        return self.make_request(interface, method='POST', payload=payload)

    def update_negative_keywords(self, keyword_id, all_data_list=None, **params):
        interface = 'sp/negativeKeywords'

        if all_data_list is not None:
            return self.make_request(interface, method='PUT', payload=all_data_list)
        MyTypeAssert.number_assert(keyword_id)
        data = [{'keywordId': keyword_id}]
        data[0].update(params)
        return self.make_request(interface, method='PUT', payload=data)

    def archive_negative_keyword(self, keyword_id):
        MyTypeAssert.number_assert(keyword_id)
        interface = 'sp/negativeKeywords/{}'.format(keyword_id)
        return self.make_request(interface, method='DELETE')

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
        return self.make_request(interface, payload=payload)

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
        return self.make_request(interface, payload=payload)

    # Used to create, read, update, or delete ad campaign-level negative keywords
    # for Sponsored Products. Negative keywords are not used with Sponsored Brands.
    def get_campaign_negative_keyword(self, keyword_id):
        MyTypeAssert.number_assert(keyword_id)
        interface = 'sp/campaignNegativeKeywords/{}'.format(keyword_id)
        return self.make_request(interface)

    def get_campaign_negative_keyword_ex(self, keyword_id):
        MyTypeAssert.number_assert(keyword_id)
        interface = 'sp/campaignNegativeKeywords/extended/{}'.format(keyword_id)
        return self.make_request(interface)

    def create_campaign_negative_keywords(self, campaign_id,
                                          keyword_text, match_type,
                                          state, all_data_list=None,
                                          **params):
        interface = 'sp/campaignNegativeKeywords'

        if all_data_list is not None:
            return self.make_request(interface, method='POST', payload=all_data_list)
        MyTypeAssert.number_assert(campaign_id)

        assert state in ["enabled", "deleted"]
        assert match_type in ["negativeExact", "negativePhrase"]

        payload = [{
            'campaignId': campaign_id,
            'keywordText': keyword_text,
            'matchType': match_type,
            'state': state
        }]
        payload[0].update(params)

        return self.make_request(interface, method='POST', payload=payload)

    def update_campaign_negative_keywords(self, keyword_id,
                                          state, all_data_list=None,
                                          ):
        interface = 'sp/campaignNegativeKeywords'

        if all_data_list is not None:
            return self.make_request(interface, method='PUT', payload=all_data_list)
        MyTypeAssert.number_assert(keyword_id)

        assert state in ["enabled", "deleted"]

        payload = [{
            'keywordId': keyword_id,
            'state': state
        }]

        return self.make_request(interface, method='PUT', payload=payload)

    def delete_campaign_negative_keyword(self, keyword_id):
        MyTypeAssert.number_assert(keyword_id)
        interface = 'sp/campaignNegativeKeywords{}'.format(keyword_id)
        return self.make_request(interface, method='DELETE')

    def list_campaign_negative_keywords(self, **params):
        interface = 'sp/campaignNegativeKeywords/'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'matchTypeFilter': params.get('matchTypeFilter'),
            'keywordText': params.get('keywordText'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self.make_request(interface, payload=payload)

    def list_campaign_negative_keywords_ex(self, **params):
        interface = 'sp/campaignNegativeKeywords/extended'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'matchTypeFilter': params.get('matchTypeFilter'),
            'keywordText': params.get('keywordText'),
            'campaignIdFilter': params.get('campaignIdFilter')
        }
        return self.make_request(interface, payload=payload)

    def get_ad_group_suggested_keywords(self, ad_group_id, **params):
        interface = 'adGroups/{}/suggested/keywords'.format(ad_group_id)
        payload = {
            'maxNumSuggestions': params.get('maxNumSuggestions'),
            'adStateFilter': params.get('adStateFilter')
        }
        return self.make_request(interface, payload=payload)

    def get_ad_group_suggested_keywords_ex(self, ad_group_id, **params):
        interface = 'adGroups/{}/suggested/keywords/extended'.format(ad_group_id)
        payload = {
            'maxNumSuggestions': params.get('maxNumSuggestions'),
            'adStateFilter': params.get('adStateFilter'),
            'suggestBids': params.get('suggestBids')
        }
        return self.make_request(interface, payload=payload)

    def get_asin_suggested_keywords(self, asin, **params):
        interface = 'asins/{}/suggested/keywords'.format(asin)
        MyTypeAssert.str_assert(asin)
        payload = {
            'maxNumSuggestions': params.get('maxNumSuggestions')
        }
        return self.make_request(interface, payload=payload)

    def bulk_get_asin_suggested_keywords(self, asin_list, **params):
        MyTypeAssert.other_assert(asin_list, types=list)
        interface = 'asins/suggested/keywords'
        payload = {
            'asins': asin_list,
            'maxNumSuggestions': params.get('maxNumSuggestions')
        }
        return self.make_request(interface, method='POST', payload=payload)


class Targets(Client):

    def get_targeting_clause(self, target_id):
        interface = 'sp/targets/{}'.format(target_id)
        return self.make_request(interface)

    def get_targeting_clause_ex(self, target_id):
        interface = 'sp/targets/extended/{}'.format(target_id)
        return self.make_request(interface)

    def list_targeting_clause(self, **params):
        interface = 'sp/targets'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter')
        }
        return self.make_request(interface, payload=payload)

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
        return self.make_request(interface, payload=payload)

    def create_targeting_clause(self, campaign_id, ad_group_id,
                                state, expression_type,
                                expression, all_data_list=None,
                                **params):
        interface = 'sp/targets'
        if all_data_list is not None:
            return self.make_request(interface, method='POST', payload=all_data_list)
        assert state in ["enabled", "paused", "archived"]
        assert expression_type in ["auto", "manual"]
        MyTypeAssert.other_assert(expression, types=list)
        data = [{
            'campaignId': campaign_id,
            'adGroupId': ad_group_id,
            'state': state,
            'expressionType': expression_type,
            'expression': expression,
        }]
        data[0].update(params)

        return self.make_request(interface, method='POST', payload=data)

    def update_targeting_clause(self, **params):
        interface = 'sp/targets'

        return self.make_request(interface, method='PUT', payload=params)

    def delete_targeting_clause(self, target_id):
        interface = 'sp/targets/{}'.format(target_id)
        return self.make_request(interface, method='DELETE')

    def create_target_recommendations(self, **params):
        interface = 'sp/targets/productRecommendations'

        return self.make_request(interface, method='POST', payload=params)

    def get_targeting_categories(self, **params):
        interface = 'sp/targets/categories'
        payload = {
            'asins': params.get('asins')
        }
        return self.make_request(interface, payload=payload)

    def get_brand_recommendations(self, **params):
        interface = 'sp/targets/brands'
        payload = {
            'keyword': params.get('keyword'),
            'categoryId': params.get('categoryId')
        }
        return self.make_request(interface, payload=payload)

    def get_negative_targeting_clause(self, target_id):
        interface = 'sp/negativeTargets/{}'.format(target_id)
        return self.make_request(interface)

    def get_negative_targeting_clause_ex(self, target_id):
        interface = 'sp/negativeTargets/extended/{}'.format(target_id)
        return self.make_request(interface)

    def create_negative_targeting_clauses(self, **params):
        interface = 'sp/negativeTargets'

        return self.make_request(interface, method='POST', payload=params)

    def update_negative_targeting_clauses(self, **params):
        interface = 'sp/negativeTargets'

        return self.make_request(interface, method='PUT', payload=params)

    def list_negative_targeting_clauses(self, **params):
        interface = 'sp/negativeTargets'
        payload = {
            'startIndex': params.get('startIndex'),
            'count': params.get('count'),
            'stateFilter': params.get('stateFilter'),
            'campaignIdFilter': params.get('campaignIdFilter'),
            'adGroupIdFilter': params.get('adGroupIdFilter')
        }
        return self.make_request(interface, payload=payload)

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
        return self.make_request(interface, payload=payload)

    def delete_negative_targeting_clause(self, target_id):
        interface = 'sp/negativeTargets/{}'.format(target_id)
        return self.make_request(interface)


class Reports(Client):

    def request_report(self, record_type, report_date, metrics_list, segment=None):
        assert record_type in ['campaigns', 'adGroups', 'keywords', 'productAds', 'targets']
        interface = 'sp/{}/report'.format(record_type)
        MyTypeAssert.other_assert(metrics_list, types=list)

        # report_date must format YYYYMMDD . and not older than 60 days .
        assert len(report_date) == 8
        payload = {
            'reportDate': report_date,
            'metrics': ','.join(metrics_list)
        }
        if segment:
            payload['segment'] = segment

        return self.make_request(interface, method='POST', payload=payload)

    def get_report(self, report_id):
        # The ReportResponse will contain a report status code.When the report has completed,
        # the location field will provide a redirect URL for the gzipped file containing the report.
        interface = 'reports/{}/download'.format(report_id)
        resp = self.make_request(interface)
        if resp.status_code == 200:
            json_file = gzip.decompress(resp.content)
            result = json.loads(json_file)
            return result
        return resp


class EntitySnapshots(Client):

    def request_snapshot(self, record_type, state_filter):
        assert record_type in ['campaigns', 'adGroups', 'keywords',
                               'negativeKeywords', 'campaignNegativeKeywords',
                               'productAds', 'targets', 'negativeTargets']
        assert state_filter in ['enabled', 'paused', 'archived']
        interface = 'sp/{}/snapshot'.format(record_type)
        data = {
            'stateFilter': state_filter
        }
        return self.make_request(interface, method='POST', payload=data)

    def get_snapshot_by_id(self, snapshot_id):
        interface = 'sp/snapshots/{}'.format(snapshot_id)
        return self.make_request(interface)

    def download_snapshot_file(self, url):
        return self.make_request(url=url)
