import os, threading, requests, re, time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.utils import platform

# --- OPRAVA CERTIFIKÁTŮ PRO ANDROID ---
if platform == 'android':
    try:
        import certifi
        os.environ['SSL_CERT_FILE'] = certifi.where()
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    except Exception:
        pass

class IPTV_Master_v30_5(App):
    def build(self):
        self.all_data = []
        self.filtered_data = []
        # Identifikace jako prohlížeč, aby nás servery neblokovaly
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        self.root = BoxLayout(orientation='vertical')
        
        # Horní ovládací panel
        top = BoxLayout(orientation='vertical', size_hint_y=0.72, spacing=3, padding=5)
        
        self.status = Button(text="V30.5 - READY", size_hint_y=0.1, background_color=(0,0,0,1), disabled=True)
        top.add_widget(self.status)
        
        # Mřížka s hlavními tlačítky
        src_grid = GridLayout(cols=3, spacing=5, size_hint_y=0.3)
        
        btn_explore = Button(text="🔍 WEB\nINDEX", bold=True, background_color=(0.1, 0.5, 0.1, 1), font_size='11sp')
        btn_explore.bind(on_press=self.show_main_menu)
        src_grid.add_widget(btn_explore)
        
        btn_czsk = Button(text="🇨🇿/🇸🇰\nCZ-SK", bold=True, background_color=(0.1, 0.3, 0.6, 1), font_size='11sp')
        btn_czsk.bind(on_press=lambda inst: self.start_load("https://iptv-org.github.io/iptv/countries/cz.m3u"))
        src_grid.add_widget(btn_czsk)
        
        btn_free = Button(text="📺\nFREE TV", bold=True, background_color=(0.5, 0.2, 0.5, 1), font_size='11sp')
        btn_free.bind(on_press=lambda inst: self.start_load("https://raw.githubusercontent.com/glotovpa/Free-TV-IPTV/master/playlist.m3u8"))
        src_grid.add_widget(btn_free)
        top.add_widget(src_grid)

        # Vkládání vlastního linku
        url_row = BoxLayout(size_hint_y=0.15, spacing=5)
        self.custom_url = TextInput(hint_text="Vložit .m3u link...", multiline=False, font_size='14sp')
        btn_load = Button(text="NAČÍST", size_hint_x=0.25, bold=True, background_color=(0.7, 0.4, 0, 1))
        btn_load.bind(on_press=lambda x: self.start_load(self.custom_url.text))
        url_row.add_widget(self.custom_url)
        url_row.add_widget(btn_load)
        top.add_widget(url_row)

        # Hledání
        search_row = BoxLayout(size_hint_y=0.15, spacing=5)
        self.search_input = TextInput(hint_text="Hledat v seznamu...", multiline=False, font_size='16sp')
        self.search_input.bind(text=self.apply_filter)
        search_row.add_widget(self.search_input)
        top.add_widget(search_row)

        # Tlačítka pro akce
        act_row = BoxLayout(size_hint_y=0.15, spacing=5)
        btn_save = Button(text="ULOŽIT PLAYLIST", bold=True, background_color=(0, 0.5, 0.8, 1))
        btn_save.bind(on_press=self.save_to_device)
        act_row.add_widget(btn_save)
        top.add_widget(act_row)
        
        self.root.add_widget(top)

        # Spodní část (Seznam kanálů)
        self.display_area = BoxLayout(orientation='vertical', size_hint_y=0.28)
        self.grid = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll = ScrollView()
        self.scroll.add_widget(self.grid)
        self.display_area.add_widget(self.scroll)
        self.root.add_widget(self.display_area)
        
        return self.root

    def log(self, msg):
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', str(msg)))

    def save_to_device(self, instance):
        try:
            path = self.user_data_dir if platform == 'android' else "."
            fname = os.path.join(path, "moje_tv.m3u")
            m3u_content = "#EXTM3U\n"
            for c in self.filtered_data:
                m3u_content += f'#EXTINF:-1,{c["n"]}\n{c["u"]}\n'
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(m3u_content)
            self.log(f"ULOŽENO: {fname}")
        except Exception as e:
            self.log(f"CHYBA ULOŽENÍ: {str(e)[:20]}")

    def show_main_menu(self, i):
        self.grid.clear_widgets()
        self.log("NAČÍTÁM INDEX...")
        menu = {"🌍 ZEMĚ": "countries", "🎬 ŽÁNRY": "categories", "🗣 JAZYKY": "languages"}
        for name, path in menu.items():
            btn = Button(text=name, size_hint_y=None, height='60dp', background_color=(0.1, 0.1, 0.1, 1), bold=True)
            btn.bind(on_press=lambda inst, p=path: self.fetch_index(p))
            self.grid.add_widget(btn)

    def fetch_index(self, path):
        threading.Thread(target=self.fetch_index_logic, args=(path,), daemon=True).start()

    def fetch_index_logic(self, path):
        try:
            v = certifi.where() if platform == 'android' else True
            url = f"https://api.github.com/repos/iptv-org/iptv/contents/{path}"
            r = requests.get(url, headers=self.headers, timeout=15, verify=v)
            if r.status_code == 200:
                items = [{"n": f['name'].replace('.m3u', '').upper(), "u": f['download_url']} 
                         for f in r.json() if f['name'].endswith('.m3u')]
                Clock.schedule_once(lambda dt: self.display_index(items))
                self.log(f"NAČTENO: {len(items)} POLOŽEK")
            else:
                self.log(f"API CHYBA: {r.status_code}")
        except Exception as e:
            self.log(f"CHYBA SÍTĚ: {str(e)[:20]}")

    def display_index(self, items):
        self.grid.clear_widgets()
        for item in items:
            btn = Button(text=item['n'], size_hint_y=None, height='45dp', background_color=(0.15, 0.15, 0.15, 1))
            btn.bind(on_press=lambda inst, u=item['u']: self.start_load(u))
            self.grid.add_widget(btn)

    def start_load(self, url):
        if not url: return
        self.all_data = []
        threading.Thread(target=self.load_logic, args=(url,), daemon=True).start()

    def load_logic(self, url):
        self.log("STAHOVÁNÍ...")
        try:
            r = requests.get(url, headers=self.headers, timeout=20, verify=False)
            r.encoding = 'utf-8'
            temp = []; last_name = "Neznámý"
            for line in r.text.splitlines():
                line = line.strip()
                if line.upper().startswith("#EXTINF"):
                    if "," in line: last_name = line.split(",")[-1].strip()
                elif line.startswith("http"):
                    is_cz = any(x in (last_name + " " + line).lower() for x in ["cz", "sk", "hbo", "nova", "czech"])
                    temp.append({"n": last_name, "u": line, "raw": (last_name + " " + line).lower(), "cz": is_cz})
            
            self.all_data = sorted(temp, key=lambda x: x["cz"], reverse=True)
            self.log(f"NAČTENO: {len(self.all_data)} KANÁLŮ")
            Clock.schedule_once(lambda dt: self.apply_filter())
        except Exception:
            self.log("CHYBA NAČÍTÁNÍ M3U")

    def apply_filter(self, *args):
        query = self.search_input.text.lower().strip()
        if not query:
            self.filtered_data = self.all_data
        else:
            self.filtered_data = [x for x in self.all_data if query in x['raw']]
        self.refresh_ui()

    def refresh_ui(self, *args):
        self.grid.clear_widgets()
        # Zobrazíme jen prvních 100 pro rychlost, zbytek se prohledá filtrem
        for c in self.filtered_data[:100]:
            prefix = "⭐ " if c['cz'] else ""
            btn = Button(text=f"{prefix}{c['n'].upper()}", size_hint_y=None, height='50dp',
                         background_color=(0.05, 0.1, 0.2, 1) if c["cz"] else (0.1, 0.1, 0.1, 1))
            btn.bind(on_press=lambda inst, u=c["u"]: self.play(u))
            self.grid.add_widget(btn)

    def play(self, url):
        if platform == 'android':
            try:
                from jnius import autoclass, cast
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(Uri.parse(url), "video/*")
                currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
                currentActivity.startActivity(intent)
            except Exception as e:
                self.log("CHYBA PŘEHRÁVAČE")
        else:
            print(f"Přehrávám link: {url}")

if __name__ == '__main__':
    IPTV_Master_v30_5().run()
