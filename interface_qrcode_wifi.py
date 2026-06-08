import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from gerar_qrcode_wifi import generate_wifi_qr


class WifiQrApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Gerador de QR Code Wi-Fi")
        self.root.geometry("680x500")
        self.root.minsize(640, 460)

        self.ssid_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.security_var = tk.StringVar(value="WPA")
        self.hidden_var = tk.BooleanVar(value=False)
        self.use_logo_var = tk.BooleanVar(value=False)
        self.logo_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar(value=str(Path("wifi_qr.png").resolve()))
        self.logo_scale_var = tk.DoubleVar(value=0.20)
        self.box_size_var = tk.IntVar(value=10)
        self.border_var = tk.IntVar(value=4)
        self.fill_color_var = tk.StringVar(value="black")
        self.back_color_var = tk.StringVar(value="white")

        self._build_ui()
        self._update_password_state()
        self._update_logo_state()

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=14)
        container.pack(fill="both", expand=True)

        row = 0

        ttk.Label(container, text="SSID:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(container, textvariable=self.ssid_var, width=50).grid(row=row, column=1, sticky="ew", pady=4)
        row += 1

        ttk.Label(container, text="Seguranca:").grid(row=row, column=0, sticky="w", pady=4)
        security_combo = ttk.Combobox(
            container,
            textvariable=self.security_var,
            values=["WPA", "WEP", "nopass"],
            state="readonly",
            width=18,
        )
        security_combo.grid(row=row, column=1, sticky="w", pady=4)
        security_combo.bind("<<ComboboxSelected>>", lambda _evt: self._update_password_state())
        row += 1

        ttk.Label(container, text="Senha:").grid(row=row, column=0, sticky="w", pady=4)
        self.password_entry = ttk.Entry(container, textvariable=self.password_var, width=50, show="*")
        self.password_entry.grid(row=row, column=1, sticky="ew", pady=4)
        row += 1

        ttk.Checkbutton(container, text="Rede oculta", variable=self.hidden_var).grid(
            row=row, column=1, sticky="w", pady=4
        )
        row += 1

        ttk.Separator(container, orient="horizontal").grid(row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        ttk.Checkbutton(
            container,
            text="Usar logo da empresa",
            variable=self.use_logo_var,
            command=self._update_logo_state,
        ).grid(row=row, column=1, sticky="w", pady=4)
        row += 1

        ttk.Label(container, text="Arquivo do logo:").grid(row=row, column=0, sticky="w", pady=4)
        self.logo_entry = ttk.Entry(container, textvariable=self.logo_path_var, width=50)
        self.logo_entry.grid(row=row, column=1, sticky="ew", pady=4)
        self.logo_button = ttk.Button(container, text="Procurar", command=self._pick_logo)
        self.logo_button.grid(row=row, column=2, padx=6, pady=4)
        row += 1

        ttk.Label(container, text="Escala do logo (0.05-0.35):").grid(row=row, column=0, sticky="w", pady=4)
        self.logo_scale_entry = ttk.Entry(container, textvariable=self.logo_scale_var, width=10)
        self.logo_scale_entry.grid(row=row, column=1, sticky="w", pady=4)
        row += 1

        ttk.Separator(container, orient="horizontal").grid(row=row, column=0, columnspan=3, sticky="ew", pady=10)
        row += 1

        ttk.Label(container, text="Saida PNG:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(container, textvariable=self.output_path_var, width=50).grid(row=row, column=1, sticky="ew", pady=4)
        ttk.Button(container, text="Salvar como", command=self._pick_output).grid(row=row, column=2, padx=6, pady=4)
        row += 1

        ttk.Label(container, text="Box size:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(container, textvariable=self.box_size_var, width=10).grid(row=row, column=1, sticky="w", pady=4)
        row += 1

        ttk.Label(container, text="Borda:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(container, textvariable=self.border_var, width=10).grid(row=row, column=1, sticky="w", pady=4)
        row += 1

        ttk.Label(container, text="Cor do QR:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(container, textvariable=self.fill_color_var, width=14).grid(row=row, column=1, sticky="w", pady=4)
        row += 1

        ttk.Label(container, text="Cor de fundo:").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(container, textvariable=self.back_color_var, width=14).grid(row=row, column=1, sticky="w", pady=4)
        row += 1

        ttk.Button(container, text="Gerar QR Code", command=self._generate_qr).grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=14
        )

        container.columnconfigure(1, weight=1)

    def _update_password_state(self) -> None:
        if self.security_var.get() == "nopass":
            self.password_entry.configure(state="disabled")
            self.password_var.set("")
        else:
            self.password_entry.configure(state="normal")

    def _update_logo_state(self) -> None:
        state = "normal" if self.use_logo_var.get() else "disabled"
        self.logo_entry.configure(state=state)
        self.logo_button.configure(state=state)
        self.logo_scale_entry.configure(state=state)

    def _pick_logo(self) -> None:
        path = filedialog.askopenfilename(
            title="Selecionar logo",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.webp *.bmp"), ("Todos", "*.*")],
        )
        if path:
            self.logo_path_var.set(path)

    def _pick_output(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Salvar QR Code",
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
        )
        if path:
            self.output_path_var.set(path)

    def _generate_qr(self) -> None:
        ssid = self.ssid_var.get().strip()
        password = self.password_var.get()
        security = self.security_var.get().strip()

        if not ssid:
            messagebox.showerror("Erro", "Informe o SSID da rede.")
            return

        if security in ("WPA", "WEP") and not password:
            messagebox.showerror("Erro", "Informe a senha para seguranca WPA/WEP.")
            return

        logo_path = None
        if self.use_logo_var.get():
            logo_str = self.logo_path_var.get().strip()
            if not logo_str:
                messagebox.showerror("Erro", "Selecione o arquivo de logo.")
                return
            logo_path = Path(logo_str)

        output_str = self.output_path_var.get().strip()
        if not output_str:
            messagebox.showerror("Erro", "Informe o caminho do arquivo de saida.")
            return

        try:
            output = generate_wifi_qr(
                ssid=ssid,
                password=password,
                security=security,
                hidden=self.hidden_var.get(),
                output=Path(output_str),
                logo=logo_path,
                logo_scale=float(self.logo_scale_var.get()),
                box_size=int(self.box_size_var.get()),
                border=int(self.border_var.get()),
                fill_color=self.fill_color_var.get().strip() or "black",
                back_color=self.back_color_var.get().strip() or "white",
            )
        except Exception as exc:
            messagebox.showerror("Falha", f"Nao foi possivel gerar o QR Code.\n\nDetalhes: {exc}")
            return

        messagebox.showinfo("Sucesso", f"QR Code criado com sucesso:\n{output.resolve()}")


def main() -> None:
    root = tk.Tk()
    app = WifiQrApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
