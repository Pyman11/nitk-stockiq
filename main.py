
import wx
from wx.lib.scrolledpanel import ScrolledPanel
import news
from webbrowser import open as op
import data
from ast import literal_eval
import general
import google.generativeai as genai
import graph

p = ""
ref = ""

def get_result ( vals ):
    for i in range ( len ( vals ) ):
        if vals[i] == None:
            vals[i] = 0
    final_metric = []
    genai.configure(api_key="AIzaSyB7rjodkd1sxe_EJ5lSi_cb6ro7anTi3XQ")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("""Earnings per share (EPS): {}
    P/E: {}
    P/B: {}
    Dividend Yield for AMZN: {}
    Beta:{}
    Environmental Score: {}
    Social Score: {}
    Governance Score: {}
    Tell whether each metric is bad/moderate/good (only one word). Do not type anything else.""".format ( str ( float ( vals[0] ) ), str ( float ( vals[1] ) ), str ( float ( vals[2] ) ), str ( float ( vals[3] ) ), str ( float ( vals[4] ) ), str ( float ( vals[5] ) ), str ( float ( vals[6] ) ), str ( float ( vals[7] ) ) ) )
    t = response.text.split('\n')
    for i in t:
        if i.lower() == 'good':
            final_metric.append ( 'up' )
        if i.lower() == 'bad':
            final_metric.append ( 'down' )
        if i.lower() == 'moderate':
            final_metric.append ( 'neutral' )

    return final_metric

def get_metric_lines ( title, val, cname ):
    genai.configure(api_key="AIzaSyB7rjodkd1sxe_EJ5lSi_cb6ro7anTi3XQ")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("{} : {}. Comment about the {} in 2 lines(nothing else).".format ( title, val, title ) )
    return response.text

def add_template ( code ):
    if data.check_validity ( code ):
        try:
            f = open ( "stocks.txt", "r" )
            d = literal_eval ( f.read() )
            f.close()
            l = [ data.get_name ( code ), data.get_current ( code ) ]
            d[code] = l
            f = open ( "stocks.txt", "w" )
            f.write ( str ( d ) )
            f.close()
        except:
            wx.MessageBox ( "The entered stock does not exist.", "Stock Code Not Found", wx.OK | wx.ICON_ERROR )
    else:
        wx.MessageBox ( "The entered stock does not exist.", "Stock Code Not Found", wx.OK | wx.ICON_ERROR )

def get_list():
    f = open ( "stocks.txt", "r" )
    d = literal_eval ( f.read() )
    f.close()
    return d

stocks = get_list()

class CustomMessageBox(wx.Dialog):
    def __init__(self, parent, message, title):
        super(CustomMessageBox, self).__init__(parent, title=title, size=(500, 150))
        self.SetBackgroundColour(wx.Colour(30, 30, 30))  
        
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(30, 30, 30))  
        
        text = wx.StaticText(panel, label=message, style=wx.ALIGN_CENTER)
        text.SetForegroundColour(wx.Colour(255, 255, 255)) 
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 1, wx.ALL | wx.EXPAND, 10)
        panel.SetSizer(sizer)
        
        self.Centre()

    def on_close(self, event):
        self.Destroy()

