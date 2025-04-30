#
# Copyright (c) 1999--2012 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.
#

""" Query hwdata database and return description of vendor and/or device. """


# pylint: disable=misplaced-bare-raise

class USB:
    """ Interface to usb.ids from hwdata package """
    filename = './usb.ids'
    devices = None

    def __init__(self, filename=None):
        """ Load pci.ids from file to internal data structure.
            parameter 'filename' can specify location of this file
        """
        if filename:
            self.filename = filename
        else:
            self.filename = USB.filename
        self.cache = 1

        if self.cache and not USB.devices:
            # parse usb.ids
            USB.devices = {}
            f = open(self.filename, encoding='ISO8859-1')
            lineno = 0
            vendor = None
            device = None
            for line in f.readlines():
                lineno += 1
                l = line.split()
                if line.startswith('#'):
                    if line.startswith('# List of known device classes, subclasses and protocols'):
                        break  # end of database of devices, rest is protocols, types etc.
                    else:
                        continue
                elif len(l) == 0:
                    continue
                elif line.startswith('\t\t'):
                    interface_id = l[0].lower()
                    if len(l) > 2:
                        interface_name = ' '.join(l[1:])
                    else:
                        interface_name = ''
                    try:
                        USB.devices[vendor][1][device][0][interface_id] = interface_name
                    except TypeError:
                        sys.stderr.write("Unknown line at line {0} in {1}.\n".format(lineno, self.filename))
                elif line.startswith('\t'):
                    device = l[0].lower()
                    device_name = ' '.join(l[1:])
                    USB.devices[vendor][1][device] = [device_name, {}]
                else:
                    vendor = l[0].lower()
                    vendor_name = ' '.join(l[1:])
                    if vendor not in USB.devices:
                        USB.devices[vendor] = [vendor_name, {}]
                    else:  # this should not happen
                        USB.devices[vendor][0] = vendor_name

    def get_vendor(self, vendor):
        """ Return description of vendor. Parameter is two byte code in hexa.
            If vendor is unknown None is returned.
        """
        vendor = vendor.lower()
        if self.cache:
            if vendor in USB.devices:
                return USB.devices[vendor][0]
            else:
                return None
        else:
            raise NotImplementedError()

    def get_device(self, vendor, device):
        """ Return description of device. Parameters are two byte code variables in hexa.
            If device is unknown None is returned.
        """
        vendor = vendor.lower()
        device = device.lower()
        if self.cache:
            if vendor in USB.devices:
                if device in USB.devices[vendor][1]:
                    return USB.devices[vendor][1][device][0]
                else:
                    return None
            else:
                return None
        else:
            raise NotImplementedError()


class PCI:
    """ Interface to pci.ids from hwdata package """
    filename = './pci.ids'
    devices = None

    def __init__(self, filename=None):
        """ Load pci.ids from file to internal data structure.
            parameter 'filename' can specify location of this file
        """
        if filename:
            self.filename = filename
        else:
            self.filename = PCI.filename
        self.cache = 1

        if self.cache and not PCI.devices:
            # parse pci.ids
            PCI.devices = {}
            f = open(self.filename, encoding='ISO8859-1')
            vendor = None
            device = None
            for line in f.readlines():
                l = line.split()
                if line.startswith('#'):
                    continue
                elif len(l) == 0:
                    continue
                elif line.startswith('\t\t'):
                    subsystem = '{0}:{1}'.format(l[0].lower(), l[1].lower())
                    subsystem_name = ' '.join(l[2:])
                    PCI.devices[vendor][1][device][1][subsystem] = subsystem_name
                elif line.startswith('\t'):
                    device = l[0].lower()
                    device_name = ' '.join(l[1:])
                    PCI.devices[vendor][1][device] = [device_name, {}]
                else:
                    vendor = l[0].lower()
                    vendor_name = ' '.join(l[1:])
                    if not vendor in list(PCI.devices.keys()):
                        PCI.devices[vendor] = [vendor_name, {}]
                    else:  # this should not happen
                        PCI.devices[vendor][0] = vendor_name

    def get_vendor(self, vendor):
        """ Return description of vendor. Parameter is two byte code in hexa.
            If vendor is unknown None is returned.
        """
        vendor = vendor.lower()
        if self.cache:
            if vendor in list(PCI.devices.keys()):
                return PCI.devices[vendor][0]
            else:
                return None
        else:
            raise NotImplementedError()

    def get_device(self, vendor, device):
        """ Return description of device. Parameters are two byte code variables in hexa.
            If device is unknown None is returned.
        """
        vendor = vendor.lower()
        device = device.lower()
        if self.cache:
            if vendor in list(PCI.devices.keys()):
                if device in list(PCI.devices[vendor][1].keys()):
                    return PCI.devices[vendor][1][device][0]
                else:
                    return None
            else:
                return None
        else:
            raise NotImplementedError()

    def get_subsystem(self, vendor, device, subsystem):
        """ Return description of subsystem.
            'vendor' and 'device' are two byte code variables in hexa.
            'subsystem' is two colon separated hexa values.
            If subsystem is unknown None is returned.
        """
        vendor = vendor.lower()
        device = device.lower()
        subsystem = subsystem.lower()
        if self.cache:
            if vendor in list(PCI.devices.keys()):
                if device in list(PCI.devices[vendor][1].keys()):
                    if subsystem in list(PCI.devices[vendor][1][device][1].keys()):
                        return PCI.devices[vendor][1][device][1][subsystem]
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            raise NotImplementedError()


import time
import urllib.request
from urllib.error import URLError

from utils import *


def update_hwdata() -> bool:
    pci_ids_link = "https://pci-ids.ucw.cz/v2.2/pci.ids"
    usb_ids_link = "http://www.linux-usb.org/usb.ids"
    success = True
    downloaded = False  # 用于跟踪是否有文件被实际下载

    def need_download(file_path: str) -> bool:
        """检查文件是否需要下载"""
        if not os.path.exists(file_path):
            return True
        # 计算文件最后修改时间距今是否超过2小时（7200秒）
        return (time.time() - os.path.getmtime(file_path)) > 7200

    # 下载PCI ID列表
    pci_file = "./pci.ids"
    if need_download(pci_file):
        try:
            print_info("正在下载 PCI IDs...")
            urllib.request.urlretrieve(pci_ids_link, pci_file)
            downloaded = True
        except URLError as e:
            print_warn(f"PCI IDs 下载失败: {e.reason}")
            success = False

    # 下载USB ID列表
    usb_file = "./usb.ids"
    if need_download(usb_file):
        try:
            print_info("正在下载 USB IDs...")
            urllib.request.urlretrieve(usb_ids_link, usb_file)
            downloaded = True
        except URLError as e:
            print_warn(f"USB IDs 下载失败: {e.reason}")
            success = False

    # 最终状态反馈
    if downloaded and success:
        print_info("设备数据库全部更新完毕!")
    elif success:
        print_info("设备数据库已经是最新的. 若要重新获取, 请删除项目目录下已有的文件.")

    return success
