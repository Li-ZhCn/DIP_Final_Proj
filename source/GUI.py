import customtkinter
from PIL.Image import open, fromarray, FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM

from skimage import exposure, filters, util, morphology
from numpy import array, max

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("李志成-2022190503030.py")
        self.geometry(f"{900}x{680}")
        self.iconbitmap('assets/image-processing.ico')

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # global setting
        self.button_font = customtkinter.CTkFont(family="微软雅黑", size=14)
        self.tab_font = customtkinter.CTkFont(family="微软雅黑", size=8)
        self.image_font = customtkinter.CTkFont(family="微软雅黑", size=10)

        # global var
        self.history_len = 50
        self.img_path = customtkinter.StringVar()
        self.img_open_default = open('assets/frame.png')
        self.img_origin = customtkinter.CTkImage(light_image=self.img_open_default, size=self.img_open_default.size)
        self.img_processed = customtkinter.CTkImage(light_image=self.img_open_default, size=self.img_open_default.size)
        self.img_processed_list = []

        # menu frame
        self.menu_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.menu_frame, text="MyDIP",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.menu_frame, command=self.choose_image_button_event,
                                                        fg_color='transparent',
                                                        text='选择图片', font=self.image_font,
                                                        image=customtkinter.CTkImage(
                                                            dark_image=open('assets/open-photo.png'),
                                                            size=(48, 48)),
                                                        compound='top', width=96, height=96, corner_radius=24)

        self.sidebar_button_1.grid(row=1, column=0, padx=10, pady=5)

        self.img_path_entry = customtkinter.CTkEntry(self.menu_frame, state='disabled', textvariable=self.img_path)
        self.img_path_entry.grid(row=4, column=0, padx=10, pady=5)

        self.sidebar_button_2 = customtkinter.CTkButton(self.menu_frame, command=self.save_image_button_event,
                                                        fg_color='transparent',
                                                        text='导出图片', font=self.image_font,
                                                        image=customtkinter.CTkImage(
                                                            dark_image=open('assets/save-photo.png'),
                                                            size=(48, 48)),
                                                        compound='top', width=96, height=96, corner_radius=24
                                                        )
        self.sidebar_button_2.grid(row=2, column=0, padx=10, pady=5)

        self.sidebar_button_3 = customtkinter.CTkButton(self.menu_frame, command=self.undo_event, text='撤销',
                                                        fg_color='transparent',
                                                        font=self.image_font,
                                                        image=customtkinter.CTkImage(
                                                            dark_image=open('assets/left-arrow.png'),
                                                            size=(48, 48)),
                                                        compound='top', width=96, height=96, corner_radius=24)
        self.sidebar_button_3.grid(row=3, column=0, padx=10, pady=5)


        # img frame
        self.img_frame = customtkinter.CTkScrollableFrame(self, width=760, corner_radius=5, orientation='horizontal',
                                                          border_width=10)
        self.img_frame.grid(row=0, column=1, sticky="nsew")

        self.label_origin_img = customtkinter.CTkLabel(self.img_frame, text="原始图像", image=self.img_origin,
                                                       compound='top', padx=20, pady=20)
        self.label_origin_img.grid(row=0, column=0, padx=50, pady=20)

        self.label_processed_img = customtkinter.CTkLabel(self.img_frame, text="编辑后图像", image=self.img_processed,
                                                          compound='top', padx=20, pady=20)
        self.label_processed_img.grid(row=0, column=1)


        # tool frame
        self.tool_frame = customtkinter.CTkFrame(self, width=760, corner_radius=0, border_width=0)
        self.tool_frame.grid(row=1, column=1, sticky="nsew")

        self.tool_tabview = customtkinter.CTkTabview(master=self.tool_frame, width=760)
        self.tool_tabview.pack(padx=20, pady=20)
        self.tool_tabview.add("Basic")
        self.tool_tabview.add("Exposure")
        self.tool_tabview.add("Filter")
        self.tool_tabview.add("Morphology")

        # tool basic tab
        # resize
        self.tool_basic_resize_button = customtkinter.CTkButton(self.tool_tabview.tab("Basic"), text="调整大小",
                                                                command=self.resize_button_event)
        self.tool_basic_resize_button.grid(row=0, column=0, padx=10, pady=5)
        self.tool_basic_resize_x_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Basic"), placeholder_text=
        self.img_processed.cget("light_image").size[0])
        self.tool_basic_resize_x_entry.grid(row=0, column=1, padx=10, pady=5)
        self.tool_basic_resize_y_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Basic"), placeholder_text=
        self.img_processed.cget("light_image").size[1])
        self.tool_basic_resize_y_entry.grid(row=0, column=2, padx=10, pady=5)
        # flip
        self.tool_basic_flip_button = customtkinter.CTkButton(self.tool_tabview.tab("Basic"), text="镜像翻转",
                                                              command=self.flip_button_event)
        self.tool_basic_flip_button.grid(row=1, column=0, padx=10, pady=5)
        self.tool_basic_flip_option = customtkinter.CTkOptionMenu(self.tool_tabview.tab("Basic"),
                                                                  values=["左右翻转", "上下翻转"])
        self.tool_basic_flip_option.grid(row=1, column=1, padx=10, pady=5)

        # tool exposure tab
        # equalize_hist
        self.tool_exposure_equalize_hist_button = customtkinter.CTkButton(self.tool_tabview.tab("Exposure"),
                                                                          text="均衡化直方图",
                                                                          command=self.equalize_hist_button_event)
        self.tool_exposure_equalize_hist_button.grid(row=0, column=0, padx=10, pady=5)
        # adjust_gamma
        self.tool_exposure_adjust_gamma_button = customtkinter.CTkButton(self.tool_tabview.tab("Exposure"),
                                                                         text="调整gamma",
                                                                         command=self.adjust_gamma_button_event)
        self.tool_exposure_adjust_gamma_button.grid(row=1, column=0, padx=10, pady=5)
        self.tool_exposure_adjust_gamma_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Exposure"), placeholder_text="default=1")
        self.tool_exposure_adjust_gamma_entry.grid(row=1, column=1, padx=10, pady=5)
        # adjust_log
        self.tool_exposure_adjust_log_button = customtkinter.CTkButton(self.tool_tabview.tab("Exposure"),
                                                                         text="调整log",
                                                                         command=self.adjust_log_button_event)
        self.tool_exposure_adjust_log_button.grid(row=2, column=0, padx=10, pady=5)
        self.tool_exposure_adjust_log_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Exposure"),
                                                                       placeholder_text="default=1")
        self.tool_exposure_adjust_log_entry.grid(row=2, column=1, padx=10, pady=5)
        # adjust_sigmoid
        self.tool_exposure_adjust_sigmoid_button = customtkinter.CTkButton(self.tool_tabview.tab("Exposure"),
                                                                       text="调整对比度",
                                                                       command=self.adjust_sigmoid_button_event)
        self.tool_exposure_adjust_sigmoid_button.grid(row=3, column=0, padx=10, pady=5)
        self.tool_exposure_adjust_sigmoid_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Exposure"),
                                                                     placeholder_text="default=10")
        self.tool_exposure_adjust_sigmoid_entry.grid(row=3, column=1, padx=10, pady=5)

        # tool filter tab
        # butterworth
        self.tool_filter_butterworth_button = customtkinter.CTkButton(self.tool_tabview.tab("Filter"),
                                                                          text="巴特沃斯滤波器",
                                                                          command=self.butterworth_button_event)
        self.tool_filter_butterworth_button.grid(row=0, column=0, padx=10, pady=5)
        self.tool_filter_butterworth_segemented_button = customtkinter.CTkSegmentedButton(self.tool_tabview.tab("Filter"), values=["低通", "高通"])
        self.tool_filter_butterworth_segemented_button.grid(row=0, column=1, padx=10, pady=5)
        self.tool_filter_butterworth_slider = customtkinter.CTkSlider(self.tool_tabview.tab("Filter"), from_=0, to=0.5)
        self.tool_filter_butterworth_slider.grid(row=1, column=1, padx=10, pady=5)
        # sobel
        self.tool_filter_sobel_button = customtkinter.CTkButton(self.tool_tabview.tab("Filter"),
                                                                      text="索贝尔滤波器",
                                                                      command=self.sobel_button_event)
        self.tool_filter_sobel_button.grid(row=2, column=0, padx=10, pady=5)
        # gaussian
        self.tool_filter_gaussian_button = customtkinter.CTkButton(self.tool_tabview.tab("Filter"),
                                                                text="高斯滤波器",
                                                                command=self.gaussian_button_event)
        self.tool_filter_gaussian_button.grid(row=3, column=0, padx=10, pady=5)
        self.tool_filter_gaussian_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Filter"), placeholder_text='sigma')
        self.tool_filter_gaussian_entry.grid(row=3, column=1, padx=10, pady=5)
        # otsu
        self.tool_filter_otsu_button = customtkinter.CTkButton(self.tool_tabview.tab("Filter"),
                                                                   text="OTSU",
                                                                   command=self.otsu_button_event)
        self.tool_filter_otsu_button.grid(row=4, column=0, padx=10, pady=5)
        self.tool_filter_otsu_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Filter"),
                                                                 placeholder_text='size')
        self.tool_filter_otsu_entry.grid(row=4, column=1, padx=10, pady=5)

        # tool morphology tab
        # dilation
        self.tool_morphology_dilation_button = customtkinter.CTkButton(self.tool_tabview.tab("Morphology"),
                                                                      text="膨胀",
                                                                      command=self.dilation_button_event)
        self.tool_morphology_dilation_button.grid(row=0, column=0, padx=10, pady=5)
        self.tool_morphology_dilation_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Morphology"),
                                                             placeholder_text='size')
        self.tool_morphology_dilation_entry.grid(row=0, column=1, padx=10, pady=5)
        # erosion
        self.tool_morphology_erosion_button = customtkinter.CTkButton(self.tool_tabview.tab("Morphology"),
                                                                       text="腐蚀",
                                                                       command=self.erosion_button_event)
        self.tool_morphology_erosion_button.grid(row=1, column=0, padx=10, pady=5)
        self.tool_morphology_erosion_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Morphology"),
                                                                     placeholder_text='size')
        self.tool_morphology_erosion_entry.grid(row=1, column=1, padx=10, pady=5)
        # open
        self.tool_morphology_open_button = customtkinter.CTkButton(self.tool_tabview.tab("Morphology"),
                                                                      text="开操作",
                                                                      command=self.open_button_event)
        self.tool_morphology_open_button.grid(row=2, column=0, padx=10, pady=5)
        self.tool_morphology_open_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Morphology"),
                                                                    placeholder_text='size')
        self.tool_morphology_open_entry.grid(row=2, column=1, padx=10, pady=5)
        # close
        self.tool_morphology_close_button = customtkinter.CTkButton(self.tool_tabview.tab("Morphology"),
                                                                   text="闭操作",
                                                                   command=self.close_button_event)
        self.tool_morphology_close_button.grid(row=3, column=0, padx=10, pady=5)
        self.tool_morphology_close_entry = customtkinter.CTkEntry(self.tool_tabview.tab("Morphology"),
                                                                 placeholder_text='size')
        self.tool_morphology_close_entry.grid(row=3, column=1, padx=10, pady=5)


    def update_list(self):
        list_len = len(self.img_processed_list)
        if list_len > self.history_len:
            self.img_processed_list.pop(0)
            self.update_list()

    def append_img_list(self, img):
        self.img_processed_list.append(img)
        self.update_list()
        print(len(self.img_processed_list))

    def sidebar_button_event(self):
        print("sidebar_button click")

    def choose_image_button_event(self):
        print("choose image")
        img_path_ = customtkinter.filedialog.askopenfilename(
            filetypes=[("BMP", 'bmp'), ("PNG", ".png"), ("GPF", ".gpf"), ("JPG", ".jpg")])
        self.img_path.set(img_path_)
        print(img_path_)
        img_open = open(self.img_path_entry.get())
        print(img_open.size)
        if img_open.size[1] > 256:
            img_open = img_open.resize((256, 256))
        self.img_origin.configure(light_image=img_open, size=img_open.size)
        self.img_processed.configure(light_image=img_open, size=img_open.size)
        self.append_img_list(img_open)

    def save_image_button_event(self):
        print("save")
        file = customtkinter.filedialog.asksaveasfilename(filetypes=[("BMP", 'bmp'), ("PNG", ".png"), ("GPF", ".gpf"), ("JPG", ".jpg")], defaultextension='bmp' )
        img_temp = self.img_processed.cget("light_image")
        img_temp.save(file)

    def undo_event(self):
        if len(self.img_processed_list) < 2:
            print("cannot undo")
            return
        self.img_processed_list.pop()
        img_undo = self.img_processed_list[-1]
        self.img_processed.configure(light_image=img_undo, size=img_undo.size)
        print(len(self.img_processed_list))

    def resize_button_event(self):
        print("resize")
        img_temp = self.img_processed.cget("light_image")
        x = self.tool_basic_resize_x_entry.get()
        y = self.tool_basic_resize_y_entry.get()
        if not x.isdigit():
            x = img_temp.size[0]
        if not y.isdigit():
            y = img_temp.size[0]

        x = int(x)
        y = int(y)

        if x > 0 and y > 0:
            img_temp = img_temp.resize((x, y))
            self.img_processed_undo()
            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.tool_basic_resize_x_entry.configure(placeholder_text=img_temp.size[0])
            self.tool_basic_resize_y_entry.configure(placeholder_text=img_temp.size[1])
            self.append_img_list(img_temp)

    def flip_button_event(self):
        print("flip")
        img_temp = self.img_processed.cget("light_image")
        flip_option = self.tool_basic_flip_option.get()
        if flip_option == "左右翻转":
            self.img_processed.configure(light_image=img_temp.transpose(FLIP_LEFT_RIGHT), size=img_temp.size)
        if flip_option == "上下翻转":
            self.img_processed.configure(light_image=img_temp.transpose(FLIP_TOP_BOTTOM), size=img_temp.size)
        self.append_img_list(img_temp)

    def equalize_hist_button_event(self):
        print("equalize_hist")
        img_temp = self.img_processed.cget("light_image")
        img_np_temp = array(img_temp)
        img_np_temp = exposure.equalize_hist(img_np_temp)
        img_temp = fromarray(img_np_temp * 255)
        self.img_processed.configure(light_image=img_temp, size=img_temp.size)
        self.append_img_list(img_temp)

    def adjust_gamma_button_event(self):
        print("adjust gamma")
        img_temp = self.img_processed.cget("light_image")

        gamma = self.tool_exposure_adjust_gamma_entry.get()
        if gamma.isdigit():
            gamma = float(gamma)
            img_np_temp = array(img_temp)
            img_np_temp = exposure.adjust_gamma(img_np_temp, gamma=gamma, gain=1)
            img_temp = fromarray(img_np_temp * 255)

            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.append_img_list(img_temp)


    def adjust_log_button_event(self):
        print("adjust log")
        img_temp = self.img_processed.cget("light_image")

        gain = self.tool_exposure_adjust_log_entry.get()
        if gain.isdigit():
            gain = float(gain)
            img_np_temp = array(img_temp)
            img_np_temp = exposure.adjust_log(img_np_temp, gain=gain)
            img_temp = fromarray(img_np_temp * 255)

            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.append_img_list(img_temp)


    def adjust_sigmoid_button_event(self):
        print("adjust sigmoid")
        img_temp = self.img_processed.cget("light_image")

        gain = self.tool_exposure_adjust_sigmoid_entry.get()
        if gain.isdigit():
            gain = float(gain)
            img_np_temp = array(img_temp)
            img_np_temp = exposure.adjust_sigmoid(img_np_temp, gain=gain)
            img_temp = fromarray(img_np_temp * 255)

            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.append_img_list(img_temp)


    def butterworth_button_event(self):
        print("butterworth")
        img_temp = self.img_processed.cget("light_image")
        img_np_temp = array(img_temp)

        bw_model_var = self.tool_filter_butterworth_segemented_button.get()
        bw_fc_var = self.tool_filter_butterworth_slider.get()

        if bw_model_var == '低通':
            img_np_temp = filters.butterworth(img_np_temp, high_pass=False, cutoff_frequency_ratio=bw_fc_var)
        elif bw_model_var == '高通':
            img_np_temp = filters.butterworth(img_np_temp, high_pass=True, cutoff_frequency_ratio=bw_fc_var)

        img_temp = fromarray(img_np_temp * 255)

        self.img_processed.configure(light_image=img_temp, size=img_temp.size)
        self.append_img_list(img_temp)

    def sobel_button_event(self):
        print("sobel")
        img_temp = self.img_processed.cget("light_image")
        img_np_temp = array(img_temp)

        img_np_temp = filters.sobel(img_np_temp)

        img_temp = fromarray(img_np_temp * 255)

        self.img_processed.configure(light_image=img_temp, size=img_temp.size)
        self.append_img_list(img_temp)

    def gaussian_button_event(self):
        print("gaussian")
        img_temp = self.img_processed.cget("light_image")
        img_np_temp = array(img_temp)

        sigma = self.tool_filter_gaussian_entry.get()
        if sigma.isdigit():
            sigma = float(sigma)
            img_np_temp = filters.gaussian(img_np_temp, sigma=sigma)

            img_temp = fromarray(img_np_temp * 255)

            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.append_img_list(img_temp)

    def otsu_button_event(self):
        print("otsu")
        img_temp = self.img_processed.cget("light_image")
        img_np_temp = array(img_temp)
        img_np_temp_max = max(img_np_temp)
        img_np_temp = img_np_temp / img_np_temp_max
        img_np_temp = util.img_as_ubyte(img_np_temp)

        size = self.tool_filter_otsu_entry.get()
        if size.isdigit():
            size = float(size)
            disk = morphology.disk(size)
            img_np_temp = filters.rank.otsu(img_np_temp, disk)

            img_temp = fromarray(img_np_temp * 255)

            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.append_img_list(img_temp)

    def dilation_button_event(self):
        print("dilation")
        img_temp = self.img_processed.cget("light_image")
        img_np_temp = array(img_temp)

        size = self.tool_morphology_dilation_entry.get()
        if size.isdigit():
            size = float(size)
            disk = morphology.disk(size)
            img_np_temp = morphology.dilation(img_np_temp, disk)

            img_temp = fromarray(img_np_temp * 255)

            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.append_img_list(img_temp)

    def erosion_button_event(self):
        print("erosion")
        img_temp = self.img_processed.cget("light_image")
        img_np_temp = array(img_temp)

        size = self.tool_morphology_erosion_entry.get()
        if size.isdigit():
            size = float(size)
            disk = morphology.disk(size)
            img_np_temp = morphology.erosion(img_np_temp, disk)

            img_temp = fromarray(img_np_temp * 255)

            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.append_img_list(img_temp)

    def open_button_event(self):
        print("open")
        img_temp = self.img_processed.cget("light_image")
        img_np_temp = array(img_temp)

        size = self.tool_morphology_open_entry.get()
        if size.isdigit():
            size = float(size)
            img_np_temp = morphology.diameter_opening(img_np_temp, diameter_threshold=size)

            img_temp = fromarray(img_np_temp * 255)

            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.append_img_list(img_temp)

    def close_button_event(self):
        print("close")
        img_temp = self.img_processed.cget("light_image")
        img_np_temp = array(img_temp)

        size = self.tool_morphology_open_entry.get()
        if size.isdigit():
            size = float(size)
            img_np_temp = morphology.diameter_closing(img_np_temp, diameter_threshold=size)

            img_temp = fromarray(img_np_temp * 255)

            self.img_processed.configure(light_image=img_temp, size=img_temp.size)
            self.append_img_list(img_temp)


if __name__ == "__main__":
    app = App()
    app.mainloop()
