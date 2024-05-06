import base64
VERIFIER_SEAL = 'verifier_seal'

def check_operation(id, details):
    # print(f"[debug] checking policies for event {id}, details: {details}")
    print(f"[info] checking policies for event {id},"
          f" {details['source']}->{details['deliver_to']}: {details['operation']}")
    src = details['source']
    dst = details['deliver_to']
    operation = details['operation']

    # if src == 'data_input' and dst == 'data_processor' \ # TODO: Переделать под наши требования
    #     and operation == 'process_new_data':
    #     authorized = True
    if src == 'connection' and dst == 'data_processing' \
        and operation == 'data_processing':
        authorized = True
    
    # kea - Kafka events analyzer - an extra service for internal monitoring,
    # can only communicate with itself
    if src == 'kea' and dst == 'kea' \
            and (operation == 'self_test' or operation == 'test_param'):
        authorized = True

    return authorized


def check_payload_seal(payload):
    try:
        p = base64.b64decode(payload).decode()
        if p.endswith(VERIFIER_SEAL):
            print('[info] payload seal is valid')
            return True
    except Exception as e:
        print(f'[error] seal check error: {e}')
        return False