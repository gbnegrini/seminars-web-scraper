class Log:
    file = None

    def __init__(self):
        pass

    def create(self):
        """Creates a .txt file for logging"""
        try:
            # the filename is the current system time
            file_name = self.get_time().replace(":", "-").replace(" ", "_")

            # checks if a log folder exists, if it doesn't then creates one
            import os
            directory = 'logs'
            if not os.path.exists(directory):
                os.makedirs(directory)

            # creates a log file
            self.file = open("logs/{0}.txt".format(file_name), "w")
            self.write("Log file created")

        except Exception as error:
            print(error)

    def close(self):
        """Closes the file object"""
        try:
            self.file.close()
        except Exception as error:
            print(error)

    def get_time(self):
        """Gets the current system time"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    def write(self, log):
        """Writes a log entry"""
        try:
            self.file.write(">> " + self.get_time())
            self.file.write("\n" + log)
            self.file.write("\n----------------------------------\n")
        except TypeError as error:
            print("ERROR: .write(log=) argument " + error.__str__())