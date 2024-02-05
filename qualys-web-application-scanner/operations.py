""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

import base64
import requests
import re
import arrow
import os
from connectors.core.connector import get_logger, ConnectorError
from requests.auth import HTTPBasicAuth
from connectors.cyops_utilities.builtins import upload_file_to_cyops
from django.conf import settings

logger = get_logger('qualys-was')
DATE_PATTERN = re.compile("^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d+")


class QualysWAS:
    def __init__(self, config):
        self.base_url = config.get('server_url').strip('/')
        if not self.base_url.startswith('https://'):
            self.base_url = 'https://{0}'.format(self.base_url)
        self.username = config['username']
        self.password = config['password']
        self.verify_ssl = config['verify_ssl']
        self.error_msg = {
            'You are not authorized to access the application API': 'You must be granted the API access permission in your roles and scopes',
            'Unauthorized Access': 'You are not authorized to access the application through the APU or User is not authorized to perform this operation or Quta of web applicable has beene exceeded',
            'time_out': 'The request timed out while trying to connect to the remote server',
            'ssl_error': 'SSL certificate validation failed'}
        # self.aouth_cred = {'client_id': '', 'secret_id': '', 'admin_id': '', 'token_expiration': '', 'token': ''}

    def make_rest_call(self, endpoint, params=None,
                       headers={"Content-Type": "application/json", "Accept": "application/json"}, data=None,
                       method='GET', is_tag_action=False, is_user_action=False, is_file_action=False):
        if is_tag_action:
            url = '{0}/qps/rest/2.0/{1}'.format(self.base_url, endpoint)
        elif is_user_action:
            url = '{0}/qps/rest/1.0/{1}'.format(self.base_url, endpoint)
        else:
            url = '{0}/qps/rest/3.0/{1}'.format(self.base_url, endpoint)
        auth = self.username + ':' + self.password
        auth_header = {'Authorization': 'Basic ' + base64.b64encode(auth.encode('utf-8')).decode()}
        headers.update(auth_header)
        logger.info('Request URL {}'.format(url))
        try:
            response = requests.request(method,
                                        url,
                                        json=data,
                                        headers=headers,
                                        verify=self.verify_ssl,
                                        params=params)
            if response.ok:
                if response.status_code == 200:
                    if is_file_action:
                        return response.content
                    else:
                        return response.json()
            # return json.loads(response.content.decode('utf-8')) if response.content.decode('utf-8') else ''
            else:
                err_resp = response.json()
                if err_resp.get("ServiceResponse").get("responseCode") and err_resp.get("ServiceResponse").get("responseErrorDetails").get("errorMessage") and err_resp.get("ServiceResponse").get("responseErrorDetails").get("errorResolution"):
                    err_msg = '{0}:{1}:{2}'.format(err_resp.get("ServiceResponse").get("responseCode"), err_resp.get("ServiceResponse").get("responseErrorDetails").get("errorMessage"), err_resp.get("ServiceResponse").get("responseErrorDetails").get("errorResolution"))
                    logger.error(err_msg)
                    raise ConnectorError(err_msg)
            # response.raise_for_status()
        except requests.exceptions.SSLError as e:
            logger.exception('{}'.format(e))
            raise ConnectorError('{}'.format(self.error_msg['ssl_error']))
        except requests.exceptions.ConnectionError as e:
            logger.exception('{}'.format(e))
            raise ConnectorError('{}'.format(self.error_msg['time_out']))
        except Exception as e:
            logger.exception('{}'.format(e))
            raise ConnectorError('{}'.format(e))


def get_config(config):
    if config:
        server_url = config.get('server_url')
        username = config.get('username')
        password = config.get('password')
        verify_ssl = config.get('verify_ssl')
        if all([username, server_url, password]):
            if not server_url.startswith('https://'):
                server_url = 'https://' + server_url
            return server_url + ':' + username, password, verify_ssl
        else:
            raise ConnectorError("Please provide required configuration")


def make_rest_call1(method, endpoint, config, params=None, data=None):
    server_url, username, password, verify_ssl = get_config(config)
    endpoint_url = '{0}{1}{2}'.format(server_url, '/qps/rest/3.0', endpoint)
    try:
        headers = {"content-type": "application/json", "Accept": "application/json"}
        if method == 'GET':
            logger.info("Endpoint [{0}] params [{1}]".format(endpoint_url, str(params)))
            response = requests.get(url=endpoint_url, headers=headers, auth=HTTPBasicAuth(username, password),
                                    params=params, verify=verify_ssl)
        else:
            logger.info("Endpoint [{0}] params [{1}] data [{2}]".format(endpoint_url, str(params), str(data)))
            response = requests.request(method=method, url=endpoint_url, headers=headers,
                                        auth=HTTPBasicAuth(username, password), json=data if data else None,
                                        params=params, verify=verify_ssl)

        if response.status_code == 200 or response.status_code == 201:
            logger.info("make_rest_call: Success for {0}".format(endpoint_url))
            if method == "DELETE":
                return {"status": "Success"}
            return response.json()
        else:
            try:
                resp = response.json()
                message = resp['message']
            except Exception as e:
                message = 'Operation Failed'
            logger.error(
                "make_rest_call:Failure with Status: [{0}] Description: [{1}]".format(str(response.status_code),
                                                                                      str(message)))
            raise ConnectorError("Status: [{0}] Description: [{1}]".format(str(response.status_code), str(message)))
    except Exception as err:
        logger.error("{}".format(str(err)))
        raise ConnectorError("{}".format(str(err)))


