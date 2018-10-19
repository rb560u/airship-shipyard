# Copyright 2017 AT&T Intellectual Property.  All other rights reserved.
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
import enum
import json

from .base_client import BaseClient


class ApiPaths(enum.Enum):
    """ Enumeration of api paths.

    This implementation assumes that the endpoint for shipyard
    includes api/v1.0, so it is not repeated here.
    """
    _BASE_URL = '{}/'
    GET_CONFIGDOCS = _BASE_URL + 'configdocs'
    POST_GET_CONFIG = _BASE_URL + 'configdocs/{}'
    GET_RENDERED = _BASE_URL + 'renderedconfigdocs'
    COMMIT_CONFIG = _BASE_URL + 'commitconfigdocs'
    POST_GET_ACTIONS = _BASE_URL + 'actions'
    GET_ACTION_DETAIL = _BASE_URL + 'actions/{}'
    GET_VALIDATION_DETAIL = _BASE_URL + 'actions/{}/validations/{}'
    GET_STEP_DETAIL = _BASE_URL + 'actions/{}/steps/{}'
    GET_STEP_LOG = _BASE_URL + 'actions/{}/steps/{}/logs'
    POST_CONTROL_ACTION = _BASE_URL + 'actions/{}/control/{}'
    GET_NOTEDETAILS = _BASE_URL + 'notedetails/{}'
    GET_WORKFLOWS = _BASE_URL + 'workflows'
    GET_DAG_DETAIL = _BASE_URL + 'workflows/{}'
    GET_SITE_STATUSES = _BASE_URL + 'site_statuses'


