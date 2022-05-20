# Библиотеки
from PyQt5 import QtWidgets, uic

from PyQt5.QtCore import QIODevice

# Импортируем библиотеки для работы с ком портом
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
#Методы для работы с ардуино
from  Python.Metods_for_VNA import Metods_Ports_For_Arduino

#Методы для работы с ардуино
from  Python.Command_for_VNA import Command_for_VNA

s = Metods_Ports_For_Arduino()
b = Command_for_VNA()
app = QtWidgets.QApplication([])
ko = uic.loadUi(r"C:/Users/tor/Desktop/Проект прога/Programm_VNA/Interface_for_TRVNA/Dizain.ui")
print(type(ko))
ko.setWindowTitle("SerialGUI")

# добавляем в комбобокс все порты
ko.PortListComboBox.addItems(s.Get_info_about_portlist())


print(s.Get_info_about_portlist())

# по клику на PortListComboBox вызываем функцию проверка на нажатие
ko.PortListComboBox.currentIndexChanged.connect(print_bebra)

# при нажатии на кнопку вызываем функцию открытия порта
ko.OpenPortButton.clicked.connect(lambda: s.OpenPortByComboBox(ko))  #ээээ как это делать ko.OpenPortButton.clicked.connect(lambda x: s.OpenPort(ko))

#если в порт поступли сообщения, то читаем их
s.serial.readyRead.connect(lambda: s.ReadSerial(ko))

# при нажатии на кнопку вызываем функцию окрытия порта
ko.ClosePortButton.clicked.connect(s.ClosePort)

# при нажатиии отправляем в порт текст из строчки
ko.SendButton.clicked.connect(lambda: s.SerialSend(ko.SendTextWindow.displayText()))

# при нажатии подключаемся к ардуино
ko.ArduinoConnectButton.clicked.connect(lambda: s.Arduino_Connect(ko))

ko.VNA_Button.clicked.connect(lambda: b.Start_VNA())
# при нажатии на галочку вызываем функцию
# ko.RGBSlider_R.valueChanged.connect(RGBControl)
# # при нажатии на галочку вызываем функцию
# ko.RGBSlider_G.valueChanged.connect(RGBControl)
# # при нажатии на галочку вызываем функцию
# ko.RGBSlider_B.valueChanged.connect(RGBControl)
# ko.dial.valueChanged.connect(ServoControl)


ko.show()
app.exec()
