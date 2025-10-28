import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QScrollArea, QFrame, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QPixmap, QFont, QPainter, QBrush, QColor, QPalette
from PyQt5.QtCore import QRect, QSize


class CircularLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(120, 120)
        self.setScaledContents(False)

    def setPixmap(self, pixmap):
        if pixmap:
            # Масштабируем изображение до круглой формы
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

            # Создаем круглую маску
            result_pixmap = QPixmap(100, 100)
            result_pixmap.fill(Qt.transparent)

            painter = QPainter(result_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(scaled_pixmap))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, 100, 100)
            painter.end()

            super().setPixmap(result_pixmap)


class HoverButton(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            HoverButton {
                background-color: white;
                color: #667eea;
                padding: 8px 16px;
                border-radius: 12px;
                font-weight: bold;
                border: 1px solid #667eea;
            }
            HoverButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.PointingHandCursor)


class UserProfilePyQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.avatar_path = None
        self.upload_btn = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Профиль пользователя - PyQt")
        self.setGeometry(100, 100, 450, 600)
        self.setMinimumSize(400, 500)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Создаем прокручиваемую область
        self.create_scrollable_area(main_layout)

    def create_scrollable_area(self, parent_layout):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #f8f9fa; }")

        # Содержимое прокрутки
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #f8f9fa;")
        scroll_area.setWidget(content_widget)

        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        parent_layout.addWidget(scroll_area)

        # Создаем интерфейс
        self.create_header_section(content_layout)
        self.create_profile_section(content_layout)

    def create_header_section(self, parent_layout):
        header_widget = QWidget()
        header_widget.setFixedHeight(180)
        header_widget.setStyleSheet("background-color: #667eea;")

        header_layout = QVBoxLayout(header_widget)
        header_layout.setAlignment(Qt.AlignCenter)

        # Контейнер для аватарки
        avatar_container = QWidget()
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setAlignment(Qt.AlignCenter)

        # Создаем аватарку
        self.avatar_label = CircularLabel()
        self.create_default_avatar()

        # Кнопка загрузки
        self.upload_btn = HoverButton("📷 Загрузить фото")
        self.upload_btn.setFixedSize(140, 30)
        self.upload_btn.hide()

        # Подключаем события
        self.avatar_label.mousePressEvent = self.upload_photo
        self.upload_btn.mousePressEvent = self.upload_photo

        # Показываем кнопку при наведении на аватарку
        self.avatar_label.enterEvent = self.on_avatar_enter
        self.avatar_label.leaveEvent = self.on_avatar_leave
        self.upload_btn.enterEvent = self.on_button_enter
        self.upload_btn.leaveEvent = self.on_button_leave

        avatar_layout.addWidget(self.avatar_label)
        avatar_layout.addWidget(self.upload_btn)

        header_layout.addWidget(avatar_container)
        parent_layout.addWidget(header_widget)

    def on_avatar_enter(self, event):
        self.upload_btn.show()

    def on_avatar_leave(self, event):
        if not self.upload_btn.underMouse():
            self.upload_btn.hide()

    def on_button_enter(self, event):
        pass

    def on_button_leave(self, event):
        if not self.avatar_label.underMouse():
            self.upload_btn.hide()

    def create_default_avatar(self):
        """Создание аватарки по умолчанию"""
        pixmap = QPixmap(100, 100)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Рисуем круг
        painter.setBrush(QBrush(QColor('#e74c3c')))
        painter.setPen(QColor('white'))
        painter.drawEllipse(0, 0, 100, 100)

        # Рисуем текст
        painter.setPen(QColor('white'))
        painter.setFont(QFont('Arial', 24, QFont.Bold))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "ВН")
        painter.end()

        self.avatar_label.setPixmap(pixmap)

    def upload_photo(self, event):
        """Загрузка фотографии"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите фотографию",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif *.tiff);;Все файлы (*)"
        )

        if file_path:
            try:
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    self.avatar_label.setPixmap(pixmap)
                    self.avatar_path = file_path
                    self.upload_btn.hide()
                    QMessageBox.information(self, "Успех", "Фотография успешно загружена!")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение")

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке фото: {str(e)}")

    def create_profile_section(self, parent_layout):
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: white;")

        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Отступ сверху
        content_layout.addSpacing(30)

        # Имя
        name_label = QLabel("Владимир Небогатиков")
        name_label.setStyleSheet("""
            font-size: 22px; 
            font-weight: bold; 
            color: #2c3e50;
            padding: 0px;
            margin: 0px;
        """)
        name_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(name_label)

        # Должность
        position_label = QLabel("Студент 2 курса")
        position_label.setStyleSheet("""
            font-size: 14px; 
            color: #7f8c8d;
            padding: 0px;
            margin: 0px 0px 25px 0px;
        """)
        position_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(position_label)

        # Разделитель
        self.create_separator(content_layout)

        # Биография
        self.create_info_section(content_layout, "Биография",
                                 "Уроженец города Щёлково. Сейчас учусь в МАИ на направлении 'Инноватика'. Увлекаюсь UFC, футболом, баскетболом. Имею рельефный пресс.")

        self.create_separator(content_layout)

        # Навыки
        self.create_info_section(content_layout, "Навыки", "Python, MySQL")

        self.create_separator(content_layout)

        # Опыт работы
        self.create_experience_section(content_layout)

        # Отступ снизу
        content_layout.addSpacing(30)

        parent_layout.addWidget(content_widget)

    def create_separator(self, parent_layout):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #ecf0f1; margin: 20px 30px;")
        separator.setFixedHeight(1)
        parent_layout.addWidget(separator)

    def create_info_section(self, parent_layout, title, content):
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(30, 0, 30, 0)

        # Заголовок
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignLeft)
        section_layout.addWidget(title_label)

        # Содержимое
        content_label = QLabel(content)
        content_label.setStyleSheet("""
            font-size: 12px; 
            color: #34495e;
            margin: 0px;
        """)
        content_label.setWordWrap(True)
        content_label.setAlignment(Qt.AlignLeft)
        section_layout.addWidget(content_label)

        parent_layout.addWidget(section_widget)

    def create_experience_section(self, parent_layout):
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(30, 0, 30, 0)

        # Заголовок раздела
        title_label = QLabel("Опыт работы")
        title_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        title_label.setAlignment(Qt.AlignLeft)
        section_layout.addWidget(title_label)

        # Опыт 1
        exp1_widget = QWidget()
        exp1_layout = QVBoxLayout(exp1_widget)

        exp1_title = QLabel("Разнорабочий")
        exp1_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #2c3e50;")
        exp1_title.setWordWrap(True)
        exp1_layout.addWidget(exp1_title)

        exp1_company = QLabel("ООО 'Дядя Рафик'")
        exp1_company.setStyleSheet("font-size: 12px; color: #3498db; margin-top: 5px;")
        exp1_layout.addWidget(exp1_company)

        exp1_period = QLabel("Лето 2023")
        exp1_period.setStyleSheet("font-size: 11px; color: #7f8c8d; margin-top: 2px;")
        exp1_layout.addWidget(exp1_period)

        section_layout.addWidget(exp1_widget)
        section_layout.addSpacing(20)

        # Опыт 2
        exp2_widget = QWidget()
        exp2_layout = QVBoxLayout(exp2_widget)

        exp2_title = QLabel("Технический инженер")
        exp2_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #2c3e50;")
        exp2_layout.addWidget(exp2_title)

        exp2_company = QLabel("У бати")
        exp2_company.setStyleSheet("font-size: 12px; color: #3498db; margin-top: 5px;")
        exp2_layout.addWidget(exp2_company)

        exp2_period = QLabel("Июнь 2025 - настоящее время")
        exp2_period.setStyleSheet("font-size: 11px; color: #7f8c8d; margin-top: 2px;")
        exp2_layout.addWidget(exp2_period)

        section_layout.addWidget(exp2_widget)
        parent_layout.addWidget(section_widget)


def main():
    app = QApplication(sys.argv)

    # Устанавливаем стиль приложения
    app.setStyle('Fusion')

    window = UserProfilePyQt()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()