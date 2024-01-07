class TableOfRecords:
    """
    класс таблица рекордов
    """
    def __init__(self, filename):
        self.filename = filename
        self.records = []  
        file_content = None  
        try:  
            with open(self.filename, 'r', encoding="utf-8") as file:  
                file_content = file.read()  
        except FileNotFoundError:  
            self.table_of_cors = False  
        else:  
            if file_content:  
                self.records.extend(self.parse_content(file_content))  
                self.table_of_cors = True

    def parse_content(self, content) -> list:
        """записывает рекорды из текстового файла в лист как словарь"""
        content = content.split('\n')
        return_list = []
        for item in content:
            if item != "":
                list_NP = item.split(":")
                return_list.append(
                    {'name': list_NP[0], 'points': list_NP[1]}
                    )  
        return return_list
    
    def add_record(self, record) -> None:
        """создание нового рекорда"""
        if not any(
            record['name'] == old_record['name'] for old_record in self.records
            ):
            self.records.append(record)
        else:
            old_record = next(
                old_rec for old_rec in self.records 
                if old_rec['name'] == record['name']
                )
            if int(old_record['points']) < int(record['points']):
                self.records[self.records.index(old_record)] = record
            else:
                print("извините но старый рекорд был лучше")
                return
        print("новый рекорд был успешно добавлен!")

    def write_records_to_file(self) -> None:
        """перезаписывает текстовый файл"""
        with open(self.filename, 'w', encoding="utf-8") as f:
            for record in self.records:
                name, points = record["name"], record["points"]
                f.write(f"{name}:{points}\n")

    def show_scores(self) -> None:
        """показывает текущие рекорды"""
        for score in self.records:
            print(f"Имя: {score['name']}, рекорд: {score['points']}")

    def sorted_scores(self) -> None:
        """сортировка рекордов по их убыванию"""
        self.records = sorted(self.records, key=lambda x: -(int(x['points'])))

    def compare_records(self, new_score):
        """сравнивает набранные очки со старыми"""
        if len(self.records) < 10:
            return True
        else:
            self.sorted_scores()
            if new_score > self.records[9]:
                self.records.pop(9)
                return True
            else:
                return False
