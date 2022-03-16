#Библиотеки
from PyQt5 import QtWidgets, uic

# Импортируем библиотеки для работы с ком портом
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

#принтую свои функции
from Python.Rundom_Funncion import print_bebra


app = QtWidgets.QApplication([])
ko = uic.loadUi("Dizain.ui")
ko.setWindowTitle("SerialGUI")

#создаем объект сериал и объект порт
serial = QSerialPort()
serial.setBaudRate(115200)
portlist = []
ports = QSerialPortInfo().availablePorts()

#перебираем название портов
for port in ports:
  portlist.append(port.portName())
print(portlist)

#добавляем в комбобокс все порты
ko.PortListComboBox.addItems(portlist)

ko.PortListComboBox.currentIndexChanged.connect(print_bebra)


ko.show()
app.exec()
