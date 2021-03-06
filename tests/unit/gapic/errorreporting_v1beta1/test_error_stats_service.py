# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.errorreporting_v1beta1.services.error_stats_service import (
    ErrorStatsServiceAsyncClient,
)
from google.cloud.errorreporting_v1beta1.services.error_stats_service import (
    ErrorStatsServiceClient,
)
from google.cloud.errorreporting_v1beta1.services.error_stats_service import pagers
from google.cloud.errorreporting_v1beta1.services.error_stats_service import transports
from google.cloud.errorreporting_v1beta1.types import common
from google.cloud.errorreporting_v1beta1.types import error_stats_service
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert ErrorStatsServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        ErrorStatsServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ErrorStatsServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        ErrorStatsServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ErrorStatsServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        ErrorStatsServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


@pytest.mark.parametrize(
    "client_class", [ErrorStatsServiceClient, ErrorStatsServiceAsyncClient]
)
def test_error_stats_service_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == "clouderrorreporting.googleapis.com:443"


def test_error_stats_service_client_get_transport_class():
    transport = ErrorStatsServiceClient.get_transport_class()
    assert transport == transports.ErrorStatsServiceGrpcTransport

    transport = ErrorStatsServiceClient.get_transport_class("grpc")
    assert transport == transports.ErrorStatsServiceGrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ErrorStatsServiceClient, transports.ErrorStatsServiceGrpcTransport, "grpc"),
        (
            ErrorStatsServiceAsyncClient,
            transports.ErrorStatsServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    ErrorStatsServiceClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ErrorStatsServiceClient),
)
@mock.patch.object(
    ErrorStatsServiceAsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(ErrorStatsServiceAsyncClient),
)
def test_error_stats_service_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(ErrorStatsServiceClient, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(ErrorStatsServiceClient, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=client_cert_source_callback,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=True,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_MTLS_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "auto"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.mtls.has_default_client_cert_source",
                return_value=False,
            ):
                patched.return_value = None
                client = client_class()
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                    client_cert_source=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ErrorStatsServiceClient, transports.ErrorStatsServiceGrpcTransport, "grpc"),
        (
            ErrorStatsServiceAsyncClient,
            transports.ErrorStatsServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_error_stats_service_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (ErrorStatsServiceClient, transports.ErrorStatsServiceGrpcTransport, "grpc"),
        (
            ErrorStatsServiceAsyncClient,
            transports.ErrorStatsServiceGrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_error_stats_service_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_error_stats_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.errorreporting_v1beta1.services.error_stats_service.transports.ErrorStatsServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = ErrorStatsServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_group_stats(
    transport: str = "grpc", request_type=error_stats_service.ListGroupStatsRequest
):
    client = ErrorStatsServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_group_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = error_stats_service.ListGroupStatsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_group_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == error_stats_service.ListGroupStatsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGroupStatsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_group_stats_from_dict():
    test_list_group_stats(request_type=dict)


@pytest.mark.asyncio
async def test_list_group_stats_async(transport: str = "grpc_asyncio"):
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = error_stats_service.ListGroupStatsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_group_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            error_stats_service.ListGroupStatsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_group_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListGroupStatsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_group_stats_field_headers():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = error_stats_service.ListGroupStatsRequest()
    request.project_name = "project_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_group_stats), "__call__"
    ) as call:
        call.return_value = error_stats_service.ListGroupStatsResponse()

        client.list_group_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project_name=project_name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_list_group_stats_field_headers_async():
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = error_stats_service.ListGroupStatsRequest()
    request.project_name = "project_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_group_stats), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            error_stats_service.ListGroupStatsResponse()
        )

        await client.list_group_stats(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project_name=project_name/value",) in kw[
        "metadata"
    ]


def test_list_group_stats_flattened():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_group_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = error_stats_service.ListGroupStatsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_group_stats(
            project_name="project_name_value",
            time_range=error_stats_service.QueryTimeRange(
                period=error_stats_service.QueryTimeRange.Period.PERIOD_1_HOUR
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_name == "project_name_value"

        assert args[0].time_range == error_stats_service.QueryTimeRange(
            period=error_stats_service.QueryTimeRange.Period.PERIOD_1_HOUR
        )


def test_list_group_stats_flattened_error():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_group_stats(
            error_stats_service.ListGroupStatsRequest(),
            project_name="project_name_value",
            time_range=error_stats_service.QueryTimeRange(
                period=error_stats_service.QueryTimeRange.Period.PERIOD_1_HOUR
            ),
        )


@pytest.mark.asyncio
async def test_list_group_stats_flattened_async():
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_group_stats), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = error_stats_service.ListGroupStatsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            error_stats_service.ListGroupStatsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_group_stats(
            project_name="project_name_value",
            time_range=error_stats_service.QueryTimeRange(
                period=error_stats_service.QueryTimeRange.Period.PERIOD_1_HOUR
            ),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_name == "project_name_value"

        assert args[0].time_range == error_stats_service.QueryTimeRange(
            period=error_stats_service.QueryTimeRange.Period.PERIOD_1_HOUR
        )


@pytest.mark.asyncio
async def test_list_group_stats_flattened_error_async():
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_group_stats(
            error_stats_service.ListGroupStatsRequest(),
            project_name="project_name_value",
            time_range=error_stats_service.QueryTimeRange(
                period=error_stats_service.QueryTimeRange.Period.PERIOD_1_HOUR
            ),
        )


def test_list_group_stats_pager():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_group_stats), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                ],
                next_page_token="abc",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[], next_page_token="def",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[error_stats_service.ErrorGroupStats(),],
                next_page_token="ghi",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project_name", ""),)),
        )
        pager = client.list_group_stats(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, error_stats_service.ErrorGroupStats) for i in results)


