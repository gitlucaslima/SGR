
from datetime import date, datetime


def isDateMaior(dataInicio,dataFim):

    print(dataFim,dataInicio)
    dadosDataInicio = dataInicio.split("-")
    dadosDataFim = dataFim.split("-")

    dataFormInicio = datetime(int(dadosDataInicio[0]),int(dadosDataInicio[1]),int(dadosDataInicio[2]))
    dataFormFim = datetime(int(dadosDataFim[0]),int(dadosDataFim[1]),int(dadosDataFim[2]))

    return dataFormInicio > dataFormFim


def isDatePassou(data):

    print(data)
    print(date(datetime.now().year,datetime.now().month,datetime.now().day))
    return data > date(datetime.now().year,datetime.now().month,datetime.now().day)

  
  