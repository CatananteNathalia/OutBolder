import tkintermapview
import customtkinter
from PIL import Image
import json


# Definindo uma janela superior customizada que exibirá detalhes de uma rota
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, route_info, main_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_app = main_app

        # Função para centralizar a janela na tela
        def center_screen():
            global screen_height, screen_width, x_cordinate, y_cordinate
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (450 / 2))
            y_cordinate = int((screen_height / 2) - (700 / 2))
            self.geometry("{}x{}+{}+{}".format(450, 700, x_cordinate, y_cordinate))

        # Rótulo exibindo o nome e a dificuldade da rota
        name_label = customtkinter.CTkLabel(self, text=f"{route_info['name']} - {route_info['difficulty']}", font=('Fixedsys', 18))
        name_label.grid(row=0, column=0, padx=20, pady=5)

        # Exibição da imagem da rota
        my_image = customtkinter.CTkImage(light_image=Image.open(route_info['image_path']),
                                          size=(300, 300))

        image_label = customtkinter.CTkLabel(self, image=my_image, text="")
        image_label.grid(row=1, column=0, padx=20, pady=5)

        # Caixa de texto exibindo a descrição da rota
        self.textbox = customtkinter.CTkTextbox(self, width=400, height=100, corner_radius=0, font=('Fixedsys', 15))
        self.textbox.grid(row=2, column=0, padx=20, pady=5)
        self.textbox.insert("0.0", f"{route_info['description']}")

        # Widget do mapa
        map_widget = tkintermapview.TkinterMapView(self, width=500, height=200, corner_radius=0)
        map_widget.grid(row=3, column=0, padx=20, pady=5)

        map_widget.set_position(route_info['latitude'], route_info['longitude'], marker=True)
        map_widget.set_zoom(13)

        # Botão "Voltar"
        back_button = customtkinter.CTkButton(self, text="Voltar", command=self.go_back)
        back_button.grid(row=4, column=0, padx=20, pady=5)

        # Centralizar a janela ao criá-la
        center_screen()

    # Função para retornar à janela principal
    def go_back(self):
        self.destroy()  # Destruir a janela atual
        self.main_app.deiconify()  # Mostrar a janela principal novamente


