import requests

from utils import *


def search_pci_driverscollection(_pci_id: str) -> str:
    _VendorID = _pci_id[0:4]
    _ProductID = _pci_id[5:9]
    search_address = f"https://driverscollection.com/Search/PCI%5CVEN_{_VendorID}%26DEV_{_ProductID}"
    get_successfully = False

    while not get_successfully:
        try:
            search = requests.get(url=search_address)
            get_successfully = True
        except:
            get_successfully = False
            print_warn(_pci_id + " 查询失败, 正在重试...")
            pass

    search_result = search.text
    try:
        search_result.index("Nothing found")
        # print_data("未找到 " + _pci_id + " 的名称.")
        return "-"
    except:
        search_result = search_result.split("<br />This is Device ID of <b>")[1].split("</b>")[0].split(" - ")[0]
        # print_data("找到了 " + _pci_id + " 的名称: \"" + search_result + "\"")
        return search_result


def search_usb_driverscollection(_usb_id: str) -> str:
    _VendorID = _usb_id[0:4]
    _ProductID = _usb_id[5:9]
    search_address = f"https://driverscollection.com/Search/USB%5CVID_{_VendorID}%26PID_{_ProductID}"
    get_successfully = False

    while not get_successfully:
        try:
            search = requests.get(url=search_address)
            get_successfully = True
        except:
            get_successfully = False
            print_warn(_usb_id + " 查询失败, 正在重试...")
            pass

    search_result = search.text

    try:
        search_result.index("Nothing found")
        return "-"
    except:
        search_result = search_result.split("<br />This is Device ID of <b>")[1].split("</b>")[0].split(" - ")[0]
        return search_result


def search_pci_linuxhardware(_pci_id: str) -> str:
    _VendorID = _pci_id[0:4]
    _ProductID = _pci_id[5:9]
    headers_with_ua = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    search_address = f"https://linux-hardware.org/?id=pci:{_VendorID}-{_ProductID}"

    get_successfully = False

    while not get_successfully:
        try:
            search = requests.get(url=search_address, headers=headers_with_ua)
            get_successfully = True
        except requests.exceptions.SSLError:
            print_warn(_pci_id + " 查询失败, 正在重试...")
            get_successfully = False
            pass

    if search.status_code != 200:
        # print_data("未找到 " + _pci_id + " 的名称.")
        return ("-")
    try:
        search_result = search.text.split("Device '")[1].split("'")[0]
        # print_data("找到了 " + _pci_id + " 的名称: \"" + search_result + "\"")
        return search_result
    except:
        # print_data("未找到 " + _pci_id + " 的名称.")
        return ("-")


def search_usb_linuxhardware(_usb_id: str) -> str:
    _VendorID = _usb_id[0:4]
    _ProductID = _usb_id[5:9]
    headers_with_ua = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    search_address = f"https://linux-hardware.org/?id=usb:{_VendorID}-{_ProductID}"
    # print(search_address)
    get_successfully = False

    while not get_successfully:
        try:
            search = requests.get(url=search_address, headers=headers_with_ua)
            get_successfully = True
        except requests.exceptions.SSLError:
            print_warn(_usb_id + " 查询失败, 正在重试...")
            get_successfully = False
            pass

    if search.status_code != 200:
        return ("-")
    try:
        search_result = search.text.split("Device '")[1].split("'")[0]
        return search_result
    except:
        return ("-")


def search_pci_treexy(_usb_id: str) -> str:
    _VendorID = _usb_id[0:4]
    _ProductID = _usb_id[5:9]
    headers_with_ua = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    search_address = f"https://treexy.com/products/driver-fusion/database/id/pci/ven_{_VendorID}/dev_{_ProductID}/"

    get_successfully = False

    while not get_successfully:
        try:
            search = requests.get(url=search_address, headers=headers_with_ua)
            get_successfully = True
        except requests.exceptions.SSLError:
            print_warn(_usb_id + " 查询失败, 正在重试...")
            get_successfully = False
            pass

    if search.status_code != 200:
        return ("-")

    search_result_set = set()
    search_result_raw = search.text.splitlines()

    # print(search_result_raw)

    for line in search_result_raw:
        if line.find("<a href=\"/products/driver-fusion/database") != -1:
            search_result_set.add(line.split("/\">")[1].split("</a>")[0])
        if line.find("Collections") != -1:
            return ("-")

    if len(search_result_set) == 0:
        return ("-")

    if len(search_result_set) == 1:
        return list(search_result_set)[0]

    if len(search_result_set) > 1:
        return str(search_result_set)


def search_usb_treexy(_usb_id: str) -> str:
    _VendorID = _usb_id[0:4]
    _ProductID = _usb_id[5:9]
    headers_with_ua = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    search_address = f"https://treexy.com/products/driver-fusion/database/id/usb/vid_{_VendorID}/pid_{_ProductID}/"
    # print(search_address)
    get_successfully = False

    while not get_successfully:
        try:
            search = requests.get(url=search_address, headers=headers_with_ua)
            get_successfully = True
        except requests.exceptions.SSLError:
            print_warn(_usb_id + " 查询失败, 正在重试...")
            get_successfully = False
            pass

    if search.status_code != 200:
        return ("-")

    search_result_set = set()
    search_result_raw = search.text.splitlines()

    # print(search_result_raw)

    is_a_specific_driver = False
    next_line_is_name = False
    next_line_is_manufacturer = False

    for line in search_result_raw:
        if line.find("<a href=\"/products/driver-fusion/database") != -1:
            search_result_set.add(line.split("/\">")[1].split("</a>")[0])
        if line.find("Collections") != -1:
            return ("-")

        if next_line_is_name:
            next_line_is_name = False
            name = line.split("<div>")[1].split("</div>")[0].strip()

        if next_line_is_manufacturer:
            next_line_is_manufacturer = False
            manufacturer = line.split("<div>")[1].split("</div>")[0].strip()

        if line.find("Name</h3>") != -1:
            is_a_specific_driver = True
            next_line_is_name = True

        if line.find("Manufacturer</h3>") != -1:
            next_line_is_manufacturer = True

    if is_a_specific_driver:
        search_result_set.add(manufacturer + " " + name)

    if len(search_result_set) == 0:
        return ("-")

    if len(search_result_set) == 1:
        return list(search_result_set)[0]

    if len(search_result_set) > 1:
        return str(search_result_set)


if __name__ == "__main__":
    ret = search_usb_treexy("13d3:3548")
    print(ret)
