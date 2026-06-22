import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import threading
import urllib.request
from io import BytesIO
try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:
    PIL_OK = False

try:
    import pygame
    pygame.mixer.init()
    PYGAME_OK = True
except Exception:
    PYGAME_OK = False

# ─── CONFIGURAÇÃO ─────────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "database": "Trabalho-Final",
    "user":     "postgres",
    "password": "ruavagas27"
}

# ─── PALETA ───────────────────────────────────────────────────────────────────
BG       = "#080B12"
SURFACE  = "#111520"
SURFACE2 = "#1C2035"
SURFACE3 = "#252A42"
ACCENT   = "#6C8EF5"
ACCENT2  = "#2DDFA0"
ACCENT3  = "#A78BFA"   # roxo suave
DANGER   = "#F26B6B"
WARN     = "#F5A623"
TEXT     = "#EDF0FA"
SUBTEXT  = "#BCC2DC"
MUTED    = "#6B728F"
BORDER   = "#252A42"
BORDER2  = "#353A5A"

FH  = ("Segoe UI", 20, "bold")
FT  = ("Segoe UI", 13, "bold")   # títulos de painel
FB  = ("Segoe UI", 10)
FSM = ("Segoe UI",  9)
FM  = ("Segoe UI", 11)
FC  = ("Segoe UI", 10, "bold")

# ─── DB ───────────────────────────────────────────────────────────────────────
def con():
    return psycopg2.connect(**DB_CONFIG)

def run(sql, params=(), fetch=False):
    try:
        conn = con()
        cur  = conn.cursor()
        cur.execute(sql, params)
        result = cur.fetchall() if fetch else None
        conn.commit()
        conn.close()
        return result or []
    except Exception as e:
        messagebox.showerror("Erro SQL", str(e))
        return []

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def lighten(h, amt=30):
    r,g,b = int(h[1:3],16), int(h[3:5],16), int(h[5:7],16)
    return f"#{min(r+amt,255):02x}{min(g+amt,255):02x}{min(b+amt,255):02x}"

def darken(h, amt=20):
    r,g,b = int(h[1:3],16), int(h[3:5],16), int(h[5:7],16)
    return f"#{max(r-amt,0):02x}{max(g-amt,0):02x}{max(b-amt,0):02x}"

def lbl(p, t, font=FB, fg=TEXT, bg=None):
    return tk.Label(p, text=t, font=font, fg=fg, bg=bg or p["bg"])

def btn(p, t, color, cmd, width=None):
    """Botão com hover suave e visual premium."""
    is_light = color not in (DANGER, SURFACE2, SURFACE3, WARN, MUTED)
    fg_col   = BG if is_light else TEXT
    hover_col = lighten(color, 28)

    kw = dict(bg=color, fg=fg_col,
              font=FC, relief="flat", cursor="hand2",
              activebackground=hover_col, activeforeground=fg_col,
              padx=14, pady=8, bd=0, command=cmd)
    if width:
        kw["width"] = width
    b = tk.Button(p, text=t, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=hover_col))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def entry_widget(p, ph=""):
    # Frame com borda colorida ao focar
    f = tk.Frame(p, bg=SURFACE3, highlightbackground=BORDER2, highlightthickness=1)
    e = tk.Entry(f, bg=SURFACE3, fg=TEXT, insertbackground=ACCENT,
                 font=FB, relief="flat", bd=7)
    e.pack(fill="x")
    e._ph = ph
    if ph:
        e.insert(0, ph); e.config(fg=MUTED)
        e.bind("<FocusIn>",  lambda ev: (
            (e.delete(0,"end"), e.config(fg=TEXT)) if e.get()==ph else None,
            f.config(highlightbackground=ACCENT, highlightthickness=2)
        ))
        e.bind("<FocusOut>", lambda ev: (
            (e.insert(0,ph), e.config(fg=MUTED)) if e.get()=="" else None,
            f.config(highlightbackground=BORDER2, highlightthickness=1)
        ))
    else:
        e.bind("<FocusIn>",  lambda ev: f.config(highlightbackground=ACCENT, highlightthickness=2))
        e.bind("<FocusOut>", lambda ev: f.config(highlightbackground=BORDER2, highlightthickness=1))
    return f, e

def get_val(e):
    v = e.get().strip()
    return "" if v == getattr(e,"_ph","") else v

def combo_widget(p, values):
    f = tk.Frame(p, bg=SURFACE3, highlightbackground=BORDER2, highlightthickness=1)
    style = ttk.Style(); style.configure("C.TCombobox", fieldbackground=SURFACE3,
        background=SURFACE3, foreground=TEXT, arrowcolor=ACCENT)
    c = ttk.Combobox(f, values=values, state="readonly", style="C.TCombobox",
                     font=FB, foreground=TEXT)
    c.pack(fill="x", padx=1, pady=1)
    return f, c

def tree_style(name="T"):
    s = ttk.Style()
    s.theme_use("clam")
    s.configure(f"{name}.Treeview",
                background=SURFACE, foreground=TEXT,
                fieldbackground=SURFACE, font=FB,
                rowheight=34, borderwidth=0)
    s.configure(f"{name}.Treeview.Heading",
                background=SURFACE2, foreground=ACCENT,
                font=("Segoe UI", 10, "bold"), relief="flat", padding=(8, 6))
    s.map(f"{name}.Treeview",
          background=[("selected", ACCENT3)],
          foreground=[("selected", TEXT)])

def make_tree(parent, cols, widths):
    tree_style()
    tv = ttk.Treeview(parent, columns=cols, show="headings",
                      style="T.Treeview", selectmode="browse")
    for c, w in zip(cols, widths):
        tv.heading(c, text=c)
        tv.column(c, width=w, anchor="w", minwidth=40)
    tv.tag_configure("odd",  background=SURFACE)
    tv.tag_configure("even", background=SURFACE2)
    # Scrollbar estilizada
    style = ttk.Style()
    style.configure("Dark.Vertical.TScrollbar",
                    background=SURFACE3, troughcolor=SURFACE,
                    arrowcolor=MUTED, borderwidth=0, relief="flat")
    sb = ttk.Scrollbar(parent, orient="vertical", command=tv.yview,
                       style="Dark.Vertical.TScrollbar")
    tv.configure(yscrollcommand=sb.set)
    tv.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return tv

