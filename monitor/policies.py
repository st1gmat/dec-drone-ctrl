import base64
VERIFIER_SEAL = 'verifier_seal'

def check_operation(id, details):
    authorized = False
    # print(f"[debug] checking policies for event {id}, details: {details}")
    print(f"[info] checking policies for event {id},"
          f" {details['source']}->{details['deliver_to']}: {details['operation']}")
    src = details['source']
    dst = details['deliver_to']
    operation = details['operation']

    if src == 'data_input' and dst == 'data_processor' \
        and operation == 'process_new_data':
        authorized = True

    if src == 'data_processor' and dst == 'data_output' \
        and operation == 'process_new_events':
        authorized = True

    if src == 'downloader' and dst == 'manager' \
            and operation == 'download_done':
        authorized = True
    if src == 'manager' and dst == 'downloader' \
            and operation == 'download_file':
        authorized = True
    if src == 'manager' and dst == 'storage' \
            and operation == 'commit_blob':
        authorized = True
    if src == 'manager' and dst == 'verifier' \
            and operation == 'verification_requested':
        authorized = True
    if src == 'verifier' and dst == 'manager' \
            and operation == 'handle_verification_result':
        authorized = True
    if src == 'manager' and dst == 'updater' \
            and operation == 'proceed_with_update' \
            and details['verified'] is True:
        authorized = True
    if src == 'storage' and dst == 'manager' \
            and operation == 'blob_committed':
        authorized = True
    if src == 'storage' and dst == 'verifier' \
            and operation == 'blob_committed':
        authorized = True
    if src == 'verifier' and dst == 'storage' \
            and operation == 'get_blob':
        authorized = True
    if src == 'verifier' and dst == 'storage' \
            and operation == 'commit_sealed_blob' \
            and details['verified'] is True:
        authorized = True
    if src == 'storage' and dst == 'verifier' \
            and operation == 'blob_content':
        authorized = True
    if src == 'updater' and dst == 'storage' \
            and operation == 'get_blob':
        authorized = True
    if src == 'storage' and dst == 'updater' \
            and operation == 'blob_content' and check_payload_seal(details['blob']) is True:
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