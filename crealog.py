from datetime import datetime

class log_event:
    def crealog(self,id_process, oggetto):
        f = open("logs/"+id_process + ".txt", "a")
        datetime_event = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        descrizione_evento = oggetto
        f.write("\n"+datetime_event + " | " + descrizione_evento)
        f.close()