import os
import json
import shutil
if (not os.path.isdir("Files")):
    os.mkdir("Files")
    os.mkdir("Files/Customers")
    os.mkdir("Files/Customers/Domestic")
    os.mkdir("Files/Customers/Export")
    with open("Files/Customers/Domestic/Domestic_Customers.json","w",encoding="utf-8") as f:
        json.dump({},f)
    with open("Files/Customers/Export/Export_Customers.json","w",encoding="utf-8") as f:
        json.dump({},f)

with open("Files/Customers/Export/Export_Customers.json","r",encoding="utf-8") as f:
    Export_list=json.load(f)
with open("Files/Customers/Domestic/Domestic_Customers.json","r",encoding="utf-8") as f:
    Domestic_list=json.load(f)


def update_export():
    with open("Files/Customers/Export/Export_Customers.json","w",encoding="utf-8") as f:
        json.dump(Export_list,f)
def update_domestic():
    with open("Files/Customers/Domestic/Domestic_Customers.json","w",encoding="utf-8") as f:
        json.dump(Domestic_list,f)
def get_shipments(Customers_name,Customers_type):
    if Customers_type=="i":
        Customers_id=Export_list[Customers_name]
        with open(f"Files/Customers/Export/{Customers_id}/shipments.txt","r",encoding="utf-8") as f:
            shipments=f.readlines()
    elif Customers_type=="y":
        Customers_id=Domestic_list[Customers_name]
        with open(f"Files/Customers/Domestic/{Customers_id}/shipments.txt","r",encoding="utf-8") as f:
            shipments=f.readlines()
    return shipments
def create_new_Customers_dirs(Customers_id,Customers_type):
    if Customers_type=="i":
        os.mkdir(f"Files/Customers/Export/{Customers_id}")
        os.mkdir(f"Files/Customers/Export/{Customers_id}/Documents")
        with open(f"Files/Customers/Export/{Customers_id}/shipments.txt","w",encoding="utf-8") as f:
            f.write("")
    elif (Customers_type=="y"):
        os.mkdir(f"Files/Customers/Domestic/{Customers_id}")
        os.mkdir(f"Files/Customers/Domestic/{Customers_id}/Documents")
        with open(f"Files/Customers/Domestic/{Customers_id}/shipments.txt","w",encoding="utf-8") as f:
            f.write("")
def update_Customers_entries(Customers_id,entry,Customers_type):
    if Customers_type=="i":
        with open(f"Files/Customers/Export/{Customers_id}/shipments.txt","a",encoding="utf-8") as f:
            f.write((entry+"\n"))
    elif (Customers_type=="y"):
        with open(f"Files/Customers/Domestic/{Customers_id}/shipments.txt","a",encoding="utf-8") as f:
            f.write((entry+"\n"))
def open_loc(Customers_id):
    if Customers_id[0]=="i":
        os.system(f"start Files\\Customers\\Export\\{Customers_id}\\Documents")
    elif Customers_id[0]=="y":
        os.system(f"start Files\\Customers\\Domestic\\{Customers_id}\\Documents")
def remove_Customers_files(Customers_id):
    if Customers_id[0]=="i":
        shutil.rmtree(f"Files/Customers/Export/{Customers_id}")
    elif Customers_id[0]=="y":
        shutil.rmtree(f"Files/Customers/Domestic/{Customers_id}")