def _check_health(config):
    try:
        resp = scan_count(config, params={})
        logger.info(resp)
        return True
    except Exception as err:
        logger.error("Please make sure the credentials are valid.[{0}]".format(str(err)))
        raise ConnectorError(
            "Please make sure the credentials are valid.[{0}]".format(str(err)))


def build_payload(params):
    result = dict()
    for key, value in params.items():
        if value:
            result[key] = value
    return result


def build_criteria_list(params, use_contains_opr=None):
    criteria_list = []
    for key, value in params.items():
        if use_contains_opr and key in use_contains_opr:
            if isinstance(value, str) and "," in value:
                for element in [item.strip() for item in value.split(",")]:
                    criteria_list.append({
                         "field": key,
                         "operator": "CONTAINS",
                         "value": element
                    })
            elif isinstance(value, list):
                for item in value:
                    criteria_list.append({
                         "field": key,
                         "operator": "CONTAINS",
                         "value": item
                    })
            else:
                criteria_list.append({
                 "field": key,
                 "operator": "CONTAINS",
                 "value": value
                })
        elif isinstance(value, str) and "," in value:
            for element in [item.strip() for item in value.split(",")]:
                criteria_list.append({
                 "field": key,
                 "operator": "EQUALS",
                 "value": element
                })
        elif isinstance(value, list):
            for item in value:
                criteria_list.append({
                 "field": key,
                 "operator": "EQUALS",
                 "value": item
                })
        elif isinstance(value, str) and DATE_PATTERN.match(value):
            value = value[:19] + "Z"
            criteria_list.append({
                "field": key,
                "operator": "GREATER",
                "value": value
            })
        elif isinstance(value, bool):
            criteria_list.append({
                "field": key,
                "operator": "EQUALS",
                "value": str(value).lower()
            })
        else:
            criteria_list.append({
                 "field": key,
                 "operator": "EQUALS",
                 "value": value
            })
    return criteria_list


def build_preferences(params):
    preferences_dict = {}
    if params.get("limitResults"):
        preferences_dict.update({"limitResults": str(params.pop("limitResults"))})
    if params.get("startFromOffset"):
        preferences_dict.update({"startFromOffset": str(params.pop("startFromOffset"))})
    if params.get("verbose"):
        preferences_dict.update({"verbose": "true"})
    if "verbose" in params:
        params.pop("verbose")
    return preferences_dict


def scan_count(config, params):
    qualyswas_obj = QualysWAS(config)
    use_contains_opr = ["name", "webApp.name", "reference"]
    filter_criteria_list = build_criteria_list(build_payload(params), use_contains_opr)
    payload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": filter_criteria_list
            }
        }
    }
    endpoint = 'count/was/wasscan'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST')


def search_scans(config, params):
    qualyswas_obj = QualysWAS(config)
    params = build_payload(params)
    preferences_dict = build_preferences(params)
    use_contains_opr = ["name", "webApp.name", "reference"]
    filter_criteria_list = build_criteria_list(params, use_contains_opr)
    payload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": filter_criteria_list
            }
        }
    }
    if preferences_dict:
        payload["ServiceRequest"].update({"preferences": preferences_dict})
    endpoint = 'search/was/wasscan'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST')


def get_scan_details(config, params):
    qualyswas_obj = QualysWAS(config)
    scan_id = params.get('scan_id')
    endpoint = 'get/was/wasscan/' + str(scan_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint)


def retrieve_scan_status(config, params):
    qualyswas_obj = QualysWAS(config)
    scan_id = params.get('scan_id')
    endpoint = 'status/was/wasscan/' + str(scan_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint)


def retrieve_scan_results(config, params):
    qualyswas_obj = QualysWAS(config)
    scan_id = params.get('scan_id')
    endpoint = 'download/was/wasscan/' + str(scan_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint)


