#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Removes the entire sitelink campaign extension setting.

Removes both the sitelink campaign extension setting itself and its associated
sitelink extension feed items. This requires two steps, since removing the
campaign extension setting doesn't automatically remove its extension feed
items.

To make this example work with other types of extensions, replace
ExtensionType.SITELINK with the extension type you wish to remove.
"""


import argparse
import sys

from google.api_core import protobuf_helpers

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from google.ads.google_ads.util import ResourceName


def main(client, customer_id, campaign_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_id: the campaign ID.
    """
    # Initialize an array of MutateOperations
    mutate_operations = []
    sitelink_campaign_extension_setting_mutate_operation = _create_sitelink_campaign_extension_setting_mutate_operation(
        client, customer_id, campaign_id
    )
    mutate_operations.append(sitelink_campaign_extension_setting_mutate_operation)

    ga_service = client.get_service("GoogleAdsService", version="v6")
    extension_feed_item_resource_names = _get_all_sitelink_extension_feed_items(
        client, ga_service, customer_id, campaign_id
    )
    extension_feed_item_mutate_operations = _create_extension_feed_item_mutate_operations(
        client, extension_feed_item_resource_names
    )
    mutate_operations.extend(extension_feed_item_mutate_operations)

    try:
        # Issue a mutate request to remove the campaign extension setting and
        # its extension feed items.
        response = ga_service.mutate(customer_id, mutate_operations)
        mutate_operation_responses = response.mutate_operation_responses
        print(
            "Removed a campaign extension setting with resource name "
            f'"{mutate_operation_responses[0].campaign_extension_setting_result.resource_name}".'
        )
        # Iterate through the remainder of the mutate operation responses,
        # which are the extension feed item removal responses
        for mutate_operation_response in mutate_operation_responses[1:]:
            print(
                "Removed an extension feed item with resource name "
                f'"{mutate_operation_response.extension_feed_item_result.resource_name}".'
            )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)


def _create_sitelink_campaign_extension_setting_mutate_operation(
    client, customer_id, campaign_id
):
    """Creates a MutateOperation for the sitelink campaign extension setting
    that will be removed.

    Args:
        client: an initialized GoogleAdsClient instance
        customer_id: the client customer ID.
        campaign_id: the campaign ID.

    Returns:
        The created MutateOperation for the sitelink campaign extension
            setting.
    """
    extension_type_enum = client.get_type("ExtensionTypeEnum", version="v6")
    composite_id = ResourceName.format_composite(
        campaign_id,
        extension_type_enum.ExtensionType.Name(
            extension_type_enum.ExtensionType.SITELINK
        ),
    )
    # Construct the campaign extension setting resource name, in format:
    # customers/{customer_id}/campaignExtensionSettings/{campaign_id}~{extension_type}
    resource_name = client.get_service(
        "CampaignExtensionSettingService", version="v6"
    ).campaign_extension_setting_path(customer_id, composite_id)

    # Create a MutateOperation for the campaign extension setting.
    mutate_operation = client.get_type("MutateOperation", version="v6")
    mutate_operation.campaign_extension_setting_operation.remove = resource_name
    return mutate_operation


def _get_all_sitelink_extension_feed_items(
    client, ga_service, customer_id, campaign_id
):
    """Gets all sitelink extension feed items associated to the specified
    campaign extension setting.

    Args:
        client: an initialized GoogleAdsClient instance.
        ga_service: the Google Ads API service client.
        customer_id: the client customer ID.
        campaign_id: the ID of the campaign to get the sitelink extension feed
            items from.

    Returns:
        An array of str resource names of extension feed items.
    """
    campaign_resource_name = client.get_service(
        "CampaignService", version="v6"
    ).campaign_path(customer_id, campaign_id)
    extension_type_enum = client.get_type("ExtensionTypeEnum", version="v6")
    extension_type_name = extension_type_enum.ExtensionType.Name(
        extension_type_enum.ExtensionType.SITELINK
    )

    # Construct the query.
    query = f"""
        SELECT
          campaign_extension_setting.campaign,
          campaign_extension_setting.extension_type,
          campaign_extension_setting.extension_feed_items
        FROM campaign_extension_setting
        WHERE campaign_extension_setting.campaign = '{campaign_resource_name}'
        AND campaign_extension_setting.extension_type =
          '{extension_type_name}'"""

    # Issue a search request using streaming.
    response = ga_service.search_stream(customer_id, query=query)
    extension_feed_item_resource_names = []
    # Iterate through each row and append the extension feed item resource
    # names to the return array.
    for batch in response:
        for row in batch.results:
            extension_feed_item_resource_names.extend(
                row.campaign_extension_setting.extension_feed_items
            )

    if len(extension_feed_item_resource_names) == 0:
        print(
            "The specified campaign does not contain a sitelink campaign "
            "extension setting."
        )
        sys.exit(1)

    return extension_feed_item_resource_names


def _create_extension_feed_item_mutate_operations(
    client, extension_feed_item_resource_names
):
    """Creates MutateOperations for the sitelink extension feed items that will
    be removed.

    Args:
        client: an initialized GoogleAdsClient instance.
        extension_feed_item_resource_names: the extension feed item resource
            names.

    Returns:
        An array of MutateOperations for the extension feed items.
    """
    mutate_operations = []
    # Create a MutateOperation for each extension feed item to remove.
    for resource_name in extension_feed_item_resource_names:
        mutate_operation = client.get_type("MutateOperation", version="v6")
        mutate_operation.extension_feed_item_operation.remove = resource_name
        mutate_operations.append(mutate_operation)

    return mutate_operations


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description="Removes the entire sitelink campaign extension setting."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID",
    )
    parser.add_argument(
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        help="The campaign ID",
    )
    args = parser.parse_args()

    main(
        google_ads_client, args.customer_id, args.campaign_id
    )