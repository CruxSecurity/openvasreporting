import uuid

from gvm.protocols.gmpv7 import AliveTest
from gvm.protocols.gmpv9 import Gmp as GmpV9

ull_and_fast_scan_config_id = 'daba56c8-73ec-11df-a475-002264764cea'
openvas_scanner_id = '08b69003-5fc2-4037-a479-93b440211c73'


def create_task(gmp, ipaddress, target_id, scan_config_id, scanner_id):
    name = "Scan Suspect Host {}".format(ipaddress)
    response = gmp.create_task(
        name=name,
        config_id=scan_config_id,
        target_id=target_id,
        scanner_id=scanner_id,
    )
    return response.get('id')


def start_task(gmp, task_id):
    response = gmp.start_task(task_id)
    # the response is
    # <start_task_response><report_id>id</report_id></start_task_response>
    return response[0].text


def main(gmp: GmpV9, args: [str]) -> uuid:
    scan_name = args[1]
    host_list = args[2].split(',')

    res = gmp.create_target(
        name=scan_name,
        hosts=host_list,
        alive_test=AliveTest.TCP_SYN_SERVICE_PING,
    )

    target_id = res.get('id')

    task_id = gmp.create_task(
        name=scan_name,
        target_id=target_id,

    )


if __name__ == '__gmp__':
    main(gmp, args)