def fill_tree(tv, rows):
    tv.delete(*tv.get_children())
    for i, r in enumerate(rows):
        tv.insert("", "end", values=r, tags=("odd" if i%2==0 else "even",))

def _fade_toast(t, steps=8, delay=60):
    """Destrói o toast depois de alguns ms sem depender de alpha no Windows."""
    t.after(2200, t.destroy)

def toast(root, msg, color=ACCENT2):
    t = tk.Toplevel(root)
    t.overrideredirect(True)
    t.attributes("-topmost", True)
    # Fundo com borda
    outer = tk.Frame(t, bg=BORDER2, padx=1, pady=1)
    outer.pack()
    inner = tk.Frame(outer, bg=color, padx=16, pady=10)
    inner.pack()
    # Ícone + mensagem
    icon = "✓" if color == ACCENT2 else ("✕" if color == DANGER else "!")
    tk.Label(inner, text=f"{icon}  {msg}", bg=color,
             fg=BG, font=("Segoe UI", 10, "bold")).pack()
    root.update_idletasks()
    w = t.winfo_reqwidth()
    x = root.winfo_x() + root.winfo_width()  - w - 24
    y = root.winfo_y() + root.winfo_height() - 74
    t.geometry(f"+{x}+{y}")
    _fade_toast(t)

# ─── BASE TAB ─────────────────────────────────────────────────────────────────
class BaseTab(tk.Frame):
    title   = ""
    cols    = []
    widths  = []

    def __init__(self, parent, root):
        super().__init__(parent, bg=BG)
        self.root = root
        self._sel_id   = None
        self._editing  = False
        self._build()

    def _build(self):
        # ── Header da aba ────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=SURFACE, pady=14)
        hdr.pack(fill="x")
        # Barra lateral colorida com gradiente simulado
        accent_bar = tk.Frame(hdr, bg=ACCENT, width=4)
        accent_bar.pack(side="left", fill="y", padx=(20, 0))
        tk.Frame(hdr, bg=ACCENT3, width=2).pack(side="left", fill="y")
        lbl(hdr, self.title, ("Segoe UI", 14, "bold"), TEXT, SURFACE).pack(
            side="left", padx=(14, 0))
        # Badge de contagem
        self._count_frame = tk.Frame(hdr, bg=SURFACE3)
        self._count_frame.pack(side="right", padx=20, pady=4)
        self._lbl_count = tk.Label(self._count_frame, text="", font=FSM,
                                   fg=ACCENT,
                                   bg=SURFACE3, padx=8, pady=2)
        self._lbl_count.pack()

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=14)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)

        # ── Área tabela ──────────────────────────────────────────────────────
        tframe = tk.Frame(body, bg=BG)
        tframe.grid(row=0, column=0, sticky="nsew")
        tframe.rowconfigure(1, weight=1)
        tframe.columnconfigure(0, weight=1)

        # Barra de busca + atualizar
        bar = tk.Frame(tframe, bg=BG)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        bar.columnconfigure(0, weight=1)
        sf, self._search = entry_widget(bar, "🔍  Buscar...")
        sf.grid(row=0, column=0, sticky="ew")
        self._search.bind("<KeyRelease>", lambda e: self._filter())
        btn(bar, "↻  Atualizar", SURFACE3, self.load).grid(row=0, column=1, padx=(10, 0))

        tf = tk.Frame(tframe, bg=BG)
        tf.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self._tv = make_tree(tf, self.cols, self.widths)
        self._tv.bind("<<TreeviewSelect>>", self._on_sel)
        self._tv.bind("<Double-1>", lambda e: self._edit_selected())

        # ── Painel lateral (formulário) ──────────────────────────────────────
        panel = tk.Frame(body, bg=SURFACE, width=272,
                         highlightbackground=BORDER2, highlightthickness=1)
        panel.grid(row=0, column=1, sticky="nsew", padx=(16, 0))
        panel.pack_propagate(False)
        self._build_form(panel)
        self._build_actions(panel)
        self.load()

    def _build_form(self, panel):
        # Cabeçalho do painel
        ph = tk.Frame(panel, bg=SURFACE2, pady=12)
        ph.pack(fill="x")
        tk.Frame(ph, bg=ACCENT, width=3).pack(side="left", fill="y", padx=(14, 0))
        col = tk.Frame(ph, bg=SURFACE2)
        col.pack(side="left", padx=10)
        tk.Label(col, text="Novo registro", font=("Segoe UI", 11, "bold"),
                 fg=TEXT, bg=SURFACE2).pack(anchor="w")
        tk.Label(col, text="Preencha os campos abaixo", font=FSM,
                 fg=MUTED, bg=SURFACE2).pack(anchor="w")

        self._fields = {}
        for name, ph_txt in self.form_fields():
            tk.Label(panel, text=name, font=("Segoe UI", 9, "bold"),
                     fg=MUTED, bg=SURFACE).pack(
                anchor="w", padx=16, pady=(12, 2))
            ff, fe = entry_widget(panel, ph_txt)
            ff.pack(fill="x", padx=16)
            self._fields[name] = fe

        tk.Frame(panel, bg=BORDER2, height=1).pack(fill="x", padx=16, pady=(16, 10))
        self._btn_save = btn(panel, "＋  Adicionar", ACCENT, self._save)
        self._btn_save.pack(fill="x", padx=16, pady=(0, 6))
        self._btn_cancel = btn(panel, "✕  Cancelar", SURFACE3, self._cancel)
        self._btn_cancel.pack(fill="x", padx=16)
        self._btn_cancel.pack_forget()

    def _build_actions(self, panel):
        tk.Frame(panel, bg=BORDER2, height=1).pack(fill="x", padx=16, pady=(14, 10))
        tk.Label(panel, text="AÇÕES", font=("Segoe UI", 8, "bold"),
                 fg=MUTED, bg=SURFACE).pack(anchor="w", padx=16, pady=(0, 8))
        btn(panel, "✏  Editar selecionado",  ACCENT2, self._edit_selected).pack(
            fill="x", padx=16, pady=(0, 6))
        btn(panel, "🗑  Excluir selecionado", DANGER,  self._delete_selected).pack(
            fill="x", padx=16)

    # ── a subclasse define ────────────────────────────────────────────────────
    def form_fields(self): return []          # [(label, placeholder), ...]
    def load(self):        pass
    def insert_record(self, vals): pass
    def update_record(self, id_, vals): pass
    def delete_record(self, id_): pass
    def row_to_form(self, row): return {}     # {label: value}

    # ── lógica comum ─────────────────────────────────────────────────────────
    def _filter(self):
        term = get_val(self._search).lower()
        rows = getattr(self, "_all_rows", [])
        filtered = [r for r in rows if any(term in str(c).lower() for c in r)] if term else rows
        fill_tree(self._tv, filtered)
        self._lbl_count.config(text=f"{len(filtered)} registro(s)")

    def _on_sel(self, _=None):
        sel = self._tv.selection()
        if sel:
            self._sel_id = self._tv.item(sel[0])["values"][0]

    def _edit_selected(self):
        sel = self._tv.selection()
        if not sel:
            messagebox.showinfo("Selecione", "Clique em uma linha primeiro."); return
        row = self._tv.item(sel[0])["values"]
        self._sel_id  = row[0]
        self._editing = True
        mapping = self.row_to_form(row)
        for name, fe in self._fields.items():
            fe.delete(0, "end")
            fe.insert(0, mapping.get(name, ""))
            fe.config(fg=TEXT)
        self._btn_save.config(text="✔  Salvar alterações", bg=ACCENT2)
        self._btn_cancel.pack(fill="x", padx=16)

    def _cancel(self):
        self._editing = False; self._sel_id = None
        for fe in self._fields.values():
            fe.delete(0, "end")
            fe.insert(0, fe._ph); fe.config(fg=MUTED)
        self._btn_save.config(text="＋  Adicionar", bg=ACCENT)
        self._btn_cancel.pack_forget()

    def _save(self):
        vals = {k: get_val(v) for k, v in self._fields.items()}
        if any(v == "" for v in vals.values()):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos."); return
        try:
            if self._editing:
                self.update_record(self._sel_id, vals)
                toast(self.root, "Registro atualizado!")
            else:
                self.insert_record(vals)
                toast(self.root, "Registro adicionado!")
            self._cancel(); self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _delete_selected(self):
        sel = self._tv.selection()
        if not sel:
            messagebox.showinfo("Selecione", "Clique em uma linha primeiro."); return
        row = self._tv.item(sel[0])["values"]
        if messagebox.askyesno("Confirmar", f"Excluir '{row[1]}'?"):
            try:
                self.delete_record(row[0])
                toast(self.root, "Registro removido.", DANGER)
                self.load()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def _set_rows(self, rows):
        self._all_rows = rows
        fill_tree(self._tv, rows)
        self._lbl_count.config(text=f"{len(rows)} registro(s)")

