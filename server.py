import requests, logging
from datetime import datetime
from typing import Union, Literal, List
from mcp.server import FastMCP
from pydantic import Field
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP, Context
import os
from dotenv import load_dotenv
load_dotenv()
yelp_api_key = os.getenv("YELP_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

__rapidapi_url__ = 'https://rapidapi.com/oneapiproject/api/yelp-business'

mcp = FastMCP('yelp-business')

@mcp.tool()
def yelp_chat( query: Annotated[str, Field(description="Natural language text for querying Yelp-specific information；Accepts any prompt related to Yelp businesses, such as “Can you find a Thai restaurant near me?”；This should be plain text (no special formatting needed).")],
               chat_id: Annotated[Union[str, None], Field(description="Uniquely identifies the current conversation (chat session)；For the first request, set this to null or omit it; the API will respond with a new chat_id；Use the returned chat_id on subsequent requests to continue the same conversation；If omitted on subsequent requests, a new conversation is started；If an invalid chat_id is provided, the request will fail.")] = None,
               latitude: Annotated[Union[float, None], Field(description="User’s approximate latitude；If provided, it helps return more location-specific results；Otherwise, the system may ask for location details if needed")] = None,
               longitude: Annotated[Union[float, None], Field(description="User’s approximate longitude；If provided, it helps return more location-specific results；Otherwise, the system may ask for location details if needed.")] = None) -> dict:
    """
    Conversational AI for Yelp business queries. Supports multi-turn conversations and location-aware responses.
    Requires YELP_API_KEY environment variable with Bearer token.
    """
    url = "https://api.yelp.com/ai/chat/v2"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {yelp_api_key}"
    }
    # Build the payload
    payload = {
        'query': query,
        'chat_id': chat_id
    }

    if latitude is not None and longitude is not None:
        payload['user_context'] = {'latitude': latitude, 'longitude': longitude}
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.post(url, headers=headers, json=payload)  # Changed params to json
    return response.json()

