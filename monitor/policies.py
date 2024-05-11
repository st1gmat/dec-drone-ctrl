import base64
VERIFIER_SEAL = 'verifier_seal'

def check_operation(id, details):
    # print(f"[debug] checking policies for event {id}, details: {details}")
    print(f"[info] checking policies for event {id},"
          f" {details['source']}->{details['deliver_to']}: {details['operation']}")
    src = details['source']
    dst = details['deliver_to']
    operation = details['operation']

    if src == 'connection' and dst == 'data_processing' \
        and operation == 'data_processing':
        authorized = True
    
    if src == 'data_processing' and dst == 'cooperation_tasks' \
        and operation == 'task_data':
        authorized = True

    if src == 'cooperation_tasks' and dst == 'cooperation_plane' \
        and operation == 'plane_data':
        authorized = True

    if src == 'cooperation_plane' and dst == 'flight_control' \
        and operation == 'plane_data':
        authorized = True
    
    if src == 'flight_control' and dst == 'emergency_landing' \
        and operation == 'alert':
        authorized = True
    
    if src == 'flight_control' and dst == 'motor_control' \
        and operation == 'movement_data':
        authorized = True
    
    if src == 'motor_control' and dst == 'technical_data' \
        and operation == 'motor_data':
        authorized = True

    if src == 'battery_control' and dst == 'technical_data' \
        and operation == 'battery_status':
        authorized = True

    if src == 'technical_data' and dst == 'flight_control' \
        and operation == 'data':
        authorized = True

    if src == 'navigation' and dst == 'flight_control' \
        and operation == 'location_data':
        authorized = True 

    if src == 'lps' and dst == 'navigation' \
        and operation == 'location_data':
        authorized = True 
    
    if src == 'gps' and dst == 'navigation' \
        and operation == 'location_data':
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