# Classe para exibir as rotas em um quadro rolável
class Rotas(customtkinter.CTkScrollableFrame):
    def __init__(self, master, main_app, **kwargs):
        super().__init__(master, **kwargs)

        self.main_app = main_app
        file_path = 'trilhas.json'
        with open(file_path, 'r', encoding='utf-8') as json_file:
            self.names_and_images = json.load(json_file)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.buttons = []

    # Função para abrir a janela superior ao clicar em uma rota
    def open_toplevel(self, route_info):
        self.main_app.withdraw()  # Esconder a janela principal
        self.main_app.toplevel_window = ToplevelWindow(route_info, self.main_app, self)  # Passar route_info e main_app para a ToplevelWindow

    # Função para atualizar o conteúdo com base na cidade selecionada
    def update_content(self, selected_city):
        for button in self.buttons:
            button.destroy()

        # Filtrar rotas com base na cidade selecionada
        filtered_routes = [route for route in self.names_and_images if route["city"] == selected_city]

        for i, route_info in enumerate(filtered_routes):
            name = route_info["name"]
            image_path = route_info["image_path"]

            # Criar um objeto PhotoImage a partir do arquivo de imagem
            image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(300, 300))

            font = customtkinter.CTkFont('Fixedsys', 18)

            # Criar um botão com a imagem e vincular a função ao evento de clique
            button = customtkinter.CTkButton(self, text=name, image=image, compound="top",
                                             command=lambda info=route_info: self.open_toplevel(info), font=font)
            button.image = image  # Para evitar a coleta de lixo da imagem
            button.grid(row=i // 1, column=i % 1, padx=10, pady=10)
            self.buttons.append(button)  # Armazenar a referência do botão


# Janela para adicionar uma nova rota
class AddRouteWindow(customtkinter.CTkToplevel):
    def __init__(self, main_app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Adicionar Rota")
        self.main_app = main_app

        # Função para centralizar a janela na tela
        def center_screen():
            global screen_height, screen_width, x_cordinate, y_cordinate
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (320 / 2))
            y_cordinate = int((screen_height / 2) - (300 / 2))
            self.geometry("{}x{}+{}+{}".format(320, 400, x_cordinate+550, y_cordinate))

        center_screen()

        # Criar e posicionar widgets de entrada para as informações da rota
        self.name_entry = customtkinter.CTkEntry(self,  placeholder_text="Nome da Rota", font=('Fixedsys', 12))
        self.name_entry.grid(row=0, column=0, padx=10, pady=10)
        self.description = customtkinter.CTkEntry(self, placeholder_text="descrição", height=100, width= 300, font=('Fixedsys', 12))
        self.description.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        self.difficulty = customtkinter.CTkEntry(self, placeholder_text="dificuldade", font=('Fixedsys', 12))
        self.difficulty.grid(row=0, column=1, padx=10, pady=10)
        self.city = customtkinter.CTkEntry(self, placeholder_text="cidade", font=('Fixedsys', 12))
        self.city.grid(row=3, column=0, padx=10, pady=10)
        self.image = customtkinter.CTkEntry(self, placeholder_text="arquivo de imagem", font=('Fixedsys', 12))
        self.image.grid(row=3, column=1, padx=10, pady=10)
        self.latitude = customtkinter.CTkEntry(self, placeholder_text="latitude", font=('Fixedsys', 12))
        self.latitude.grid(row=4, column=0, padx=10, pady=10)
        self.longitude = customtkinter.CTkEntry(self, placeholder_text="longitude", font=('Fixedsys', 12))
        self.longitude.grid(row=4, column=1, padx=10, pady=10)

        # Criar botões "Salvar Rota" e "Voltar"
        save_button = customtkinter.CTkButton(self, text="Salvar Rota", command=self.save_route)
        save_button.grid(row=6, column=0, padx=10, pady=10)

        back_button = customtkinter.CTkButton(self, text="Voltar", command=self.destroy)
        back_button.grid(row=6, column=1, padx=10, pady=10)

    # Função para salvar a rota
    def save_route(self):
        # Obter informações dos widgets de entrada
        route_info = {
            "name": self.name_entry.get(),
            "image_path": self.image.get(),
            "description": self.description.get(),
            "difficulty": self.difficulty.get(),
            "city": self.city.get(),
            "latitude": float(self.latitude.get()),
            "longitude": float(self.longitude.get()),
        }

        # Carregar dados existentes de trilhas.json
        trilhas_data = self.load_trilhas_data()
        trilhas_data.append(route_info)
        self.save_trilhas_data(trilhas_data)

        print("Salvando rota:", route_info)
        # Adicionar lógica para salvar os dados da rota conforme necessário

        # Fechar a janela AddRouteWindow
        self.destroy()

    # Função para carregar dados de trilhas.json
    def load_trilhas_data(self):
        try:
            with open("trilhas.json", "r", encoding="utf-8") as file:
                trilhas_data = json.load(file)
        except FileNotFoundError:
            trilhas_data = []
        return trilhas_data

    # Função para salvar dados em trilhas.json
    def save_trilhas_data(self, trilhas_data):
        with open("trilhas.json", "w", encoding="utf-8") as file:
            json.dump(trilhas_data, file, indent=2, ensure_ascii=False)


# Classe principal para a aplicação
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("dark")
        self.title("OutBolder")

        # Função para centralizar a janela principal na tela
        def center_screen():
            global screen_height, screen_width, x_cordinate, y_cordinate
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x_cordinate = int((screen_width / 2) - (450 / 2))
            y_cordinate = int((screen_height / 2) - (700 / 2))
            self.geometry("{}x{}+{}+{}".format(450, 700, x_cordinate, y_cordinate))

        center_screen()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Rótulo principal da aplicação
        label = customtkinter.CTkLabel(self, text="OutBolder", font=('Fixedsys', 30))
        label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        font = customtkinter.CTkFont('Fixedsys', 18)

        # Função de retorno para o menu suspenso
        def optionmenu_callback(choice):
            print("Menu suspenso clicado:", choice)
            self.my_frame.update_content(choice)

        # Obter valores das cidades a partir de trilhas.json
        city_values = self.get_city_values_from_trilhas()
        optionmenu_var = customtkinter.StringVar(value="Selecione a cidade")
        optionmenu = customtkinter.CTkOptionMenu(self,
                                                 values= city_values,
                                                 command=optionmenu_callback, font=font, dropdown_hover_color='#1657bb',
                                                 dropdown_fg_color='#212325', corner_radius=10, dropdown_font=font,
                                                 variable=optionmenu_var)

        optionmenu.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # Instanciar e posicionar o quadro de rotas
        self.my_frame = Rotas(master=self, main_app=self, width=300, height=400)
        self.my_frame.grid(row=2, column=0, padx=20, pady=20)
        self.my_frame.update_content("")

        # Botão para adicionar uma nova rota
        add_route_button = customtkinter.CTkButton(self, text="Adicionar nova rota", command=self.open_add_route_window, font=font)
        add_route_button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        self.toplevel_window = None

    # Obter valores das cidades a partir de trilhas.json
    def get_city_values_from_trilhas(self):
        try:
            with open("trilhas.json", "r", encoding="utf-8") as file:
                trilhas_data = json.load(file)
                # Extrair valores únicos de cidade de trilhas_data
                city_values = list(set(route.get("city", "") for route in trilhas_data))
                # Remover valores vazios ou None
                city_values = [city for city in city_values if city]
        except FileNotFoundError:
            city_values = []
        return ["Selecione a cidade"] + sorted(city_values)

    # Abrir a janela para adicionar uma nova rota
    def open_add_route_window(self):
        AddRouteWindow(self)

    # Executar o loop principal da aplicação
    def run(self):
        self.mainloop()


# Instanciar e executar a aplicação
app = App()
app.run()