class stats ( wx.MiniFrame ):
    def __init__ ( self, parent, stock ):
        wx.MiniFrame.__init__ ( self, parent = parent, title = "Stock Analysis", style = wx.CAPTION | wx.CLOSE_BOX, size = ( 1500, 800 ) )
        self.SetBackgroundColour ( 'black' )
        l = data.get_name ( (stock.split())[0] )
        try:
            n = news.get_news ( (stock.split())[0] )
        except:
            n = [ "No recent news available.", "No insights." ]
        self.cname = stock.split()[0]
        values = data.get_data ( stock.split()[0] )
        self.values = values

        self.mainsizer = wx.BoxSizer ( wx.HORIZONTAL ) 

        self.leftsizer = wx.BoxSizer ( wx.VERTICAL )
        self.rightsizer = wx.BoxSizer ( wx.VERTICAL )
        
        self.statictext = wx.StaticText ( self, label = "{} ({}): {}".format ( (stock.split())[0], l, (stock.split())[1] ) )
        self.statictext.SetFont ( wx.Font ( 30, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.statictext.SetBackgroundColour ( "black" )
        self.statictext.SetForegroundColour ( "white" )
        self.leftsizer.Add ( self.statictext, 0, wx.RIGHT, 20 )

        self.buttonsizer = wx.BoxSizer ( wx.HORIZONTAL )
        self.b1 = wx.Button ( self, label = "Add to Homepage", name = (stock.split())[0] )
        self.b1.SetBackgroundColour ( "black" )
        self.b1.SetForegroundColour ( "white" )
        self.Bind ( wx.EVT_BUTTON, self.b1_press, self.b1 )
        self.buttonsizer.Add ( self.b1, 0, wx.ALL, 20 )
        self.b2 = wx.Button ( self, label = "Remove from Homepage", name = (stock.split())[0] )
        self.b2.SetBackgroundColour ( "black" )
        self.b2.SetForegroundColour ( "white" )
        self.buttonsizer.Add ( self.b2, 0, wx.ALL, 20 )
        self.Bind ( wx.EVT_BUTTON, self.b2_press, self.b2 )
        self.leftsizer.Add ( self.buttonsizer, 0, wx.RIGHT, 20 )

        details = get_list()
        if (stock.split())[0] not in details:
            self.b2.Disable()
        if len ( details ) >= 5 or (stock.split())[0] in details.keys():
            self.b1.Disable()
        self.gridsizer = wx.GridSizer ( len ( values ), 3, 10, 10 )

        temp = 0
        final_metric = get_result ( list ( values.values() ) )
        for i in values:
            self.name = wx.StaticText ( self, label = "{}: ".format ( i ), style = wx.BORDER_NONE )
            self.name.SetFont ( wx.Font ( 15, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
            self.name.SetBackgroundColour ( "black" )
            self.name.SetForegroundColour ( "#42adf5" )
            self.gridsizer.Add ( self.name, 0, wx.EXPAND )

            self.name = wx.Button ( self, label = " {} ".format ( values[i] )[:7].format ( 3.68 ), name = i )
            self.name.SetFont ( wx.Font ( 15, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
            self.name.SetBackgroundColour ( "black" )
            self.name.SetForegroundColour ( "green" )
            self.name.Bind ( wx.EVT_BUTTON, self.on_press, self.name )
            self.gridsizer.Add ( self.name, 0, wx.EXPAND )
            try:
                self.img = wx.StaticBitmap ( self, -1, wx.Bitmap ( "./{}.bmp".format(final_metric[temp]) ) )
                self.gridsizer.Add ( self.img, 0 )
            except:
                self.img = wx.StaticBitmap ( self, -1, wx.Bitmap ( "./neutral.bmp" ) )
                self.gridsizer.Add ( self.img, 0 )
            temp += 1

        self.leftsizer.Add ( self.gridsizer, 0, wx.ALL, 20 )

        self.statictext = wx.StaticText ( self, label = "Recent News on {}".format ( stock.split()[0] ) )
        self.statictext.SetFont ( wx.Font ( 30, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )   
        self.statictext.SetBackgroundColour ( "black" )
        self.statictext.SetForegroundColour ( "#03fcb1" )
        self.rightsizer.Add ( self.statictext, 0, wx.ALL, 0 )
        self.rightsizer.AddSpacer ( 10 )

        self.listbox = wx.ListBox ( self, choices = n[0], size = ( 600, 300 ) )
        self.listbox.SetFont ( wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL) )
        self.listbox.SetBackgroundColour ( "black" )
        self.listbox.SetForegroundColour ( "white" )
        self.Bind ( wx.EVT_LISTBOX_DCLICK, self.process_click, self.listbox )
        self.rightsizer.Add ( self.listbox, 0, wx.RIGHT | wx.UP | wx.DOWN, 0 )

        self.rightsizer.AddSpacer ( 70 )

        self.statictext = wx.StaticText ( self, label = "Overall Insights".format ( stock ) )
        self.statictext.SetFont ( wx.Font ( 30, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )   
        self.statictext.SetBackgroundColour ( "black" )
        self.statictext.SetForegroundColour ( "#03fcb1" )
        self.rightsizer.Add ( self.statictext, 0, wx.ALL, 0 )

        self.rightsizer.AddSpacer ( 10 )
        self.listbox = wx.ListBox ( self, choices = n[1] , style = wx.BORDER_NONE )
        self.listbox.SetFont ( wx.Font ( 15, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )   
        self.listbox.SetBackgroundColour ( "black" )
        self.listbox.SetForegroundColour ( "white" )
        self.Bind ( wx.EVT_LISTBOX_DCLICK, self.process_click, self.listbox )
        self.rightsizer.Add ( self.listbox, 0, wx.RIGHT | wx.UP | wx.DOWN, 0 )
        
        self.mainsizer.Add ( self.leftsizer, 0, wx.ALL, 20 )
        self.mainsizer.Add ( self.rightsizer, 0, wx.ALL, 20 )
        self.SetSizer ( self.mainsizer )
                
        self.Show()

    def process_click ( self, event ):
        op ( "https://www.google.com/search?q=" + event.EventObject.GetString ( event.EventObject.GetSelection() )[2:200] )

    def on_press ( self, event ):
        title = event.EventObject.Name
        val = self.values[event.EventObject.Name]
        d = CustomMessageBox ( self, get_metric_lines ( title, val, self.cname ), "Info about {}".format ( title ) )
        d.ShowModal()

    def b1_press ( self, event ):
        add_template ( event.EventObject.Name )
        ref ( p )

    def b2_press ( self, event ):
        f = open ( "stocks.txt", "r" )
        d = literal_eval ( f.read() )
        f.close()
        del d[event.EventObject.Name]
        f = open ( "stocks.txt", "w" )
        f.write ( str ( d ) )
        f.close()
        ref ( p )
        
class panel ( ScrolledPanel ):
    def __init__ ( self, parent ):
        ScrolledPanel.__init__ ( self, parent = parent )
        self.SetBackgroundColour ( 'black' )

        stocks = get_list()
        green_red = []
        color = []
        for i in stocks:
            r = graph.create_graph ( i )
            if r < data.get_current ( i ):
                color.append ( 'green' )
                green_red.append ( "up" )
            else:
                color.append ( 'red' )
                green_red.append ( "down" )

        global p
        p = parent

        self.mainsizer = wx.BoxSizer ( wx.VERTICAL )
        self.mainsizer.AddSpacer ( 30 )

        self.topsizer = wx.BoxSizer ( wx.HORIZONTAL )        
        
        self.statictext = wx.StaticText ( self, label = "Your Stocks" )
        self.statictext.SetFont ( wx.Font ( 30, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.statictext.SetBackgroundColour ( "black" )
        self.statictext.SetForegroundColour ( "white" )
        self.topsizer.Add ( self.statictext, 0, wx.ALL | wx.ALIGN_LEFT, 5 )
        
        self.mainsizer.Add ( self.topsizer, 0, wx.ALL | wx.ALIGN_LEFT, 10 )

        self.searchsizer = wx.BoxSizer ( wx.HORIZONTAL )

        self.name = wx.StaticText ( self, label = "Lookup stocks using code: " )
        self.name.SetFont ( wx.Font ( 15, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
        self.name.SetBackgroundColour ( "black" )
        self.name.SetForegroundColour ( "#bafc03" )
        self.searchsizer.Add ( self.name, 0, wx.UP, 10 )

        self.search = wx.TextCtrl ( self, style = wx.TE_PROCESS_ENTER )
        self.search.Bind(wx.EVT_TEXT_ENTER, self.on_search)
        self.search.SetBackgroundColour ( "black" )
        self.search.SetForegroundColour ( "white" )
        self.searchsizer.Add ( self.search, 0, wx.UP, 10 )

        self.mainsizer.Add ( self.searchsizer, 0, wx.ALL, 20 )

        self.stocksizer = wx.BoxSizer ( wx.HORIZONTAL )

        temp = 0
        for i in stocks:
            self.asizer = wx.BoxSizer ( wx.VERTICAL )
            self.bsizer = wx.BoxSizer ( wx.HORIZONTAL )

            self.name = wx.StaticText ( self, label = "{}: ".format(stocks[i][0]) )
            self.name.SetFont ( wx.Font ( 15, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
            self.name.SetBackgroundColour ( "black" )
            self.name.SetForegroundColour ( "#42adf5" )
            self.bsizer.Add ( self.name, 0, wx.UP, 10 )

            self.name = wx.StaticText ( self, label = "{}".format(stocks[i][1]) )
            self.name.SetFont ( wx.Font ( 15, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )
            self.name.SetBackgroundColour ( "black" )
            self.name.SetForegroundColour ( "{}".format ( color[temp] ) )
            self.bsizer.Add ( self.name, 0, wx.UP | wx.RIGHT, 10 )

            self.img = wx.StaticBitmap ( self, -1, wx.Bitmap ( "./{}.bmp".format(green_red[temp]) ) )
            self.bsizer.Add ( self.img, 0, wx.UP, 10 )
            self.asizer.Add ( self.bsizer, 0, wx.ALL, 10 )

            self.graph = wx.StaticBitmap(self, -1, wx.Bitmap("./{}.png".format ( i ), wx.BITMAP_TYPE_ANY))
            self.asizer.Add ( self.graph, 0, wx.ALL, 10 )
            self.stocksizer.Add ( self.asizer, 0, wx.ALL, 0 )
            self.stocksizer.AddSpacer ( 10 )

            self.csizer = wx.BoxSizer ( wx.HORIZONTAL )
            
            self.an = wx.BitmapButton ( self, -1, wx.Bitmap ( r"./statistics.bmp" ), style = wx.BORDER_NONE, name = str ( i ) + " " + str ( stocks[i][1] ) )
            self.an.SetBackgroundColour ( "black" )
            self.csizer.Add ( self.an, 0, wx.ALL, 10 )
            self.Bind ( wx.EVT_BUTTON, self.press_an, self.an )

            self.csizer.AddSpacer ( 50 )

            stocks[i].append ( self.name )

            self.asizer.Add ( self.csizer, 0, wx.LEFT, 10 )
            temp += 1
        
        self.mainsizer.Add ( self.stocksizer, 0, wx.ALL | wx.ALIGN_LEFT, 10 )

        self.downsizer = wx.BoxSizer ( wx.VERTICAL )

        self.gen_news = general.get_general()

        self.statictext = wx.StaticText ( self, label = "General Stock News"  )
        self.statictext.SetFont ( wx.Font ( 30, wx.DEFAULT, wx.NORMAL, wx.BOLD ) )   
        self.statictext.SetBackgroundColour ( "black" )
        self.statictext.SetForegroundColour ( "#03fcb1" )
        self.downsizer.Add ( self.statictext, 0, wx.ALL, 0 )
        self.downsizer.AddSpacer ( 10 )

        self.listbox = wx.ListBox ( self, choices = [""]+self.gen_news[0], size = ( 1000, 400 ) )
        self.listbox.SetFont ( wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL) )
        self.listbox.SetBackgroundColour ( "black" )
        self.listbox.SetForegroundColour ( "white" )
        self.Bind ( wx.EVT_LISTBOX_DCLICK, self.process_click, self.listbox )
        self.downsizer.Add ( self.listbox, 0, wx.RIGHT | wx.UP | wx.DOWN, 0 )

        self.mainsizer.Add ( self.downsizer, 0, wx.ALL, 20 )
 
        self.SetSizer ( self.mainsizer )
        
        self.Show()

    def process_click ( self, event ):
        op ( self.gen_news[1][event.EventObject.GetSelection()-1] )

    def press_an ( self, event ):
        stats ( self, event.EventObject.Name )

    def on_search ( self, event ):
        if data.check_validity ( event.EventObject.GetValue() ):
            try:
                stats ( self, event.EventObject.GetValue() + " " + str ( data.get_current ( event.EventObject.GetValue() ) ) )
            except:
                wx.MessageBox ( "The entered stock does not exist.", "Stock Code Not Found", wx.OK | wx.ICON_ERROR )
        else:
            wx.MessageBox ( "The entered stock does not exist.", "Stock Code Not Found", wx.OK | wx.ICON_ERROR )
        event.EventObject.SetValue("")

class Window ( wx.Frame ):
    def __init__ ( self ):
        wx.Frame.__init__ ( self, parent = None, title = "StockIQ" )
        self.SetIcon ( wx.Icon ( "./logo.ico" ) )
        self.Maximize ( True )

        global p
        global ref
        p = self
        ref = self.refresh
        
        self.p = panel(self)
        self.Show()

    def refresh ( self, event ):
        self.p.Destroy()
        self.p = panel ( self )
        self.Layout()

if __name__ == "__main__":
    app = wx.App()
    window = Window()
    app.MainLoop()
