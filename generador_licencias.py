"""
╔══════════════════════════════════════════════════════════════╗
║   GENERADOR DE LICENCIAS — JURIS-GESTIÓN-PRO                 ║
║   Herramienta privada del proveedor (Fer Ardón)              ║
║   No distribuir con el software cliente                      ║
╚══════════════════════════════════════════════════════════════╝
"""

import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta, date

# ── Constantes de cifrado (deben coincidir con main.py) ────────
SECRET_KEY = "JURIS_PRO_FER_ARDON_2026"
BASE_DATE  = date(2024, 1, 1)

TIPOS_LICENCIA = {
    "10D  — Prueba (10 días)":        "10D",
    "1M   — 1 mes":                   "1M",
    "6M   — 6 meses":                 "6M",
    "1Y   — 1 año":                   "1Y",
    "PERM — Permanente (pago único)": "PERM",
}

# ── Paleta de colores (tema oscuro) ────────────────────────────
C = {
    "bg":          "#0f1724",
    "panel":       "#1a2640",
    "card":        "#1f2e4a",
    "border":      "#2a3f5f",
    "accent":      "#0067C0",
    "accent_h":    "#0078D4",
    "text":        "#FFFFFF",
    "text_muted":  "#7a9cc7",
    "success":     "#6BCB77",
    "error":       "#FF6B6B",
    "hw":          "#4CC2FF",
    "entry_bg":    "#111c2e",
    "row_alt":     "#1c2a42",
}


# ══════════════════════════════════════════════════════════════
# LÓGICA DE LICENCIAS
# ══════════════════════════════════════════════════════════════

def generar_licencia(hw_id: str, tipo: str) -> dict:
    """
    Genera una clave de licencia.
    Retorna dict con: key (str), exp_date (str), valida (bool), error (str).
    """
    hoy = datetime.now().date()

    duraciones = {
        "10D":  10,
        "1M":   30,
        "6M":   180,
        "1Y":   365,
        "PERM": None,
        "PERMANENTE": None,
    }

    tipo_norm = tipo.strip().upper()
    if tipo_norm not in duraciones:
        return {"valida": False, "error": f"Tipo inválido: '{tipo}'."}

    dias = duraciones[tipo_norm]
    if dias is not None:
        exp_date = hoy + timedelta(days=dias)
        dias_totales = (exp_date - BASE_DATE).days
        exp_hex = f"{dias_totales:04X}"
        exp_str = exp_date.strftime("%d/%m/%Y")
    else:
        exp_hex = "FFFF"
        exp_str = "PERMANENTE"

    hw_norm = hw_id.strip().upper()
    signature = hashlib.sha256(
        f"{exp_hex}{hw_norm}{SECRET_KEY}".encode()
    ).hexdigest()[:16].upper()

    raw = exp_hex + signature
    key = f"{raw[:5]}-{raw[5:10]}-{raw[10:15]}-{raw[15:20]}"
    return {"valida": True, "key": key, "exp_str": exp_str, "hw_id": hw_norm}


def verificar_licencia(key: str, hw_id: str) -> dict:
    """Verifica una clave existente. Retorna dict con resultado."""
    try:
        limpia = key.strip().upper().replace("-", "")
        if len(limpia) != 20:
            return {"valida": False, "msg": "La clave debe tener 20 caracteres."}

        exp_hex   = limpia[:4]
        signature = limpia[4:20]
        hw_norm   = hw_id.strip().upper()

        # Verificar contra HW ID dado
        firma_esp = hashlib.sha256(
            f"{exp_hex}{hw_norm}{SECRET_KEY}".encode()
        ).hexdigest()[:16].upper()

        # Verificar también contra UNIVERSAL
        firma_uni = hashlib.sha256(
            f"{exp_hex}UNIVERSAL{SECRET_KEY}".encode()
        ).hexdigest()[:16].upper()

        if signature != firma_esp and signature != firma_uni:
            return {"valida": False, "msg": "Firma inválida. Clave no corresponde al HW ID."}

        if exp_hex == "FFFF":
            return {"valida": True, "msg": "✅ Licencia PERMANENTE — Sin vencimiento."}

        dias_totales = int(exp_hex, 16)
        exp_date = BASE_DATE + timedelta(days=dias_totales)
        hoy = date.today()

        if hoy > exp_date:
            return {"valida": False, "msg": f"❌ Licencia VENCIDA el {exp_date.strftime('%d/%m/%Y')}."}

        dias_rest = (exp_date - hoy).days
        return {"valida": True, "msg": f"✅ Válida hasta {exp_date.strftime('%d/%m/%Y')} ({dias_rest} días restantes)."}

    except Exception as e:
        return {"valida": False, "msg": f"Error al verificar: {e}"}