# ═══════════════════════════════════════════════════════════════════════════════
# ABAS CONCRETAS
# ═══════════════════════════════════════════════════════════════════════════════

class TabArtista(BaseTab):
    title  = "🎤  Artistas"
    cols   = ("ID","Nome","Ouvintes/mês","Ano Debut","Gravadora")
    widths = (40, 180, 120, 90, 150)

    def form_fields(self):
        return [("Nome","Nome do artista"),("Ouvintes Mensais","Ex: 1000000"),
                ("Descrição","Descrição"),("Ano Debut","Ex: 2010"),("ID Gravadora","Ex: 1")]

    def load(self):
        rows = run("""SELECT a.id, a.nome, a.ouvintes_mensais, a.ano_debut, g.nome
                      FROM artista a LEFT JOIN gravadora g ON a.id_gravadora=g.id
                      ORDER BY a.id""", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO artista(nome,ouvintes_mensais,descricao,ano_debut,id_gravadora) VALUES(%s,%s,%s,%s,%s)",
            (v["Nome"],v["Ouvintes Mensais"],v["Descrição"],v["Ano Debut"],v["ID Gravadora"]))

    def update_record(self, id_, v):
        run("UPDATE artista SET nome=%s,ouvintes_mensais=%s,descricao=%s,ano_debut=%s,id_gravadora=%s WHERE id=%s",
            (v["Nome"],v["Ouvintes Mensais"],v["Descrição"],v["Ano Debut"],v["ID Gravadora"],id_))

    def delete_record(self, id_):
        run("DELETE FROM artista WHERE id=%s", (id_,))

    def row_to_form(self, row):
        rows2 = run("SELECT descricao,id_gravadora FROM artista WHERE id=%s",(row[0],),fetch=True)
        desc, id_grav = rows2[0] if rows2 else ("","")
        return {"Nome":row[1],"Ouvintes Mensais":str(row[2]),"Descrição":desc,
                "Ano Debut":str(row[3]),"ID Gravadora":str(id_grav)}