def launch_scans(config, params):
    qualyswas_obj = QualysWAS(config)
    scan_name = params.get('scan_name')
    scan_type = params.get('scan_type')
    web_app_id = params.get('web_app_id')
    web_app_auth_record = params.get('web_app_auth_record')
    scanner_appliance = params.get('scanner_appliance')
    profile_id = params.get('profile_id')
    endpoint = 'launch/was/wasscan'
    payload = {
        'ServiceRequest': {
            'data': {
                'WasScan': {
                    'name': scan_name,
                    'type': scan_type,
                    'target': {
                        'webApp': {
                            'id': web_app_id
                        },
                        'webAppAuthRecord': {
                            'isDefault': web_app_auth_record
                        },
                        'scannerAppliance': {
                            'type': scanner_appliance
                        }
                    },
                    'profile': {
                        'id': profile_id
                    }
                }
            }
        }
    }
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST')


def delete_scan(config, params):
    qualyswas_obj = QualysWAS(config)
    scan_id = params.get('scan_id')
    endpoint = 'delete/was/wasscan/' + str(scan_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint, method='POST')


def count_webapp(config, params):
    qualyswas_obj = QualysWAS(config)
    use_contains_opr = ["name", "url", "tags.name"]
    filter_criteria_list = build_criteria_list(build_payload(params), use_contains_opr)
    payload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": filter_criteria_list
            }
        }
    }
    endpoint = 'count/was/webapp'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST')


def search_webapp(config, params):
    qualyswas_obj = QualysWAS(config)
    params = build_payload(params)
    preferences_dict = build_preferences(params)
    use_contains_opr = ["name", "url", "tags.name"]
    filter_criteria_list = build_criteria_list(params, use_contains_opr)
    payload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": filter_criteria_list
            }
        }
    }
    if preferences_dict:
        payload["ServiceRequest"].update({"preferences": preferences_dict})
    endpoint = 'search/was/webapp'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST')


def get_webapp_details(config, params):
    qualyswas_obj = QualysWAS(config)
    web_app_id = params.get('id')
    endpoint = 'get/was/webapp/' + str(web_app_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint)


def delete_webapp(config, params):
    qualyswas_obj = QualysWAS(config)
    app_id = params.get('app_id')
    endpoint = 'delete/was/webapp/' + str(app_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint, method='POST')


def create_web_app(config, params):
    qualyswas_obj = QualysWAS(config)
    name = params.get('name')
    url = params.get('url')
    id = params.get('id')
    endpoint = 'create/was/webapp'
    if id:
        payload = {
            'ServiceRequest': {
                'data': {
                    'WebApp': {
                        'name': name,
                        'url': url,
                        'authRecords': {
                            'set': {
                                'WebAppAuthRecord': {
                                    'id': id
                                }
                            }
                        }
                    }
                }
            }
        }
    else:
        payload = {
            'ServiceRequest': {
                'data': {
                    'WebApp': {
                        'name': name,
                        'url': url
                    }
                }
            }
        }
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST')


def search_reports(config, params):
    qualyswas_obj = QualysWAS(config)
    params = build_payload(params)
    preferences_dict = build_preferences(params)
    use_contains_opr = ["name", "tags.name"]
    filter_criteria_list = build_criteria_list(params, use_contains_opr)
    payload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": filter_criteria_list
            }
        }
    }
    if preferences_dict:
        payload["ServiceRequest"].update({"preferences": preferences_dict})
    endpoint = 'search/was/report'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST')


def download_report(config, params):
    qualyswas_obj = QualysWAS(config)
    report_id = params.get('report_id')
    endpoint = 'download/was/report/' + str(report_id)
    response = qualyswas_obj.make_rest_call(endpoint=endpoint, is_file_action=True)
    time = arrow.utcnow()
    file_name = f'qualys_was_{time}'
    path = os.path.join(settings.TMP_FILE_ROOT, file_name)
    logger.error("Path: {0}".format(path))
    with open(path, 'wb') as fp:
        fp.write(response)
    attach_response = upload_file_to_cyops(file_path=file_name, filename=file_name,
                                           name=file_name, create_attachment=True)
    return attach_response


def search_option_profiles(config, params):
    qualyswas_obj = QualysWAS(config)
    params = build_payload(params)
    preferences_dict = build_preferences(params)
    use_contains_opr = ["name", "tags.name", "owner.name", "owner.username"]
    filter_criteria_list = build_criteria_list(params, use_contains_opr)
    payload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": filter_criteria_list
            }
        }
    }
    if preferences_dict:
        payload["ServiceRequest"].update({"preferences": preferences_dict})
    endpoint = 'search/was/optionprofile'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST')


def search_schedule(config, params):
    qualyswas_obj = QualysWAS(config)
    params = build_payload(params)
    preferences_dict = build_preferences(params)
    use_contains_opr = ["name", "webApp.name"]
    filter_criteria_list = build_criteria_list(params, use_contains_opr)
    payload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": filter_criteria_list
            }
        }
    }
    if preferences_dict:
        payload["ServiceRequest"].update({"preferences": preferences_dict})
    endpoint = 'search/was/wasscanschedule'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST')