def test_list_group_stats_pages():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.list_group_stats), "__call__"
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                ],
                next_page_token="abc",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[], next_page_token="def",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[error_stats_service.ErrorGroupStats(),],
                next_page_token="ghi",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_group_stats(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_group_stats_async_pager():
    client = ErrorStatsServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_group_stats),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                ],
                next_page_token="abc",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[], next_page_token="def",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[error_stats_service.ErrorGroupStats(),],
                next_page_token="ghi",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_group_stats(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(
            isinstance(i, error_stats_service.ErrorGroupStats) for i in responses
        )


@pytest.mark.asyncio
async def test_list_group_stats_async_pages():
    client = ErrorStatsServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_group_stats),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                ],
                next_page_token="abc",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[], next_page_token="def",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[error_stats_service.ErrorGroupStats(),],
                next_page_token="ghi",
            ),
            error_stats_service.ListGroupStatsResponse(
                error_group_stats=[
                    error_stats_service.ErrorGroupStats(),
                    error_stats_service.ErrorGroupStats(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_group_stats(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_list_events(
    transport: str = "grpc", request_type=error_stats_service.ListEventsRequest
):
    client = ErrorStatsServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_events), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = error_stats_service.ListEventsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == error_stats_service.ListEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEventsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_events_from_dict():
    test_list_events(request_type=dict)


@pytest.mark.asyncio
async def test_list_events_async(transport: str = "grpc_asyncio"):
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = error_stats_service.ListEventsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            error_stats_service.ListEventsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEventsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_events_field_headers():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = error_stats_service.ListEventsRequest()
    request.project_name = "project_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_events), "__call__") as call:
        call.return_value = error_stats_service.ListEventsResponse()

        client.list_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project_name=project_name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_list_events_field_headers_async():
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = error_stats_service.ListEventsRequest()
    request.project_name = "project_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_events), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            error_stats_service.ListEventsResponse()
        )

        await client.list_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project_name=project_name/value",) in kw[
        "metadata"
    ]


def test_list_events_flattened():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_events), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = error_stats_service.ListEventsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_events(
            project_name="project_name_value", group_id="group_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_name == "project_name_value"

        assert args[0].group_id == "group_id_value"


def test_list_events_flattened_error():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_events(
            error_stats_service.ListEventsRequest(),
            project_name="project_name_value",
            group_id="group_id_value",
        )


@pytest.mark.asyncio
async def test_list_events_flattened_async():
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = error_stats_service.ListEventsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            error_stats_service.ListEventsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_events(
            project_name="project_name_value", group_id="group_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_name == "project_name_value"

        assert args[0].group_id == "group_id_value"


@pytest.mark.asyncio
async def test_list_events_flattened_error_async():
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_events(
            error_stats_service.ListEventsRequest(),
            project_name="project_name_value",
            group_id="group_id_value",
        )


def test_list_events_pager():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_events), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            error_stats_service.ListEventsResponse(
                error_events=[
                    common.ErrorEvent(),
                    common.ErrorEvent(),
                    common.ErrorEvent(),
                ],
                next_page_token="abc",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[], next_page_token="def",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[common.ErrorEvent(),], next_page_token="ghi",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[common.ErrorEvent(), common.ErrorEvent(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("project_name", ""),)),
        )
        pager = client.list_events(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, common.ErrorEvent) for i in results)


