#!/bin/python
import subprocess
import fileinput


packages = ['postgresql-9.2', 'postgresql-contrib', 'postgresql-server']


def rpm_qa_package(package):
    args1 = ["rpm", "-qa"]
    args2 = ["grep", package]
    rpm = subprocess.Popen(args1, stdout=subprocess.PIPE)
    grep = subprocess.Popen(args2, stdin=rpm.stdout, stdout=subprocess.PIPE)
    rpm.stdout.close()
    output = grep.communicate()[0].rstrip()
    rpm.wait()
    output_length = len(output)
    if (output_length != 0):
        return output


def rpm_qa_packages(array):
    qa_list = []
    install_list = []
    return_list = [qa_list, install_list]
    for item in array:
        package = rpm_qa_package(item)
        package_type = type(package)
        if (package_type is str):
            qa_list.append(package)
        else:
            install_list.append(item)
    return return_list


def yum_package_install(package):
    args1 = ["yum", "install", "-y", package]
    yum = subprocess.Popen(args1, stdout=subprocess.PIPE)
    output = yum.communicate()[0]
    return output


def install_packages(packages):
    package_list = rpm_qa_packages(packages)
    un = len(package_list[1])
    if (un != 0):
        for package in package_list[1]:
            yum_package_install(package)
    return package_list[1]


def ident_md5():
    edits = []
    for line in fileinput.input(
        "/var/lib/pgsql/data/pg_hba.conf", inplace=True
    ):
        print(line)
    return


def init_database():
    args1 = ["postgresql-setup", "initdb"]
    postgresql_setup = subprocess.Popen(args1, stdout=subprocess.PIPE)
    output = postgresql_setup.communicate()[0]
    return output


def main(packages):
    install_packages(packages)
    database = init_database()
    print database


check = ident_md5()
print check
