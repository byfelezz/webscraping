import requests
import json
from bs4 import BeautifulSoup
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QDesktopWidget, QMessageBox

class WebScraperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.url_label = QLabel("Sayfa URL:")
        self.url_entry = QLineEdit()

        self.results_text = QTextEdit()
        self.search_button = QPushButton("Veriyi Çek")
        self.search_button.clicked.connect(self.scrape_data)

        self.keyword_label = QLabel("Aramak İstediğiniz Kelime/Kelimeler (virgülle ayırın):")
        self.keyword_entry = QLineEdit()
        self.search_keyword_button = QPushButton("Arama Yap")
        self.search_keyword_button.clicked.connect(self.search_data)

        v_layout = QVBoxLayout()
        v_layout.addWidget(self.url_label)
        v_layout.addWidget(self.url_entry)
        v_layout.addWidget(self.search_button)
        v_layout.addWidget(self.results_text)
        v_layout.addWidget(self.keyword_label)
        v_layout.addWidget(self.keyword_entry)
        v_layout.addWidget(self.search_keyword_button)

        self.setLayout(v_layout)

        self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle("Web Veri Çekme ve Arama Aracı")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def scrape_data(self):
        url = self.url_entry.text()
        if not url:
            QMessageBox.critical(self, "Hata", "Lütfen bir Sayfa URL'si girin.")
            return

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            data = {
                "title": soup.title.string,
                "paragraphs": [p.get_text() for p in soup.find_all('p')],
                "links": [a['href'] for a in soup.find_all('a')]
            }

            json_data = json.dumps(data, ensure_ascii=False, indent=4)
            self.results_text.setPlainText(json_data)
        except Exception as e:
            self.results_text.setPlainText("Hata oluştu: " + str(e))

    def search_data(self):
        keywords = self.keyword_entry.text().split(',')
        data = self.results_text.toPlainText()
        if not data:
            QMessageBox.critical(self, "Hata", "Veri çekilmedi.")
            return

        matching_data = []
        json_data = json.loads(data)
        for keyword in keywords:
            for key, value in json_data.items():
                if isinstance(value, list):
                    matching_data.extend([f"{key}: {item}" for item in value if keyword.strip() in item])
                elif keyword.strip() in value:
                    matching_data.append(f"{key}: {value}")

        if matching_data:
            self.results_text.setPlainText('\n'.join(matching_data))
        else:
            self.results_text.setPlainText("Aranan kelime/kelimeler için eşleşen veri bulunamadı.")

def main():
    app = QApplication(sys.argv)
    ex = WebScraperApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()