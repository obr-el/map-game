import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
import citygame as cg
import statecapitalgame as scg
import worldcitygame as wcg
from tkinter.messagebox import showerror, showwarning, showinfo

"""
GUI window: choose between state and city mode
Buttons for enter hint, 
"""


def reverseList(in_list):
    """
    Return the reverse of a list
    :param in_list:
    :return:
    """
    new_list = []
    x = len(in_list)
    y = 0
    while x >= 0:
        new_list[y] = in_list[x]
        y += 1
        x -= 1
    return new_list


def list_to_string(in_list):
    list_str = ""
    for x in in_list:
        list_str = list_str + x
    return list_str


def check_guess(in_string, in_list):
    """
    Removes any list elements that don't start with the given string and returns the result \n
    :param in_string: input str
    :param in_list: input str list
    :return: list of elements which begin with the given string
    """
    out_list = []
    string_list = list(in_string)
    for term in in_list:
        is_term = True
        term_list = list(term)
        x = 0
        if len(string_list) > len(term_list):
            is_term = False
        while x < len(string_list) and x < len(term_list):
            if string_list[x] != term_list[x]:  # if the xth char of in_string is not the xth char of the list element
                is_term = False
            x += 1
        if is_term:
            out_list.append(term)
    return out_list


class MainMenu(tk.Tk):
    """
    A menu window with buttons to start a new state mode game or start a new world mode game
    """

    def __init__(self):
        super().__init__()
        self.is_world = tk.IntVar()
        self.title("City Guesser")
        self.geometry('300x100')
        state_select = tk.Radiobutton(self, text="USA State Capitals Mode", variable=self.is_world,
                                      value=0, command=self.enableGame)
        world_select = tk.Radiobutton(self, text="World Cities Mode (WIP)", variable=self.is_world,
                                      value=1, command=self.enableGame)
        state_select.pack()
        world_select.pack()
        self.newgame_btn = ttk.Button(self, text="New Game", command=self.new_game, state='disabled')
        self.newgame_btn.pack()

    def enableGame(self):
        self.newgame_btn['state'] = 'normal'

    def new_game(self):
        """
        Create a new window to play the game in. \n
        :return: None
        """
        mode = bool(self.is_world.get())
        import random
        if not mode:
            newWindow = tk.Toplevel(self)
            newWindow.title("US City Guesser")
            newWindow.geometry("400x350")
            usgame = scg.StateGame
            usgame.attempt = 0
            usgame.guess_left = 5
            usgame.city = random.choice(usgame.city_list)
            frame = GameMode(newWindow, usgame)
            frame.mapImg = tk.PhotoImage(file='usmap.png')
            frame.pack()
        else:
            newWindow = tk.Toplevel(self)
            newWindow.title("World City Guesser")
            newWindow.geometry("400x350")
            worgame = wcg.WorldGame
            worgame.city = random.choice(worgame.city_list)
            frame = GameMode(newWindow, worgame)
            frame.pack()


