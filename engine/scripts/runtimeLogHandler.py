class LogHandler:
    def __init__(self) -> None:
        self.current_log = []

    def add_to_log(self, message):
        self.current_log.append(message)

    def print_log(self):
        if len(self.current_log) > 0:
            latest_log = self.sum_log()
            self.join_log()

            print(latest_log)

            self.clear_log()

    def sum_log(self):
        summed_log = ""
        curr_item_count = 0

        for i in range(len(self.current_log)):
            try:
                if self.current_log[i] == self.current_log[i+1]:
                    curr_item_count += 1
            except:
                if curr_item_count == 0:
                    summed_log += f"{self.current_log[i]}"
                    curr_item_count = 0 # safety
                else:
                    summed_log += f"{self.current_log[i]} ({curr_item_count + 1}x)\n"
                    curr_item_count = 0

        return summed_log

    def join_log(self):
        pass

    def dump_log(self):
        pass # could eventually dump all the log data into a file

    def clear_log(self):
        self.current_log.clear()