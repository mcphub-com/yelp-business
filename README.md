# yelp-business   

## Overview
The Yelp-Business MCP is designed to enhance interactions between businesses and customers through various communication tools. This platform includes five primary tools to facilitate business discovery, inquiries, and detailed information retrieval.

## Tools

### 1. **Yelp Chat**
   - **Description**: A conversational AI tool that handles business inquiries, supporting multi-turn dialogue and location awareness.
   - **Input Requirements**:
     - `query` (required): Natural language text for querying specific Yelp information (e.g., "Where is the nearest Thai restaurant?").
     - `chat_id` (optional): A unique identifier for the current session, can be omitted on the first request.
     - `latitude` (optional): User's latitude for more accurate results.
     - `longitude` (optional): User's longitude for more accurate results.

### 2. **Yelp Search**
- **Description**: The Yelp Search feature allows users to search for businesses using the Yelp Fusion API, returning up to 50 businesses based on various criteria. This feature provides a flexible way to find local services and establishments tailored to user preferences.

- **Input Requirements**:
  - `location` (required): The geographic area to search for businesses (e.g., "San Francisco"). This can be a city name, neighborhood, or specific address.
  - `latitude` (optional): Required if `location` is not provided. This specifies the latitude of the search area.
  - `longitude` (optional): Required if `location` is not provided. This specifies the longitude of the search area.
  - `term` (optional): Keywords to refine the search (e.g., "coffee", "pizza"). This can be a specific type of cuisine, service, or any relevant term.
  - `radius` (optional): The search radius in meters, with a maximum value of 40,000 meters (approximately 25 miles). This helps narrow down results to a specific distance from the specified location.
  - `categories` (optional): Categories to filter businesses (e.g., "restaurants", "bars"). This allows users to focus on specific types of establishments.
  - `locale` (optional): The locale for the results, which can help localize the search (e.g., "en_US" for English in the United States).
  - `price` (optional): Price levels to filter businesses, represented as a string (e.g., "1,2" for $ and $$).
  - `open_now` (optional): A boolean indicating whether to return only businesses that are currently open.
  - `open_at` (optional): A Unix timestamp indicating a specific time to check if businesses are open.
  - `attributes` (optional): Special attributes to filter businesses (e.g., "wifi", "outdoor_seating").
  - `sort_by` (optional): The sorting method for results, such as "best_match", "rating", or "distance". This determines how the results are ordered.
  - `device_platform` (optional): The platform of the device making the request (e.g., "web", "iOS", "Android").
  - `reservation_date` (optional): Date for making reservations at restaurants or similar establishments.
  - `reservation_time` (optional): Time for making reservations.
  - `reservation_covers` (optional): Number of people for the reservation.
  - `matches_party_size_param` (optional): A boolean indicating whether to filter results based on the party size parameter.
  - `limit` (optional): The number of results to return, with a default of 20. The maximum value is 50.
  - `offset` (optional): The number of results to skip before starting to collect the result set. This is useful for pagination.

### 3. **Yelp Phone Search**
   - **Description**: Searches for businesses based on phone number, returning matching results.
   - **Input Requirements**:
     - `phone` (required): Business phone number (including country code).
     - `locale` (optional): Locale code for regional results (e.g., "en_US").

### 4. **Yelp Business Match**
- **Description**: The Yelp Business Match feature allows users to match business data using precise information. This tool helps ensure that the business information provided matches existing Yelp entries accurately. It requires the `YELP_API_KEY` environment variable to be set with a Bearer token.

- **Input Requirements**:
  - `name` (required): Exact name of the business (max 64 characters). Allowed characters include letters, digits, spaces, and special characters such as `!#$%&+,./:?@'`.
  - `address1` (required): First line of the business address (max 64 characters). Allowed characters include letters, digits, spaces, and `/#&,.:`.
  - `city` (required): Name of the city where the business is located (1-64 characters). Allowed characters include letters, digits, spaces, and `'.()`.
  - `state` (required): ISO 3166-2 state code (1-3 characters).
  - `country` (required): ISO 3166-1 alpha-2 country code (2 characters).
  - `postal_code` (optional): Postal/ZIP code of the business (max 12 characters).
  - `phone` (optional): Business phone number (1-32 characters). Can be in local or international format.
  - `address2` (optional): Second line of the business address (max 64 characters). Can be null.
  - `address3` (optional): Third line of the business address (max 64 characters). Can be null.
  - `latitude` (optional): Latitude of the business location (-90 to 90). Required if no location is provided.
  - `longitude` (optional): Longitude of the business location (-180 to 180). Required if no location is provided.
  - `yelp_business_id` (optional): 22-character Yelp business ID. Can be null.
  - `limit` (optional): Limit on the number of results returned (1-10), with a default of 3.
  - `match_threshold` (optional): Match quality threshold, which can be set to either `'none'` or `'default'`. The default value is `'default'`.

### 5. **Yelp Business Details**
   - **Description**: Retrieves detailed information for a specific business using its Business ID or alias.
   - **Input Requirements**:
     - `business_id_or_alias` (required): Unique identifier or alias for the business.
     - `locale` (optional): Locale code for regional results (e.g., "en_US").
     - `device_platform` (optional): Device platform information (e.g., "web" or "mobile").
