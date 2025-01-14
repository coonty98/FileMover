import tkinter as tk
from tkinter import filedialog
import tksheet, re, os, shutil
from collections import defaultdict

window=tk.Tk()

window.title(" FileMover ")

window.geometry("900x500")
introFrame = tk.Frame()
introFrame.grid(column=0,row=0,columnspan=5,padx=10)
introLabel = tk.Label(introFrame,text = """ Welcome to FileMover!
        This program allows the user to quickly move files.
        Simply identify your SOURCE and DESTINATION folders and enter or scan your case numbers.
        The table will display what shade folder each file was placed in.
        Be sure to check that files were assigned the correct shade.
        If no files found, case number added to list on the left. """)

introLabel.grid(column=0,row=0,sticky="w")

shadeguide = {
    'A1': ('A1' ,'1M2', '2L1.5', '2M1', '2R1.5'),
    'A2': ('A2', '2M2'),
    'A3.5': ('A3.5', '3L2.5', '3M3', '3R2.5', '4L2.5', '4M2'),
    'A3': ('A3', '2L2.5', '2M3', '2R2.5'),
    'A4': ('A4', '4M3', '4R2.5', '5M2', '5M3'),
    'B1': ('B1', '1M1'),
    'B2': ('B2'),
    'B3': ('B3'),
    'B4': ('B4'),
    'C1': ('C1', '3M1'),
    'C2': ('C2'),
    'C3': ('C3', '4L1.5'),
    'C4': ('C4', '5M1'),
    'D2': ('D2'),
    'D3': ('D3', '3L1.5', '3M2', '3R1.5', '4M1', '4R1.5'),
    'D4': ('D4'),
    'OM1': ('OM1'),
    'OM2': ('OM2'),
    'OM3': ('OM3'),
    }

tableFrame = tk.Frame()
tableFrame.grid(column=2,row=2,rowspan=10)

sheet = tksheet.Sheet(tableFrame,headers=("Case #","Shade","Filename"),show_row_index=False,default_row_index_width=0,width=650)
sheet.column_width(column=2,width=495)
sheet.column_width(column=0,width=75)
sheet.column_width(column=1,width=75)
sheet.align_columns(columns=0,align="c")
sheet.align_columns(columns=1,align="c")
sheet.grid(column=0,row=0)
sheet.enable_bindings(("single_select","row_select","column_select","column_width_resize","arrowkeys","right_click_popup_menu","rc_select","copy"))

def browseSource():
    global folder_selected_src
    folder_selected_src = filedialog.askdirectory(initialdir="/",title="Select SOURCE folder")
    label_source.configure(text="Source: " + folder_selected_src)
def browseDestination():
    global folder_selected_dest
    folder_selected_dest = filedialog.askdirectory(initialdir="/")
    label_destination.configure(text="Destination: " + folder_selected_dest)
srcdestFrame = tk.Frame(border=1,borderwidth=1,relief="solid")
srcdestFrame.grid(column=0,row=1,sticky="w",padx=10,pady=10,columnspan=3)
button_explore_src = tk.Button(srcdestFrame,text = "Browse Files",command = browseSource)
button_explore_src.grid(column = 0, row = 0)
button_explore_dest = tk.Button(srcdestFrame,text = "Browse Files",command = browseDestination)
button_explore_dest.grid(column = 0, row = 1)
label_source = tk.Label(srcdestFrame,text="Enter Source")
label_source.grid(column=1,row=0,sticky="w")
label_destination = tk.Label(srcdestFrame,text="Enter Destination")
label_destination.grid(column=1,row=1,sticky="w")

entryFrame = tk.Frame()
entryFrame.grid(column=0,row=2,sticky="w",padx=10)
textFrame = tk.Frame()
textFrame.grid(column=0,row=3,rowspan=10,sticky="w",padx=10)

nameEntry = tk.Entry(entryFrame)
nameEntry.grid(column=0,row=0)

textArea = tk.Text(master=entryFrame,height=10,width=15)
textArea.grid(column=0,row=1,pady=20)
textArea.config(state="disabled")

def getInput(event=None):
    caseNumber = nameEntry.get()
    def file_manager(file_source_dir, file_destination_dir):
        file_names = os.listdir(file_source_dir)
        casesFromFiles = []

        for file_name in file_names:
            splitString = str(file_name).split("_")
            casesFromFiles.append(splitString[0])
            
            if file_name.startswith(caseNumber):
                regex = r"_[abcd][1234]\D[5]_|_[abcd][1234]_|_(?:om)[123]_|_[12345][m][123]_|_[234][lr][12]\D[5]_"
                matches = re.finditer(regex, file_name, re.MULTILINE | re.IGNORECASE)
                for match in matches:
                    shade = match.group(0).split('_')
                    shades = str(shade[1]).upper()
                    for key, value in shadeguide.items():
                        if shades in value:
                            x = key
                    if not os.path.isdir(os.path.join(file_destination_dir, x)):
                        os.mkdir(os.path.join(file_destination_dir, x))
                        shutil.move(os.path.join(file_source_dir, file_name), os.path.join(file_destination_dir, x))
                        sheet.insert_row([caseNumber, x, file_name],idx=0)
                    else:
                        shutil.move(os.path.join(file_source_dir, file_name), os.path.join(file_destination_dir, x))
                        sheet.insert_row([caseNumber, x, file_name],idx=0)
        if caseNumber not in casesFromFiles:
            textArea.config(state="normal")
            textArea.insert(tk.END,caseNumber + '\n')
            textArea.config(state="disabled")
    def clear():
        totalRows = sheet.get_total_rows()
        for allrow in range(totalRows):
            sheet.del_row(idx=0)
        textArea.config(state="normal")
        textArea.delete(1.0,tk.END)
        textArea.config(state="disabled")
    
    clearButton=tk.Button(entryFrame,text="Clear",command=clear,bg="silver")
    clearButton.grid(column=1,row=1,sticky="nw")
    
    nameEntry.delete(0,tk.END)
    file_manager(folder_selected_src,folder_selected_dest)
    
window.bind('<Return>', getInput)
button=tk.Button(entryFrame,text="Submit",command=getInput,bg="light green")
button.grid(column=1,row=0,sticky="w")

window.mainloop()