# ══════════════════════════════════════════════════════════════
# INTERFAZ GRÁFICA
# ══════════════════════════════════════════════════════════════

class GeneradorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Licencias — JURIS-GESTIÓN-PRO")
        self.geometry("780x640")
        self.minsize(700, 580)
        self.configure(bg=C["bg"])
        self.resizable(True, True)

        # Historial de claves generadas en esta sesión
        self._historial = []  # lista de dicts

        self._build_ui()
        self.mainloop()

    # ── Construcción de la UI ───────────────────────────────────
    def _build_ui(self):
        # Encabezado
        hdr = tk.Frame(self, bg=C["panel"], pady=16)
        hdr.pack(fill="x", side="top")

        tk.Label(hdr, text="⚖️  JURIS-GESTIÓN-PRO",
                 font=("Segoe UI Variable", 16, "bold"),
                 bg=C["panel"], fg=C["text"]).pack()
        tk.Label(hdr, text="Herramienta de Generación y Verificación de Licencias",
                 font=("Segoe UI Variable", 9),
                 bg=C["panel"], fg=C["text_muted"]).pack()

        # Notebook (pestañas)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Dark.TNotebook",
                         background=C["bg"], borderwidth=0)
        style.configure("Dark.TNotebook.Tab",
                         background=C["panel"], foreground=C["text_muted"],
                         padding=[16, 8], font=("Segoe UI Variable", 9, "bold"))
        style.map("Dark.TNotebook.Tab",
                  background=[("selected", C["accent"])],
                  foreground=[("selected", "#FFFFFF")])

        nb = ttk.Notebook(self, style="Dark.TNotebook")
        nb.pack(fill="both", expand=True, padx=12, pady=12)

        # Pestaña 1: Generar
        self._tab_generar = tk.Frame(nb, bg=C["bg"])
        nb.add(self._tab_generar, text="🔑  Generar Clave")

        # Pestaña 2: Verificar
        self._tab_verificar = tk.Frame(nb, bg=C["bg"])
        nb.add(self._tab_verificar, text="🔍  Verificar Clave")

        # Pestaña 3: Historial
        self._tab_historial = tk.Frame(nb, bg=C["bg"])
        nb.add(self._tab_historial, text="📋  Historial de Sesión")

        self._build_tab_generar()
        self._build_tab_verificar()
        self._build_tab_historial()

    # ── PESTAÑA GENERAR ─────────────────────────────────────────
    def _build_tab_generar(self):
        f = self._tab_generar
        pad = {"padx": 28, "pady": 6}

        # ── Campo Hardware ID
        tk.Label(f, text="Hardware ID del Cliente",
                 font=("Segoe UI Variable", 9, "bold"),
                 bg=C["bg"], fg=C["text_muted"]).pack(anchor="w", **pad)

        hw_frame = tk.Frame(f, bg=C["bg"])
        hw_frame.pack(fill="x", padx=28)

        self._hw_var = tk.StringVar()
        hw_entry = tk.Entry(hw_frame, textvariable=self._hw_var,
                            font=("Cascadia Code", 13, "bold"),
                            bg=C["entry_bg"], fg=C["hw"],
                            insertbackground=C["hw"],
                            relief="flat", bd=0, highlightthickness=1,
                            highlightcolor=C["accent"],
                            highlightbackground=C["border"])
        hw_entry.pack(side="left", fill="x", expand=True, ipady=8, ipadx=10)

        tk.Button(hw_frame, text="UNIVERSAL",
                  font=("Segoe UI Variable", 8, "bold"),
                  bg=C["border"], fg=C["text_muted"],
                  relief="flat", cursor="hand2", bd=0,
                  padx=10, pady=4,
                  command=lambda: self._hw_var.set("UNIVERSAL")
                  ).pack(side="left", padx=(6, 0))

        tk.Label(f, text="Déjelo en blanco o use 'UNIVERSAL' para una clave sin vínculo de equipo.",
                 font=("Segoe UI Variable", 8),
                 bg=C["bg"], fg=C["text_muted"]).pack(anchor="w", padx=28)

        # ── Tipo de Licencia
        tk.Label(f, text="Tipo de Licencia",
                 font=("Segoe UI Variable", 9, "bold"),
                 bg=C["bg"], fg=C["text_muted"]).pack(anchor="w", pady=(16, 4), padx=28)

        self._tipo_var = tk.StringVar(value=list(TIPOS_LICENCIA.keys())[0])

        tipo_frame = tk.Frame(f, bg=C["bg"])
        tipo_frame.pack(fill="x", padx=28)

        for label in TIPOS_LICENCIA:
            rb = tk.Radiobutton(tipo_frame, text=label,
                                variable=self._tipo_var, value=label,
                                font=("Segoe UI Variable", 9),
                                bg=C["bg"], fg=C["text"],
                                selectcolor=C["panel"],
                                activebackground=C["bg"],
                                activeforeground=C["accent"],
                                cursor="hand2")
            rb.pack(anchor="w", pady=2)

        # ── Botón Generar
        tk.Button(f, text="🔑  GENERAR CLAVE DE LICENCIA",
                  font=("Segoe UI Variable", 11, "bold"),
                  bg=C["accent"], fg="#FFFFFF",
                  activebackground=C["accent_h"], activeforeground="#FFFFFF",
                  relief="flat", cursor="hand2", bd=0,
                  pady=12,
                  command=self._accion_generar
                  ).pack(fill="x", padx=28, pady=(20, 0))

        # ── Resultado
        res_frame = tk.Frame(f, bg=C["card"],
                             highlightthickness=1,
                             highlightbackground=C["border"])
        res_frame.pack(fill="x", padx=28, pady=(14, 0))

        tk.Label(res_frame, text="CLAVE GENERADA",
                 font=("Segoe UI Variable", 7, "bold"),
                 bg=C["card"], fg=C["text_muted"],
                 pady=6).pack()

        self._resultado_var = tk.StringVar(value="—")
        self._lbl_resultado = tk.Label(res_frame,
                                       textvariable=self._resultado_var,
                                       font=("Cascadia Code", 18, "bold"),
                                       bg=C["card"], fg=C["success"],
                                       pady=8)
        self._lbl_resultado.pack()

        self._lbl_info_gen = tk.Label(res_frame, text="",
                                      font=("Segoe UI Variable", 8),
                                      bg=C["card"], fg=C["text_muted"],
                                      pady=4)
        self._lbl_info_gen.pack()

        tk.Button(res_frame, text="📋  Copiar al portapapeles",
                  font=("Segoe UI Variable", 9),
                  bg=C["border"], fg=C["text"],
                  activebackground=C["panel"], activeforeground="#FFFFFF",
                  relief="flat", cursor="hand2", bd=0, pady=6,
                  command=self._copiar_resultado
                  ).pack(pady=(0, 10))

    # ── PESTAÑA VERIFICAR ───────────────────────────────────────
    def _build_tab_verificar(self):
        f = self._tab_verificar
        pad = {"padx": 28, "pady": 6}

        tk.Label(f, text="Clave a Verificar (XXXXX-XXXXX-XXXXX-XXXXX)",
                 font=("Segoe UI Variable", 9, "bold"),
                 bg=C["bg"], fg=C["text_muted"]).pack(anchor="w", **pad)

        self._ver_key_var = tk.StringVar()
        key_entry = tk.Entry(f, textvariable=self._ver_key_var,
                             font=("Cascadia Code", 12),
                             bg=C["entry_bg"], fg=C["text"],
                             insertbackground=C["text"],
                             relief="flat", bd=0, highlightthickness=1,
                             highlightcolor=C["accent"],
                             highlightbackground=C["border"])
        key_entry.pack(fill="x", padx=28, ipady=8, ipadx=10)
        key_entry.bind("<KeyRelease>", self._autoformat_key)

        tk.Label(f, text="Hardware ID (dejar vacío para verificar como UNIVERSAL)",
                 font=("Segoe UI Variable", 9, "bold"),
                 bg=C["bg"], fg=C["text_muted"]).pack(anchor="w", pady=(16, 4), padx=28)

        self._ver_hw_var = tk.StringVar()
        tk.Entry(f, textvariable=self._ver_hw_var,
                 font=("Cascadia Code", 12),
                 bg=C["entry_bg"], fg=C["hw"],
                 insertbackground=C["hw"],
                 relief="flat", bd=0, highlightthickness=1,
                 highlightcolor=C["accent"],
                 highlightbackground=C["border"]
                 ).pack(fill="x", padx=28, ipady=8, ipadx=10)

        tk.Button(f, text="🔍  VERIFICAR CLAVE",
                  font=("Segoe UI Variable", 11, "bold"),
                  bg=C["accent"], fg="#FFFFFF",
                  activebackground=C["accent_h"], activeforeground="#FFFFFF",
                  relief="flat", cursor="hand2", bd=0, pady=12,
                  command=self._accion_verificar
                  ).pack(fill="x", padx=28, pady=(20, 0))

        # Resultado verificación
        ver_res_frame = tk.Frame(f, bg=C["card"],
                                 highlightthickness=1,
                                 highlightbackground=C["border"])
        ver_res_frame.pack(fill="x", padx=28, pady=(14, 0))

        self._lbl_ver_resultado = tk.Label(ver_res_frame, text="Ingrese una clave y presione Verificar.",
                                           font=("Segoe UI Variable", 10),
                                           bg=C["card"], fg=C["text_muted"],
                                           wraplength=500, pady=18)
        self._lbl_ver_resultado.pack()

    # ── PESTAÑA HISTORIAL ───────────────────────────────────────
    def _build_tab_historial(self):
        f = self._tab_historial

        cols = ("hw_id", "tipo", "vencimiento", "clave")
        self._tree = ttk.Treeview(f, columns=cols, show="headings",
                                  selectmode="browse")

        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=C["card"],
                        foreground=C["text"],
                        fieldbackground=C["card"],
                        rowheight=32,
                        font=("Segoe UI Variable", 9))
        style.configure("Dark.Treeview.Heading",
                        background=C["panel"],
                        foreground=C["text_muted"],
                        font=("Segoe UI Variable", 8, "bold"))
        style.map("Dark.Treeview",
                  background=[("selected", C["accent"])],
                  foreground=[("selected", "#FFFFFF")])
        self._tree.configure(style="Dark.Treeview")

        self._tree.heading("hw_id",       text="Hardware ID")
        self._tree.heading("tipo",        text="Tipo")
        self._tree.heading("vencimiento", text="Vencimiento")
        self._tree.heading("clave",       text="Clave Generada")

        self._tree.column("hw_id",       width=140, anchor="w")
        self._tree.column("tipo",        width=100, anchor="center")
        self._tree.column("vencimiento", width=130, anchor="center")
        self._tree.column("clave",       width=240, anchor="w")

        sb = ttk.Scrollbar(f, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=sb.set)
        self._tree.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=12)
        sb.pack(side="right", fill="y", pady=12, padx=(0, 12))

        # Botón copiar clave seleccionada
        btn_frame = tk.Frame(f, bg=C["bg"])
        btn_frame.pack(side="bottom", fill="x", padx=12, pady=(0, 8))
        tk.Button(btn_frame, text="📋 Copiar clave seleccionada",
                  font=("Segoe UI Variable", 9),
                  bg=C["border"], fg=C["text"],
                  relief="flat", cursor="hand2", bd=0, pady=6,
                  command=self._copiar_historial
                  ).pack(side="left")
        tk.Button(btn_frame, text="🗑 Limpiar historial",
                  font=("Segoe UI Variable", 9),
                  bg=C["border"], fg=C["text_muted"],
                  relief="flat", cursor="hand2", bd=0, pady=6,
                  command=self._limpiar_historial
                  ).pack(side="left", padx=(8, 0))

    # ── ACCIONES ────────────────────────────────────────────────
    def _accion_generar(self):
        hw_raw = self._hw_var.get().strip()
        hw = hw_raw.upper() if hw_raw else "UNIVERSAL"

        label_tipo = self._tipo_var.get()
        tipo = TIPOS_LICENCIA.get(label_tipo, "")

        resultado = generar_licencia(hw, tipo)

        if not resultado["valida"]:
            self._resultado_var.set("ERROR")
            self._lbl_resultado.config(fg=C["error"])
            self._lbl_info_gen.config(text=resultado.get("error", ""))
            return

        key = resultado["key"]
        self._resultado_var.set(key)
        self._lbl_resultado.config(fg=C["success"])
        self._lbl_info_gen.config(
            text=f"HW ID: {resultado['hw_id']}   |   Vencimiento: {resultado['exp_str']}"
        )

        # Agregar al historial
        self._historial.append(resultado | {"label_tipo": label_tipo.split("—")[0].strip()})
        self._tree.insert("", "end",
                          values=(resultado["hw_id"],
                                  resultado["label_tipo"].split("—")[0].strip(),
                                  resultado["exp_str"],
                                  key))
        # Alternar color de fila
        n = len(self._historial)
        tag = "alt" if n % 2 == 0 else "norm"
        self._tree.tag_configure("alt",  background=C["row_alt"], foreground=C["text"])
        self._tree.tag_configure("norm", background=C["card"], foreground=C["text"])
        for item in self._tree.get_children():
            idx = self._tree.index(item)
            self._tree.item(item, tags=("alt" if idx % 2 == 0 else "norm",))

    def _accion_verificar(self):
        key = self._ver_key_var.get().strip()
        hw  = self._ver_hw_var.get().strip() or "UNIVERSAL"

        if not key:
            self._lbl_ver_resultado.config(text="⚠️ Ingrese una clave para verificar.",
                                           fg=C["text_muted"])
            return

        res = verificar_licencia(key, hw)
        color = C["success"] if res["valida"] else C["error"]
        self._lbl_ver_resultado.config(text=res["msg"], fg=color)

    def _copiar_resultado(self):
        key = self._resultado_var.get()
        if key and key != "—" and "ERROR" not in key:
            self.clipboard_clear()
            self.clipboard_append(key)
            messagebox.showinfo("Copiado", f"Clave copiada al portapapeles:\n\n{key}")

    def _copiar_historial(self):
        sel = self._tree.selection()
        if not sel:
            return
        valores = self._tree.item(sel[0], "values")
        if valores:
            key = valores[3]
            self.clipboard_clear()
            self.clipboard_append(key)
            messagebox.showinfo("Copiado", f"Clave copiada:\n\n{key}")

    def _limpiar_historial(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._historial.clear()

    def _autoformat_key(self, event=None):
        """Formatea automáticamente la clave mientras el usuario escribe."""
        raw = self._ver_key_var.get().upper().replace("-", "")
        raw = "".join(c for c in raw if c.isalnum())[:20]
        fmt = ""
        for i, c in enumerate(raw):
            if i > 0 and i % 5 == 0:
                fmt += "-"
            fmt += c
        entry = event.widget if event else None
        self._ver_key_var.set(fmt)
        if entry:
            entry.icursor(len(fmt))


# ══════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    GeneradorApp()
