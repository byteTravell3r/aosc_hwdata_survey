import csv
import requests

PCIeDevInfoTableCSV = "MissingName_PCIe.csv"

newPCIeDevInfoTableCSV = "Searched_MissingName_PCIe.csv"

def SearchInDriversCollection(_VendorID: str, _ProductID: str) -> str:
    SearchAddress = f"https://driverscollection.com/Search/PCI%5CVEN_{_VendorID}%26DEV_{_ProductID}"
    Search = requests.get(url=SearchAddress)
    SearchResult = Search.text
    try:
        SearchResult.index("Nothing found")
        return "-"
    except:
        SearchResult = SearchResult.split("<br />This is Device ID of <b>")[1].split("</b>")[0].split(" - ")[0]
        return SearchResult


def SearchInLinuxHardware(_VendorID: str, _ProductID: str) -> str:
    HeadersWithUA = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    SearchAddress = f"https://linux-hardware.org/?id=pci:{_VendorID}-{_ProductID}"

    GetSuccessfully = False

    while not GetSuccessfully:
        try:
            Search = requests.get(url=SearchAddress, headers=HeadersWithUA)
            GetSuccessfully = True
        except requests.exceptions.SSLError:
            GetSuccessfully = False
            pass

    if Search.status_code != 200:
        return ("-")
    try:
        SearchResult = Search.text.split("Device '")[1].split("'")[0]
        return SearchResult
    except:
        return ("-")


if __name__ == "__main__":

    with open(PCIeDevInfoTableCSV, encoding="utf-8") as TableFile:
        TableContents = TableFile.readlines()

    TableReader = csv.DictReader(TableContents, dialect="excel")

    with open(newPCIeDevInfoTableCSV, mode="w+", encoding="utf-8") as TableFile:
        TableWriter = csv.DictWriter(f=TableFile, dialect="excel", fieldnames=TableReader.fieldnames)
        TableWriter.writeheader()
        for Row in TableReader:
            VendorID = Row.get("VendorID").upper()
            ProductID = Row.get("ProductID").upper()
            print(f"{VendorID}:{ProductID}", end=", ")
            Row["NameInDriversCollection"] = SearchInDriversCollection(VendorID, ProductID)
            print(Row["NameInDriversCollection"], end=", ")
            Row["NameInLinuxHardware"] = SearchInLinuxHardware(VendorID, ProductID)
            print(Row["NameInLinuxHardware"])
            TableWriter.writerow(Row)
            # break
    pass
