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

from collections import OrderedDict
import functools
import re
from typing import Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.errorreporting_v1beta1.types import report_errors_service

from .transports.base import ReportErrorsServiceTransport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import ReportErrorsServiceGrpcAsyncIOTransport
from .client import ReportErrorsServiceClient


class ReportErrorsServiceAsyncClient:
    """An API for reporting error events."""

    _client: ReportErrorsServiceClient

    DEFAULT_ENDPOINT = ReportErrorsServiceClient.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = ReportErrorsServiceClient.DEFAULT_MTLS_ENDPOINT

    from_service_account_file = ReportErrorsServiceClient.from_service_account_file
    from_service_account_json = from_service_account_file

    get_transport_class = functools.partial(
        type(ReportErrorsServiceClient).get_transport_class,
        type(ReportErrorsServiceClient),
    )

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, ReportErrorsServiceTransport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiate the report errors service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.ReportErrorsServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """

        self._client = ReportErrorsServiceClient(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def report_error_event(
        self,
        request: report_errors_service.ReportErrorEventRequest = None,
        *,
        project_name: str = None,
        event: report_errors_service.ReportedErrorEvent = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> report_errors_service.ReportErrorEventResponse:
        r"""Report an individual error event.

        This endpoint accepts **either** an OAuth token, **or** an `API
        key <https://support.google.com/cloud/answer/6158862>`__ for
        authentication. To use an API key, append it to the URL as the
        value of a ``key`` parameter. For example:

        ``POST https://clouderrorreporting.googleapis.com/v1beta1/projects/example-project/events:report?key=123ABC456``

        Args:
            request (:class:`~.report_errors_service.ReportErrorEventRequest`):
                The request object. A request for reporting an
                individual error event.
            project_name (:class:`str`):
                Required. The resource name of the Google Cloud Platform
                project. Written as ``projects/`` plus the `Google Cloud
                Platform project
                ID <https://support.google.com/cloud/answer/6158840>`__.
                Example: ``projects/my-project-123``.
                This corresponds to the ``project_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            event (:class:`~.report_errors_service.ReportedErrorEvent`):
                Required. The error event to be
                reported.
                This corresponds to the ``event`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.report_errors_service.ReportErrorEventResponse:
                Response for reporting an individual
                error event. Data may be added to this
                message in the future.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        if request is not None and any([project_name, event]):
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = report_errors_service.ReportErrorEventRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.

        if project_name is not None:
            request.project_name = project_name
        if event is not None:
            request.event = event

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.report_error_event,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("project_name", request.project_name),)
            ),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution(
            "google-cloud-errorreporting",
        ).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("ReportErrorsServiceAsyncClient",)
