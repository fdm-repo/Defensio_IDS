from datetime import datetime

class log_event:
    def crealog(self,id_process, oggetto):
        f = open("logs/"+id_process + ".txt", "a")
        datetime_event = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        descrizione_evento = oggetto
        f.write("\n"+datetime_event + " | " + descrizione_evento)
        f.close()

        f = open("logs/"+id_process + ".txt", "r")
        size = len(f.readlines())
        f.close()

        if size > 1000:
            with open("logs/" + id_process + ".txt", 'r+') as fp:
                # read an store all lines into list
                lines = fp.readlines()
                # move file pointer to the beginning of a file
                fp.seek(0)
                # truncate the file
                fp.truncate()

                # start writing lines except the first line
                # lines[1:] from line 2 to last line
                fp.writelines(lines[1:])
            fp.close()