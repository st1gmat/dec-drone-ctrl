from monitor.policies import check_operation
import pytest


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            {
                "source": 'connection',
                "deliver_to": 'data_processing',
                "operation": 'data_processing'
            },
            True
        ),
        (
            {
                "source": 'data_processing',
                "deliver_to": 'connection',
                "operation": 'data_outputting'
            },
            True
        ),
        (
            {
                "source": 'data_processing',
                "deliver_to": 'connection',
                "operation": 'task_confirm'
            },
            True
        ),
        (
            {
                "source": 'data_processing',
                "deliver_to": 'cooperation-tasks',
                "operation": 'task_plane_data'
            },
            True
        ),
        (
            {
                "source": 'cooperation-tasks',
                "deliver_to": 'cooperation_plane',
                "operation": 'plane_data'
            },
            True
        ),
        (
            {
                "source": 'cooperation-tasks',
                "deliver_to": 'data_processing',
                "operation": 'three_in_one'
            },
            True
        ),
        (
            {
                "source": 'cooperation_plane',
                "deliver_to": 'flight_control',
                "operation": 'loc_data'
            },
            True
        ),
        (
            {
                "source": 'cooperation_plane',
                "deliver_to": 'cooperation-tasks',
                "operation": 'plane_data'
            },
            True
        ),
        (
            {
                "source": 'flight_control',
                "deliver_to": 'emergency_landing',
                "operation": 'alert'
            },
            True
        ),
        (
            {
                "source": 'flight_control',
                "deliver_to": 'motor_control',
                "operation": 'movement_data'
            },
            True
        ),
        (
            {
                "source": 'motor_control',
                "deliver_to": 'technical_data',
                "operation": 'motor_status'
            },
            True
        ),
        (
            {
                "source": 'battery_control',
                "deliver_to": 'technical_data',
                "operation": 'battery_status'
            },
            True
        ),
        (
            {
                "source": 'technical_data',
                "deliver_to": 'flight_control',
                "operation": 'tech_data'
            },
            True
        ),
        (
            {
                "source": 'flight_control',
                "deliver_to": 'cooperation_plane',
                "operation": 'plane_status'
            },
            True
        ),
        (
            {
                "source": 'navigation',
                "deliver_to": 'flight_control',
                "operation": 'location_data'
            },
            True
        ),
        (
            {
                "source": 'lps',
                "deliver_to": 'navigation',
                "operation": 'lps_location_data'
            },
            True
        ),
        (
            {
                "source": 'gps',
                "deliver_to": 'navigation',
                "operation": 'gps_location_data'
            },
            True
        ),
        (
            {
                "source": 'detector',
                "deliver_to": 'detector_control',
                "operation": 'detection'
            },
            True
        ),
        (
            {
                "source": 'detector_control',
                "deliver_to": 'cooperation_plane',
                "operation": 'req_loc_data'
            },
            True
        ),
        (
            {
                "source": 'cooperation_plane',
                "deliver_to": 'detector_control',
                "operation": 'loc_data'
            },
            True
        ),
        (
            {
                "source": 'detector_control',
                "deliver_to": 'cooperation-tasks',
                "operation": 'detection_data'
            },
            True
        ),
        (
            {
                "source": 'detector_control',
                "deliver_to": 'cooperation-tasks',
                "operation": 'detection_data'
            },
            True
        ),
        (
            {
                "source": 'data_processing',
                "deliver_to": 'cooperation-tasks',
                "operation": 'invalid_operation'
            },
            False
        ),
        (
            {
                "source": 'invalid_source',
                "deliver_to": 'data_processing',
                "operation": 'data_processing'
            },
            False
        ),
    ]
)
def test_check_operation(test_input, expected):
    assert check_operation(None, test_input) == expected
