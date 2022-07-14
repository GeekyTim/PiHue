import time

from phue import Bridge


class HueControl:
    """
    Controls the Hue Lights
    """

    def __init__(self, bridge, roomname, waittime):
        """
        IMPORTANT: If running for the first time:
            Uncomment the b.connect() line
            Press button on bridge
            Run the code
        This will save your connection details in /home/pi/.python_hue
        Delete that file if you change bridges

        :param bridge:
        :param roomname:
        :return:
        """

        try:
            # Connect to the bridge
            self.__bridge = Bridge(bridge)
            # self.__bridge.connect()  # Uncomment to connect to the bridge <<<<<<<<<<
        except:
            print("Unable to connect to the bridge")
            exit()

        # Find the room number from the room name
        roomnumber = 0
        allrooms = self.__bridge.get_group()

        for room in allrooms.keys():
            if allrooms[room]['name'] == roomname:
                roomnumber = int(room)
                break

        if roomnumber == 0:
            print('The room name you have supplied in roomname is not recognised. Please try again. Exiting.')
            exit()

        self.__waittime = waittime
        self.__roomnumber = roomnumber
        self.__alertinprogress = False
        self.__roomstatus = self.__bridge.get_group(self.__roomnumber)

    def __getroomstatus(self):
        """
        Get the status of a room BEFORE the alert is set, so it can be returned to that state
        """
        self.__roomstatus = self.__bridge.get_group(self.__roomnumber)

    def __resetroomstatus(self):
        """
        Return the status of the room to what it was before the alert
        """
        self.__bridge.set_group(self.__roomnumber,
                                {'xy': self.__roomstatus['action']['xy'], 'bri': self.__roomstatus['action']['bri'],
                                 'on': self.__roomstatus['action']['on']}, transitiontime=0)
        time.sleep(self.__waittime)

    def alert(self, alertpattern):
        """
        Runs through the alert dictionary defined in alert_pattern

        :param alertpattern: containes the pre-defined alert pattern
        """
        self.__getroomstatus()

        # Using the pre-defined alert patterns, change the lamp status
        for rep in range(alertpattern[0]):
            for runalert in range(2, len(alertpattern)):
                self.__bridge.set_group(self.__roomnumber, alertpattern[runalert], transitiontime=0)
                time.sleep(alertpattern[1])
        # Return the lamps to the previous status
        self.__resetroomstatus()

    def setcolour(self, colour):
        """

        :param colour: The colour to set the lights to
        :return:
        """
        self.__bridge.set_group(self.__roomnumber, colour, transitiontime=0)
        time.sleep(self.__waittime)

    def turnoff(self):
        """
        Turns all the lights off
        """
        self.__bridge.set_group(self.__roomnumber, 'on', False)
        time.sleep(self.__waittime)
