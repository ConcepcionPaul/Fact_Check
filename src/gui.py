import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from training import train_or_load
from evaluation import evaluate_or_load
from bow import export_vocab_csv
from preprocessing import reload_stopwords
from cli_helpers import classify_text, classify_url, classify_image, scrape_multiple

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PAK CHECKER')
        self.geometry('980x760')
        self.configure(bg='#1e272e')
        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style(self)
        self.font_family = 'Segoe UI'

        style.theme_use('clam')

        style.configure('TNotebook', background='#1e272e', borderwidth=0)
        style.configure('TNotebook.Tab',
                        font=(self.font_family, 12, 'bold'),
                        padding=[12, 8],
                        background='#485460',
                        foreground='#d2dae2')
        style.map('TNotebook.Tab',
                  background=[('selected', '#0fbcf9')],
                  foreground=[('selected', '#1e272e')])

        style.configure('TFrame', background='#2f3640')
        style.configure('TLabel', background='#2f3640', foreground='#d2dae2', font=(self.font_family, 11))
        style.configure('Header.TLabel', font=(self.font_family, 14, 'bold'), background='#2f3640', foreground='#0fbcf9')
        style.configure('Result.TLabel', font=(self.font_family, 12, 'bold'), background='#2f3640', foreground='#d2dae2')
        style.configure('TButton',
                        font=(self.font_family, 11),
                        padding=6,
                        background='#0fbcf9',
                        foreground='#1e272e')
        style.map('TButton',
                  background=[('active', '#54a0ff')],
                  foreground=[('active', '#1e272e')])

        style.configure('Result.TLabel', relief='groove', borderwidth=2, anchor='center', background='#2f3640', foreground='#0fbcf9')


    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=12, pady=12)

        self.tab_detect = ttk.Frame(nb)
        self.tab_scrape = ttk.Frame(nb)
        self.tab_train = ttk.Frame(nb)

        nb.add(self.tab_detect, text='Detect News')
        nb.add(self.tab_scrape, text='Scraping')
        nb.add(self.tab_train, text='Training & Settings')

        self._build_detect_tab()
        self._build_scrape_tab()
        self._build_train_tab()

    def _build_detect_tab(self):
        f = self.tab_detect
        f.columnconfigure(1, weight=1)
        f.rowconfigure(2, weight=1)

        ttk.Label(f, text='Title:', style='Header.TLabel').grid(row=0, column=0, sticky='w', padx=10, pady=(15,5))
        self.title_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.title_var, width=80, font=(self.font_family, 11)).grid(row=0, column=1, sticky='ew', padx=10, pady=(15,5))

        ttk.Label(f, text='URL (optional):', style='Header.TLabel').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.url_var = tk.StringVar()
        ttk.Entry(f, textvariable=self.url_var, width=80, font=(self.font_family, 11)).grid(row=1, column=1, sticky='ew', padx=10, pady=5)

        ttk.Label(f, text='Article Text:', style='Header.TLabel').grid(row=2, column=0, sticky='nw', padx=10, pady=5)
        self.text_box = scrolledtext.ScrolledText(f, width=80, height=18, font=(self.font_family, 11), wrap='word',
                                                  relief='solid', borderwidth=1,
                                                  background='#485460', foreground='#d2dae2', insertbackground='white')
        self.text_box.grid(row=2, column=1, sticky='nsew', padx=10, pady=5)

        btn_frame = ttk.Frame(f, style='TFrame')
        btn_frame.grid(row=3, column=1, sticky='ew', padx=10, pady=10)
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        ttk.Button(btn_frame, text='Classify Text', command=self.on_classify_text).grid(row=0, column=0, sticky='ew', padx=(0,5))
        ttk.Button(btn_frame, text='Upload Image (OCR)', command=self.on_upload_image).grid(row=0, column=1, sticky='ew', padx=(5,0))

        self.detect_result = ttk.Label(f, text='Result will be shown here', style='Result.TLabel', width=80, anchor='center')
        self.detect_result.grid(row=4, column=0, columnspan=2, sticky='ew', padx=10, pady=(10,20))

    def _build_scrape_tab(self):
        f = self.tab_scrape
        f.columnconfigure(0, weight=1)
        f.rowconfigure(1, weight=1)
        f.rowconfigure(5, weight=1)

        ttk.Label(f, text='Paste URLs (comma/newline separated):', style='Header.TLabel').grid(row=0, column=0, sticky='w', padx=10, pady=(15,5))
        self.scrape_text = scrolledtext.ScrolledText(f, width=90, height=8, font=(self.font_family, 11), wrap='word',
                                                     relief='solid', borderwidth=1,
                                                     background='#485460', foreground='#d2dae2', insertbackground='white')
        self.scrape_text.grid(row=1, column=0, sticky='nsew', padx=10)

        settings_frame = ttk.Frame(f, style='TFrame')
        settings_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        for i in range(4):
            settings_frame.columnconfigure(i, weight=1)

        ttk.Label(settings_frame, text='Target CSV:', style='Header.TLabel').grid(row=0, column=0, sticky='w')
        self.target_entry = tk.StringVar(value='true.csv')
        ttk.Entry(settings_frame, textvariable=self.target_entry, width=20, font=(self.font_family, 11)).grid(row=0, column=1, sticky='w')

        ttk.Label(settings_frame, text='Delay Min (s):', style='Header.TLabel').grid(row=0, column=2, sticky='e')
        self.delay_min = tk.StringVar(value='2')
        ttk.Entry(settings_frame, textvariable=self.delay_min, width=8, font=(self.font_family, 11)).grid(row=0, column=3, sticky='w', padx=(5,0))

        ttk.Label(settings_frame, text='Delay Max (s):', style='Header.TLabel').grid(row=1, column=2, sticky='e', pady=(5,0))
        self.delay_max = tk.StringVar(value='4')
        ttk.Entry(settings_frame, textvariable=self.delay_max, width=8, font=(self.font_family, 11)).grid(row=1, column=3, sticky='w', padx=(5,0), pady=(5,0))

        ttk.Button(f, text='Start Scrape', command=self.on_start_scrape).grid(row=3, column=0, sticky='w', padx=10, pady=5)

        self.scrape_log = scrolledtext.ScrolledText(f, width=90, height=12, font=(self.font_family, 11), state='disabled',
                                                    relief='solid', borderwidth=1,
                                                    background='#485460', foreground='#d2dae2', insertbackground='white')
        self.scrape_log.grid(row=5, column=0, sticky='nsew', padx=10, pady=(5,15))

    def _build_train_tab(self):
        f = self.tab_train
        f.columnconfigure(1, weight=1)

        ttk.Label(f, text='Random Seed:', style='Header.TLabel').grid(row=0, column=0, sticky='w', padx=10, pady=(15,10))
        self.seed_var = tk.StringVar(value='42')
        ttk.Entry(f, textvariable=self.seed_var, width=15, font=(self.font_family, 11)).grid(row=0, column=1, sticky='w', padx=10, pady=(15,10))

        btn_frame = ttk.Frame(f, style='TFrame')
        btn_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        ttk.Button(btn_frame, text='Train / Retrain Model', command=self.on_train).grid(row=0, column=0, sticky='ew', padx=5)
        ttk.Button(btn_frame, text='Evaluate Model', command=self.on_evaluate).grid(row=0, column=1, sticky='ew', padx=5)
        ttk.Button(btn_frame, text='Export Bag-of-Words CSV', command=self.on_export_bow).grid(row=0, column=2, sticky='ew', padx=5)
        ttk.Button(btn_frame, text='Reload Stopwords', command=self.on_reload_stopwords).grid(row=0, column=3, sticky='ew', padx=5)

        self.metrics_label = ttk.Label(f, text='Metrics will be shown here', style='Result.TLabel', width=80, anchor='center')
        self.metrics_label.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=(10,20))

    # Actions
    def on_classify_text(self):
        title = self.title_var.get().strip()
        text = self.text_box.get('1.0', 'end').strip()
        if not (title or text):
            messagebox.showwarning('Input', 'Please provide title or text')
            return
        pred, conf = classify_text(title, text)
        color = '#2ed573' if pred == 'REAL' else '#ff4757'
        self.detect_result.config(text=f'Prediction: {pred}\nConfidence: {conf:.3f}', foreground=color)

    def on_upload_image(self):
        p = filedialog.askopenfilename(filetypes=[('Images', '*.png;*.jpg;*.jpeg;*.bmp')])
        if not p:
            return
        pred, conf = classify_image(p)
        color = '#2ed573' if pred == 'REAL' else '#ff4757'
        self.detect_result.config(text=f'Prediction: {pred}\nConfidence: {conf:.3f}', foreground=color)

    def on_start_scrape(self):
        txt = self.scrape_text.get('1.0', 'end').strip()
        if not txt:
            messagebox.showwarning('No URLs', 'Enter URLs')
            return
        urls = [u.strip() for u in txt.replace(',', '\n').split('\n') if u.strip()]
        target = self.target_entry.get().strip() or 'true.csv'
        try:
            dmin = float(self.delay_min.get())
            dmax = float(self.delay_max.get())
        except Exception:
            messagebox.showerror('Error', 'Invalid delay values')
            return
        results = scrape_multiple(urls, target_csv=target, delay_min=dmin, delay_max=dmax)
        self.scrape_log.config(state='normal')
        for r in results:
            self.scrape_log.insert('end', str(r) + '\n')
        self.scrape_log.see('end')
        self.scrape_log.config(state='disabled')

    def on_train(self):
        try:
            seed = int(self.seed_var.get())
        except Exception:
            seed = 42
        train_or_load(seed=seed, retrain=True)
        messagebox.showinfo('Training', 'Training completed')

    def on_evaluate(self):
        try:
            seed = int(self.seed_var.get())
        except Exception:
            seed = 42
        metrics = evaluate_or_load(seed=seed)
        text = (f"Accuracy: {metrics['accuracy']:.3f}\n"
                f"Precision: {metrics['precision']:.3f}\n"
                f"Recall: {metrics['recall']:.3f}\n"
                f"F1: {metrics['f1']:.3f}")
        self.metrics_label.config(text=text)

    def on_export_bow(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV', '*.csv')])
        if not path:
            return
        import os
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        model_files = [f for f in os.listdir(model_dir) if f.startswith('vocab_seed')]
        if not model_files:
            messagebox.showwarning('No Vocab', 'No trained vocab found. Train first.')
            return
        path_v = os.path.join(model_dir, model_files[-1])
        from bow import Vocabulary, export_vocab_csv
        vocab = Vocabulary()
        vocab.load(path_v)
        export_vocab_csv(vocab, path)
        messagebox.showinfo('Export', 'Vocabulary exported')

    def on_reload_stopwords(self):
        reload_stopwords()
        messagebox.showinfo('Stopwords', 'Stopwords reloaded from data/stopwords.csv')

def run_gui():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    run_gui()
