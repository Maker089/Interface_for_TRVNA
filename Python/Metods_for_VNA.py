# Библиотеки
from PyQt5 import QtWidgets, uic

from PyQt5.QtCore import QIODevice

# Импортируем библиотеки для работы с ком портом
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

class Metods_Ports_For_Arduino:
    def __init__(self):
        """создаю сериал порт"""
        self.serial = QSerialPort()
        self.serial.setBaudRate(57600)
        self.portlist = []
        self.start_mod_for_Read_Serial  =True
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
        max_simbol_for_read = 1
        limit_for_while = 100;
        simbol = ''
        simbol_for_replace = "'"
        mass_simbols = []
        count_limit = 0
        start_mod_limit = 5
        self.start_mod_for_Read_Serial = False

        while simbol != "'\\n'" and count_limit != limit_for_while and self.start_mod_for_Read_Serial == False:
            simbol = str(self.serial.read(max_simbol_for_read))[1:]
            mass_simbols.append(simbol.replace(simbol_for_replace,""))
            count_limit +=1
        print("Message: ", mass_simbols)
        return

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



