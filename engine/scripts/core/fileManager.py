import csv
""" from engine.scripts.datablock import Datablock """ ## rewrite to use multiple .extensions (ntd, nbd, nid - text, binary, image)

class FileManager():

    @staticmethod
    def save_to_file(file_name: str, data):
        with open(file_name + ".ntd", "w", newline="") as to_write: # ntd = Nebula Text Data
            writer = csv.writer(to_write)

            print(type(data).__name__)

            if type(data).__name__ == "str":
                writer.writerow(["str"])
                try: writer.writerow([data])
                except: print(f"{__name__}: couldn't write data to file '{file_name}' (type: str)")

            elif type(data).__name__ == "float":
                writer.writerow(["int_float"])
                try: writer.writerow([str(data)])
                except: print(f"{__name__}: couldn't write data to file '{file_name}' (type: int | float)")

            elif type(data).__name__ == "list":
                writer.writerow(["list"])
                try: writer.writerow(data)
                except: print(f"{__name__}: couldn't write data to file '{file_name}' (type: list)")

            elif type(data).__name__ == "dict": # dict writer? dict reader????
                fieldnames = [i for i in data]
                writer = csv.DictWriter(to_write, fieldnames=fieldnames)
                try:
                    writer.writeheader()
                    writer.writerows([data])
                except: print(f"{__name__}: couldn't write data to file '{file_name}' (type: dict)")

            else:
                print(f"{__name__}: couldn't write data to file '{file_name}' (unsupported data type: {type(data).__name__})")


    @staticmethod
    def read_from_file(file_name: str):
        with open(file_name + ".ntd", "r") as to_read:
            reader = csv.reader(to_read)

            if reader[0] == "str":
                return reader[1]
            
            elif reader[0] == "int_float":
                return float(reader[1])
            
            elif reader[0] == "list":
                temp_list = []
                for i in reader:
                    temp_list.append(i)

                return temp_list
            
            elif reader[0] == "dict":
                temp_dict = {}
                dict_reader = csv.DictReader(to_read)
                for i in dict_reader: print(i)
                return temp_dict