# Allows time.sleep() command
import time

class Command_for_VNA:
    ###########################
    #
    #  Input parameters
    #
    instrument = "TR1300"  # "S5048","S7530","Planar804","Planar304",
    #  "S8081" (Planar808/1), "R54", "R140",
    #  "TR1300", "TR5048", or "TR7530"
    use_center_and_span = 0  # false = use fstart/fstop, true = use center/span
    power_level_dbm = 0  # dBm power level (ignored for R54/140)
    f1_hz = 400e6  # fstart=400e6 or center, as per above, in Hz
    f2_hz = 600e6  # fstop=600e6 or span, as per above, in Hz
    num_points = 401  # number of measurement points
    parameter = "S21"  # "S21", "S11", "S12", etc. R54/140 must use
    #  "S11"; TR devices must use "S11" or "S21";
    #  Ports 3 and 4 available for S8081 only
    format = "mlog"  # "mlog" or "phase"
    time_per_iter_sec = 1  # 1.0 seconds per measurement interval
    num_iter = 10  # 10 number of times to loop
    num_iter_to_store = 2  # 1 number of function iterations to store

    ###########################

    def __init__(self):
        # Allows communication via COM interface
        try:
            import win32com.client as win32com
        except:
            print("You will first need to import the pywin32 extension")
            print("to get COM interface support.")
            print("Try http://sourceforge.net/projects/pywin32/files/ )?")
            input("\nPress Enter to Exit Program\n")
            exit()
         self.app = win32com.Dispatch(instrument + ".application")

        # Wait up to 20 seconds for instrument to be ready
        if self.app.Ready == 0:
            print("Instrument not ready! Waiting...")
            for k in range(1, 21):
                time.sleep(1)
                if self.app.Ready != 0:
                    break
                print("%d" % k)

    def Start_VNA(self, uci_modul):
        # If the software is still not ready, cancel the program
        if self.app.Ready == 0:
            print("Error, timeout waiting for instrument to be ready.")
            print("Check that VNA is powered on and connected to PC.")
            print("The status Ready should appear in the lower right")
            print("corner of the VNA application window.")
            input("\nPress Enter to Exit Program\n")
            exit()
        else:
            print("Instrument ready! Continuing...")

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
        if use_center_and_span == 1:
            #
            #  [This is a simple example of setting an ActiveX property in Python. Note
            #	that when indexed parameters are referenced, the Get prefix and SCPI
            #	 capitalization must be used (e.g. GetSENSe(1) rather than simply sense(1) )]
            self.app.scpi.GetSENSe(1).frequency.center = f1_hz #Эта команда задает/получает количество трассировок выбранного канала
            self.app.scpi.GetSENSe(1).frequency.span = f2_hz #Эта команда задает центральное значение диапазона развертки выбранного канала
        else:
            self.app.scpi.GetSENSe(1).frequency.start = f1_hz #Эта команда задает начальное значение диапазона развертки выбранного канала
            self.app.scpi.GetSENSe(1).frequency.stop = f2_hz #Эта команда задает значение остановки диапазона развертки выбранного канала

        self.app.scpi.GetSENSe(1).sweep.points = num_points #Эта команда задает количество точек измерения выбранного канала

        if instrument[0] != "R":
            self.app.scpi.GetSOURce(1).power.level.immediate.amplitude = power_level_dbm #Эта команда задает уровень мощности выбранного канала

        # Configure the measurement
        self.app.scpi.GetCALCulate(1).GetPARameter(1).define = "S11" #Эта команда задает параметр измерения импеданса выбранной трассировки (Tr) для выбранного канала (Ch).
        self.app.scpi.GetCALCulate(1).GetPARameter(1).select() #Эта команда задает для выбранной трассировки (Tr) выбранного канала (Ch) активную трассировку.
        self.app.scpi.GetCALCulate(1).selected.format = "mlog" #Эта команда задает формат данных активной трассировки выбранного канала (Ch).
        self.app.scpi.trigger.sequence.source = "bus" #Эта команда задает источник триггера "Bus trigger"

        for iter in range(1, num_iter):

            # Execute the measurement
            self.app.scpi.trigger.sequence.single() #Эта команда немедленно генерирует триггер и выполняет измерение, независимо от настройки режима триггера.

            self.app.scpi.GetCALCulate(1).GetPARameter(1).select()
            Y = self.app.scpi.GetCALCulate(1).selected.data.Fdata

            # Discard complex-valued points
            Y = Y[0::2]

            F = self.app.scpi.GetSENSe(1).frequency.data

            if iter <= num_iter_to_store:
                self.app.scpi.mmemory.store.image = str(iter) + ".png"
                self.app.scpi.mmemory.store.fdata = str(iter) + ".csv"

            time.sleep(time_per_iter_sec)

        # Echo last measurement
        print("\nFrequency data\n")
        print(F)
        print("\nMeasurement result\n")
        print(Y)

        # Wait for a keystroke to exit, so as to
        # keep the VNA application open
        raw_input("\nPress Enter to Exit Program\n")