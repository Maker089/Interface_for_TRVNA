# Библиотеки
from PyQt5 import QtWidgets, uic
from  PyQt5.QtWidgets import  QMessageBox

# Импортируем библиотеки для работы с ком портом
#Методы для работы с ардуино
from Interface_for_TRVNA.Python.Arduino_metods.Arduino_ports_modul import Arduino_ports_modul

#Методы для работы с ардуино
from Interface_for_TRVNA.Python.VNA_Metods.Command_for_VNA import Command_for_VNA

#для записи данных в эксельку
from Interface_for_TRVNA.Python.CSV_Metods.CSV_Modul import CSV_Modul


#############################################################################

app = QtWidgets.QApplication([])
ko = uic.loadUi(r"C:/Users/tor/Desktop/Проект прога/Programm_VNA/Interface_for_TRVNA/Dizain.ui")
ko.setWindowTitle("Programm for VNA experement")
s = Arduino_ports_modul()
c = CSV_Modul()
vna  =Command_for_VNA(ko)

#############################################################################

installation_is_ready_for_testing = False
Ready_points = dict([("vna",0),("steps_x",0),("steps_y",0),("connect_arduino",0)])

msg = QMessageBox(ko)
msg.setWindowTitle("Message Box")
msg.setText("nope")

message = ""
steps_x = 1
steps_y = 1
size_step = 1

#############################################################################

def setEnabled_aLL_buttons(Enabled_mod):
    if Enabled_mod == True:
        ko.Set_step_size_button.setEnabled(True)
        ko.Start_experement_button.setEnabled(True)
        ko.OpenPortButton.setEnabled(True)
        ko.ClosePortButton.setEnabled(True)
        ko.Set_steps_x_number_button.setEnabled(True)
        ko.Set_steps_y_number_button.setEnabled(True)
        ko.VNA_Button.setEnabled(True)
    elif Enabled_mod == False:
        ko.Set_step_size_button.setEnabled(False)
        ko.Start_experement_button.setEnabled(False)
        ko.OpenPortButton.setEnabled(False)
        ko.ClosePortButton.setEnabled(False)
        ko.Set_steps_x_number_button.setEnabled(False)
        ko.Set_steps_y_number_button.setEnabled(False)
        ko.VNA_Button.setEnabled(False)

def Set_steps_x_number(number_of_steps):
    if int(number_of_steps) >= 1:
        c.Take_Steps_x(int(number_of_steps))
        Ready_points["steps_x"] = 1

        global  steps_x
        steps_x = number_of_steps

    else:
        msg.exec_() #тут мессэдж бокс должен быть вот


def Set_steps_y_number(number_of_steps):
    if int(number_of_steps) >= 1:
        c.Take_Steps_y(int(number_of_steps))
        Ready_points["steps_y"] = 1

        global steps_y
        steps_y = number_of_steps

    else:
        msg.exec_() #тут мессэдж бокс должен быть вот


def Set_step_size(size_of_step):
    try:
        if int(size_of_step)>=0:
            c.Set_Step_Size(int(size_of_step))
        else:
            msg.exec_()
    except:
        msg.exec_()


def Make_VNA_objeckt():
    try:
        global vna
        vna.Start_VNA(ko)
        vna.Set_VNA_Settings(ko)
        Ready_points["vna"] = 1
    except:
        msg.exec_()


def Recive_a_message():
    if s.serial.readyRead:
        message = s.Read_Serial(ko)
        print(message)
    else:
        msg.exec_()


def Arduino_connect_whith_ready_points():
    s.Arduino_Connect(ko)
    if s.Arduino_conected:
        Ready_points["connect_arduino"] = 1
    else:
        msg.exec_()

def Parsing_message(mes):
    measure = vna.Make_a_measure
    x_pos = ""
    y_pos = ""
    return dict([("measure",measure), ("x_pos",x_pos), ("y_pos",y_pos)])


def Do_experement():
    try:
        if installation_is_ready_for_testing:

            setEnabled_aLL_buttons(False)

            for y_pos in range(0, size_step, steps_y * size_step):
                for x_pos in range(0, size_step, steps_x * size_step):
                    s.Serial_Send("message for arduino sdelat shag")

                    s.serial.readyRead.connect(lambda: Recive_a_message())
                    Parsing_dict =  Parsing_message(message)

                    c.Append_measurement(Parsing_dict["measure"], Parsing_dict["x_pos"], Parsing_dict["y_pos"]) # да тут можно сделать чтобы позицию в файлик записывалась с помощью преременных позиции в проге Programm_Baza, но прибору лучше знать, на какой он сейчас позиции
                s.Serial_Send("message for next step y and go back to srart x_pos")
    except:
        msg.exec_()
#############################################################################

if not("not_ready" in Ready_points):
    installation_is_ready_for_testing = True


print(type(ko))
ko.setWindowTitle("SerialGUI")

# добавляем в комбобокс все порты
ko.PortListComboBox.addItems(s.Get_info_about_portlist())

print(s.Get_info_about_portlist())


# по клику на PortListComboBox вызываем функцию проверка на нажатие
ko.PortListComboBox.currentIndexChanged.connect(lambda: s.Print_Bebra())

# при нажатии на кнопку вызываем функцию открытия порта
ko.OpenPortButton.clicked.connect(lambda: s.Open_Port_By_Combo_Box(ko))  #ээээ как это делать ko.OpenPortButton.clicked.connect(lambda x: s.OpenPort(ko))

#если в порт поступли сообщения, то читаем их
s.serial.readyRead.connect(lambda: Recive_a_message()) # тут надо считывание с порта

# при нажатии на кнопку вызываем функцию окрытия порта
ko.ClosePortButton.clicked.connect(lambda: s.Close_Port(ko))

# при нажатиии отправляем в порт текст из строчки
ko.SendButton.clicked.connect(lambda: s.Serial_Send(ko.SendTextWindow.displayText()))

# при нажатии подключаемся к ардуино
ko.ArduinoConnectButton.clicked.connect(lambda: s.Arduino_Connect(ko))

# при нажатии устанавливаем параметры количество шага
ko.Set_steps_x_number_button.clicked.connect(lambda: Set_steps_x_number(ko.Set_steps_x_number_send_text_window.displayText()))

# при нажатии устанавливаем параметры количество шага
ko.Set_steps_y_number_button.clicked.connect(lambda: Set_steps_y_number(ko.Set_steps_y_number_send_text_window.displayText()))

# при нажатии устанавливаем параметры устанавливаем длинну шага у шаговиков для замера
ko.Set_step_size_button.clicked.connect(lambda: Set_step_size(ko.Set_step_size_text_window.displayText()))

# кнопка эксперемент
ko.Start_experement_button.clicked.connect(lambda: Do_experement())

# устанавливаем связь с ардуино
ko.ArduinoConnectButton.clicked.connect(lambda: s.Arduino_Connect(ko))

# устанавливаем сязь и настройки с vna
ko.VNA_Button.clicked.connect(lambda: Make_VNA_objeckt())







#####################################
ko.show()
app.exec()
