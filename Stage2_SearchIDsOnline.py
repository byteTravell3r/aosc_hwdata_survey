from concurrent.futures import ThreadPoolExecutor
import openpyxl

from utils import *
from online_info_checker import search_pci_linuxhardware, search_pci_driverscollection

hwdata_excel_file = "hwdata.xlsx"

hwdata_workbook = openpyxl.load_workbook(hwdata_excel_file)
hwdata_pcie_sheet = hwdata_workbook["整理后的PCIe数据"]
hwdata_usb_sheet = hwdata_workbook["整理后的USB数据"]

pcie_data_list = list(hwdata_pcie_sheet.columns)[0]
usb_data_list = list(hwdata_usb_sheet.columns)[0]
hwdata_workbook.close()

# 创建两个字典(用于多线程)
pcie_name_on_linuxhardware_dict = dict()
pcie_name_on_driverscollection_dict = dict()

for block in pcie_data_list:
    pci_id = block.value
    pcie_name_on_linuxhardware_dict[pci_id] = "检索中..."
    pcie_name_on_driverscollection_dict[pci_id] = "检索中..."

def search_pci_linuxhardware_and_save(pci_id: str) -> None:
    result = search_pci_linuxhardware(pci_id)
    pcie_name_on_linuxhardware_dict[pci_id] = result

def search_pci_driverscollection_and_save(pci_id: str) -> None:
    result = search_pci_driverscollection(pci_id)
    pcie_name_on_driverscollection_dict[pci_id] = result

clear_screen()

with ThreadPoolExecutor(max_workers=8) as executor:
    for pci_id in pcie_name_on_linuxhardware_dict:
        executor.submit(search_pci_linuxhardware_and_save, pci_id)
    executor.shutdown(wait=True)

clear_screen()

useful_data_count = 0
for pci_id, dev_name in pcie_name_on_linuxhardware_dict.items():
    if dev_name != "-" and dev_name != "检索中...":
        useful_data_count += 1

print_info(f"已完成在 LinuxHardware.org 上的信息检索. 找到 {useful_data_count} 条有效信息, " +
           f"有 {len(pcie_name_on_linuxhardware_dict) - useful_data_count} 条未知.")

with ThreadPoolExecutor(max_workers=8) as executor:
    for pci_id in pcie_name_on_driverscollection_dict:
        executor.submit(search_pci_driverscollection_and_save(), pci_id)
    executor.shutdown(wait=True)

useful_data_count = 0
for pci_id, dev_name in pcie_name_on_driverscollection_dict.items():
    if dev_name != "-" and dev_name != "检索中...":
        useful_data_count += 1

print_info(f"已完成在 DriversCollection 上的信息检索. 找到 {useful_data_count} 条有效信息, " +
           f"有 {len(pcie_name_on_driverscollection_dict) - useful_data_count} 条未知.")

