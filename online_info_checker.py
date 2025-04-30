import requests

from utils import *


def search_pci_driverscollection(_pci_id: str) -> str:
    _VendorID = _pci_id[0:4]
    _ProductID = _pci_id[5:9]
    print_info("在 DriversCollection 网站上查询: " + _pci_id)
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
        print_info("未找到 " + _pci_id + " 的名称.")
        return "-"
    except:
        search_result = search_result.split("<br />This is Device ID of <b>")[1].split("</b>")[0].split(" - ")[0]
        print_info("找到了 " + _pci_id + " 的名称: \"" + search_result + "\"")
        return search_result


def search_pci_linuxhardware(_pci_id: str) -> str:
    _VendorID = _pci_id[0:4]
    _ProductID = _pci_id[5:9]
    print_info("在 LinuxHardware.org 网站上查询: " + _pci_id)
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
        print_info("未找到 " + _pci_id + " 的名称.")
        return ("-")
    try:
        search_result = search.text.split("Device '")[1].split("'")[0]
        print_info("找到了 " + _pci_id + " 的名称: \"" + search_result + "\"")
        return search_result
    except:
        print_info("未找到 " + _pci_id + " 的名称.")
        return ("-")
