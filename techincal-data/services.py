logs = []

def check_battery(value):
    value = int(value)
    if value > logs[-1]:
        return False
    logs.append(value)
    return True