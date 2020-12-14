#!/usr/bin/env python3

import csv
import re
import sys


def generate_pattern(service):
    result = r"" + service + ": ([A-Z]+) ([\w+ ]+ .*) \(([\w.]+)\)"
    return result


def service_in_line(service, line):
    pattern = generate_pattern(service)
    result = re.search(pattern, line)
    return result


def dict_updater(user_dict, error_dict, message):
    log_type = message.group(1)
    log_message = message.group(2)
    log_user = message.group(3)
    if log_user not in user_dict:
        user_dict[log_user] = [0, 0]
    if log_type == "ERROR":
        user_dict[log_user][1] += 1
        if log_message not in error_dict:
            error_dict[log_message] = 0
        error_dict[log_message] += 1
    if log_type == "INFO":
        user_dict[log_user][0] += 1


def from_file_to_dict(log_file, service_name):
    user_dict1 = {}
    error_dict1 = {}
    with open(log_file) as file:
        for line in file:
            message = service_in_line(service_name, line)
            if message is not None:
                dict_updater(user_dict1, error_dict1, message)
    return user_dict1, error_dict1


def generate_csv(errors_dict, users_dict):
    with open("user_statistics.csv", "w", newline="") as user_file:
        writer = csv.writer(user_file)
        writer.writerow(["User_name", "INFO", "ERROR"])
        for key, value in sorted(users_dict.items()):
            writer.writerow([key, value[0], value[1]])
    with open('error_message.csv', 'w', newline="") as error_file:
        writer = csv.writer(error_file)
        writer.writerow(['Error', 'Count'])
        for key, value in sorted(errors_dict.items()):
            writer.writerow([key, value])
    return error_file, user_file


if __name__ == "__main__":
    logfile = "C:/Users/David/PycharmProjects/pythonProject10/syslog.log"
    user_dict, error_dict = from_file_to_dict(logfile, "ticky")
    error_csv, user_csv = generate_csv(error_dict, user_dict)
