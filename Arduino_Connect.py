#Библиотеки
from PyQt5 import QtWidgets, uic

from PyQt5.QtCore import QIODevice

# Импортируем библиотеки для работы с ком портом
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

#принтую свои функции
from Python.Rundom_Funncion import print_bebra,print_niggers


app = QtWidgets.QApplication([])
ko = uic.loadUi("Dizain.ui")
ko.setWindowTitle("SerialGUI")

#создаем объект сериал и объект порт
serial = QSerialPort()
serial.setBaudRate(57600)
portlist = []
ports = QSerialPortInfo().availablePorts()

#перебираем название портов
for port in ports:
  portlist.append(port.portName())
print(portlist)

#открыть порт присваиваем имя порта из исписка и открываем для записи и чтения
def OpenPort():
  serial.setPortName(ko.PortListComboBox.currentText())
  serial.open(QIODevice.ReadWrite)
  print("connect Niccee")

#закрываем порт
def ClosePort():
  serial.close()
  print("unconnect Niccee")

#Читаем строку с стринга
def ReadSerial():
  mass_simbols = serial.readLine()
  mass_simbols_str = str(mass_simbols, 'utf-8').strip()
  StR = mass_simbols_str.split(',')
  if StR[0] == '0':
    ko.ProgressBar.setValue(int(StR[3]))
    ko.TextTemp.setValue(int(StR[3]))
    print(StR[3])



def ledControl(val):
  print(val)

def fanControl(val):
  print(val)

def blabControl(val):
  print(val)

#отправляем сообщение
def SerialSend(data):
  txs =""
  for val in data:
    txs += str(val)
    txs += ','
  txs =txs[:-1]
  txs +=';'
  serial.write(txs.encode())
  print(txs)
#
def RGBControl():
  SerialSend(1,ko.RGBSlider_R.value(),ko.RGBSlider_B.value(),ko.RGBSlider_G.value())
  print('RGBConrol-ok',1,ko.RGBSlider_R.value(),ko.RGBSlider_B.value(),ko.RGBSlider_G.value())
#
def ServoControl():
  SerialSend([2,ko.dial.value()])

def SendText():
  txs = "5, "
  txs += ko.textF.displayText()
  txs += ';'
  serial.write(txs.encode())

serial.readyRead.connect(ReadSerial)

#добавляем в комбобокс все порты
ko.PortListComboBox.addItems(portlist)
#по клику на PortListComboBox вызываем функцию 
ko.PortListComboBox.currentIndexChanged.connect(print_bebra)
#при нажатии на кнопку вызываем функцию открытия порта
ko.OpenPortButton.clicked.connect(OpenPort)
#при нажатии на кнопку вызываем функцию pfкрытия порта
ko.ClosePortButton.clicked.connect(ClosePort)

#при нажатии на галочку вызываем функцию
ko.RGBSlider_R.valueChanged.connect(RGBControl)
#при нажатии на галочку вызываем функцию
ko.RGBSlider_G.valueChanged.connect(RGBControl)
#при нажатии на галочку вызываем функцию
ko.RGBSlider_B.valueChanged.connect(RGBControl)

ko.dial.valueChanged.connect(ServoControl)

#пр изменени
vals = [10,11,12]
SerialSend(vals)

ko.show()
app.exec()