class TabAlbum(BaseTab):
    title  = "💿  Álbuns"
    cols   = ("ID","Nome","Lançamento","Faixas","Artista")
    widths = (40, 200, 100, 60, 150)

    def form_fields(self):
        return [("Nome","Nome do álbum"),("Data Lançamento","AAAA-MM-DD"),
                ("Qtd Faixas","Ex: 12"),("ID Artista","Ex: 1"),("ID Capa","Ex: 1")]

    # ── painel direito customizado com capa ───────────────────────────────────
    def _build_form(self, panel):
        self._cover_panel = panel

        # Área da capa
        self._img_frame = tk.Frame(panel, bg=SURFACE3, width=198, height=198,
                                   highlightbackground=BORDER2, highlightthickness=1)
        self._img_frame.pack(padx=16, pady=(16, 0))
        self._img_frame.pack_propagate(False)

        self._img_label = tk.Label(self._img_frame, bg=SURFACE3, fg=MUTED,
                                   font=FB, text="Selecione\num álbum",
                                   justify="center")
        self._img_label.place(relx=0.5, rely=0.5, anchor="center")
        self._img_ref = None

        # Nome e artista abaixo da capa
        self._lbl_album_nome = lbl(panel, "", ("Segoe UI", 10, "bold"), TEXT, SURFACE)
        self._lbl_album_nome.pack(anchor="w", padx=16, pady=(10, 0))
        self._lbl_album_art  = lbl(panel, "", FB, MUTED, SURFACE)
        self._lbl_album_art.pack(anchor="w", padx=16, pady=(2, 10))

        tk.Frame(panel, bg=BORDER2, height=1).pack(fill="x", padx=16, pady=(0, 10))

        # Campos do formulário
        tk.Label(panel, text="Editar / Novo álbum",
                 font=("Segoe UI", 10, "bold"), fg=ACCENT, bg=SURFACE).pack(
            anchor="w", padx=16, pady=(0, 8))
        self._fields = {}
        for name, ph in self.form_fields():
            tk.Label(panel, text=name, font=("Segoe UI", 9, "bold"),
                     fg=MUTED, bg=SURFACE).pack(anchor="w", padx=16, pady=(8, 2))
            ff, fe = entry_widget(panel, ph)
            ff.pack(fill="x", padx=16)
            self._fields[name] = fe

        tk.Frame(panel, bg=BORDER2, height=1).pack(fill="x", padx=16, pady=(14, 8))
        self._btn_save = btn(panel, "＋  Adicionar", ACCENT, self._save)
        self._btn_save.pack(fill="x", padx=16, pady=(0, 6))
        self._btn_cancel = btn(panel, "✕  Cancelar", SURFACE3, self._cancel)
        self._btn_cancel.pack(fill="x", padx=16)
        self._btn_cancel.pack_forget()

    def _build_actions(self, panel):
        tk.Frame(panel, bg=BORDER2, height=1).pack(fill="x", padx=16, pady=(12, 10))
        tk.Label(panel, text="AÇÕES", font=("Segoe UI", 8, "bold"),
                 fg=MUTED, bg=SURFACE).pack(anchor="w", padx=16, pady=(0, 8))
        btn(panel, "✏  Editar selecionado",  ACCENT2, self._edit_selected).pack(
            fill="x", padx=16, pady=(0, 6))
        btn(panel, "🗑  Excluir selecionado", DANGER,  self._delete_selected).pack(
            fill="x", padx=16)

    # ── seleção atualiza capa ─────────────────────────────────────────────────
    def _on_sel(self, _=None):
        sel = self._tv.selection()
        if not sel:
            return
        row = self._tv.item(sel[0])["values"]
        self._sel_id = row[0]
        self._lbl_album_nome.config(text=row[1][:30])
        self._lbl_album_art.config(text=row[4] if len(row) > 4 else "")
        self._load_cover(row[0])

    def _load_cover(self, album_id):
        result = run("""SELECT c.url_imagem FROM album al
                        JOIN capa c ON al.id_capa = c.id
                        WHERE al.id = %s""", (album_id,), fetch=True)
        if not result or not result[0][0]:
            self._img_label.config(image="", text="Sem capa\ndisponível")
            self._img_ref = None
            return

        url = result[0][0]
        self._img_label.config(text="Carregando...", image="")

        def fetch_img():
            try:
                if not PIL_OK:
                    self._img_label.config(text="Instale\npillow")
                    return
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    data = resp.read()
                img = Image.open(BytesIO(data)).resize((198, 198), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self._img_ref = photo
                self._img_label.config(image=photo, text="")
            except Exception:
                self._img_label.config(image="", text="Erro ao\ncarregar")

        threading.Thread(target=fetch_img, daemon=True).start()

    def load(self):
        rows = run("""SELECT al.id, al.nome, al.data_lancamento, al.quantidade_faixas, ar.nome
                      FROM album al LEFT JOIN artista ar ON al.id_artista=ar.id ORDER BY al.id""", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO album(nome,data_lancamento,quantidade_faixas,id_artista,id_capa) VALUES(%s,%s,%s,%s,%s)",
            (v["Nome"],v["Data Lançamento"],v["Qtd Faixas"],v["ID Artista"],v["ID Capa"]))

    def update_record(self, id_, v):
        run("UPDATE album SET nome=%s,data_lancamento=%s,quantidade_faixas=%s,id_artista=%s,id_capa=%s WHERE id=%s",
            (v["Nome"],v["Data Lançamento"],v["Qtd Faixas"],v["ID Artista"],v["ID Capa"],id_))

    def delete_record(self, id_):
        run("DELETE FROM album WHERE id=%s", (id_,))

    def row_to_form(self, row):
        r2 = run("SELECT id_artista,id_capa FROM album WHERE id=%s",(row[0],),fetch=True)
        id_ar, id_ca = r2[0] if r2 else ("","")
        return {"Nome":row[1],"Data Lançamento":str(row[2]),"Qtd Faixas":str(row[3]),
                "ID Artista":str(id_ar),"ID Capa":str(id_ca)}


class TabMusica(BaseTab):
    title  = "🎵  Músicas"
    cols   = ("ID","Nome","Álbum")
    widths = (40, 250, 250)

    def form_fields(self):
        return [("Nome","Nome da música"),("ID Álbum","Ex: 1")]

    def load(self):
        rows = run("""SELECT m.id, m.nome, al.nome
                      FROM musica m LEFT JOIN album al ON m.id_album=al.id ORDER BY m.id""", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO musica(nome,id_album) VALUES(%s,%s)", (v["Nome"],v["ID Álbum"]))

    def update_record(self, id_, v):
        run("UPDATE musica SET nome=%s,id_album=%s WHERE id=%s", (v["Nome"],v["ID Álbum"],id_))

    def delete_record(self, id_):
        run("DELETE FROM musica WHERE id=%s", (id_,))

    def row_to_form(self, row):
        r2 = run("SELECT id_album FROM musica WHERE id=%s",(row[0],),fetch=True)
        return {"Nome":row[1],"ID Álbum":str(r2[0][0]) if r2 else ""}


class TabUsuario(BaseTab):
    title  = "👤  Usuários"
    cols   = ("ID","Nome","Apelido","Plano")
    widths = (40, 160, 140, 160)

    def form_fields(self):
        return [("Nome","Nome do usuário"),("Apelido","@apelido"),("ID Plano","Ex: 1")]

    def load(self):
        rows = run("""SELECT u.id, u.nome, u.apelido, p.nome
                      FROM usuario u LEFT JOIN plano_assinatura p ON u.id_plano_assinatura=p.id
                      ORDER BY u.id""", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO usuario(nome,apelido,id_plano_assinatura) VALUES(%s,%s,%s)",
            (v["Nome"],v["Apelido"],v["ID Plano"]))

    def update_record(self, id_, v):
        run("UPDATE usuario SET nome=%s,apelido=%s,id_plano_assinatura=%s WHERE id=%s",
            (v["Nome"],v["Apelido"],v["ID Plano"],id_))

    def delete_record(self, id_):
        run("DELETE FROM usuario WHERE id=%s", (id_,))

    def row_to_form(self, row):
        r2 = run("SELECT id_plano_assinatura FROM usuario WHERE id=%s",(row[0],),fetch=True)
        return {"Nome":row[1],"Apelido":row[2],"ID Plano":str(r2[0][0]) if r2 else ""}


class TabPlaylist(BaseTab):
    title  = "📋  Playlists"
    cols   = ("ID","Nome","Data Criação","Usuário")
    widths = (40, 180, 110, 160)

    def form_fields(self):
        return [("Nome","Nome da playlist"),("ID Usuário","Ex: 1")]

    def load(self):
        rows = run("""SELECT pl.id, pl.nome, pl.data_criacao, u.nome
                      FROM playlist pl LEFT JOIN usuario u ON pl.id_usuario=u.id ORDER BY pl.id""", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO playlist(nome,id_usuario) VALUES(%s,%s)", (v["Nome"],v["ID Usuário"]))

    def update_record(self, id_, v):
        run("UPDATE playlist SET nome=%s,id_usuario=%s WHERE id=%s", (v["Nome"],v["ID Usuário"],id_))

    def delete_record(self, id_):
        run("DELETE FROM playlist WHERE id=%s", (id_,))

    def row_to_form(self, row):
        r2 = run("SELECT id_usuario FROM playlist WHERE id=%s",(row[0],),fetch=True)
        return {"Nome":row[1],"ID Usuário":str(r2[0][0]) if r2 else ""}


class TabGravadora(BaseTab):
    title  = "🏢  Gravadoras"
    cols   = ("ID","Nome")
    widths = (60, 400)

    def form_fields(self):
        return [("Nome","Nome da gravadora")]

    def load(self):
        rows = run("SELECT id, nome FROM gravadora ORDER BY id", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO gravadora(nome) VALUES(%s)", (v["Nome"],))

    def update_record(self, id_, v):
        run("UPDATE gravadora SET nome=%s WHERE id=%s", (v["Nome"],id_))

    def delete_record(self, id_):
        run("DELETE FROM gravadora WHERE id=%s", (id_,))

    def row_to_form(self, row):
        return {"Nome": row[1]}


class TabGenero(BaseTab):
    title  = "🎸  Gêneros"
    cols   = ("ID","Nome")
    widths = (60, 400)

    def form_fields(self):
        return [("Nome","Nome do gênero")]

    def load(self):
        rows = run("SELECT id, nome FROM genero ORDER BY id", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO genero(nome) VALUES(%s)", (v["Nome"],))

    def update_record(self, id_, v):
        run("UPDATE genero SET nome=%s WHERE id=%s", (v["Nome"],id_))

    def delete_record(self, id_):
        run("DELETE FROM genero WHERE id=%s", (id_,))

    def row_to_form(self, row):
        return {"Nome": row[1]}


class TabPlano(BaseTab):
    title  = "💳  Planos de Assinatura"
    cols   = ("ID","Nome","Valor (R$)","Descrição")
    widths = (40, 130, 90, 280)

    def form_fields(self):
        return [("Nome","Nome do plano"),("Valor","Ex: 20.00"),("Descrição","Descrição do plano")]

    def load(self):
        rows = run("SELECT id, nome, valor, descricao FROM plano_assinatura ORDER BY id", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO plano_assinatura(nome,valor,descricao) VALUES(%s,%s,%s)",
            (v["Nome"],v["Valor"],v["Descrição"]))

    def update_record(self, id_, v):
        run("UPDATE plano_assinatura SET nome=%s,valor=%s,descricao=%s WHERE id=%s",
            (v["Nome"],v["Valor"],v["Descrição"],id_))

    def delete_record(self, id_):
        run("DELETE FROM plano_assinatura WHERE id=%s", (id_,))

    def row_to_form(self, row):
        return {"Nome":row[1],"Valor":str(row[2]),"Descrição":row[3]}


class TabAvaliacao(BaseTab):
    title  = "⭐  Avaliações"
    cols   = ("ID Álbum","ID Usuário","Estrelas","Comentário")
    widths = (80, 80, 80, 320)

    def form_fields(self):
        return [("ID Álbum","Ex: 1"),("ID Usuário","Ex: 1"),
                ("Estrelas","0 a 5 (incrementos de 0.5)"),("Comentário","Seu comentário")]

    def _build_form(self, panel):
        super()._build_form(panel)

    def load(self):
        rows = run("""SELECT av.id_album, av.id_usuario, av.quantidade_estrelas, av.comentario
                      FROM avaliacao av ORDER BY av.id_album""", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO avaliacao(id_album,id_usuario,quantidade_estrelas,comentario) VALUES(%s,%s,%s,%s)",
            (v["ID Álbum"],v["ID Usuário"],v["Estrelas"],v["Comentário"]))

    def update_record(self, id_, v):
        run("UPDATE avaliacao SET quantidade_estrelas=%s,comentario=%s WHERE id_album=%s AND id_usuario=%s",
            (v["Estrelas"],v["Comentário"],v["ID Álbum"],v["ID Usuário"]))

    def delete_record(self, id_):
        # id_ aqui é id_album da linha selecionada
        sel = self._tv.selection()
        if sel:
            row = self._tv.item(sel[0])["values"]
            run("DELETE FROM avaliacao WHERE id_album=%s AND id_usuario=%s", (row[0],row[1]))

    def row_to_form(self, row):
        return {"ID Álbum":str(row[0]),"ID Usuário":str(row[1]),
                "Estrelas":str(row[2]),"Comentário":row[3]}

    def _delete_selected(self):
        sel = self._tv.selection()
        if not sel:
            messagebox.showinfo("Selecione","Clique em uma linha primeiro."); return
        row = self._tv.item(sel[0])["values"]
        if messagebox.askyesno("Confirmar", f"Excluir avaliação do álbum {row[0]} pelo usuário {row[1]}?"):
            run("DELETE FROM avaliacao WHERE id_album=%s AND id_usuario=%s",(row[0],row[1]))
            toast(self.root, "Avaliação removida.", DANGER)
            self.load()


class TabMembro(BaseTab):
    title  = "👥  Membros"
    cols   = ("ID","Nome","Nascimento","Nacionalidade","Artista")
    widths = (40, 170, 80, 120, 150)

    def form_fields(self):
        return [("Nome","Nome do membro"),("Nascimento","Ex: 1990"),
                ("Nacionalidade","Ex: Brasileiro"),("ID Artista","Ex: 1")]

    def load(self):
        rows = run("""SELECT m.id, m.nome, m.nascimento, m.nacionalidade, a.nome
                      FROM membro m LEFT JOIN artista a ON m.id_artista=a.id ORDER BY m.id""", fetch=True)
        self._set_rows(rows)

    def insert_record(self, v):
        run("INSERT INTO membro(nome,nascimento,nacionalidade,id_artista) VALUES(%s,%s,%s,%s)",
            (v["Nome"],v["Nascimento"],v["Nacionalidade"],v["ID Artista"]))

    def update_record(self, id_, v):
        run("UPDATE membro SET nome=%s,nascimento=%s,nacionalidade=%s,id_artista=%s WHERE id=%s",
            (v["Nome"],v["Nascimento"],v["Nacionalidade"],v["ID Artista"],id_))

    def delete_record(self, id_):
        run("DELETE FROM membro WHERE id=%s", (id_,))

    def row_to_form(self, row):
        r2 = run("SELECT id_artista FROM membro WHERE id=%s",(row[0],),fetch=True)
        return {"Nome":row[1],"Nascimento":str(row[2]),"Nacionalidade":row[3],
                "ID Artista":str(r2[0][0]) if r2 else ""}


class TabPreview(tk.Frame):
    """Aba de Previews com player de áudio integrado."""
    title = "▶  Previews"

    def __init__(self, parent, root):
        super().__init__(parent, bg=BG)
        self.root      = root
        self._sel_id   = None
        self._editing  = False
        self._playing  = False
        self._tmp_file = None
        self._all_rows = []
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=SURFACE, pady=14)
        hdr.pack(fill="x")
        accent_bar = tk.Frame(hdr, bg=ACCENT, width=4)
        accent_bar.pack(side="left", fill="y", padx=(20, 0))
        tk.Frame(hdr, bg=ACCENT3, width=2).pack(side="left", fill="y")
        lbl(hdr, "▶  Previews", ("Segoe UI", 14, "bold"), TEXT, SURFACE).pack(
            side="left", padx=(14, 0))
        # Badge de contagem
        count_frame = tk.Frame(hdr, bg=SURFACE3)
        count_frame.pack(side="right", padx=20, pady=4)
        self._lbl_count = tk.Label(count_frame, text="", font=FSM,
                                   fg=ACCENT, bg=SURFACE3, padx=8, pady=2)
        self._lbl_count.pack()

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=16, pady=12)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)

        # ── Tabela (esquerda) ─────────────────────────────────────────────────
        tframe = tk.Frame(body, bg=BG)
        tframe.grid(row=0, column=0, sticky="nsew")
        tframe.rowconfigure(1, weight=1)
        tframe.columnconfigure(0, weight=1)

        bar = tk.Frame(tframe, bg=BG)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,8))
        bar.columnconfigure(0, weight=1)
        sf, self._search = entry_widget(bar, "🔍  Filtrar...")
        sf.grid(row=0, column=0, sticky="ew")
        self._search.bind("<KeyRelease>", lambda e: self._filter())
        btn(bar, "↻ Atualizar", SURFACE2, self.load).grid(row=0, column=1, padx=(8,0))

        tf = tk.Frame(tframe, bg=BG)
        tf.grid(row=1, column=0, columnspan=2, sticky="nsew")
        cols   = ("ID", "Música", "URL do Áudio")
        widths = (40, 220, 380)
        self._tv = make_tree(tf, cols, widths)
        self._tv.bind("<<TreeviewSelect>>", self._on_sel)
        self._tv.bind("<Double-1>", lambda e: self._play_selected())

        # ── Painel direito ────────────────────────────────────────────────────
        panel = tk.Frame(body, bg=SURFACE, width=260,
                         highlightbackground=BORDER, highlightthickness=1)
        panel.grid(row=0, column=1, sticky="ns", padx=(14,0))
        panel.pack_propagate(False)

        # Player
        lbl(panel, "Player", ("Segoe UI",12,"bold"), ACCENT, SURFACE).pack(anchor="w", padx=16, pady=(18,4))

        self._lbl_musica = lbl(panel, "Nenhuma selecionada", ("Segoe UI",10,"bold"), TEXT, SURFACE)
        self._lbl_musica.pack(anchor="w", padx=16, pady=(0,2))
        self._lbl_url = lbl(panel, "", FB, MUTED, SURFACE)
        self._lbl_url.pack(anchor="w", padx=16, pady=(0,14))
        self._lbl_url.config(wraplength=220, justify="left")

        # Ícone grande de nota musical
        self._lbl_icon = tk.Label(panel, text="♪", font=("Segoe UI",52), fg=ACCENT,
                                  bg=SURFACE2, width=6, height=3)
        self._lbl_icon.pack(padx=16, pady=(0,14))

        self._lbl_status = lbl(panel, "Parado", FB, MUTED, SURFACE)
        self._lbl_status.pack(pady=(0,10))

        # Botões do player
        pbtn_frame = tk.Frame(panel, bg=SURFACE)
        pbtn_frame.pack(fill="x", padx=16, pady=(0,4))
        self._btn_play = btn(pbtn_frame, "▶  Reproduzir", ACCENT, self._play_selected)
        self._btn_play.pack(fill="x", pady=(0,8))
        btn(pbtn_frame, "■  Parar", SURFACE2, self._stop).pack(fill="x")

        if not PYGAME_OK:
            lbl(panel, "⚠ pygame não instalado\npip install pygame", FB, WARN, SURFACE).pack(
                padx=16, pady=10)

        tk.Frame(panel, bg=BORDER, height=1).pack(fill="x", padx=16, pady=14)

        # Formulário CRUD
        lbl(panel, "Adicionar / Editar", ("Segoe UI",11,"bold"), ACCENT, SURFACE).pack(
            anchor="w", padx=16, pady=(0,10))

        lbl(panel, "ID Música", FB, MUTED, SURFACE).pack(anchor="w", padx=16)
        ff, self._ent_musica = entry_widget(panel, "Ex: 1")
        ff.pack(fill="x", padx=16, pady=(3,8))

        lbl(panel, "URL do Áudio", FB, MUTED, SURFACE).pack(anchor="w", padx=16)
        ff2, self._ent_url = entry_widget(panel, "https://...")
        ff2.pack(fill="x", padx=16, pady=(3,12))

        self._btn_save = btn(panel, "＋  Adicionar", ACCENT, self._save)
        self._btn_save.pack(fill="x", padx=16, pady=(0,6))
        self._btn_cancel = btn(panel, "Cancelar edição", SURFACE2, self._cancel)
        self._btn_cancel.pack(fill="x", padx=16)
        self._btn_cancel.pack_forget()

        tk.Frame(panel, bg=BORDER, height=1).pack(fill="x", padx=16, pady=12)
        lbl(panel, "Linha selecionada", FB, MUTED, SURFACE).pack(anchor="w", padx=16, pady=(0,8))
        btn(panel, "✏  Editar",  ACCENT2, self._edit_selected).pack(fill="x", padx=16, pady=(0,8))
        btn(panel, "🗑  Excluir", DANGER,  self._delete_selected).pack(fill="x", padx=16)

        self.load()

    # ── dados ─────────────────────────────────────────────────────────────────
    def load(self):
        rows = run("""SELECT p.id, m.nome, p.url_audio
                      FROM preview p LEFT JOIN musica m ON p.id_musica=m.id
                      ORDER BY p.id""", fetch=True)
        self._all_rows = rows
        fill_tree(self._tv, rows)
        self._lbl_count.config(text=f"{len(rows)} registro(s)")

    def _filter(self):
        term = get_val(self._search).lower()
        filtered = [r for r in self._all_rows
                    if any(term in str(c).lower() for c in r)] if term else self._all_rows
        fill_tree(self._tv, filtered)
        self._lbl_count.config(text=f"{len(filtered)} registro(s)")

    def _on_sel(self, _=None):
        sel = self._tv.selection()
        if not sel:
            return
        row = self._tv.item(sel[0])["values"]
        self._sel_id = row[0]
        nome = str(row[1])
        url  = str(row[2]) if row[2] else ""
        self._lbl_musica.config(text=nome[:32])
        short = (url[:34] + "...") if len(url) > 37 else url
        self._lbl_url.config(text=short or "Sem URL cadastrada")
        self._stop()

    # ── player ────────────────────────────────────────────────────────────────
    def _play_selected(self):
        sel = self._tv.selection()
        if not sel:
            messagebox.showinfo("Selecione", "Clique em uma preview primeiro.")
            return
        row = self._tv.item(sel[0])["values"]
        url = str(row[2]).strip() if row[2] else ""
        if not url or url in ("", "None"):
            messagebox.showwarning("Sem áudio", "Essa preview não tem URL cadastrada.")
            return
        if not PYGAME_OK:
            messagebox.showerror("pygame ausente", "Instale com: pip install pygame")
            return

        self._stop()
        self._lbl_status.config(text="Carregando...", fg=WARN)
        self._btn_play.config(text="⏳ Carregando...")
        self.root.update()

        def _load_and_play():
            try:
                import tempfile, os
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = resp.read()

                suffix = ".mp3" if "mp3" in url.lower() else ".ogg" if "ogg" in url.lower() else ".mp3"
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                tmp.write(data); tmp.close()
                self._tmp_file = tmp.name

                pygame.mixer.music.load(tmp.name)
                pygame.mixer.music.play()
                self._playing = True
                self._lbl_status.config(text="▶ Reproduzindo", fg=ACCENT2)
                self._btn_play.config(text="▶  Reproduzir", bg=ACCENT)
            except Exception as ex:
                self._lbl_status.config(text="Erro ao carregar", fg=DANGER)
                self._btn_play.config(text="▶  Reproduzir", bg=ACCENT)
                messagebox.showerror("Erro de áudio", str(ex))

        threading.Thread(target=_load_and_play, daemon=True).start()

    def _stop(self):
        if PYGAME_OK:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
        self._playing = False
        self._lbl_status.config(text="Parado", fg=MUTED)
        self._btn_play.config(text="▶  Reproduzir", bg=ACCENT)
        if self._tmp_file:
            try:
                import os; os.unlink(self._tmp_file)
            except Exception:
                pass
            self._tmp_file = None

    # ── CRUD ──────────────────────────────────────────────────────────────────
    def _save(self):
        id_m = get_val(self._ent_musica)
        url  = get_val(self._ent_url)
        if not id_m or not url:
            messagebox.showwarning("Campos obrigatórios", "Preencha ID Música e URL."); return
        try:
            if self._editing and self._sel_id:
                run("UPDATE preview SET id_musica=%s, url_audio=%s WHERE id=%s",
                    (id_m, url, self._sel_id))
                toast(self.root, "Preview atualizada!")
            else:
                run("INSERT INTO preview(url_audio, id_musica) VALUES(%s,%s)", (url, id_m))
                toast(self.root, "Preview adicionada!")
            self._cancel(); self.load()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def _edit_selected(self):
        sel = self._tv.selection()
        if not sel:
            messagebox.showinfo("Selecione", "Clique em uma linha primeiro."); return
        row = self._tv.item(sel[0])["values"]
        self._sel_id  = row[0]
        self._editing = True
        r2 = run("SELECT id_musica, url_audio FROM preview WHERE id=%s", (row[0],), fetch=True)
        if r2:
            for e, v in [(self._ent_musica, str(r2[0][0])), (self._ent_url, str(r2[0][1]))]:
                e.delete(0,"end"); e.insert(0, v); e.config(fg=TEXT)
        self._btn_save.config(text="✔  Salvar alterações", bg=ACCENT2)
        self._btn_cancel.pack(fill="x", padx=16)

    def _cancel(self):
        self._editing = False; self._sel_id = None
        for e, ph in [(self._ent_musica,"Ex: 1"),(self._ent_url,"https://...")]:
            e.delete(0,"end"); e.insert(0,ph); e.config(fg=MUTED)
        self._btn_save.config(text="＋  Adicionar", bg=ACCENT)
        self._btn_cancel.pack_forget()

    def _delete_selected(self):
        sel = self._tv.selection()
        if not sel:
            messagebox.showinfo("Selecione", "Clique em uma linha primeiro."); return
        row = self._tv.item(sel[0])["values"]
        if messagebox.askyesno("Confirmar", f"Excluir preview de '{row[1]}'?"):
            self._stop()
            run("DELETE FROM preview WHERE id=%s", (row[0],))
            toast(self.root, "Preview removida.", DANGER)
            self.load()


