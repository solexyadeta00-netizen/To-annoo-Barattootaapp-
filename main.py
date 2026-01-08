
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import json
import os

class SoftwareBarataaPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Software To'annoo Barattootaa Pro")
        self.root.geometry("600x800")
        self.root.configure(bg="#f4f7f6")
        
        self.students = {}
        self.subjects = ["A/Oromoo", "Ing", "Her", "S/Naannoo", "Gadaa", "Safuu", "Og-Artii", "Amariffa", "Fjq"]
        
        if os.path.exists("data_final.json"):
            with open("data_final.json", "r") as f:
                data = json.load(f)
                self.students = {int(k): v for k, v in data.items()}

        self.main_menu()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_frame()
        header = tk.Frame(self.root, bg="#2c3e50", height=100)
        header.pack(fill=tk.X)
        tk.Label(header, text="MAIN MENU", font=("Arial", 24, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)
        
        btn_frame = tk.Frame(self.root, bg="#f4f7f6")
        btn_frame.pack(pady=20)

        menus = [
            ("1. Barattoota Galmeessuu", "#3498db", self.ui_register),
            ("2. Odeeffannoo Jijjiruu", "#f1c40f", self.ui_edit),
            ("3. Qabxii Galmeessuu", "#1abc9c", self.ui_input_scores),
            ("4. Kuusaa Qabxii Ilaaluu", "#9b59b6", self.ui_archive),
            ("5. Qaacceessa Qabxii", "#e67e22", self.ui_analysis_main),
            ("6. Barattoota Hunda Ilaaluu", "#34495e", self.ui_view_all),
            ("7. Odeeffannoo Kuusuu (Save)", "#2ecc71", self.save_data),
            ("8. Odeeffannoo Haquu", "#e74c3c", self.ui_delete),
            ("9. Sagantaa Cufi", "#7f8c8d", self.root.quit)
        ]

        for text, color, cmd in menus:
            tk.Button(btn_frame, text=text, command=cmd, width=40, bg=color, fg="white", 
                      font=("Arial", 11, "bold"), pady=10, relief=tk.FLAT, cursor="hand2").pack(pady=5)

    # --- 1. Galmeessuu ---
    def ui_register(self):
        self.clear_frame()
        tk.Label(self.root, text="Barattoota Galmeessuu", font=("Arial", 18, "bold"), bg="#f4f7f6").pack(pady=20)
        fields = ["Maqaa", "Korn (Dhi/Dub)", "Umrii", "Kutaa", "Bara"]
        ents = {}
        for f in fields:
            f_row = tk.Frame(self.root, bg="#f4f7f6")
            f_row.pack(pady=5)
            tk.Label(f_row, text=f"{f}:", width=15, anchor="w", bg="#f4f7f6").pack(side=tk.LEFT)
            e = tk.Entry(f_row, font=("Arial", 12)); e.pack(side=tk.RIGHT)
            ents[f] = e
        
        def save():
            new_id = len(self.students) + 1
            self.students[new_id] = {
                'id': new_id, 'name': ents["Maqaa"].get(), 'gender': ents["Korn (Dhi/Dub)"].get(),
                'age': ents["Umrii"].get(), 'grade': ents["Kutaa"].get(), 'year': ents["Bara"].get(),
                'scores': {'sem1': {s: 0 for s in self.subjects}, 'sem2': {s: 0 for s in self.subjects}}
            }
            messagebox.showinfo("Milkii", f"Barataan ID {new_id} galmaa'eera")
            self.main_menu()
        tk.Button(self.root, text="GALMEESSI", bg="#2ecc71", fg="white", command=save, pady=10, width=20).pack(pady=20)
        tk.Button(self.root, text="DEEBI'I", command=self.main_menu).pack()

    # --- 2. Edit (Jijjiruu) ---
    def ui_edit(self):
        self.clear_frame()
        tk.Label(self.root, text="Odeeffannoo Jijjiruu", font=("Arial", 18, "bold"), bg="#f4f7f6").pack(pady=20)
        tk.Label(self.root, text="ID Barataa:").pack()
        e_id = tk.Entry(self.root); e_id.pack()

        def edit_win():
            sid = int(e_id.get())
            if sid in self.students:
                win = tk.Toplevel(self.root); win.geometry("400x500")
                std = self.students[sid]
                ents = {}
                for k in ['name', 'gender', 'age', 'grade', 'year']:
                    tk.Label(win, text=k).pack(); e = tk.Entry(win); e.insert(0, std[k]); e.pack(); ents[k] = e
                
                tk.Label(win, text="Sem (sem1/sem2)").pack(); e_sem = tk.Entry(win); e_sem.pack()
                tk.Label(win, text="Gosa Barnootaa").pack(); e_sub = tk.Entry(win); e_sub.pack()
                tk.Label(win, text="Qabxii Haaraa").pack(); e_scr = tk.Entry(win); e_scr.pack()

                def update():
                    for k, e in ents.items(): std[k] = e.get()
                    if e_sem.get() and e_sub.get():
                        std['scores'][e_sem.get()][e_sub.get()] = float(e_scr.get())
                    messagebox.showinfo("Milkii", "Jijjiramni kuufameera"); win.destroy()
                tk.Button(win, text="UPDATE", command=update, bg="blue", fg="white").pack(pady=10)
            else: messagebox.showerror("Error", "ID hin jiru")
        tk.Button(self.root, text="Jijjiri", command=edit_win, bg="#f1c40f").pack(pady=10)
        tk.Button(self.root, text="Deebi'i", command=self.main_menu).pack()

    # --- 3. Qabxii (Empty 0) ---
    def ui_input_scores(self):
        self.clear_frame()
        tk.Label(self.root, text="Qabxii Galmeessuu", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self.root, text="ID Barataa:").pack(); e_id = tk.Entry(self.root); e_id.pack()
        tk.Label(self.root, text="Semister (sem1/sem2):").pack(); e_sem = tk.Entry(self.root); e_sem.pack()

        def open_scr():
            sid = int(e_id.get()); sem = e_sem.get().lower()
            if sid in self.students:
                win = tk.Toplevel(self.root); win.title(f"ID: {sid}")
                scr_ents = {}
                for s in self.subjects:
                    r = tk.Frame(win); r.pack()
                    tk.Label(r, text=s, width=15).pack(side=tk.LEFT)
                    e = tk.Entry(r); val = self.students[sid]['scores'][sem][s]
                    if val != 0: e.insert(0, str(val)) # 0 Haqamee jira
                    e.pack(side=tk.RIGHT); scr_ents[s] = e
                def save():
                    for s in self.subjects: 
                        self.students[sid]['scores'][sem][s] = float(scr_ents[s].get() or 0)
                    messagebox.showinfo("Ok", "Qabxiin kuufameera"); win.destroy()
                tk.Button(win, text="KUUSI", command=save, bg="green", fg="white").pack()
            else: messagebox.showerror("Err", "ID hin jiru")
        tk.Button(self.root, text="QABXII GALCHI", command=open_scr, bg="#1abc9c").pack(pady=10)
        tk.Button(self.root, text="Deebi'i", command=self.main_menu).pack()

    # --- 4. Archive (Sem1, Sem2, Total) ---
    def ui_archive(self):
        self.clear_frame()
        tk.Label(self.root, text="Kuusaa Qabxii", font=("Arial", 18, "bold")).pack()
        tk.Label(self.root, text="Kutaa:").pack(); e_g = tk.Entry(self.root); e_g.pack()
        tk.Label(self.root, text="Bara:").pack(); e_y = tk.Entry(self.root); e_y.pack()

        def show():
            win = tk.Toplevel(self.root); win.geometry("500x700")
            txt = scrolledtext.ScrolledText(win, font=("Courier", 10))
            txt.pack(fill=tk.BOTH, expand=True)
            g, y = e_g.get(), e_y.get()
            peers = [i for i, s in self.students.items() if s['grade'] == g and s['year'] == y]
            
            # Ranking (Sem1 + Sem2)
            rank_data = []
            for i in peers:
                t = sum(self.students[i]['scores']['sem1'].values()) + sum(self.students[i]['scores']['sem2'].values())
                rank_data.append((i, t))
            rank_data.sort(key=lambda x: x[1], reverse=True)
            ranks = {sid: r for r, (sid, tot) in enumerate(rank_data, 1)}

            for i in peers:
                s = self.students[i]; s1 = s['scores']['sem1']; s2 = s['scores']['sem2']
                txt.insert(tk.END, f"ID: {i} | Maqaa: {s['name']} | Korn: {s['gender']} | Umrii: {s['age']}\n{'-'*50}\n")
                txt.insert(tk.END, f"{'Subject':<15} | {'Sem1':<6} | {'Sem2':<6} | {'Total':<6}\n")
                for sub in self.subjects:
                    v1, v2 = s1[sub], s2[sub]
                    txt.insert(tk.END, f"{sub:<15} | {v1:<6} | {v2:<6} | {v1+v2:<6}\n")
                t_total = sum(s1.values()) + sum(s2.values())
                avg = round(t_total / (len(self.subjects)*2), 2)
                txt.insert(tk.END, f"\nSem1 Tot={sum(s1.values())} | Sem2 Tot={sum(s2.values())}\n")
                txt.insert(tk.END, f"Ida'ama Waliigalaa = {t_total}\nAvg = {avg}\nSadarkaa = {ranks[i]}\n{'='*50}\n\n")

        tk.Button(self.root, text="ILAALI", command=show, bg="#9b59b6", fg="white").pack(pady=10)
        tk.Button(self.root, text="Deebi'i", command=self.main_menu).pack()

    # --- 5. Analysis Sub-Menus ---
    def ui_analysis_main(self):
        self.clear_frame()
        tk.Label(self.root, text="Qaacceessa Qabxii", font=("Arial", 20, "bold"), bg="#f4f7f6").pack(pady=20)
        tk.Label(self.root, text="Kutaa:").pack(); e_g = tk.Entry(self.root); e_g.pack()
        tk.Label(self.root, text="Bara:").pack(); e_y = tk.Entry(self.root); e_y.pack()

        btn_box = tk.Frame(self.root, bg="#f4f7f6")
        btn_box.pack(pady=20)
        
        btns = [
            ("1. Qaacceessa Barattoota fi Barnootaa", "#3498db", lambda: self.logic_ana_1(e_g.get(), e_y.get())),
            ("2. Qaacceessa Barnootaa (Ida/Avg)", "#1abc9c", lambda: self.logic_ana_2(e_g.get(), e_y.get())),
            ("3. Sadarkaa Barattootaa (1-3)", "#f1c40f", lambda: self.logic_ana_3(e_g.get(), e_y.get())),
            ("GARA MAIN MENUTTI", "#7f8c8d", self.main_menu)
        ]
        for t, c, cmd in btns:
            tk.Button(btn_box, text=t, bg=c, fg="white", font=("Arial", 10, "bold"), width=35, pady=8, command=cmd).pack(pady=5)

    def logic_ana_1(self, g, y):
        win = tk.Toplevel(self.root); txt = scrolledtext.ScrolledText(win, width=60)
        txt.pack(fill=tk.BOTH, expand=True)
        peers = [i for i, s in self.students.items() if s['grade'] == g and s['year'] == y]
        
        def mfw(id_list, cond=None):
            d = len([i for i in id_list if self.students[i]['gender'].lower() in ['dhi','m'] and (cond(i) if cond else True)])
            f = len([i for i in id_list if self.students[i]['gender'].lower() in ['dub','f'] and (cond(i) if cond else True)])
            return d, f, d+f

        txt.insert(tk.END, "Baay'ina Barattoota Galma'anii\n")
        d, f, w = mfw(peers); txt.insert(tk.END, f"Dhi={d}\nDub={f}\nW/gala={w}\n{'-'*20}\n")
        
        # Qoramanii (at least one score > 0)
        q_ids = [i for i in peers if sum(self.students[i]['scores']['sem1'].values()) > 0]
        txt.insert(tk.END, "Baay'ina Barattoota Qoramanii\n")
        d, f, w = mfw(q_ids); txt.insert(tk.END, f"Dhi={d}\nDub={f}\nW/gala={w}\n{'-'*20}\n")

        # Kufanii (Avg sem1 < 50)
        k_ids = [i for i in q_ids if (sum(self.students[i]['scores']['sem1'].values())/len(self.subjects)) < 50]
        txt.insert(tk.END, "Baay'ina Barattoota Kufanii\n")
        d, f, w = mfw(k_ids); txt.insert(tk.END, f"Dhi={d}\nDub={f}\nW/gala={w}\n{'-'*20}\n")

        txt.insert(tk.END, "\nQAACCEESSA GOSA BARNOOTAA\n" + "="*30 + "\n")
        for sub in self.subjects:
            txt.insert(tk.END, f"\n{sub.upper()}\n{'_'*15}\n")
            ranges = [("50 gadi", 0, 49), ("50-64", 50, 64), ("65-79", 65, 79), ("80-89", 80, 89), ("90-100", 90, 100)]
            for lbl, low, high in ranges:
                txt.insert(tk.END, f"Baay'ina {lbl} fidanii:\n")
                d, f, w = mfw(q_ids, lambda i: low <= self.students[i]['scores']['sem1'][sub] <= high)
                txt.insert(tk.END, f"      Dhi={d}\n      Dub={f}\n      W/gala={w}\n")

    def logic_ana_2(self, g, y):
        win = tk.Toplevel(self.root); txt = scrolledtext.ScrolledText(win)
        txt.pack(fill=tk.BOTH, expand=True)
        peers = [i for i, s in self.students.items() if s['grade'] == g and s['year'] == y]
        txt.insert(tk.END, f"Qaacceessa Barnootaa Kutaa {g}\n" + "="*30 + "\n")
        for sub in self.subjects:
            total_sum = sum(self.students[i]['scores']['sem1'][sub] for i in peers)
            avg = round(total_sum / len(peers), 2) if peers else 0
            txt.insert(tk.END, f"{sub}\nIda = {total_sum}\nAvg = {avg}\n{'-'*20}\n")

    def logic_ana_3(self, g, y):
        win = tk.Toplevel(self.root); win.geometry("450x600")
        txt = scrolledtext.ScrolledText(win, font=("Arial", 10))
        txt.pack(fill=tk.BOTH, expand=True)
        peers = [i for i, s in self.students.items() if s['grade'] == g and s['year'] == y]
        
        rank_list = []
        for i in peers:
            t = sum(self.students[i]['scores']['sem1'].values()) + sum(self.students[i]['scores']['sem2'].values())
            rank_list.append((i, t))
        rank_list.sort(key=lambda x: x[1], reverse=True)

        txt.insert(tk.END, f"Sadarkaa Barattootaa Kutaa {g} ({y})\n" + "="*40 + "\n")
        # Top 3 Overall
        txt.insert(tk.END, "SADARKAA WALIGALAA (1-3):\n")
        for r, (sid, tot) in enumerate(rank_list[:3], 1):
            s = self.students[sid]
            txt.insert(tk.END, f"{r}. {s['name']}, {s['gender']}, {s['age']}\nIda={tot}\nAvg={round(tot/(len(self.subjects)*2), 2)}\nSad={r}\n{'-'*20}\n")
        
        # Top 3 Girls
        txt.insert(tk.END, "\nSADARKAA SHAMARRANII (1-3):\n")
        girls = [(sid, tot) for sid, tot in rank_list if self.students[sid]['gender'].lower() in ['dub', 'f', 'female']]
        for r, (sid, tot) in enumerate(girls[:3], 1):
            s = self.students[sid]
            txt.insert(tk.END, f"{r}. {s['name']}, {s['gender']}, {s['age']}\nIda={tot}\nAvg={round(tot/(len(self.subjects)*2), 2)}\nSad={r}\n{'-'*20}\n")

    # --- Utility ---
    def save_data(self):
        with open("data_final.json", "w") as f: json.dump(self.students, f)
        messagebox.showinfo("Milkii", "Odeeffannoon hundi kuufameera.")

    def ui_view_all(self):
        win = tk.Toplevel(self.root); txt = scrolledtext.ScrolledText(win)
        txt.pack(); txt.insert(tk.END, "BARATTOOTA HUNDA\n" + "="*30 + "\n")
        for i, s in self.students.items():
            txt.insert(tk.END, f"ID: {i} | {s['name']} | {s['grade']} | {s['year']}\n")

    def ui_delete(self):
        self.clear_frame()
        tk.Label(self.root, text="Odeeffannoo Haquu", font=("Arial", 18, "bold"), fg="red").pack(pady=20)
        tk.Label(self.root, text="ID Barataa:").pack(); e_id = tk.Entry(self.root); e_id.pack()
        
        def del_one():
            sid = int(e_id.get())
            if sid in self.students: 
                del self.students[sid]
                # Auto Re-order IDs
                temp = sorted(self.students.values(), key=lambda x: x['id'])
                self.students = {i+1: {**data, 'id': i+1} for i, data in enumerate(temp)}
                messagebox.showinfo("Ok", "Haqamee ID'n haareffameera.")
            self.main_menu()
        
        tk.Button(self.root, text="Barataa Tokko Haqu", bg="red", fg="white", command=del_one).pack(pady=10)
        tk.Button(self.root, text="Hunda Haqu", bg="black", fg="white", command=lambda:(self.students.clear(), self.main_menu())).pack()
        tk.Button(self.root, text="Deebi'i", command=self.main_menu).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SoftwareBarataaPro(root)
    root.mainloop()
