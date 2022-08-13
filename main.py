import kivy
import file_api
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
Window.clearcolor = (44/255, 208/255, 245/255, 1)
def is_on_search_page_setter(x):
    global is_on_search_page
    is_on_search_page=x
    return None
def current_customer_nuller():
    global current_customer
    current_customer=None
    return None
def show_customer_pg(customer_name):
    global current_page
    global customer_pg
    global current_customer
    current_customer=customer_name
    customer_pg=customer_page(customer_name)
    upper_grid.clear_widgets()
    upper_grid.add_widget(Label(text=customer_name,bold=True,font_size=32))
    pg.clear_widgets()
    pg.add_widget(customer_pg)
    lower_grid.remove_widget(add_customer_box)
    lower_grid.add_widget(add_entry_box)
    return None
def home_btn_func():
    pg.remove_widget(current_page)
    pg.add_widget(main_pg)
    customer_type_setter(None)
def customer_type_setter(x):
    global current_customer_type
    current_customer_type=x
    return None
def add_customer(self):
    global current_customer_type
    customer_name=add_customer_box.customer_bar.text
    if (customer_name==""):
        add_customer_box.customer_bar.text="Lütfen geçerli isim girin!!!"
        return None
    if current_customer_type=="e":
        if customer_name in file_api.Export_list:
            add_customer_box.customer_bar.text="Zaten öyle müşteri var!!!"
            return None
        customer_id=f"i{len(file_api.Export_list)}"
        file_api.Export_list[customer_name]=customer_id
        file_api.update_export()
        file_api.create_new_customer_dirs(customer_id=customer_id,customer_type="e")
        export_pg.grid.add_widget(customer_box(customer_name))
    elif (current_customer_type=="d"):
        if customer_name in file_api.Domestic_list:
            add_customer_box.customer_bar.text="Zaten öyle müşteri var!!!"
            return None
        customer_id=f"y{len(file_api.Domestic_list)}"
        file_api.Domestic_list[customer_name]=customer_id
        file_api.update_domestic()
        file_api.create_new_customer_dirs(customer_id=customer_id,customer_type="d")
        domestic_pg.grid.add_widget(customer_box(customer_name))
def add_entry(entry):
    global current_customer
    if current_customer_type=="e":
        customer_id=file_api.Export_list[current_customer]
    elif current_customer_type=="d":
        customer_id=file_api.Domestic_list[current_customer]
    customer_pg.grid.add_widget(sevkiyat_box((len(customer_pg.sevkiyatlistesi)+1),entry))
    customer_pg.sevkiyatlistesi.append(entry)
    file_api.update_customer_entries(customer_id,entry,current_customer_type)
    return None
def search(keyword_to_search):
    global current_customer_type
    search_results=list()
    if current_customer_type=="e":
        for customer in file_api.Export_list.keys():
            if keyword_to_search in customer:
                search_results.append(customer)
    elif current_customer_type=="d":
        for customer in file_api.Domestic_list.keys():
            if keyword_to_search in customer:
                search_results.append(customer)
    search_pg=name_pages("s",search_results)
    pg.clear_widgets()
    pg.add_widget(search_pg)
    is_on_search_page_setter(True)    
def open_file_location(customer_name):
    global current_customer_type
    if current_customer_type=="e":
        customer_id=file_api.Export_list[customer_name]
    elif current_customer_type=="e":
        customer_id=file_api.Domestic_list[customer_name]
    file_api.open_loc(customer_id)
    return None
def delete_customer_btn(self):
    global customer_box_in_question
    customer_box_in_question=self.parent
    customer_box_in_question.remove_widget(customer_box_in_question.del_btn)
    yes_no_grid=GridLayout(cols=1,rows=2,size_hint_x=0.1)
    yes_btn=Button(background_color=(1,0,0,1),font_size=18,text="Yes delete", size_hint_y=0.3)
    yes_btn.bind(on_press=lambda x:delete_customer(customer_box_in_question.customer_name,customer_box_in_question))
    no_btn=Button(font_size=18,text="Return back",size_hint_y=0.6)
    no_btn.bind(on_press=lambda x:return_delete_btn(customer_box_in_question,yes_no_grid))
    yes_no_grid.add_widget(yes_btn)
    yes_no_grid.add_widget(no_btn)
    customer_box_in_question.add_widget(yes_no_grid)