class ShipyardClient(BaseClient):
    """
    A client for shipyard API
    :param context: shipyardclient_context, context object
    """
    # Set up the values used to look up the service endpoint.
    interface = 'public'
    service_type = 'shipyard'

    def post_configdocs(self,
                        collection_id=None,
                        buffer_mode='rejectoncontents',
                        document_data=None):
        """
        Ingests a collection of documents
        :param str collection_id: identifies a collection of docs.Bucket_id
        :param str buffermode: append|replace|rejectOnContents
        :param str document_data: data in a format understood by Deckhand(YAML)
        :returns: diff from last committed revision to new revision
        :rtype: Response object
        """
        query_params = {"buffermode": buffer_mode}
        url = ApiPaths.POST_GET_CONFIG.value.format(
            self.get_endpoint(),
            collection_id
        )
        return self.post_resp(url, query_params, document_data)

    def get_configdocs(self, collection_id=None, version='buffer',
                       cleartext_secrets=False):
        """
        Get the collection of documents from deckhand specified by
        collection id
        :param collection_id: String, bucket_id in deckhand
        :param version: String, buffer|committed|last_site_action|
                                successful_site_action
        :rtype: Response object
        """
        query_params = {"version": version}
        if cleartext_secrets is True:
            query_params['cleartext-secrets'] = 'true'
        url = ApiPaths.POST_GET_CONFIG.value.format(
            self.get_endpoint(),
            collection_id)
        return self.get_resp(url, query_params)

    def get_configdocs_status(self, versions=None):
        """
        Get the status of the collection of documents from shipyard
        :returns: Response object
        :param versions: List of versions to compare
        """
        query_params = {"versions": versions}
        url = ApiPaths.GET_CONFIGDOCS.value.format(self.get_endpoint())
        return self.get_resp(url, query_params)

    def get_rendereddocs(self, version='buffer', cleartext_secrets=False):
        """
        :param str version: committed|buffer|last_site_action|
                            successful_site_action
        :returns: full set of configdocs in their rendered form.
        :rtype: Response object
        """
        query_params = {"version": version}
        if cleartext_secrets is True:
            query_params['cleartext-secrets'] = 'true'
        url = ApiPaths.GET_RENDERED.value.format(
            self.get_endpoint()
        )
        return self.get_resp(url, query_params)

    def commit_configdocs(self, force=False, dryrun=False):
        """
        :param force: boolean, True|False
        :param dryrun: boolean, True|False
        :returns: dictionary, validations from Airship components
        :rtype: Response object
        """
        query_params = {"force": force, "dryrun": dryrun}
        url = ApiPaths.COMMIT_CONFIG.value.format(self.get_endpoint())
        return self.post_resp(url, query_params)

    def get_actions(self):
        """
        A list of actions that have been executed through shipyard's action API
        :returns: lists all actions
        :rtype: Response object
        """
        url = ApiPaths.POST_GET_ACTIONS.value.format(
            self.get_endpoint()
        )
        return self.get_resp(url)

    def post_actions(self, name=None, parameters=None,
                     allow_intermediate_commits=False):
        """
        Creates an action in the system. This will cause some action to start.
        :param str name: name of supported action to invoke
        :param dict parameters: parameters to use for trigger invocation
        :param allow_intermediate_commits: boolean, True|False
        :returns: action entity created successfully
        :rtype: Response object
        """
        query_params = (
            {"allow-intermediate-commits": allow_intermediate_commits})
        action_data = {"name": name, "parameters": parameters}
        url = ApiPaths.POST_GET_ACTIONS.value.format(
            self.get_endpoint()
        )
        return self.post_resp(url=url,
                              query_params=query_params,
                              data=json.dumps(action_data),
                              content_type='application/json')

    def get_action_detail(self, action_id=None):
        """
        Used to get details about an action
        :param str action_id: Unique ID for a particular action
        :returns: information describing the action
        :rtype: Response object
        """
        url = ApiPaths.GET_ACTION_DETAIL.value.format(
            self.get_endpoint(),
            action_id
        )
        return self.get_resp(url)

    def get_validation_detail(self, action_id=None, validation_id=None):
        """
        Allows for drilldown to validation detailed info.
        :param str action_id: Unique action id
        :param str validation_id: id of the validation
        :returns: validation details about action
        :rtype: Response object
        """
        url = ApiPaths.GET_VALIDATION_DETAIL.value.format(
            self.get_endpoint(), action_id, validation_id)
        return self.get_resp(url)

    def get_step_detail(self, action_id=None, step_id=None):
        """
        Allow for drilldown to step information
        :param str action_id: Unique action id
        :param str step_id: step id
        :returns: details for a step by id for the given action by Id
        :rtype: Response object
        """
        url = ApiPaths.GET_STEP_DETAIL.value.format(
            self.get_endpoint(),
            action_id,
            step_id
        )
        return self.get_resp(url)

    def get_step_log(self, action_id=None, step_id=None, try_number=None):
        """
        Retrieve logs for a particular step
        :param str action_id: Unique action id
        :param str step_id: step id
        :param int try_number: The logs that user wants to retrieve. Note that
                               a workflow can retry multiple times with the
                               names of the logs as 1.log, 2.log, 3.log, etc.
                               Logs from the last attempt will be returned if
                               'try' is not specified.
        :returns: Logs for the step
        :rtype: Response object
        """
        if try_number:
            query_params = {'try': try_number}
        else:
            query_params = {}

        url = ApiPaths.GET_STEP_LOG.value.format(
            self.get_endpoint(),
            action_id,
            step_id
        )
        return self.get_resp(url, query_params)

    def post_control_action(self, action_id=None, control_verb=None):
        """
        Allows for issuing DAG controls against an action.
        :param str action_id: Unique action id
        :param str control_verb: control action to be taken against an activity
        :returns: containing the status of the action fail or success
        :rtype: Response object
        """
        url = ApiPaths.POST_CONTROL_ACTION.value.format(
            self.get_endpoint(), action_id, control_verb)
        return self.post_resp(url)

    def get_note_details(self, note_id):
        """Retrieve note details from a note's associated information

        :param note_id: The ID of the note having additional information
        """
        url = ApiPaths.GET_NOTEDETAILS.value.format(
            self.get_endpoint(), note_id)
        return self.get_resp(url)

    def get_workflows(self, since=None):
        """
        Queries airflow for DAGs that are running or have run
        (successfully or unsuccessfully)
        :param str since: iso8601 date optional
        :returns: DAGS running or that have run
        :rtype: Response object
        """
        query_params = {'since': since}
        url = ApiPaths.GET_WORKFLOWS.value.format(self.get_endpoint())
        return self.get_resp(url, query_params)

    def get_dag_detail(self, workflow_id=None):
        """
        details of a particular scheduled DAG's output
        :param str workflow_id: unique id for a DAG
        :returns: details of a DAGs output
        :rtype: Response object
        """
        url = ApiPaths.GET_DAG_DETAIL.value.format(self.get_endpoint(),
                                                   workflow_id)
        return self.get_resp(url)

    def get_site_statuses(self, fltrs=None):
        """
        Get statuses for the site.
        :param str filters: status-types for site statuses to retrieve.
        :rtype: Response object
        """
        if fltrs:
            query_params = {'filters': fltrs}
        else:
            query_params = {}

        url = ApiPaths.GET_SITE_STATUSES.value.format(
            self.get_endpoint())
        return self.get_resp(url, query_params)
