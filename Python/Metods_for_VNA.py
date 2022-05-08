# Библиотеки
from PyQt5 import QtWidgets, uic

from PyQt5.QtCore import QIODevice

# Импортируем библиотеки для работы с ком портом
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class MetodsPorts:
    def __init__(self):
        """создаю сериал порт"""
        self.serial = QSerialPort()
        self.serial.setBaudRate(57600)
        self.portlist = []
        ports = QSerialPortInfo().availablePorts()
        '''ищу порты'''
        for port in ports:
            self.portlist.append(port.portName())

    def OpenPort(self, uci_modul):
        self.serial.setPortName(uci_modul.PortListComboBox.currentText())
        self.serial.open(QIODevice.ReadWrite)
        print("открыл порт")
        return

    def ClosePort(self):
        self.serial.close()
        print("закрыл порт")

    def ReadSerial(self,uic_modul):
        mass_simbols = self.serial.readLine()
        mass_simbols_str = str(mass_simbols, 'utf-8').strip()
        StR = mass_simbols_str.split(',')
        if StR[0] == '0':
            uic_modul.ProgressBar.setValue(int(StR[3]))
            uic_modul.TextTemp.setValue(int(StR[3]))
            print(StR[3])

    def SerialSend(self,data):
        self.serial.write(data.encode())
        print('в порт отправленно: ', data)

    def Get_info_about_portlist(self):
        return self.portlist


er = MetodsPorts()
print(er.Get_info_about_portlist())