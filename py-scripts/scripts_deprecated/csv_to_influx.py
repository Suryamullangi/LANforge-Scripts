#!/usr/bin/env python3

# DEPRECATED, PLEASE USE InfluxRequest.py INSTEAD

# Copies the data from a CSV file from the KPI file generated from a Wifi Capacity test to an Influx database

# The CSV requires three columns in order to work: Date, test details, and numeric-score.

# Date is a unix timestamp, test details is the variable each datapoint is measuring, and numeric-score is the value for that timepoint and variable.

import sys
import os
from pprint import pprint
from influx2 import RecordInflux

if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(1)

if 'py-json' not in sys.path:
    sys.path.append(os.path.join(os.path.abspath('..'), 'py-json'))

import argparse
import datetime

def influx_add_parser_args(parser):
    parser.add_argument('--influx_host', help='Hostname for the Influx database', default=None)
    parser.add_argument('--influx_port', help='IP Port for the Influx database', default=8086)
    parser.add_argument('--influx_org', help='Organization for the Influx database', default=None)
    parser.add_argument('--influx_token', help='Token for the Influx database', default=None)
    parser.add_argument('--influx_bucket', help='Name of the Influx bucket', default=None)
    parser.add_argument('--influx_tag', action='append', nargs=2,
                        help='--influx_tag <key> <val>   Can add more than one of these.', default=[])


class CSVtoInflux():
    def __init__(self,
                 _exit_on_error=False,
                 _exit_on_fail=False,
                 _proxy_str=None,
                 _capture_signal_list=[],
                 influxdb=None,
                 _influx_tag=[],
                 target_csv=None,
                 sep='\t'):
        self.influxdb = influxdb
        self.target_csv = target_csv
        self.influx_tag = _influx_tag
        self.sep = sep

    def read_csv(self, file):
        csv = open(file).read().split('\n')
        rows = list()
        for x in csv:
            if len(x) > 0:
                rows.append(x.split(self.sep))
        return rows

    # Submit data to the influx db if configured to do so.
    def post_to_influx(self):
        df = self.read_csv(self.target_csv)
        length = list(range(0, len(df[0])))
        columns = dict(zip(df[0], length))
        print('columns: %s' % columns)
        influx_variables = ['script', 'short-description', 'test_details', 'Graph-Group',
                            'DUT-HW-version', 'DUT-SW-version', 'DUT-Serial-Num', 'testbed', 'Test Tag', 'Units']
        csv_variables = ['test-id', 'short-description', 'test details', 'Graph-Group',
                         'dut-hw-version', 'dut-sw-version', 'dut-serial-num', 'test-rig', 'test-tag', 'Units']
        csv_vs_influx = dict(zip(csv_variables, influx_variables))
        for row in df[1:]:
            row = [sub.replace('NaN', '0') for sub in row]
            tags = dict()
            print("row: %s" % row)
            short_description = row[columns['short-description']]
            if row[columns['numeric-score']] == 'NaN':
                numeric_score = '0x0'
            else:
                numeric_score = float(row[columns['numeric-score']])
            date = row[columns['Date']]
            date = datetime.datetime.utcfromtimestamp(int(date) / 1000).isoformat() #convert to datetime so influx can read it, this is required
            for variable in csv_variables:
                if variable in columns.keys():
                    index = columns[variable]
                    influx_variable = csv_vs_influx[variable]
                    tags[influx_variable] = row[index]
            self.influxdb.post_to_influx(short_description, numeric_score, tags, date)

    def script_name(self):
        with open(self.target_csv) as fp:
            line = fp.readline()
            line = line.split('\t')
            test_id_index = line.index('test-id')
            line = fp.readline()
            line.split('\t')
            return line[test_id_index]


    def create_dashboard(self,
                         dashboard_name=None):
        #Create a dashboard in Grafana to look at the data you just posted to Influx
        dashboard_name



def main():
    lfjson_host = "localhost"
    lfjson_port = 8080
    endp_types = "lf_udp"
    debug = False

    parser = argparse.ArgumentParser(
        prog='csv_to_influx.py',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''
            ''',

        description='''\
csv_to_influx.py:
--------------------

Summary : 
----------
Copies the data from a CSV file generated by a wifi capacity test to an influx database.

Column names are designed for the KPI file  generated by our Wifi Capacity Test.

A user can of course change the column names to match these in order to input any csv file.

The CSV file needs to have the following columns:
    --date - which is a UNIX timestamp
    --test details - which is the variable being measured by the test
    --numeric-score - which is the value for that variable at that point in time.

Generic command layout:
-----------------------
python .\\csv_to_influx.py


Command:
python3 csv_to_influx.py --influx_host localhost --influx_org Candela --influx_token random_token --influx_bucket lanforge
    --target_csv kpi.csv


        ''')

    influx_add_parser_args(parser)

    # This argument is specific to this script, so not part of the generic influxdb parser args
    # method above.
    parser.add_argument('--target_csv', help='CSV file to record to influx database', default="")
    parser.add_argument('--sep', help='character to split CSV by', default='\t')

    args = parser.parse_args()

    influxdb = RecordInflux(_influx_host=args.influx_host,
                            _influx_port=args.influx_port,
                            _influx_org=args.influx_org,
                            _influx_token=args.influx_token,
                            _influx_bucket=args.influx_bucket)

    csvtoinflux = CSVtoInflux(influxdb=influxdb,
                              target_csv=args.target_csv,
                              _influx_tag=args.influx_tag,
                              sep=args.sep)
    csvtoinflux.post_to_influx()


if __name__ == "__main__":
    main()
