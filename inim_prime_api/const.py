from .exceptions import *

API_PATH = "/cgi-bin/api.cgi"

# Status codes
STATUS_SUCCESS = 0
STATUS_ERROR_PARAM = 1
STATUS_ERROR_APIKEY = 2
STATUS_ERROR_COMMAND = 3
STATUS_ERROR_EXECUTION = 4
STATUS_ERROR_PROTOCOL = 5
STATUS_ERROR_AUTHORIZATION = 6

# Map of status codes to exceptions + optional messages
STATUS_EXCEPTIONS = {
    STATUS_ERROR_PARAM: ("Parameter error", InimPrimeParamError),
    STATUS_ERROR_APIKEY: ("Invalid API key", InimPrimeApiKeyError),
    STATUS_ERROR_COMMAND: ("Command error", InimPrimeCommandError),
    STATUS_ERROR_EXECUTION: ("Panel execution error", InimPrimeExecutionError),
    STATUS_ERROR_PROTOCOL: ("Protocol error", InimPrimeProtocolError),
    STATUS_ERROR_AUTHORIZATION: ("Authorization error", InimPrimeAuthorizationError),
}

CMD_VERSION = "version"
CMD_PING = "ping"
CMD_GET_ZONES_STATUS = "get_zones_status"
CMD_GET_OUTPUTS_STATUS = "get_outputs_status"
CMD_GET_PARTITIONS_STATUS = "get_partitions_status"
CMD_GET_SCENARIOS_STATUS = "get_scenarios_status"
CMD_GET_LOG_ELEMENTS = "get_log_elements"
CMD_GET_GSM_STATUS = "get_gsm_status"
CMD_GET_FAULTS_STATUS = "get_faults_status"
CMD_GET_PARTITIONS_NRZ = "get_partitions_nrz"
CMD_SET_OUTPUTS_MODE = "set_outputs_mode"
CMD_SET_PARTITIONS_MODE = "set_partitions_mode"
CMD_SET_ZONES_MODE = "set_zones_mode"
CMD_SET_SCENARIOS_MODE = "set_scenarios_mode"
