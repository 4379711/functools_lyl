# -*- coding: utf-8 -*-
import json

from requests import api as request_api
from ..config import *
from ..utils import remove_empty, MyTypeAssert, MixParams


class Client(MixParams):
    """
    Base advertising API .
    """
    VERSION = '/v2'

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
        assert self.region in MARKETPLACES.keys()
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
        print('got new token :')
        print(self._access_token)

    def _get_header(self, **params):
        # you can set headers in params.
        headers = {
            'Content-Type': 'application/json',
            'Amazon-Advertising-API-ClientId': self.client_id,
            'Authorization': 'Bearer {}'.format(self._access_token)
        }

        if self.profile_id:
            headers['Amazon-Advertising-API-Scope'] = self._profile_id

        # Some request needs special headers.
        other_header = params.pop('headers', {})
        headers.update(other_header)
        return headers

    def deal_params(self, interface, **params):
        extra_data = params.pop('payload', {})

        assert isinstance(extra_data, (dict, list))

        _data = remove_empty(extra_data)

        version = params.pop('version', self.VERSION)

        _url = 'https://{host}{version}/{interface}'.format(
            host=self._host,
            version=version,
            interface=interface
        )
        return _url, _data

    def _request(self, url, method, headers, data=None, params=None):
        resp = request_api.request(method=method, url=url, headers=headers, data=data, params=params)
        resp.data = data or params

        # try ... except block ,just for refreshing token .
        try:
            if 'UNAUTHORIZED' in resp.text:
                self.do_refresh_token()
                headers['Authorization'] = 'Bearer {}'.format(self.access_token)

                resp = request_api.request(method=method, url=url, headers=headers, data=data, params=params)
                resp.data = data
                return resp
        except (TypeError, AttributeError):
            pass
        return resp

    def make_request(self, interface=None, method='GET', url=None, **params):

        headers = self._get_header(**params)

        url_, extra_data = self.deal_params(interface, **params)
        _url = url if url else url_
        if method == 'GET':
            resp = self._request(method=method, url=_url, headers=headers, params=extra_data)
        else:
            # some params needs json type .
            extra_data = json.dumps(extra_data)
            resp = self._request(method=method, url=_url, headers=headers, data=extra_data)
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
        return self.make_request(interface)

    def list_profiles(self):
        """
        Retrieves one or more profiles associated with the authorization passed in the request header.
        :return:
        """
        interface = 'profiles'
        return self.make_request(interface)

    def update_profiles(self):
        """Updates one or more profiles."""
        interface = 'profiles'
        return self.make_request(interface, method='PUT')

    def register_profiles(self):
        """
        Registers a profile in the sandbox environment.
        If this call is made to a production endpoint an error is returned.
        """
        assert self.sandbox is True
        interface = 'profiles/register'
        data = {'countryCode': self.region}
        return self.make_request(interface, method='PUT', payload=data)

    def register_brand(self, brand):
        assert self.sandbox is True
        data = {'countryCode': self.region,
                'brand': brand
                }
        interface = 'profiles/registerBrand'
        return self.make_request(interface, method='PUT', payload=data)


class Portfolios(Client):
    __doc__ = """
            Portfolios consist of campaigns that are grouped together and linked to a distinct Advertiser Account.
            The term 'advertiser' refers to a brand, entity, account ID, or claim ID.
            An integrator can create multiple portfolios within an Advertiser Account.
            """

    def list_portfolios(self,
                        portfolio_id_filter=None,
                        portfolio_name_filter=None,
                        portfolio_state_filter=None):
        """
        Retrieve a list of up to 100 portfolios using the specified filters.

        """
        interface = 'portfolios'
        payload = {
            'portfolioIdFilter': portfolio_id_filter,
            'portfolioNameFilter': portfolio_name_filter,
            'portfolioStateFilter': portfolio_state_filter
        }
        return self.make_request(interface, payload=payload)

    def list_portfolios_ex(self,
                           portfolio_id_filter=None,
                           portfolio_name_filter=None,
                           portfolio_state_filter=None):
        """
        Retrieve a list of up to 100 portfolios with additional properties using the specified filters.
        """
        interface = 'portfolios/extended'
        payload = {
            'portfolioIdFilter': portfolio_id_filter,
            'portfolioNameFilter': portfolio_name_filter,
            'portfolioStateFilter': portfolio_state_filter
        }
        return self.make_request(interface, payload=payload)

    def get_portfolio(self, portfolio_id):
        interface = 'portfolios/{}'.format(portfolio_id)
        return self.make_request(interface)

    def get_portfolio_ex(self, portfolio_id):
        interface = 'portfolios/extended/{}'.format(portfolio_id)
        return self.make_request(interface)

    def create_portfolios(self, amount, policy, start_date=None, end_date=None,
                          name=None, state='enabled', all_data_list=None):

        interface = 'portfolios'
        if all_data_list is not None:
            return self.make_request(interface, method='PUT', payload=all_data_list)
        assert policy in ['dateRange', 'monthlyRecurring']
        if start_date:
            assert len(start_date) == 8

        # Inconsistent with the official documentation description .

        # if policy == 'monthlyRecurring' and start_date:
        #     raise ParameterError('monthlyRecurring', 'startDate')

        data = [{'name': name,
                 'budget': {'amount': amount,
                            'policy': policy,
                            'startDate': start_date,
                            'endDate': end_date
                            },
                 'state': state
                 }]
        return self.make_request(interface, method='POST', payload=data)

    def update_portfolios(self, portfolio_id: int, amount, policy, start_date=None,
                          end_date=None, state='enabled', name=None, all_data_list=None):
        interface = 'portfolios'
        if all_data_list is not None:
            return self.make_request(interface, method='PUT', payload=all_data_list)
        MyTypeAssert.number_assert(portfolio_id)
        assert policy in ['dateRange', 'monthlyRecurring']
        if start_date:
            assert len(start_date) == 8

        # Inconsistent with the official documentation description .

        # if policy == 'monthlyRecurring' and start_date:
        #     raise ParameterError('monthlyRecurring', 'startDate')

        data = [{
            'portfolioId': portfolio_id,
            'name': name,
            'budget': {'amount': amount,
                       'policy': policy,
                       'startDate': start_date,
                       'endDate': end_date
                       },
            'state': state
        }]
        return self.make_request(interface, method='PUT', payload=data)
