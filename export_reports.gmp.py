import os
import sys
from datetime import datetime
from xml.etree import ElementTree

from gvm.protocols.gmpv9 import Gmp as GmpV9
from base64 import b64decode
from pathlib import Path
from gvmtools.helper import Table

report_formats = []
quarter_str = f'{datetime.now().year}Q{(datetime.now().month - 1) // 3 + 1}'
default_filter = 'apply_overrides=1 levels=hml min_qod=70 sort-reverse=severity notes=1 overrides=1'
everything_filter = 'apply_overrides=1 levels=hmlg min_qod=0 sort-reverse=severity notes=1 overrides=1'
report_filters = {
    '': 'apply_overrides=1 levels=hml min_qod=70 sort-reverse=severity notes=1 overrides=1',
    ' Full': 'apply_overrides=1 levels=hmlg min_qod=0 sort-reverse=severity notes=1 overrides=1',
}


def main(gmp: GmpV9, args) -> None:
    fetch_report_format_ids(gmp)

    tasks = gmp.get_tasks(filter="status=Done first=1 rows=-1")
    tasks_xml = tasks.xpath('task')

    heading = ['ID', 'Name', 'Status', 'Severity', 'ReportID']
    rows = []

    for task in tasks_xml:
        name = task.xpath('name/text()')[0]
        task_id = task.get("id")
        status = task.xpath("status/text()")[0]
        severity = task.xpath('last_report/report/severity/text()')[0]
        report_id = task.xpath('last_report/report/@id')[0]

        export_reports(gmp, name, report_id)

        rows.append([task_id, name, status, severity, report_id])

    print('\nExports completed.\n\n')
    print(Table(heading=heading, rows=rows))


def export_reports(gmp: GmpV9, name: str, report_id: str) -> None:
    base_filename = f'{name} Vuln Scan Report {quarter_str}'

    for report_format in report_formats:
        for filename_suffix, report_filter in report_filters.items():
            # noinspection PyBroadException
            try:
                output_filename = f'{base_filename}{filename_suffix}.{report_format["ext"]}'
                if not os.path.isfile(output_filename):
                    res = gmp.get_report(
                        report_id=report_id,
                        report_format_id=report_format['id'],
                        filter=default_filter,
                        ignore_pagination=True,
                    )

                    save_report(output_filename, res)
                    print(f'Saved{filename_suffix} {report_format["name"]} format report for {name} to {output_filename}')
                else:
                    print(f'Skipping{filename_suffix} {report_format["name"]} format report for {name}. Already exists.')
            except:
                print(f'Unable to get{str.lower(filename_suffix)} {report_format["name"]} report for {name}')

            # noinspection PyBroadException
            # try:
            #     output_filename = f'{base_filename} Full.{report_format["ext"]}'
            #     if not os.path.isfile(output_filename):
            #         res = gmp.get_report(
            #             report_id=report_id,
            #             report_format_id=report_format['id'],
            #             filter=everything_filter,
            #             ignore_pagination=True,
            #         )
            #
            #         save_report(output_filename, res)
            #         print(f'Saved Full {report_format["name"]} format report for {name} to {output_filename}')
            #     else:
            #         print(f'Skipping {report_format["name"]} format report for {name}. Already exists.')
            # except:
            #     print(f'Unable to get full {report_format["name"]} report for {name}.')


def save_report(filename: str, res):
    report = res.find('report')
    report_content = report.find('report_format').tail
    decoded_contents = ''
    if report_content is None:
        decoded_contents = ElementTree.tostring(report)
    else:
        decoded_contents = b64decode(report_content.encode('ascii'))
    output_file = Path(filename).expanduser()
    output_file.write_bytes(decoded_contents)


def fetch_report_format_ids(gmp: GmpV9) -> None:
    global report_formats

    print('Fetching report formats for later use: ')

    report_formats_xml = gmp.get_report_formats(filter='name=PDF name=XML name="CSV Results"').xpath('report_format')

    for report_format_element in report_formats_xml:
        report_formats.append({
            'id': report_format_element.get('id'),
            'ext': report_format_element.xpath('extension/text()')[0],
            'name': report_format_element.xpath('name/text()')[0]
        })


if __name__ == '__gmp__':
    main(gmp, args)