def test_list_events_pages():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_events), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            error_stats_service.ListEventsResponse(
                error_events=[
                    common.ErrorEvent(),
                    common.ErrorEvent(),
                    common.ErrorEvent(),
                ],
                next_page_token="abc",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[], next_page_token="def",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[common.ErrorEvent(),], next_page_token="ghi",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[common.ErrorEvent(), common.ErrorEvent(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_events(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_events_async_pager():
    client = ErrorStatsServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            error_stats_service.ListEventsResponse(
                error_events=[
                    common.ErrorEvent(),
                    common.ErrorEvent(),
                    common.ErrorEvent(),
                ],
                next_page_token="abc",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[], next_page_token="def",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[common.ErrorEvent(),], next_page_token="ghi",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[common.ErrorEvent(), common.ErrorEvent(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_events(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, common.ErrorEvent) for i in responses)


@pytest.mark.asyncio
async def test_list_events_async_pages():
    client = ErrorStatsServiceAsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.list_events),
        "__call__",
        new_callable=mock.AsyncMock,
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            error_stats_service.ListEventsResponse(
                error_events=[
                    common.ErrorEvent(),
                    common.ErrorEvent(),
                    common.ErrorEvent(),
                ],
                next_page_token="abc",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[], next_page_token="def",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[common.ErrorEvent(),], next_page_token="ghi",
            ),
            error_stats_service.ListEventsResponse(
                error_events=[common.ErrorEvent(), common.ErrorEvent(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_events(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_delete_events(
    transport: str = "grpc", request_type=error_stats_service.DeleteEventsRequest
):
    client = ErrorStatsServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_events), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = error_stats_service.DeleteEventsResponse()

        response = client.delete_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == error_stats_service.DeleteEventsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, error_stats_service.DeleteEventsResponse)


def test_delete_events_from_dict():
    test_delete_events(request_type=dict)


@pytest.mark.asyncio
async def test_delete_events_async(transport: str = "grpc_asyncio"):
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = error_stats_service.DeleteEventsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            error_stats_service.DeleteEventsResponse()
        )

        response = await client.delete_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, error_stats_service.DeleteEventsResponse)


def test_delete_events_field_headers():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = error_stats_service.DeleteEventsRequest()
    request.project_name = "project_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_events), "__call__") as call:
        call.return_value = error_stats_service.DeleteEventsResponse()

        client.delete_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project_name=project_name/value",) in kw[
        "metadata"
    ]


@pytest.mark.asyncio
async def test_delete_events_field_headers_async():
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = error_stats_service.DeleteEventsRequest()
    request.project_name = "project_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_events), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            error_stats_service.DeleteEventsResponse()
        )

        await client.delete_events(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "project_name=project_name/value",) in kw[
        "metadata"
    ]


def test_delete_events_flattened():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_events), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = error_stats_service.DeleteEventsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_events(project_name="project_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].project_name == "project_name_value"


def test_delete_events_flattened_error():
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_events(
            error_stats_service.DeleteEventsRequest(),
            project_name="project_name_value",
        )


@pytest.mark.asyncio
async def test_delete_events_flattened_async():
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._client._transport.delete_events), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = error_stats_service.DeleteEventsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            error_stats_service.DeleteEventsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_events(project_name="project_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].project_name == "project_name_value"


@pytest.mark.asyncio
async def test_delete_events_flattened_error_async():
    client = ErrorStatsServiceAsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_events(
            error_stats_service.DeleteEventsRequest(),
            project_name="project_name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.ErrorStatsServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ErrorStatsServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.ErrorStatsServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ErrorStatsServiceClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.ErrorStatsServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = ErrorStatsServiceClient(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ErrorStatsServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = ErrorStatsServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.ErrorStatsServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.ErrorStatsServiceGrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = ErrorStatsServiceClient(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client._transport, transports.ErrorStatsServiceGrpcTransport,)


def test_error_stats_service_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.ErrorStatsServiceTransport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_error_stats_service_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.errorreporting_v1beta1.services.error_stats_service.transports.ErrorStatsServiceTransport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.ErrorStatsServiceTransport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_group_stats",
        "list_events",
        "delete_events",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_error_stats_service_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.errorreporting_v1beta1.services.error_stats_service.transports.ErrorStatsServiceTransport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.ErrorStatsServiceTransport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_error_stats_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        ErrorStatsServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id=None,
        )


def test_error_stats_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.ErrorStatsServiceGrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            quota_project_id="octopus",
        )


def test_error_stats_service_host_no_port():
    client = ErrorStatsServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="clouderrorreporting.googleapis.com"
        ),
    )
    assert client._transport._host == "clouderrorreporting.googleapis.com:443"


def test_error_stats_service_host_with_port():
    client = ErrorStatsServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="clouderrorreporting.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "clouderrorreporting.googleapis.com:8000"


def test_error_stats_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.ErrorStatsServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


def test_error_stats_service_grpc_asyncio_transport_channel():
    channel = aio.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.ErrorStatsServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_error_stats_service_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.ErrorStatsServiceGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_error_stats_service_grpc_asyncio_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.ErrorStatsServiceGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        credentials_file=None,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
        ssl_credentials=mock_ssl_cred,
        quota_project_id=None,
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_error_stats_service_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.ErrorStatsServiceGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers_async.create_channel", autospec=True)
def test_error_stats_service_grpc_asyncio_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.ErrorStatsServiceGrpcAsyncIOTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            credentials_file=None,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
            ssl_credentials=mock_ssl_cred,
            quota_project_id=None,
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.ErrorStatsServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        client = ErrorStatsServiceClient(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.ErrorStatsServiceTransport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = ErrorStatsServiceClient.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
