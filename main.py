
import flet as ft
import json
import os

# --- SOFTWARE TO'ANNOO BARATTOOTAA PRO (FLET VERSION) ---

def main(page: ft.Page):
    page.title = "Software To'annoo Barattootaa Pro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20
    
    # Config for Mobile
    page.window_width = 450
    page.window_height = 850

    # --- DATA MANAGEMENT (STRUCTURE) ---
    DB_FILE = "data_final.json"
    students = {}
    subjects = [
        "A/Oromoo", "Ing", "Her", "S/Naannoo", 
        "Gadaa", "Safuu", "Og-Artii", "Amariffa", "Fjq"
    ]

    def load_data():
        nonlocal students
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r") as f:
                try:
                    data = json.load(f)
                    students = {int(k): v for k, v in data.items()}
                except:
                    students = {}
        else:
            students = {}

    def save_data(e=None):
        with open(DB_FILE, "w") as f:
            json.dump(students, f)
        if e:
            page.snack_bar = ft.SnackBar(ft.Text("Odeeffannoon milkiin kuufameera!"), bgcolor=ft.colors.GREEN)
            page.snack_bar.open = True
            page.update()

    load_data()

    # --- NAVIGATION LOGIC ---
    def go_back(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # --- 1. REGISTER (GALMEESSUU) ---
    def ui_register():
        name_ref = ft.TextField(label="Maqaa Guutuu", border_color=ft.colors.BLUE)
        gender_ref = ft.TextField(label="Kornaya (Dhi/Dub)")
        age_ref = ft.TextField(label="Umrii", keyboard_type=ft.KeyboardType.NUMBER)
        grade_ref = ft.TextField(label="Kutaa")
        year_ref = ft.TextField(label="Bara")

        def register_action(e):
            if not name_ref.value:
                name_ref.error_text = "Maqaan hin guutamne!"
                page.update()
                return
            
            new_id = (max(students.keys()) + 1) if students else 1
            students[new_id] = {
                'id': new_id,
                'name': name_ref.value,
                'gender': gender_ref.value,
                'age': age_ref.value,
                'grade': grade_ref.value,
                'year': year_ref.value,
                'scores': {
                    'sem1': {s: 0 for s in subjects},
                    'sem2': {s: 0 for s in subjects}
                }
            }
            save_data()
            page.snack_bar = ft.SnackBar(ft.Text(f"Barataan ID {new_id} galmaa'eera!"))
            page.snack_bar.open = True
            page.go("/")

        page.views.append(
            ft.View("/register", [
                ft.AppBar(title=ft.Text("Barattoota Galmeessuu"), bgcolor=ft.colors.BLUE_700, color="white"),
                ft.Column([
                    ft.Text("Odeeffannoo Barataa Haaraa", size=18, weight="bold"),
                    name_ref, gender_ref, age_ref, grade_ref, year_ref,
                    ft.ElevatedButton("GALMEESSI", on_click=register_action, bgcolor=ft.colors.GREEN, color="white", width=400, height=50),
                    ft.TextButton("DUUBATTI DEEBI'I", on_click=go_back)
                ], spacing=15, scroll=ft.ScrollMode.ALWAYS)
            ])
        )
        page.update()

    # --- 2. EDIT (ODEERFFANNOO JIJJIIRUU) ---
    def ui_edit():
        id_find = ft.TextField(label="ID Barataa Jijjiramaa", keyboard_type=ft.KeyboardType.NUMBER)
        edit_container = ft.Column()

        def load_for_edit(e):
            try:
                sid = int(id_find.value)
                if sid in students:
                    st = students[sid]
                    edit_container.controls.clear()
                    n_e = ft.TextField(label="Maqaa", value=st['name'])
                    g_e = ft.TextField(label="Kutaa", value=st['grade'])
                    y_e = ft.TextField(label="Bara", value=st['year'])
                    
                    def update_done(e):
                        students[sid]['name'] = n_e.value
                        students[sid]['grade'] = g_e.value
                        students[sid]['year'] = y_e.value
                        save_data(True)
                        page.go("/")

                    edit_container.controls.extend([n_e, g_e, y_e, ft.ElevatedButton("JIJJIRAA FEE'I", on_click=update_done, bgcolor=ft.colors.AMBER_800, color="white")])
                    page.update()
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("ID hin argamne!"))
                    page.snack_bar.open = True
                    page.update()
            except: pass

        page.views.append(
            ft.View("/edit", [
                ft.AppBar(title=ft.Text("Odeeffannoo Jijjiruu"), bgcolor=ft.colors.AMBER_700),
                id_find, ft.ElevatedButton("BARATAA BARBAADI", on_click=load_for_edit),
                edit_container,
                ft.TextButton("DUUBATTI", on_click=go_back)
            ], scroll=ft.ScrollMode.ALWAYS)
        )
        page.update()

    # --- 3. INPUT SCORES (QABXII GALMEESSUU) ---
    def ui_input_scores():
        id_in = ft.TextField(label="ID Barataa Galchi", width=150)
        sem_in = ft.Dropdown(label="Semisterii", options=[ft.dropdown.Option("sem1"), ft.dropdown.Option("sem2")], width=150)
        fields_container = ft.Column()

        def fetch_scores(e):
            try:
                sid = int(id_in.value)
                sem = sem_in.value
                if sid in students and sem:
                    fields_container.controls.clear()
                    fields_container.controls.append(ft.Text(f"Qabxii: {students[sid]['name']} ({sem})", size=16, weight="bold"))
                    
                    score_inputs = {}
                    for s in subjects:
                        val = students[sid]['scores'][sem].get(s, 0)
                        tf = ft.TextField(label=s, value=str(val), width=200, keyboard_type=ft.KeyboardType.NUMBER)
                        fields_container.controls.append(tf)
                        score_inputs[s] = tf
                    
                    def save_scores_action(e):
                        for s, tf in score_inputs.items():
                            students[sid]['scores'][sem][s] = tf.value
                        save_data(True)
                        page.go("/")

                    fields_container.controls.append(ft.ElevatedButton("QABXII KUUSI", on_click=save_scores_action, bgcolor=ft.colors.TEAL, color="white"))
                    page.update()
            except: pass

        page.views.append(
            ft.View("/scores", [
                ft.AppBar(title=ft.Text("Qabxii Galmeessuu"), bgcolor=ft.colors.TEAL_800),
                ft.Row([id_in, sem_in, ft.IconButton(ft.icons.SEARCH, on_click=fetch_scores)]),
                fields_container,
                ft.TextButton("DUUBATTI", on_click=go_back)
            ], scroll=ft.ScrollMode.ALWAYS)
        )
        page.update()

    # --- 5 & 6. ANALYSIS & VIEW ALL ---
    def ui_view_all():
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Maqaa")),
                ft.DataColumn(ft.Text("Kutaa")),
                ft.DataColumn(ft.Text("Sem1 Total")),
            ],
            rows=[]
        )

        for sid, st in students.items():
            s1_total = sum([float(v) for v in st['scores']['sem1'].values()])
            table.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(sid))),
                ft.DataCell(ft.Text(st['name'])),
                ft.DataCell(ft.Text(st['grade'])),
                ft.DataCell(ft.Text(str(s1_total))),
            ]))

        page.views.append(
            ft.View("/view_all", [
                ft.AppBar(title=ft.Text("Tarree Barattootaa"), bgcolor=ft.colors.BLUE_GREY_700),
                ft.Column([table], scroll=ft.ScrollMode.ALWAYS, expand=True),
                ft.TextButton("DUUBATTI", on_click=go_back)
            ])
        )
        page.update()

    # --- 8. DELETE (ODEERFFANNOO HAQUU) ---
    def ui_delete():
        id_del = ft.TextField(label="ID Barataa Haquu Galchi")
        def delete_now(e):
            try:
                sid = int(id_del.value)
                if sid in students:
                    del students[sid]
                    save_data(True)
                    page.go("/")
            except: pass

        page.views.append(
            ft.View("/delete", [
                ft.AppBar(title=ft.Text("Odeeffannoo Haquu"), bgcolor=ft.colors.RED_800),
                id_del,
                ft.ElevatedButton("HAQUU (DELETE)", bgcolor=ft.colors.RED, color="white", on_click=delete_now),
                ft.TextButton("DUUBATTI", on_click=go_back)
            ])
        )
        page.update()

    # --- KEYBOARD SHORTCUTS (1-9) ---
    def on_keyboard(e: ft.KeyboardEvent):
        if page.route == "/":
            if e.key == "1": ui_register()
            elif e.key == "2": ui_edit()
            elif e.key == "3": ui_input_scores()
            elif e.key == "4" or e.key == "6": ui_view_all()
            elif e.key == "7": save_data(True)
            elif e.key == "8": ui_delete()
            elif e.key == "9": page.window_close()

    page.on_keyboard_event = on_keyboard

    # --- MAIN MENU BUILDER ---
    def build_main_menu():
        page.route = "/"
        page.views.append(
            ft.View("/", [
                ft.AppBar(title=ft.Text("MAIN MENU"), bgcolor=ft.colors.BLUE_GREY_900, color="white", automatically_imply_leading=False),
                ft.Container(
                    content=ft.Column([
                        ft.ElevatedButton("1. Barattoota Galmeessuu", on_click=lambda _: ui_register(), width=380, height=45, icon=ft.icons.PERSON_ADD),
                        ft.ElevatedButton("2. Odeeffannoo Jijjiruu", on_click=lambda _: ui_edit(), width=380, height=45, bgcolor=ft.colors.AMBER_400, color="black"),
                        ft.ElevatedButton("3. Qabxii Galmeessuu", on_click=lambda _: ui_input_scores(), width=380, height=45, bgcolor=ft.colors.TEAL_400, color="white"),
                        ft.ElevatedButton("4. Kuusaa Qabxii Ilaaluu", on_click=lambda _: ui_view_all(), width=380, height=45, bgcolor=ft.colors.PURPLE_400, color="white"),
                        ft.ElevatedButton("5. Qaacceessa Qabxii", on_click=lambda _: ui_view_all(), width=380, height=45, bgcolor=ft.colors.ORANGE_400, color="white"),
                        ft.ElevatedButton("6. Barattoota Hunda Ilaaluu", on_click=lambda _: ui_view_all(), width=380, height=45, bgcolor=ft.colors.BLUE_GREY_400, color="white"),
                        ft.ElevatedButton("7. Odeeffannoo Kuusuu (Save)", on_click=save_data, width=380, height=45, bgcolor=ft.colors.GREEN_400, color="white"),
                        ft.ElevatedButton("8. Odeeffannoo Haquu", on_click=lambda _: ui_delete(), width=380, height=45, bgcolor=ft.colors.RED_400, color="white"),
                        ft.ElevatedButton("9. Sagantaa Cufi", on_click=lambda _: page.window_close(), width=380, height=45, bgcolor=ft.colors.GREY_400, color="black"),
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    padding=20,
                    alignment=ft.alignment.center
                )
            ])
        )
        page.update()

    page.on_route_change = lambda _: page.update()
    build_main_menu()

# --- RUN APP ---
ft.app(target=main)