# ═══════════════════════════════════════════════════════════════════════════════
# APP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador — Banco Musical")
        self.configure(bg=BG)
        self.geometry("1060x680")
        self.minsize(900, 560)

        self._build_header()
        self._build_tabs()

    def _build_header(self):
        hdr = tk.Frame(self, bg=SURFACE, pady=0)
        hdr.pack(fill="x")

        # Barra de topo com gradiente de cor
        top_bar = tk.Frame(hdr, bg=ACCENT, height=3)
        top_bar.pack(fill="x")

        content = tk.Frame(hdr, bg=SURFACE, pady=14)
        content.pack(fill="x")

        # Ícone e título
        icon_frame = tk.Frame(content, bg=SURFACE2, padx=10, pady=10)
        icon_frame.pack(side="left", padx=(20, 0))
        tk.Label(icon_frame, text="♪", font=("Segoe UI", 18, "bold"),
                 fg=ACCENT, bg=SURFACE2).pack()

        inner = tk.Frame(content, bg=SURFACE)
        inner.pack(side="left", padx=14)
        tk.Label(inner, text="Gerenciador Musical",
                 font=("Segoe UI", 17, "bold"), fg=TEXT, bg=SURFACE).pack(anchor="w")
        tk.Label(inner, text="PostgreSQL  ·  psycopg2  ·  Banco de Dados",
                 font=("Segoe UI", 9), fg=MUTED, bg=SURFACE).pack(anchor="w", pady=(2, 0))

        # Status conectado
        status_frame = tk.Frame(content, bg=SURFACE2, padx=12, pady=6)
        status_frame.pack(side="right", padx=24)
        dot = tk.Label(status_frame, text="●", font=("Segoe UI", 10),
                       fg=ACCENT2, bg=SURFACE2)
        dot.pack(side="left", padx=(0, 4))
        tk.Label(status_frame, text="Conectado", font=("Segoe UI", 9, "bold"),
                 fg=ACCENT2, bg=SURFACE2).pack(side="left")

        # Linha separadora
        tk.Frame(hdr, bg=BORDER2, height=1).pack(fill="x")

    def _build_tabs(self):
        style = ttk.Style()
        style.configure("Dark.TNotebook",
                         background=BG, borderwidth=0, tabmargins=0)
        style.configure("Dark.TNotebook.Tab",
                         background=SURFACE2, foreground=MUTED,
                         font=("Segoe UI", 9, "bold"),
                         padding=(16, 9))
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", SURFACE)],
                  foreground=[("selected", ACCENT)],
                  expand=[("selected", [1, 1, 1, 0])])

        nb = ttk.Notebook(self, style="Dark.TNotebook")
        nb.pack(fill="both", expand=True)

        tabs = [
            TabArtista, TabAlbum, TabMusica, TabUsuario,
            TabPlaylist, TabGravadora, TabGenero, TabPlano,
            TabAvaliacao, TabMembro, TabPreview
        ]
        for TabClass in tabs:
            frame = TabClass(nb, self)
            nb.add(frame, text=TabClass.title)


if __name__ == "__main__":
    app = App()
    app.mainloop()