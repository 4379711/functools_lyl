# -*- coding: utf-8 -*-

MARKETPLACES = {'US': 'NA',
                'CA': 'NA',

                'JP': 'FE',
                'AU': 'FE',

                'UK': 'EU',
                'FR': 'EU',
                'IT': 'EU',
                'ES': 'EU',
                'DE': 'EU',
                'AE': 'EU',
                }

OAUTH_URL_ENDPOINTS = {
    'NA': 'https://api.amazon.com/auth/o2/token',
    'EU': 'https://api.amazon.co.uk/auth/o2/token',
    'FE': 'https://api.amazon.co.jp/auth/o2/token'
}

ENDPOINTS = {
    'sandbox': 'advertising-api-test.amazon.com',
    'NA': 'advertising-api.amazon.com',
    'EU': 'advertising-api-eu.amazon.com',
    'FE': 'advertising-api-fe.amazon.com'
}

