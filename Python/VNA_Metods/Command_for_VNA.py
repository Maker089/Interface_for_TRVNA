# Allows time.sleep() command
import time

class Command_for_VNA:


    def __init__(self, uic_modul):
        ###########################
        #
        #  Input parameters
        #
        self.instrument = "TR1300"  # "S5048","S7530","Planar804","Planar304",
        #  "S8081" (Planar808/1), "R54", "R140",
        #  "TR1300", "TR5048", or "TR7530"
        self.use_center_and_span = 0  # false = use fstart/fstop, true = use center/span
        self.power_level_dbm = 0  # dBm power level (ignored for R54/140)
        self.f1_hz = 400e6  # fstart=400e6 or center, as per above, in Hz
        self.f2_hz = 600e6  # fstop=600e6 or span, as per above, in Hz
        self.num_points = 401  # number of measurement points
        self.parameter = "S21"  # "S21", "S11", "S12", etc. R54/140 must use
        #  "S11"; TR devices must use "S11" or "S21";
        #  Ports 3 and 4 available for S8081 only
        self.format = "mlog"  # "mlog" or "phase"
        self.time_per_iter_sec = 1  # 1.0 seconds per measurement interval
        self.num_iter = 10  # 10 number of times to loop
        self.num_iter_to_store = 2  # 1 number of function iterations to store
        self.Y = []
        self.F = []
        ############################################################################
    def Start_VNA(self, uic_modul):
        # Allows communication via COM interface
        try:
            import win32com.client as win32com
            """Создаю элемент класса win32com"""
            self.app = win32com.Dispatch(self.instrument + ".application")
            uic_modul.Mail_Window.setText("VNA Start_settings done")
        except:
            print("You will first need to import the pywin32 extension")
            print("to get COM interface support.")
            print("Try http://sourceforge.net/projects/pywin32/files/ )?")
            input("\nPress Enter to Exit Program\n")
            uic_modul.Mail_Window.setText("VNA не подключен, проверте подключение")
            exit()




    def Set_VNA_Settings(self, uic_modul):
        # Ждем пока подсоеденится 20 секунд, иначе выдаем сообщение, что не подключенно
        if self.app.Ready == 0:
            print("Instrument not ready! Waiting...")
            uic_modul.Mail_Window.setText("Инструмент не готов. Жди...")
            for k in range(1, 21):
                time.sleep(1)
                if self.app.Ready != 0:
                    break
                print("%d" % k)
                uic_modul.Mail_Window.setText("%d" % k)

        # If the software is still not ready, cancel the program
        if self.app.Ready == 0:
            print("Error, timeout waiting for instrument to be ready.")
            print("Check that VNA is powered on and connected to PC.")
            print("The status Ready should appear in the lower right")
            print("corner of the VNA application window.")
            input("\nPress Enter to Exit Program\n")
            uic_modul.Mail_Window.setText("Инструмент не готов. Выйди и зайди нормально")
            exit()
        else:
            print("Instrument ready. Lets go to experement")
            uic_modul.Mail_Window.setText("Инструмент готов. Я твоя программа давай делай эксперемент")

        # Get and echo the instrument name, serial number, etc.
        #
        #  [This is a simple example of getting an ActiveX property in Python]
        #
        print(self.app)

        # Sets the instrument to a preset state
        #
        #  [This is an example of executing an ActiveX "method" in Python]
        #
        self.app.scpi.system.preset() # Эта команда очень похожа на команду *RST. Разница состоит в том, что команда *RST сбрасывает настройки прибора для использования SCPI, а команда SYSTem:PRESet сбрасывает настройки прибора для использования лицевой панели. Таким образом, команда *RST выключает гистограмму и статистику, а команда SYSTem:PRESet включает их (CALC:TRAN:HIST:STAT ON).

        # Configure the stimulus
        if self.use_center_and_span == 1:
            #
            #  [This is a simple example of setting an ActiveX property in Python. Note
            #	that when indexed parameters are referenced, the Get prefix and SCPI
            #	 capitalization must be used (e.g. GetSENSe(1) rather than simply sense(1) )]
            self.app.scpi.GetSENSe(1).frequency.center = self.f1_hz #Эта команда задает/получает количество трассировок выбранного канала
            self.app.scpi.GetSENSe(1).frequency.span = self.f2_hz #Эта команда задает центральное значение диапазона развертки выбранного канала
        else:
            self.app.scpi.GetSENSe(1).frequency.start = self.f1_hz #Эта команда задает начальное значение диапазона развертки выбранного канала
            self.app.scpi.GetSENSe(1).frequency.stop = self.f2_hz #Эта команда задает значение остановки диапазона развертки выбранного канала

        self.app.scpi.GetSENSe(1).sweep.points = self.num_points #Эта команда задает количество точек измерения выбранного канала

        if self.instrument[0] != "R":
            self.app.scpi.GetSOURce(1).power.level.immediate.amplitude = self.power_level_dbm #Эта команда задает уровень мощности выбранного канала

        # Configure the measurement
        self.app.scpi.GetCALCulate(1).GetPARameter(1).define = "S11" #Эта команда задает параметр измерения импеданса выбранной трассировки (Tr) для выбранного канала (Ch).
        self.app.scpi.GetCALCulate(1).GetPARameter(1).select() #Эта команда задает для выбранной трассировки (Tr) выбранного канала (Ch) активную трассировку.
        self.app.scpi.GetCALCulate(1).selected.format = "mlog" #Эта команда задает формат данных активной трассировки выбранного канала (Ch).
        self.app.scpi.trigger.sequence.source = "bus" #Эта команда задает источник триггера "Bus trigger"

        uic_modul.Mail_Window.setText("VNA не подключен, проверте подключение")

    def Make_a_measure(self):
        for iter in range(1, self.num_iter):

            # Execute the measurement
            self.app.scpi.trigger.sequence.single() #Эта команда немедленно генерирует триггер и выполняет измерение, независимо от настройки режима триггера.

            self.app.scpi.GetCALCulate(1).GetPARameter(1).select() #Эта команда задает для выбранной трассировки (Tr) выбранного канала (Ch) активную трассировку.
            self.Y = self.app.scpi.CALCulate(1).selected.data.Fdata # Эта команда получает форматированный массив данных для активной трассировки выбранного канала ( Ch). Элемент данных массива зависит от формата данных (заданного с помощью УИР. КАЛЬЦИУЛ (Ch). SELected.FORMat объект).
            print("(Frequency data) Y = ", self.Y ,"\n","(Frequency data) Y[0::2] = ", self.Y[0::2])

            # Discard complex-valued points
            self.Y = self.Y[0::2]

            self.F = self.app.scpi.GetSENSe(1).frequency.data #Эта команда считывает частоты во всех точках измерения для выбранного канала (Ch)
            print("(Measurement result) F = ",self.F)

            if iter <= self.num_iter_to_store:
                 self.app.scpi.mmemory.store.image = str(iter) + ".png" #Эта команда сохраняет отображаемое изображение на ЖК-дисплее при выполнении объекта в файл в растровом (расширение «.bmp») или переносимой сетевой графике (расширение «.png») формате.
                 self.app.scpi.mmemory.store.fdata = str(iter) + ".csv"

            time.sleep(self.time_per_iter_sec)

        return [self.Y, self.F]

