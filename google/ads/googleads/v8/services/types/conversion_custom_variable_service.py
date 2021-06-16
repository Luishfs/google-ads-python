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
import proto  # type: ignore

from google.ads.googleads.v8.enums.types import (
    response_content_type as gage_response_content_type,
)
from google.ads.googleads.v8.resources.types import (
    conversion_custom_variable as gagr_conversion_custom_variable,
)
from google.protobuf import field_mask_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v8.services",
    marshal="google.ads.googleads.v8",
    manifest={
        "GetConversionCustomVariableRequest",
        "MutateConversionCustomVariablesRequest",
        "ConversionCustomVariableOperation",
        "MutateConversionCustomVariablesResponse",
        "MutateConversionCustomVariableResult",
    },
)


class GetConversionCustomVariableRequest(proto.Message):
    r"""Request message for
    [ConversionCustomVariableService.GetConversionCustomVariable][google.ads.googleads.v8.services.ConversionCustomVariableService.GetConversionCustomVariable].

    Attributes:
        resource_name (str):
            Required. The resource name of the conversion
            custom variable to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1,)


class MutateConversionCustomVariablesRequest(proto.Message):
    r"""Request message for
    [ConversionCustomVariableService.MutateConversionCustomVariables][google.ads.googleads.v8.services.ConversionCustomVariableService.MutateConversionCustomVariables].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose
            conversion custom variables are being modified.
        operations (Sequence[google.ads.googleads.v8.services.types.ConversionCustomVariableOperation]):
            Required. The list of operations to perform
            on individual conversion custom variables.
        partial_failure (bool):
            If true, successful operations will be
            carried out and invalid operations will return
            errors. If false, all operations will be carried
            out in one transaction if and only if they are
            all valid. Default is false.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
        response_content_type (google.ads.googleads.v8.enums.types.ResponseContentTypeEnum.ResponseContentType):
            The response content type setting. Determines
            whether the mutable resource or just the
            resource name should be returned post mutation.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ConversionCustomVariableOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3,)
    validate_only = proto.Field(proto.BOOL, number=4,)
    response_content_type = proto.Field(
        proto.ENUM,
        number=5,
        enum=gage_response_content_type.ResponseContentTypeEnum.ResponseContentType,
    )


class ConversionCustomVariableOperation(proto.Message):
    r"""A single operation (create, update) on a conversion custom
    variable.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        create (google.ads.googleads.v8.resources.types.ConversionCustomVariable):
            Create operation: No resource name is
            expected for the new conversion custom variable.
        update (google.ads.googleads.v8.resources.types.ConversionCustomVariable):
            Update operation: The conversion custom
            variable is expected to have a valid resource
            name.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=3, message=field_mask_pb2.FieldMask,
    )
    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=gagr_conversion_custom_variable.ConversionCustomVariable,
    )
    update = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=gagr_conversion_custom_variable.ConversionCustomVariable,
    )


class MutateConversionCustomVariablesResponse(proto.Message):
    r"""Response message for
    [ConversionCustomVariableService.MutateConversionCustomVariables][google.ads.googleads.v8.services.ConversionCustomVariableService.MutateConversionCustomVariables].

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g. auth errors), we return an RPC
            level error.
        results (Sequence[google.ads.googleads.v8.services.types.MutateConversionCustomVariableResult]):
            All results for the mutate.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=1, message=status_pb2.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateConversionCustomVariableResult",
    )


class MutateConversionCustomVariableResult(proto.Message):
    r"""The result for the conversion custom variable mutate.
    Attributes:
        resource_name (str):
            Returned for successful operations.
        conversion_custom_variable (google.ads.googleads.v8.resources.types.ConversionCustomVariable):
            The mutated conversion custom variable with only mutable
            fields after mutate. The field will only be returned when
            response_content_type is set to "MUTABLE_RESOURCE".
    """

    resource_name = proto.Field(proto.STRING, number=1,)
    conversion_custom_variable = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gagr_conversion_custom_variable.ConversionCustomVariable,
    )


__all__ = tuple(sorted(__protobuf__.manifest))