def get_schedule_details(config, params):
    qualyswas_obj = QualysWAS(config)
    schedule_id = params.get('schedule_id')
    endpoint = 'get/was/wasscanschedule/' + str(schedule_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint)


def search_tags(config, params):
    qualyswas_obj = QualysWAS(config)
    params = build_payload(params)
    preferences_dict = build_preferences(params)
    use_contains_opr = ["name"]
    filter_criteria_list = build_criteria_list(params, use_contains_opr)
    payload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": filter_criteria_list
            }
        }
    }
    if preferences_dict:
        payload["ServiceRequest"].update({"preferences": preferences_dict})
    endpoint = 'search/am/tag'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST', is_tag_action=True)


def create_tag(config, params):
    qualyswas_obj = QualysWAS(config)
    endpoint = 'create/am/tag'
    payload = {
        "ServiceRequest": {
            "data": {
                "Tag": {
                    "name": params.get('name')
                }
            }
        }
    }
    if params.get('criticalityScore'):
        payload["ServiceRequest"]["data"]["Tag"].update({"criticalityScore": params.get('criticalityScore')})
    if params.get('ruleType'):
        payload["ServiceRequest"]["data"]["Tag"].update({"ruleType": params.get('ruleType')})
    if params.get('ruleText'):
        payload["ServiceRequest"]["data"]["Tag"].update({"ruleText": params.get('ruleText')})
    if params.get('provider'):
        payload["ServiceRequest"]["data"]["Tag"].update({"provider": params.get('provider')})
    if params.get('color'):
        payload["ServiceRequest"]["data"]["Tag"].update({"color": params.get('color')})
    if params.get('children'):
        child_tags = params.get('children').split(",")
        tag_list = [{"name": tag} for tag in child_tags]
        payload["ServiceRequest"]["data"]["Tag"].update({"children": {"set": {"TagSimple": tag_list}}})
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST', is_tag_action=True)


def update_tag(config, params):
    qualyswas_obj = QualysWAS(config)
    endpoint = 'update/am/tag/' + str(params.pop('id'))
    payload = {
        "ServiceRequest": {
            "data": {
                "Tag": {}
            }
        }
    }
    if params.get('name'):
        payload["ServiceRequest"]["data"]["Tag"].update({"name": params.get('name')})
    if params.get('criticalityScore'):
        payload["ServiceRequest"]["data"]["Tag"].update({"criticalityScore": params.get('criticalityScore')})
    if params.get('ruleType'):
        payload["ServiceRequest"]["data"]["Tag"].update({"ruleType": params.get('ruleType')})
    if params.get('ruleText'):
        payload["ServiceRequest"]["data"]["Tag"].update({"ruleText": params.get('ruleText')})
    if params.get('color'):
        payload["ServiceRequest"]["data"]["Tag"].update({"color": params.get('color')})
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST', is_tag_action=True)


def delete_tag(config, params):
    qualyswas_obj = QualysWAS(config)
    tag_id = params.get('tag_id')
    endpoint = 'delete/am/tag/' + str(tag_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint, method='POST', is_tag_action=True)


def search_users(config, params):
    qualyswas_obj = QualysWAS(config)
    params = build_payload(params)
    preferences_dict = build_preferences(params)
    use_contains_opr = ["username"]
    filter_criteria_list = build_criteria_list(params, use_contains_opr)
    payload = {
        "ServiceRequest": {
            "filters": {
                "Criteria": filter_criteria_list
            }
        }
    }
    if preferences_dict:
        payload["ServiceRequest"].update({"preferences": preferences_dict})
    endpoint = 'search/admin/user'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, data=payload, method='POST', is_user_action=True)


operations = {
    'scan_count': scan_count,
    'search_scans': search_scans,
    'get_scan_details': get_scan_details,
    'retrieve_scan_status': retrieve_scan_status,
    'retrieve_scan_results': retrieve_scan_results,
    'launch_scans': launch_scans,
    'delete_scan': delete_scan,
    'count_webapp': count_webapp,
    'search_webapp': search_webapp,
    'get_webapp_details': get_webapp_details,
    'delete_webapp': delete_webapp,
    'create_web_app': create_web_app,
    'search_reports': search_reports,
    'download_report': download_report,
    'search_option_profiles': search_option_profiles,
    'search_schedule': search_schedule,
    'get_schedule_details': get_schedule_details,
    'search_tags': search_tags,
    'create_tag': create_tag,
    "update_tag": update_tag,
    "delete_tag": delete_tag,
    "search_users": search_users
}