@mcp.tool()
def yelp_search(
    location: Annotated[Union[str, None], Field(description="Geographic area to search (e.g., 'New York City', '350 5th Ave, New York, NY'). "
        "Required if latitude/longitude not provided. Max 250 characters.")] = None,
    latitude: Annotated[Union[float, None], Field(description="Latitude for search (-90 to 90). Required if location not provided. "
        "Must be paired with longitude.")] = None,
    longitude: Annotated[Union[float, None], Field(description="Longitude for search (-180 to 180). Required if location not provided. "
        "Must be paired with latitude.")] = None,
    term: Annotated[Union[str, None], Field(description="Search term (e.g., 'food', 'restaurants', business names like 'Starbucks'). "
        "If omitted, searches popular categories.")] = None,
    radius: Annotated[Union[int, None], Field(description="Search radius in meters (0-40000, about 25 miles max). "
        "Actual radius may vary based on business density.")] = None,
    categories: Annotated[Union[str, None], Field(description="Comma-separated category aliases (e.g., 'bars,french'). "
        "See Yelp's supported categories list.")] = None,
    locale: Annotated[Union[str, None], Field(description="Locale in format '{language}_{country}' (e.g., 'en_US'). "
        "See Yelp's supported locales.")] = None,
    price: Annotated[Union[str, None], Field(description="Comma-separated price levels (1-4, e.g., '1,2' for $ or $$).")] = None,
    open_now: Annotated[Union[bool, None], Field(description="If true, returns only businesses currently open. "
        "Cannot be used with open_at.")] = None,
    open_at: Annotated[Union[int, None], Field(description="Unix timestamp for businesses open at that time. "
        "Cannot be used with open_now.")] = None,
    attributes: Annotated[Union[str, None], Field(description="Comma-separated special attributes (e.g., 'hot_and_new,outdoor_seating'). "
        "See full list in Yelp documentation.")] = None,
    sort_by: Annotated[Union[str, None], Field(description="Sort method: 'best_match', 'rating', 'review_count', or 'distance'. "
        "Default is 'best_match'.")] = None,
    device_platform: Annotated[Union[Literal['ios', 'android', 'mobile-generic'], None],Field(
        description="Platform for mobile links. Options: 'ios', 'android', or 'mobile-generic'.")]= None,
    reservation_date: Annotated[Union[str, None], Field(
        description="Reservation date in YYYY-MM-DD format.")] = None,
    reservation_time: Annotated[Union[str, None], Field(
        description="Reservation time in HH:MM format (24-hour).")] = None,
    reservation_covers: Annotated[Union[int, None], Field(
        description="Number of people for reservation (1-10).",
        ge=1, 
        le=10
    )] = None,
    matches_party_size_param: Annotated[Union[bool, None], Field(
        description="Filter businesses that can't accommodate the specified party size.")] = None,
    limit: Annotated[Union[int, None], Field(description="Number of results (0-50). Default is 20.")] = None,
    offset: Annotated[Union[int, None], Field(description="Result offset (0-1000) for pagination.")] = None) -> dict:
    """
    Search for businesses using Yelp Fusion API. Returns up to 50 businesses per request.
    Requires either location or latitude/longitude pair. 
    Requires YELP_API_KEY environment variable with Bearer token.
    """
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {yelp_api_key}"
    }
    
    # Validate location requirements
    if not location and (latitude is None or longitude is None):
        raise ValueError("Either location or both latitude/longitude must be provided")
    
    # Build query parameters
    params = {
        'location': location,
        'latitude': latitude,
        'longitude': longitude,
        'term': term,
        'radius': radius,
        'categories': categories,
        'locale': locale,
        'price': price,
        'open_now': open_now,
        'open_at': open_at,
        'attributes': attributes,
        'sort_by': sort_by,
        'device_platform': device_platform,
        'reservation_date': reservation_date,
        'reservation_time': reservation_time,
        'reservation_covers': reservation_covers,
        'matches_party_size_param': matches_party_size_param,
        'limit': limit,
        'offset': offset
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

@mcp.tool()
def yelp_phone_search(
    phone: Annotated[str, Field(
        description="Phone number of the business (with country code, e.g., +14159083801). Length 1-32.",
        min_length=1,
        max_length=32)],
    locale: Annotated[Union[str, None], Field(
        description="Locale code in {language}_{country} format (e.g., 'en_US').")] = None) -> dict:
    """
    Search businesses by phone number. Returns businesses matching the provided phone number.
    Requires YELP_API_KEY environment variable with Bearer token.
    """
    url = 'https://api.yelp.com/v3/businesses/search/phone'
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {yelp_api_key}"
    }
    params = {
        'phone': phone,
        'locale': locale
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

@mcp.tool()
def yelp_business_match(
    name: Annotated[str, Field(
        description="Exact business name (max 64 chars). Allowed chars: letters, digits, spaces and !#$%&+,./:?@'",
        max_length=64
    )],
    address1: Annotated[str, Field(
        description="First address line (max 64 chars). Allowed chars: letters, digits, spaces and '/#&,.:",
        max_length=64
    )],
    city: Annotated[str, Field(
        description="City name (1-64 chars). Allowed chars: letters, digits, spaces and '.()",
        min_length=1,
        max_length=64
    )],
    state: Annotated[str, Field(
        description="ISO 3166-2 state code (1-3 chars).",
        min_length=1,
        max_length=3
    )],
    country: Annotated[str, Field(
        description="ISO 3166-1 alpha-2 country code (2 chars).",
        min_length=2,
        max_length=2
    )],
    address2: Annotated[Union[str, None], Field(
        description="Second address line (max 64 chars).",
        max_length=64
    )] = None,
    address3: Annotated[Union[str, None], Field(
        description="Third address line (max 64 chars).",
        max_length=64
    )] = None,
    postal_code: Annotated[Union[str, None], Field(
        description="Postal/ZIP code (max 12 chars).",
        max_length=12
    )] = None,
    latitude: Annotated[Union[float, None], Field(
        description="Latitude (-90 to 90). Required if no location.",
        ge=-90,
        le=90
    )] = None,
    longitude: Annotated[Union[float, None], Field(
        description="Longitude (-180 to 180). Required if no location.",
        ge=-180,
        le=180
    )] = None,
    phone: Annotated[Union[str, None], Field(
        description="Phone number (1-32 chars). Can be local or international format.",
        min_length=1,
        max_length=32
    )] = None,
    yelp_business_id: Annotated[Union[str, None], Field(
        description="22-character Yelp business ID.",
        min_length=22,
        max_length=22
    )] = None,
    limit: Annotated[int, Field(
        description="Number of results (1-10). Default 3.",
        ge=1,
        le=10
    )] = 3,
    match_threshold: Annotated[Literal['none', 'default'], Field(
        description="Match quality threshold: 'none' or 'default'."
    )] = 'default'
) -> dict:
    """
    Match business data against Yelp listings using precise information.
    Requires YELP_API_KEY environment variable with Bearer token.
    """
    url = "https://api.yelp.com/v3/businesses/matches"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {yelp_api_key}"
    }
    params = {
        'name': name,
        'address1': address1,
        'address2': address2,
        'address3': address3,
        'city': city,
        'state': state,
        'country': country,
        'postal_code': postal_code,
        'latitude': latitude,
        'longitude': longitude,
        'phone': phone,
        'yelp_business_id': yelp_business_id,
        'limit': limit,
        'match_threshold': match_threshold
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

@mcp.tool()
def yelp_business_details(
    business_id_or_alias: Annotated[str, Field(description="22-character Yelp Business ID or Business Alias.")],
    locale: Annotated[Union[str, None], Field(description="Locale code in {language}_{country} format.")] = None,
    device_platform: Annotated[Union[Literal['ios', 'android', 'mobile-generic'], None], Field(description="Platform for mobile links: 'ios', 'android', or 'mobile-generic'.")] = None) -> dict:
    """
    Get detailed information about a specific Yelp business.
    Normally, you would get the Business ID from /v3/businesses/search, /v3/businesses/search/phone, /v3/transactions/{transaction_type}/search or /v3/autocomplete.
    To retrieve review excerpts for a business, please refer to our Reviews endpoint (/v3/businesses/{id}/reviews)
    """
    url = f"https://api.yelp.com/v3/businesses/{business_id_or_alias}"
    logging.info(url)
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {yelp_api_key}"
    }
    params = {
        'locale': locale,
        'device_platform': device_platform
    }
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(url, headers=headers, params=params)
    logging.info(response.json())
    
    return response.json()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9997
    mcp.run(transport="stdio")
