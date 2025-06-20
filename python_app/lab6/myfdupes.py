import sys
import os
from pathlib import Path
import hashlib

key = ["-r", "--help"]
listdubl = []

def sorted_to_bytes(files):
    all_dubl_group = []
    for dubl in files:
        dubl_files = []
        checked = set()
        for i in range(len(dubl)-1):
            for j in range(i+1, len(dubl)):
                file1, file2 = dubl[i], dubl[j]
                if (file1, file2) in checked or (file2, file1) in checked:
                    continue
                if compare_files(file1, file2):
                    added = False
                    for group in dubl_files:
                        if file1 in group or file2 in group:
                            group.update([file1, file2])
                            added = True
                            break
                    if not added:
                        dubl_files.append(set([file1, file2]))
                checked.add((file1, file2))
        if dubl_files:
            all_dubl_group.extend(dubl_files)
    return [list(group) for group in all_dubl_group]

def compare_files(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        while True:
            b1 = f1.read(1)
            b2 = f2.read(1)

            if not b1 and not b2:
                return True
            if b1 != b2:
                return False

def calculate_md5(files):
    hash_dubl = []
    for dubl in files:
        hash_file = []
        for file in dubl:
            hash_md5 = hashlib.md5()
            with open(file, "rb") as f:
                hash_md5 = hashlib.md5(f.read())
            hash_file.append(hash_md5.hexdigest())
        hash_dubl.append(hash_file)
    return hash_dubl

def sorted_to_hash(files):
    hash_dubl = calculate_md5(files)
    dubl_to_hash = []
    dubl_to_hash1 = []
    for i in range(len(hash_dubl)):
        dubl_to_hash.append(sorted_(files[i], hash_dubl[i]))
    for arr_dubl in dubl_to_hash:
        if len(arr_dubl) != 0:
            for dubl in arr_dubl:
                dubl_to_hash1.append(dubl)
    return dubl_to_hash1

def sorted_(files, param):
    dubl_to_param = []
    dubl_to_param1 = []
    sorted_files_to_param = sorted(zip(param, files))
    sorted_param, sorted_files = zip(*sorted_files_to_param)
    subdubl_files = [sorted_files[0]]

    for i in range(1, len(sorted_param)):
        if sorted_param[i] == sorted_param[i-1]:
            subdubl_files.append(sorted_files[i])
        else:
            dubl_to_param.append(subdubl_files)
            subdubl_files = [sorted_files[i]]
    dubl_to_param.append(subdubl_files)

    for i in range(len(dubl_to_param)):
        if len(dubl_to_param[i]) > 1:
            dubl_to_param1.append(dubl_to_param[i])
    return dubl_to_param1
    
def search(path, key):
    size = []
    search_to_size = []
    if not(os.path.exists(path)) or os.path.isfile(path):
        return 
    elif not(os.listdir(path)):
        return "zero"
    else:
        if key == "nokey":
            fil = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            files = []
            for f in fil:
                files.append((path +'/' + f))
        else:
            directory = Path(path)
            files = [str(file) for file in directory.rglob("*") if file.is_file()]
        for file in files:
            size.append(os.path.getsize(file))
        if len(size) == len(set(size)):
            return []
        else:
            dubl_to_size = sorted_(files, size)
            dubl_to_hash = sorted_to_hash(dubl_to_size)
            dublicate = sorted_to_bytes(dubl_to_hash)
            if dublicate == None:
                return []
            else:
                return dublicate

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Ошибка: неверное количество аргументов")
    else:
        if sys.argv[1] == key[1]:
            print(" Программа по умолчанию сравнивает файлы только в указанной директории.\n", "Если вам нужно также проверить файлы во всех подкаталогах, то используйте ключ '-r'.\n","Если вам нужна информация по всем ключам используйте ключ '--help'.")
            return
        elif sys.argv[1] == key[0]:
            path = sys.argv[2]
            listdubl = search(path, key)
        else:
            path = sys.argv[1]
            listdubl = search(path, "nokey")

        if listdubl == None:
            print("Ошибка: каталог не найден")
        elif listdubl == "zero" :
            print("Каталог пуст")
        elif listdubl == []:
            print("Дубликаты не найдены")
        else:
            for dubl in listdubl:
                print("Найдена новая группа дубликатов:\n")
                for i in range(len(dubl)):
                    print("[", i, "]", dubl[i])
                print("\n Выберите индекс файла, который хотите сохранить(через запятые!)")
                answear = input()
                if answear == "":
                    continue
                else:
                    variants = answear.split(",")
                    for i in range(len(dubl)):
                        if not(str(i) in variants):
                            os.remove(dubl[i])

                

if __name__ == "__main__":
    main()
