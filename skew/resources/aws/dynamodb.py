# Copyright (c) 2014 Scopely, Inc.
# Copyright (c) 2015 Mitch Garnaat
# Copyright (c) 2020 Jerome Guibert
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import logging

import jmespath

from skew.resources.aws import AWSResource

LOG = logging.getLogger(__name__)


class Table(AWSResource):
    class Meta(object):
        service = "dynamodb"
        type = "table"
        enum_spec = ("list_tables", "TableNames", None)
        id = "TableName"
        detail_spec = ("describe_table", "TableName", "Table")
        tags_spec = ("list_tags_of_resource", "Tags[]", "ResourceArn", "arn")
        filter_name = None
        name = "TableName"
        date = "CreationDateTime"
        dimension = "TableName"

    @classmethod
    def filter(cls, arn, resource_id, data):
        LOG.debug("%s: %s == %s", arn, resource_id, data)
        return resource_id == data

    def __init__(self, client, data, query=None):
        # data from list_tables operation is a table name
        super(Table, self).__init__(client, data={"TableName": data}, query=query)
        detail_op, param_name, detail_path = self.Meta.detail_spec
        params = {param_name: self.id}
        data = client.call(detail_op, **params)
        self._data = jmespath.search(detail_path, data)
