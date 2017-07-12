import iothub_client
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
from iothub_client_args import get_iothub_opt, OptionError



# MQTT transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT

# ConnectionString containing Hostname, Device Id & Device Key
CONNECTION_STRING = "HostName=IOT-CA2-IOTHUB.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=kpsQGHfvpVJV+5voaIg2m7dHxgpXlp/RrTF/RM2Wgso="

MSG_TEXT = "{\"deviceId\": \"myPythonDevice\",\"windSpeed\": %.2f}"

# some embedded platforms need certificate information

def set_certificates(client):
  from iothub_client_cert import CERTIFICATES
  try:
    client.set_option("TrustedCerts", CERTIFICATES)
    print ("set_option TrustedCerts successful!")
  except:
    print("set_option TrustedCerts failed (%s)" % iothub_client_error)

# Receive messages 
def receive_message_callback(message, counter):
    global RECEIVE_CALLBACKS
    message_buffer = message.get_bytearray()
    size = len(message_buffer)
    print ( "Received Message [%d]:" % counter )
    print ( "Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size) )
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print ( "Properties: %s" % key_value_pair )
    counter += 1
    RECEIVE_CALLBACKS += 1
    print ( "Total calls received: %d" % RECEIVE_CALLBACKS )
    return IoTHubMessageDispositionResult.ACCEPTED

# Send messages
def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print ( "Confirmation[%d] received for message with result = %s" % (user_context, result) )
    map_properties = message.properties()
    print ( "message_id: %s" % message.message_id )
    print ( "correlation_id: %s" % message.correlation_id )
    key_value_pair = map_properties.get_internals()
    print ( "Properties: %s" % key_value_pair )
    SEND_CALLBACKS += 1
    print ( "Total calls confirmed: %d" % SEND_CALLBACKS )

def iothub_client_init():
    # Connect to IoTHubClient
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    # some embedded platforms need certificate information
    set_certificates(client)
    # to enable MQTT logging set to 1
    if client.protocol == IoTHubTransportProvider.MQTT:
        client.set_option("logtrace", 1)
    client.set_message_callback(
        receive_message_callback, RECEIVE_CONTEXT)
    return client

def iothub_client_sample_run():
    try:
        client = iothub_client_init()

        if client.protocol == IoTHubTransportProvider.MQTT:
            print ( "IoTHubClient is reporting state" )
            reported_state = "{\"newState\":\"standBy\"}"
            client.send_reported_state(reported_state, len(reported_state), send_reported_state_callback, SEND_REPORTED_STATE_CONTEXT)

        while True:
            # send a few messages every minute
            print ( "IoTHubClient sending %d messages" % MESSAGE_COUNT )

            # for message_counter in range(0, MESSAGE_COUNT):
            #     temperature = MIN_TEMPERATURE + (random.random() * 10)
            #     humidity = MIN_HUMIDITY + (random.random() * 20)
            #     msg_txt_formatted = MSG_TXT % (
            #         AVG_WIND_SPEED + (random.random() * 4 + 2),
            #         temperature,
            #         humidity)
            #     # messages can be encoded as string or bytearray
            #     if (message_counter & 1) == 1:
            #         message = IoTHubMessage(bytearray(msg_txt_formatted, 'utf8'))
            #     else:
            #         message = IoTHubMessage(msg_txt_formatted)
            #     # optional: assign ids
            #     message.message_id = "message_%d" % message_counter
            #     message.correlation_id = "correlation_%d" % message_counter
            #     # optional: assign properties
            #     prop_map = message.properties()
            #     prop_map.add("temperatureAlert", 'true' if temperature > 28 else 'false')

                client.send_event_async(message, send_confirmation_callback, message_counter)
                print ( "IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % message_counter )

            # Wait for Commands or exit
            print ( "IoTHubClient waiting for commands, press Ctrl-C to exit" )

            status_counter = 0
            while status_counter <= MESSAGE_COUNT:
                status = client.get_send_status()
                print ( "Send status: %s" % status )
                time.sleep(10)
                status_counter += 1

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "\nPython %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    try:
        (CONNECTION_STRING, PROTOCOL) = get_iothub_opt(sys.argv[1:], CONNECTION_STRING, PROTOCOL)
    except OptionError as option_error:
        print ( option_error )
        sys.exit(1)

    print ( "Starting the IoT Hub Python sample..." )
    print ( "Protocol %s" % PROTOCOL )
    print ( "Connection string=%s" % CONNECTION_STRING )

    iothub_client_sample_run()
