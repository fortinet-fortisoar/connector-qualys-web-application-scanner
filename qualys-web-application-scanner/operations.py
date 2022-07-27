import base64

import requests
from connectors.core.connector import get_logger, ConnectorError
from requests.auth import HTTPBasicAuth

logger = get_logger('qualys-was')


class QualysWAS:
    def __init__(self, config):
        self.base_url = config.get('server_url').strip('/') + '/qps/rest/3.0/'
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
        self.aouth_cred = {'client_id': '', 'secret_id': '', 'admin_id': '', 'token_expiration': '', 'token': ''}

    def make_rest_call(self, endpoint, params=None,
                       headers={"content-type": "application/json", "Accept": "application/json"}, data=None,
                       method='GET'):
        url = '{0}{1}'.format(self.base_url, endpoint)
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
                    return response.json()
            # return json.loads(response.content.decode('utf-8')) if response.content.decode('utf-8') else ''
            if self.error_msg[response.status_code]:
                logger.error('{}'.format(response.content))
                raise ConnectorError('{}'.format(self.error_msg[response.status_code]))
            response.raise_for_status()
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


def scan_count(config, params):
    qualyswas_obj = QualysWAS(config)
    payload = build_payload(params)
    endpoint = 'count/was/wasscan'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, params=payload, method='POST')


def search_scans(config, params):
    qualyswas_obj = QualysWAS(config)
    payload = build_payload(params)
    endpoint = 'search/was/wasscan'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, params=payload, method='POST')


def get_scan_details(config, params):
    qualyswas_obj = QualysWAS(config)
    scan_id = params.get('scan_id')
    endpoint = 'get/was/wasscan/' + str(scan_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint, method='GET')


def retrieve_scan_status(config, params):
    qualyswas_obj = QualysWAS(config)
    scan_id = params.get('scan_id')
    endpoint = 'status/was/wasscan/' + str(scan_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint, method='GET')


def retrieve_scan_results(config, params):
    qualyswas_obj = QualysWAS(config)
    scan_id = params.get('scan_id')
    endpoint = 'download/was/wasscan/' + str(scan_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint, method='GET')


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
    payload = build_payload(params)
    endpoint = 'count/was/webapp'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, params=payload, method='POST')


def search_webapp(config, params):
    qualyswas_obj = QualysWAS(config)
    payload = build_payload(params)
    endpoint = 'search/was/webapp'
    return qualyswas_obj.make_rest_call(endpoint=endpoint, params=payload, method='POST')


def get_webapp_details(config, params):
    qualyswas_obj = QualysWAS(config)
    scan_id = params.get('scan_id')
    endpoint = 'get/was/webapp/' + str(scan_id)
    return qualyswas_obj.make_rest_call(endpoint=endpoint, method='GET')


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


operations = {
    'scan_count': scan_count,
    'search_webapp': search_webapp,
    'create_web_app': create_web_app,
    'get_webapp_details': get_webapp_details,
    'delete_webapp': delete_webapp,
    'count_webapp': count_webapp,
    'search_scans': search_scans,
    'get_scan_details': get_scan_details,
    'retrieve_scan_status': retrieve_scan_status,
    'retrieve_scan_results': retrieve_scan_results,
    'launch_scans': launch_scans,
    'delete_scan': delete_scan
}
