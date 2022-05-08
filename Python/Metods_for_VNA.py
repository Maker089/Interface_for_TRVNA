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


    def OpenPort(self,port_name):
        self.serial.setPortName(port_name)
        self.serial.open(QIODevice.ReadWrite)
        print("открыт порт ", port_name)


    def OpenPortByComboBox(self, uci_modul):
        port_name = uci_modul.PortListComboBox.currentText()
        self.serial.setPortName(port_name)
        self.serial.open(QIODevice.ReadWrite)
        print("открыт порт ", port_name)

    def ClosePort(self):
        self.serial.close()
        print("закрыт порт ", self.serial.portName())

    def ReadSerial(self,uic_modul):
        mass_simbols = self.serial.readLine()
        mass_simbols_str = str(mass_simbols, 'utf-8').strip()
        print(mass_simbols_str)
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

    def Arduino_Connect(self, uic_modul):
        for port in self.portlist:
            mail_port = ''
            self.OpenPort(port)
            print(port,self.portlist,self.serial.isOpen())
            if self.serial.readyRead == True:
                mail_port = self.ReadSerial()
            if mail_port == "hello_to_comp":
                print("ардуино подключилось под портом: ", port)
                uic_modul.ArduinoConnectButton.setText("Arduino Connected")
                uic_modul.ArduinoConnectButton.enabled()
                break
            self.ClosePort()
            print(self.serial.isOpen())



er = MetodsPorts()
print(er.Get_info_about_portlist())