def delete_customer(customer_name,customer_box_in_question):
    global current_customer_type
    global domestic_pg
    global export_pg
    global is_on_search_page
    if current_customer_type=="e":
        customer_id=file_api.Export_list[customer_name]
        del file_api.Export_list[customer_name]
        file_api.update_export()
        export_pg=name_pages("e")
        if(is_on_search_page):
            search_pg.remove_widget(customer_box_in_question)
            pg.clear_widgets()
            pg.add_widget(search_pg)
        else:
            pg.clear_widgets()
            pg.add_widget(export_pg)
    elif current_customer_type=="d":
        customer_id=file_api.Domestic_list[customer_name]
        del file_api.Domestic_list[customer_name]
        file_api.update_domestic()
        domestic_pg=name_pages("d")
        if(is_on_search_page):
            search_pg.remove_widget(customer_box_in_question)
            pg.clear_widgets()
            pg.add_widget(search_pg)
        else:
            pg.clear_widgets()
            pg.add_widget(domestic_pg)
    file_api.remove_customer_files(customer_id)
    
def return_delete_btn(customer_box_in_question,yes_no_grid):
    customer_box_in_question.remove_widget(yes_no_grid)
    customer_box_in_question.add_widget(customer_box_in_question.del_btn)
    return None
class main_page(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=2
        self.rows=1
        self.btn1=Button(font_size=24,text="Customers")
        self.btn1.bind(on_press=lambda x:pg.clear_widgets() or pg.add_widget(customer_type_pg))
        self.add_widget(self.btn1)
class customer_type_page(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=2
        self.rows=1
        self.btn1=Button(font_size=24,text="Domestic")
        self.btn2=Button(font_size=24,text="Export")
        self.btn1.bind(on_press=lambda x:pg.clear_widgets() or pg.add_widget(domestic_pg) or customer_type_setter("d") or upper_grid.add_widget(searchbox) or lower_grid.add_widget(add_customer_box))
        self.btn2.bind(on_press=lambda x:pg.clear_widgets() or pg.add_widget(export_pg) or customer_type_setter("e") or upper_grid.add_widget(searchbox) or lower_grid.add_widget(add_customer_box))
        self.add_widget(self.btn1)
        self.add_widget(self.btn2)
class name_pages(ScrollView):
        def __init__(self,customer_type ,customer_list=[],**kwargs):
            super().__init__(**kwargs)
            self.size=(Window.width,Window.height)
            self.bar_width=12
            self.bar_color = [255, 0, 255, 1]
            self.grid=GridLayout(cols=1,size_hint_y=None)
            self.grid.bind(minimum_height = self.grid.setter("height"))
            if(customer_type=="d"):
                self.domesticcustomers=file_api.Domestic_list.keys()
                for i in self.domesticcustomers:    
                    self.grid.add_widget(customer_box(i))
            elif(customer_type=="e"):
                self.exportcustomers=file_api.Export_list.keys()
                for i in self.exportcustomers:    
                    self.grid.add_widget(customer_box(i))
            elif(customer_type=="s"):
                for customer in customer_list:
                    self.grid.add_widget(customer_box(customer))
            self.add_widget(self.grid)
class customer_box(GridLayout):
    def __init__(self,customer_name ,**kwargs):
        super().__init__(**kwargs)
        self.cols=4
        self.rows=1
        self.size_hint_y=None
        self.customer_name=customer_name
        self.add_widget(Label(text=customer_name,size_hint_x=0.5,bold=True,font_size=32))
        self.detail_btn=Button(font_size=24,text="Detaylar",size_hint_x=0.2)
        self.detail_btn.bind(on_press=lambda x: show_customer_pg(customer_name))
        self.add_widget(self.detail_btn)
        self.file_btn=Button(font_size=24,text="Dosyalar",size_hint_x=0.2)
        self.file_btn.bind(on_press=lambda x:open_file_location(customer_name))
        self.del_btn=Button(font_size=24,text="Sil",size_hint_x=0.1)
        self.del_btn.bind(on_press=delete_customer_btn)
        self.add_widget(self.file_btn)
        self.add_widget(self.del_btn)
class sevkiyat_box(GridLayout):
    def __init__(self,sevkiyat_sirasi,sevkiyat_adedi, **kwargs):
        super().__init__(**kwargs)
        self.cols=2
        self.rows=1
        self.size_hint_y=None
        self.add_widget(Label(text=f"{sevkiyat_sirasi}. sevkiyat: ",bold=True,font_size=32))
        self.add_widget(Label(text=str(sevkiyat_adedi),bold=True,font_size=32))
class customer_page(ScrollView):
    def __init__(self,customer_name,**kwargs):
        super().__init__(**kwargs)
        self.size=(Window.width,Window.height)
        self.customer_name=customer_name
        self.bar_width=12
        self.bar_color = [255, 0, 255, 1]
        self.grid=GridLayout(cols=1,size_hint_y=None)
        self.grid.bind(minimum_height = self.grid.setter("height"))
        self.sevkiyatlistesi=file_api.get_shipments(customer_name=customer_name,customer_type=current_customer_type)
        for i,j in enumerate(self.sevkiyatlistesi):
            self.grid.add_widget(sevkiyat_box(i+1,j))
        self.add_widget(self.grid)
class search_widget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=2
        self.rows=1
        self.search_bar=TextInput(size_hint_x=0.7,multiline=False)
        self.search_btn=Button(font_size=24,text="Ara",size_hint_x=0.3)
        self.search_btn.bind(on_press=lambda x:search(self.search_bar.text))
        self.add_widget(self.search_bar)
        self.add_widget(self.search_btn)
class add_customer_widget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=2
        self.rows=1
        self.size_hint_x=0.7
        self.customer_bar=TextInput(size_hint_x=0.7,multiline=False)
        self.add_customer_btn=Button(font_size=24,text="Müşteri Ekle",size_hint_x=0.3)
        self.add_customer_btn.bind(on_press=add_customer)
        self.add_widget(self.customer_bar)
        self.add_widget(self.add_customer_btn)
class add_entry_widget(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=2
        self.rows=1
        self.size_hint_x=0.7
        self.entry_bar=TextInput(size_hint_x=0.7,multiline=False)
        self.add_entry_btn=Button(font_size=24,text="Sevkiyat Ekle",size_hint_x=0.3)
        self.add_entry_btn.bind(on_press=lambda x:add_entry(self.entry_bar.text))
        self.add_widget(self.entry_bar)
        self.add_widget(self.add_entry_btn)
customer_pg=None
current_customer_type=None
current_customer=None
customer_box_in_question=None
is_on_search_page=False
main_pg=main_page()        
export_pg=name_pages("e")
domestic_pg=name_pages("d")
search_pg=name_pages("s")
customer_type_pg=customer_type_page()
pg=GridLayout(cols=2,rows=1,size_hint_y=0.8)
prev_page=main_pg
current_page=main_pg
upper_grid=GridLayout(cols=2,rows=1,size_hint_y=0.1)
lower_grid=GridLayout(cols=2,rows=1,size_hint_y=0.1)
home_btn=Button(font_size=24,text="Ana sayfa",size_hint_x=0.3)
home_btn.bind(on_press = lambda x:pg.clear_widgets() or pg.add_widget(main_pg) or customer_type_setter(None) or upper_grid.clear_widgets() or lower_grid.clear_widgets() or lower_grid.add_widget(home_btn) or current_customer_nuller() or is_on_search_page_setter(False))
lower_grid.add_widget(home_btn)
searchbox=search_widget()
add_customer_box=add_customer_widget()
add_entry_box=add_entry_widget()
class myGL(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows=3
        self.cols=1
        self.spacing=10
        self.add_widget(upper_grid)
        self.add_widget(pg)
        pg.add_widget(main_pg)
        self.add_widget(lower_grid)
main_window=myGL()
class SevkiyatIzleyiciApp(App):
    def build(self):
        return main_window
SevkiyatIzleyiciApp().run()