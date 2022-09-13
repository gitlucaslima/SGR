
from datetime import datetime


def isDateMaior(dataInicio,dataFim):

    print(dataFim,dataInicio)
    dadosDataInicio = dataInicio.split("-")
    dadosDataFim = dataFim.split("-")

    dataFormInicio = datetime(int(dadosDataInicio[0]),int(dadosDataInicio[1]),int(dadosDataInicio[2]))
    dataFormFim = datetime(int(dadosDataFim[0]),int(dadosDataFim[1]),int(dadosDataFim[2]))

    return dataFormInicio > dataFormFim

