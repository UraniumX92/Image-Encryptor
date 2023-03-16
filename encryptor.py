from tkinter import *
from tkinter import messagebox as msgbox
from tkinter import filedialog as fd
from webbrowser import open as display_img
import PIL
from PIL import Image,ImageTk
import imgxor
import utils
import os

BACKGROUND = "#191919"
SECONDARY_BG = "#2d2d2d"
SELECTION_COLOR = "#3a3a3a"
SELECTION_BLACK = "black"
WHITE = 'white'
bullet_char = "\u2022"
dfont = "Segoe UI"

class ImageEncryptor(Tk):
    def __init__(self,geometry,icon):
        Tk.__init__(self)
        self.geometry(geometry)
        self._icon = icon
        self.iconbitmap(icon)
        self.key_length = 30
        self.selimg_temp_path = os.path.join(os.getcwd(), "ImageEncryptor_tempfile_sel_img_preview.png")
        self.resimg_temp_path = os.path.join(os.getcwd(), "ImageEncryptor_tempfile_res_img_preview.png")
        self.title("Image Encryptor - App by Syed Usama")
        self.resizable(False,False)
        self.configure(background=BACKGROUND)

        # Variables
        self._sel_img = None
        self._res_img = None
        self._r_op = "resultant"
        self.sp_var = StringVar()
        self.rp_var = StringVar()

        # Creating main Frames
        self.topFrame = Frame(master=self,background=BACKGROUND)
        self.topFrame.pack(fill=BOTH)
        self.bottomFrame = Frame(master=self,background=BACKGROUND)
        self.bottomFrame.pack(fill=BOTH,padx=260,pady=10)

        # Top Frame and widgets
        self.leftFrame = Frame(master=self.topFrame,background=BACKGROUND)
        self.leftFrame.pack(side=LEFT,padx=5,anchor=W)
        self.rightFrame = Frame(master=self.topFrame,background=BACKGROUND)
        self.rightFrame.pack(side=RIGHT,padx=5,anchor=E)

        self.slabel = Label(master=self.leftFrame,text="Selected Image",font=(dfont,14,'bold'),width=30,height=1,background=BACKGROUND,foreground=WHITE)
        self.slabel.pack()
        self.simage_label = Label(master=self.leftFrame, text="Selected image will appear here", width=85, height=25, background=SECONDARY_BG, foreground=WHITE)
        self.simage_label.pack()
        self.spath = Entry(master=self.leftFrame,background=BACKGROUND,textvariable=self.sp_var,foreground=WHITE,font=(dfont,8),state='readonly',readonlybackground=BACKGROUND,width=90,
                           selectbackground=SELECTION_COLOR,borderwidth=0,justify=CENTER)
        self.spath.pack(pady=2)
        self.show_simg_btn = Button(master=self.leftFrame, text="Show image", background=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE, activebackground=SECONDARY_BG, state=DISABLED)
        self.show_simg_btn.pack(pady=2)

        self.rlabel = Label(master=self.rightFrame,text="Resultant Image",font=(dfont,14,'bold'),width=30,height=1,background=BACKGROUND,foreground=WHITE)
        self.rlabel.pack()
        self.rimage_label = Label(master=self.rightFrame, text="Encrypted/Decrypted image will appear here", width=85, height=25, background=SECONDARY_BG, foreground=WHITE)
        self.rimage_label.pack()
        self.rpath = Entry(master=self.rightFrame, background=BACKGROUND,textvariable=self.rp_var, foreground=WHITE,font=(dfont, 8),state='readonly',readonlybackground=BACKGROUND,width=90,
                           selectbackground=SELECTION_COLOR,borderwidth=0,justify=CENTER)
        self.rpath.pack(pady=2)
        self.show_rimg_btn = Button(master=self.rightFrame, text="Show image", background=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE, activebackground=SECONDARY_BG, state=DISABLED)
        self.show_rimg_btn.pack(pady=2)

        # Bottom Frame and widgets
        self.sel_image_button = Button(master=self.bottomFrame, text="Select image", background=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE, activebackground=SECONDARY_BG)
        self.sel_image_button.grid(row=0, column=0, padx=5, pady=5)

        self.rng_button = Button(master=self.bottomFrame, text="Use randomly generated key (recommended)", background=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE, activebackground=SECONDARY_BG)
        self.rng_button.grid(row=0,column=1,padx=5,pady=5,sticky=NW)

        self.custom_key_btn = Button(master=self.bottomFrame, text="Use custom key", background=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE, activebackground=SECONDARY_BG)
        self.custom_key_btn.grid(row=0,column=1,padx=5,pady=5,sticky=NE)

        self.ekey_label = Label(master=self.bottomFrame,background=BACKGROUND,foreground=WHITE,text="Encryption key : ",font=(dfont,10,'bold'))
        self.ekey_label.grid(row=1,column=0,padx=5,pady=5)
        self.ekey = Entry(master=self.bottomFrame,background=SECONDARY_BG,show=utils.bullet_char,disabledbackground=BACKGROUND,disabledforeground=WHITE,foreground=WHITE,width=80,insertbackground=WHITE,
                          readonlybackground=BACKGROUND,selectbackground=SELECTION_BLACK)
        self.ekey.grid(row=1,column=1,padx=5,pady=5,ipady=2)

        self.show_hide_btn = Button(master=self.bottomFrame, text="Show", background=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE, activebackground=SECONDARY_BG)
        self.show_hide_btn.grid(row=1,column=2,padx=5,pady=5)

        self.copy_key_btn = Button(master=self.bottomFrame, text="copy key to clipboard", background=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE, activebackground=SECONDARY_BG)
        self.copy_key_btn.grid(row=2,column=0,padx=5,pady=5)

        self.enc_button = Button(master=self.bottomFrame,text="Encrypt image",background=SECONDARY_BG,foreground=WHITE,activeforeground=WHITE,activebackground=SECONDARY_BG)
        self.enc_button.grid(row=2,column=1,padx=5,pady=5,sticky=W)

        self.dec_button = Button(master=self.bottomFrame, text="Decrypt image", background=SECONDARY_BG,foreground=WHITE, activeforeground=WHITE, activebackground=SECONDARY_BG)
        self.dec_button.grid(row=2, column=1, padx=5, pady=5, sticky=E)

        self.clr_fields_btn = Button(master=self.bottomFrame, text="Clear Fields", background=SECONDARY_BG,foreground=WHITE, activeforeground=WHITE, activebackground=SECONDARY_BG)
        self.clr_fields_btn.grid(row=3,column=0,pady=5,padx=5)

        self.save_rbtn = Button(master=self.bottomFrame, text="Save resultant image", background=SECONDARY_BG, activebackground=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE)
        self.save_rbtn.grid(row=3, column=1, pady=5, padx=5, sticky=E)

        self.save_sbtn = Button(master=self.bottomFrame, text="Save selected image", background=SECONDARY_BG, activebackground=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE)
        self.save_sbtn.grid(row=3,column=1,pady=5,padx=5,sticky=N)

        self.sel_rimg_btn = Button(master=self.bottomFrame, text="Select resultant image", background=SECONDARY_BG, activebackground=SECONDARY_BG, foreground=WHITE, activeforeground=WHITE)
        self.sel_rimg_btn.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        # Assigning commands
        self.sel_image_button['command'] = self.open_image
        self.enc_button['command'] = self.encrypt_image
        self.dec_button['command'] = self.decrypt_image
        self.save_rbtn['command'] = self.save_rimg
        self.save_sbtn['command'] = self.save_simg
        self.sel_rimg_btn['command'] = self.sel_res_img
        self.show_hide_btn['command'] = self.show_hide
        self.rng_button['command'] = self.rng_key
        self.custom_key_btn['command'] = self.cstm_key
        self.copy_key_btn['command'] = self.copy_key
        self.clr_fields_btn['command'] = lambda: self.clear_fields(ask=True)
        self.show_simg_btn['command'] = self.show_simg
        self.show_rimg_btn['command'] = self.show_rimg

        # misc
        self.sel_img = None
        self.res_img = None

        # destruction protocol
        self.protocol("WM_DELETE_WINDOW", self.exit_protocol)


    @property
    def recent_op(self):
        return self._r_op

    @property
    def sel_img(self):
        return self._sel_img

    @property
    def res_img(self):
        return self._res_img

    @sel_img.setter
    def sel_img(self,img):
        self._sel_img = img
        if isinstance(img,Image.Image):
            self.show_simg_btn.configure(state=NORMAL)
            self.enc_button.configure(state=NORMAL)
            self.dec_button.configure(state=NORMAL)
            self.save_sbtn.configure(state=NORMAL)
        else:
            self.show_simg_btn.configure(state=DISABLED)
            self.enc_button.configure(state=DISABLED)
            self.dec_button.configure(state=DISABLED)
            self.save_sbtn.configure(state=DISABLED)

    @res_img.setter
    def res_img(self,img):
        self._res_img = img
        if isinstance(img,Image.Image):
            self.show_rimg_btn.configure(state=NORMAL)
            self.sel_rimg_btn.configure(state=NORMAL)
            self.save_rbtn.configure(state=NORMAL)
        else:
            self.show_rimg_btn.configure(state=DISABLED)
            self.sel_rimg_btn.configure(state=DISABLED)
            self.save_rbtn.configure(state=DISABLED)

    @recent_op.setter
    def recent_op(self, value:str):
        """
        sets the button and labels as recent operation performed on image
        :param value:
        :return: str : recent operation performed
        """
        value = value.lower()
        self.save_rbtn['text'] = self.save_rbtn['text'].replace(self.recent_op, value)
        self.sel_rimg_btn['text'] = self.sel_rimg_btn['text'].replace(self.recent_op,value)
        self._r_op = value

    def clear_fields(self,ask=False):
        """
        Clears image labels and resets the text labels and entry widget and resets img variables to default,

        and deletes the temp images which are located at self.temp_path1 and self.temp_path2

        :return: None
        """
        if ask:
            ask = not msgbox.askyesno(title="Confirmation",message="Are you sure you want to clear all fields?")
        if not ask:
            self.simage_label.configure(image='',width=85,height=25)
            self.simage_label.photo = None
            self.rimage_label.configure(image='', width=85, height=25)
            self.rimage_label.photo = None
            self.slabel['text'] = "Selected Image"
            self.rlabel['text'] = "Resultant Image"
            self.recent_op = "resultant"
            self.sp_var.set("")
            self.rp_var.set("")
            self.sel_img = None
            self.res_img = None
            self.ekey.configure(state=NORMAL)
            self.ekey.delete(0, END)
            if os.path.exists(self.selimg_temp_path):
                os.remove(self.selimg_temp_path)
            if os.path.exists(self.resimg_temp_path):
                os.remove(self.resimg_temp_path)

    def img_resizer(self,img) -> Image.Image:
        """
        Resizes the given image such that image should be able to fit in app's labels

        :param img: PIL.Image.Image
        :return: PIL.Image.Image - resized image
        """
        w, h = img.size
        max_pix = int()
        max_dim = max(w,h)
        min_dim = min(w,h)
        ratio = max_dim / min_dim
        if ratio < 1.1 :
            max_pix = 450
        else:
            if max_dim==h:
                max_pix = 450
            else:
                max_pix = 580
        return imgxor.resizer(img,max_pix)

    def open_image(self):
        """
        Opens and displays image
        :return:
        """
        if self.res_img:
            if msgbox.askyesno(title="Warning",message="Are you sure you want to clear the fields and select new image?"):
                pass
            else:
                return

        file = fd.askopenfilename()
        if file:
            try:
                img = Image.open(file)
                # if image is opened successfully, only then we clear fields
                self.clear_fields()
                img = img.convert(mode="RGB") if img.mode != "RGB" else img
            except PIL.UnidentifiedImageError:
                return msgbox.showerror(title="Error", message="Selected file is not an image file.")
            else:
                w,h = img.size
                resized = self.img_resizer(img)
                self.sel_img = img
                self.slabel['text'] = f"Selected Image - ({w}x{h})"
                tkimg = ImageTk.PhotoImage(resized)
                self.simage_label.configure(image=tkimg,width=resized.width,height=resized.height)
                self.simage_label.photo = tkimg
                self.sp_var.set(file)

    def encrypt_image(self):
        """
        Encrypts the selected image

        :return:
        """
        key = self.ekey.get()
        if not key:
            return msgbox.showinfo(title="Info",message="Key cannot be empty, please enter the key")
        self.rlabel['text'] = "Please wait..."
        self.update_idletasks()
        eimg = imgxor.encrypt_image(self.sel_img,key)
        w,h = eimg.size
        self.res_img = eimg
        resized = self.img_resizer(eimg)
        tkimg = ImageTk.PhotoImage(resized)
        self.rimage_label.configure(image=tkimg,width=resized.width,height=resized.height)
        self.rimage_label.photo = tkimg
        self.recent_op = "encrypted"
        self.rlabel['text'] = f"Encrypted Image - ({w}x{h})"
        self.rp_var.set("")
        self.res_img.save(self.resimg_temp_path)

    def decrypt_image(self):
        """
        Decryptes the selected image

        :return:
        """
        key = self.ekey.get()
        if not key:
            return msgbox.showinfo(title="Info", message="Key cannot be empty, please enter the key")
        self.rlabel['text'] = "Please wait..."
        self.update_idletasks()
        dec_img = imgxor.decrypt_image(self.sel_img,key)
        w,h = dec_img.size
        self.res_img = dec_img
        resized = self.img_resizer(dec_img)
        tkimg = ImageTk.PhotoImage(resized)
        self.rimage_label.configure(image=tkimg,width=resized.width,height=resized.height)
        self.rimage_label.photo = tkimg
        self.recent_op = "decrypted"
        self.rlabel['text'] = f"Decrypted Image - ({w}x{h})"
        self.rp_var.set("")
        self.res_img.save(self.resimg_temp_path)

    def sel_res_img(self):
        """
        Selects the resultant image to perform operations

        :return:
        """
        if self.res_img:
            pass
        else:
            return msgbox.showerror(title="Error",message=f"Select a file and encrypt/decrypt to be able to select the resultant image")

        if msgbox.askyesno(title="Confirmation",message=f"Are you sure you want to select {self.recent_op} image for operations?"):
            self.sel_img = self.res_img
            w,h = self.sel_img.size
            resized = self.img_resizer(self.sel_img)
            tkimg = ImageTk.PhotoImage(resized)
            self.simage_label.configure(image=tkimg,width=resized.width,height=resized.height)
            self.simage_label.photo = tkimg
            self.rimage_label.configure(image='', width=85, height=25)
            self.rimage_label.photo = None
            self.slabel['text'] = f"Selected Image - ({w}x{h})"
            self.rlabel['text'] = f"Resultant Image"
            self.recent_op = "resultant"
            rpath = self.rp_var.get()
            self.rp_var.set("")
            if rpath:
                self.sp_var.set(rpath)
            else:
                self.res_img.save(self.selimg_temp_path)
                self.sp_var.set("")
                self.res_img = None
            if os.path.exists(self.resimg_temp_path):
                os.remove(self.resimg_temp_path)

    def save_rimg(self):
        """
        Saves the resultant image file

        :return:
        """
        file = fd.asksaveasfilename()
        if file:
            name_list = file.split(".")
            name_list.append('png') if name_list[-1] != 'png' else None
            file = ".".join(name_list)
            self.res_img.save(file)
            self.rp_var.set(file)
            if os.path.exists(self.resimg_temp_path):
                os.remove(self.resimg_temp_path)

    def save_simg(self):
        """
        Saves the selected image file

        :return:
        """
        if self.sp_var.get():
            return msgbox.showinfo(title="Info",message=f"Selected image is already saved at {self.sp_var.get()}")
        else:
            file = fd.asksaveasfilename()
            if file:
                name_list = file.split(".")
                name_list.append('png') if name_list[-1] != 'png' else None
                file = ".".join(name_list)
                self.sel_img.save(file)
                self.sp_var.set(file)
                if os.path.exists(self.selimg_temp_path):
                    os.remove(self.selimg_temp_path)

    def copy_key(self):
        """
        Copies key to the clipboard

        :return:
        """
        key = self.ekey.get()
        if key:
            self.clipboard_clear()
            self.clipboard_append(key)

    def rng_key(self):
        """
        sets randomly generated key as value in key entry and disables it

        :return:
        """
        self.ekey.configure(state=NORMAL)
        self.ekey.delete(0,END)
        random_key = utils.get_compact_key(str(utils.random_KeyGen(self.key_length)))
        self.ekey.insert(0,random_key)
        self.ekey.configure(state='readonly')

    def show_simg(self):
        """
        Displays the selected image using webbrowser.open() method. which internally uses the default image viewer to open the image

        :return:
        """
        path = self.selimg_temp_path
        if self.sel_img:
            if os.path.exists(path):
                pass
            else:
                self.sel_img.save(path)
            display_img(path)

    def show_rimg(self):
        """
        Displays the resultant image using webbrowser.open() method. which internally uses the default image viewer to open the image

        :return:
        """
        path = self.resimg_temp_path
        if self.sel_img:
            if os.path.exists(path):
                pass
            else:
                self.sel_img.save(path)
            display_img(path)

    def show_hide(self):
        """
        Command for button which is used to show/hide the key entry text
        :return:
        """
        if self.show_hide_btn['text'] == "Show":
            self.ekey.config(show="")
            self.ekey.update()
            self.show_hide_btn['text'] = "Hide"
        else:
            self.ekey.config(show=utils.bullet_char)
            self.ekey.update()
            self.show_hide_btn['text'] = "Show"

    def cstm_key(self):
        """
        enables key entry and clears the field

        :return:
        """
        if self.ekey['state'] == 'readonly':
            self.ekey.configure(state=NORMAL)
            self.ekey.delete(0,END)

    def exit_protocol(self):
        """
        Protocol function to run before closing the app

        :return: None
        """
        self.clear_fields()
        self.destroy()