class GameMode(ttk.Frame):
    """
    The frame where the game will be played.
    """

    def __init__(self, container, game):
        super().__init__(container)
        self.game = game
        self.gameInfo = [self.game.get_answer, self.game.attempt, self.game.guess_left]
        self.container = container
        self.enter_text = None
        self.guess_list = None
        self.guess = tk.StringVar()
        self.answer_list = self.game.get_list(self.game())
        self.prev_guess = []
        self.ansloaded = False
        self.isquit = False
        self.ranout = False
        self.masterList = []
        self.mapImg = None

        #  menu bar
        menubar = tk.Menu(self)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Rules", command=self.giveInst)
        helpmenu.add_command(label="Map", command=self.giveMap)
        helpmenu.add_command(label="Hint", command=self.giveHint)
        menubar.add_cascade(label="Help", menu=helpmenu)
        container.config(menu=menubar)

        # frames

        self.leftFrame = tk.Frame(self)
        self.leftFrame.pack(side='left', padx=5)
        self.sep = ttk.Separator(self, orient='vertical')
        self.sep.pack(side='left', expand=True, fill='y', padx=10, pady=5)
        self.rightFrame = tk.Frame(self)
        self.rightFrame.pack(side='right', padx=5)

        # city search frame
        # user inputs the start of a city name
        searchFrame = ttk.Frame(self.leftFrame)
        self.enter_text = tk.StringVar()
        self.searchbox = ttk.Entry(searchFrame, textvariable=self.enter_text)
        self.searchbox.grid(column=0, row=0)
        # button to update listbox to match search
        search_btn = ttk.Button(searchFrame, text='\U0001F50D', width=3, command=self.updateBox)
        search_btn.grid(column=1, row=0)
        # button to restore original list
        clear_btn = ttk.Button(searchFrame, text='RESTORE LIST', command=self.clearSearch)
        clear_btn.grid(column=0, row=1, columnspan=2, sticky='E')
        searchFrame.grid(column=0, row=0, sticky='W')

        # combobox of order (alpha by state, alpha by city, n to s, e to w, or by population)
        self.sortVar = tk.StringVar()
        sortChoice = ttk.Combobox(self.leftFrame, state='readonly',textvariable=self.sortVar)
        sortChoice['values'] = ('Alphabetical (City)', 'Alphabetical (State)', 'Population (high to low)',
                                'Latitude (North to South)', 'Longitude (East to West)')
        sortChoice.bind('<<ComboboxSelected>>', self.citySortSelect)
        sortChoice.grid(column=0, row=1)

        # list of cities to choose from
        self.inputbox = tk.Listbox(self.leftFrame, height=10)
        self.inputbox.grid(column=0, row=2)
        self.listCities()
        self.inputbox.bind('<<ListboxSelect>>', self.inputboxSelect)
        self.inputbox.bind('<Double-1>', self.giveInfo)

        inputFrame = tk.Frame(self.leftFrame)
        enter_btn = ttk.Button(inputFrame, text='Enter', command=self.play)
        enter_btn.grid(column=0, row=1)
        inputFrame.grid(column=0, row=3, sticky='E')

        # infoFrame
        self.infoFrame = ttk.LabelFrame(self.rightFrame, text="Game Info", width=20)
        # Previous Guesses:
        self.prevGuess = ""
        self.prevLabel = ttk.Label(self.infoFrame, text=self.prevGuess)
        self.prevLabel.pack()
        # Guess attempts remaining:
        self.attLeft = tk.StringVar(value=(str(self.gameInfo[2]) + " guesses remaining."))
        self.attLabel = ttk.Label(self.infoFrame, textvariable=self.attLeft)
        self.attLabel.pack()
        self.infoFrame.grid(column=1, row=0)

        # Game display
        self.gameDisplay = tk.Text(self.rightFrame,height=8,width=20)
        self.gameDisplay.grid(column=1, row=1)
        self.gameDisplay.insert(1.0," ")
        scrollbar = ttk.Scrollbar(self.gameDisplay,orient='vertical')
        # scrollbar.pack(side='right',fill='y')
        self.gameDisplay['yscrollcommand'] = scrollbar.set

        # quit
        quit_btn = ttk.Button(self.rightFrame, text="QUIT", command=self.quitGame)
        quit_btn.grid(column=1, row=3)

        # make the master List
        self.getMasterList()

    def getMasterList(self):
        self.masterList = []
        pop = self.game.population
        long = self.game.longitude
        lat = self.game.latitude
        for city in self.answer_list:
            clist = list(city)
            state = clist[-2] + clist[-1]
            newDict = {'city': city, 'state': state, 'pop': pop[city], 'long': long[city], 'lat': lat[city]}
            self.masterList.append(newDict)

    def searchboxSelect(self, event):
        selection = self.enter_text.get()
        self.guess = selection

    def clearSearch(self):
        self.inputbox.delete(first=0, last='end')
        self.answer_list = self.game.city_list
        self.getMasterList()
        self.citySort()

    def inputboxSelect(self, event):
        selection = self.inputbox.get('anchor')  # string value at current selection
        self.guess = selection

    def listCities(self):
        for city in self.answer_list:
            self.inputbox.insert('end', city)

    def updateBox(self):
        """
        Updates the input box after a search is made
        :return:
        """
        self.inputbox.delete(first=0, last='end')
        text = self.enter_text.get()
        text = text.upper()
        self.answer_list = check_guess(text, self.answer_list)
        self.getMasterList()
        self.listCities()

    def citySortSelect(self,event):
        self.citySort()

    def citySort(self):
        """
        Updates the input box order
        :return:
        """
        def returnPop(dic):
            return dic['pop']

        def returnLong(dic):
            return dic['long']

        def returnLat(dic):
            return dic['lat']

        def returnCity(dic):
            return dic['city']

        def returnState(dic):
            return dic['state']

        selection = self.sortVar.get()

        if selection == 'Alphabetical (City)':
            self.masterList.sort(key=returnCity)
        elif selection == 'Alphabetical (State)':
            self.masterList.sort(key=returnState)
        elif selection == 'Population (high to low)':
            self.masterList.sort(key=returnPop, reverse=True)
        elif selection == 'Latitude (North to South)':
            self.masterList.sort(key=returnLat, reverse=True)
        elif selection == 'Longitude (East to West)':
            self.masterList.sort(key=returnLong)
        self.answer_list = []
        for x in self.masterList:
            self.answer_list.append(x['city'])
        self.inputbox.delete(first=0, last='end')
        self.listCities()

    def play(self):
        entry = self.guess
        gameText = self.game.playgame(self.game, entry)
        self.gameInfo = [self.game.get_answer(self.game), self.game.attempt, self.game.guess_left]
        attempt = self.gameInfo[1]
        if entry == self.game.get_answer(self.game):
            # self.prevGuess = self.prevGuess + entry
            self.prev_guess.append("\n"+entry)
            self.getAnswerMode()
        else:
            self.prevLabel.destroy()
            self.attLabel.destroy()
            guess = self.game.wrongGuess[-1]
            self.gameDisplay.insert('end', gameText+"\n")
            self.prev_guess.append("\n" + guess)
            self.prevLabel = ttk.Label(self.infoFrame, text="Previous guesses: " + list_to_string(self.prev_guess))
            self.prevLabel.pack()
            self.attLeft = tk.StringVar(value=(str(self.gameInfo[2]) + " guesses remaining."))
            self.attLabel = ttk.Label(self.infoFrame, textvariable=self.attLeft)
            self.attLabel.pack()
            if self.gameInfo[2] == 0:
                self.ranout = True
                self.getAnswerMode()


    def giveInst(self):
        instWindow = tk.Toplevel(self)
        inst = self.game.instruct(self.game)
        label = tk.Label(instWindow, text=inst)
        label.pack()

    def giveHint(self):
        hintWindow = tk.Toplevel(self)
        hint = self.game.hint(self.game)
        label = tk.Label(hintWindow, text=hint)
        label.pack()

    def giveMap(self):
        mapWindow = tk.Toplevel(self)
        mapLabel = tk.Label(mapWindow,image=self.mapImg)
        mapLabel.pack()

    def giveInfo(self,event):
        infoWindow = tk.Toplevel(self)
        inguess = self.guess
        info = self.game.info(self.game, inguess)
        label = tk.Label(infoWindow, text=info)
        label.pack()

    def quitGame(self):
        self.isquit = True
        self.getAnswerMode()

    def getAnswerMode(self):
        newWin = tk.Toplevel()
        newWin.geometry("400x300")
        ans = AnswerMode
        ans.attempts = self.gameInfo[1]
        ans.prevGuess = list_to_string(self.prev_guess)  # self.prevGuess
        ans.ranout = self.ranout
        ans.isquit = self.isquit
        ans.answer = self.game.get_answer(self.game)
        AnswerMode(newWin).pack()
        self.container.destroy()


class AnswerMode(ttk.Frame):
    attempts = 0
    prevGuess = ""
    ranout = False
    isquit = False
    answer = ""

    def __init__(self, container):
        super().__init__(container)
        label = tk.Label(self)
        if self.ranout:
            label['text'] = "You ran out of guesses!"
        elif self.isquit:
            label['text'] = "You quit!"
        else:
            label['text'] = "You win!"
        label.pack()
        anslabel = tk.Label(self)
        anslabel['text'] = "The answer was " + self.answer + "."
        anslabel.pack()
        attlabel = tk.Label(self, text=("You guessed " + str(self.attempts) + " times."))
        attlabel.pack()
        guesslabel = tk.Label(self, text=("Your guesses were:\n"+self.prevGuess))
        guesslabel.pack()

