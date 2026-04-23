"""
User interface for the engineering calculator.
"""

import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QSizePolicy, QFrame, QListWidget, QListWidgetItem,
    QMenuBar, QMenu, QAction, QShortcut
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QKeySequence, QIcon
from .config import THEMES, CURRENT_THEME, get_text, save_theme, save_language
from .styles import make_btn
from .logic import CalculatorLogic

theme = THEMES[CURRENT_THEME]

class EngCalcUI(QMainWindow):
    """Main calculator window."""

    def __init__(self):
        super().__init__()
        self.logic = CalculatorLogic()
        self.setWindowTitle(get_text('window_title'))
        self.setMinimumSize(680, 620)
        self.setStyleSheet(f"background: {theme['DARK_BG']};")

        self._build_menu()
        self._build_ui()
        self._connect_keyboard()
        self._update_display()

    def _build_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu(get_text('file_menu'))
        exit_action = QAction(get_text('exit'), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        view_menu = menubar.addMenu(get_text('view_menu'))
        theme_menu = view_menu.addMenu(get_text('theme_menu'))
        dark_action = QAction(get_text('dark_theme'), self)
        dark_action.triggered.connect(lambda: self.change_theme('dark'))
        theme_menu.addAction(dark_action)
        light_action = QAction(get_text('light_theme'), self)
        light_action.triggered.connect(lambda: self.change_theme('light'))
        theme_menu.addAction(light_action)

        lang_menu = view_menu.addMenu(get_text('lang_menu'))
        ru_action = QAction(get_text('russian'), self)
        ru_action.triggered.connect(lambda: self.change_lang('ru'))
        lang_menu.addAction(ru_action)
        en_action = QAction(get_text('english'), self)
        en_action.triggered.connect(lambda: self.change_lang('en'))
        lang_menu.addAction(en_action)

    def change_theme(self, theme_name):
        save_theme(theme_name)
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, get_text('window_title'), get_text('restart_required'))

    def change_lang(self, lang):
        save_language(lang)
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, get_text('window_title'), get_text('restart_required'))

    def _build_ui(self):
        root = QWidget()
        root.setStyleSheet(f"background: {theme['DARK_BG']};")
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(10, 10, 10, 10)
        root_layout.setSpacing(10)

        # Левая колонка — основной калькулятор
        left = QWidget()
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(8)

        lv.addWidget(self._build_display())
        lv.addWidget(self._build_status_bar())
        lv.addWidget(self._build_buttons())

        # Правая колонка — история
        right = QWidget()
        right.setMinimumWidth(155)
        right.setMaximumWidth(195)
        rv = QVBoxLayout(right)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(4)
        rv.addWidget(self._build_history_panel())

        root_layout.addWidget(left, stretch=3)
        root_layout.addWidget(right, stretch=1)
        self.setCentralWidget(root)

    def _build_display(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {theme['DISPLAY_BG']};
                border: 1px solid {theme['BORDER']};
                border-radius: 12px;
            }}
        """)
        v = QVBoxLayout(frame)
        v.setContentsMargins(14, 10, 14, 10)
        v.setSpacing(2)

        self.lbl_expr = QLabel("")
        self.lbl_expr.setFont(QFont("Consolas", 11))
        self.lbl_expr.setStyleSheet(f"color: {theme['TEXT_EXPR']}; background: transparent; border: none;")
        self.lbl_expr.setAlignment(Qt.AlignRight)
        self.lbl_expr.setMinimumHeight(18)

        self.lbl_display = QLabel("0")
        self.lbl_display.setFont(QFont("Consolas", 28, QFont.Bold))
        self.lbl_display.setStyleSheet(f"color: {theme['TEXT_WHITE']}; background: transparent; border: none;")
        self.lbl_display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_display.setMinimumHeight(46)
        self.lbl_display.setWordWrap(True)

        v.addWidget(self.lbl_expr)
        v.addWidget(self.lbl_display)
        return frame

    def _build_status_bar(self):
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(6)

        def badge(text, attr):
            lbl = QLabel(text)
            lbl.setFont(QFont("Consolas", 10))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFixedSize(46, 20)
            lbl.setStyleSheet(f"""
                color: {theme['TEXT_MUTED']}; background: {theme['PANEL_BG']};
                border: 1px solid {theme['BORDER']}; border-radius: 4px;
            """)
            setattr(self, attr, lbl)
            return lbl

        h.addWidget(badge(get_text('degrees'), "badge_deg"))
        h.addWidget(badge(get_text('radians'), "badge_rad"))
        h.addWidget(badge(get_text('memory'), "badge_mem"))
        h.addWidget(badge(get_text('inverse'), "badge_inv"))
        h.addStretch()
        self._update_badges()
        return w

    def _badge_on(self, lbl):
        lbl.setStyleSheet(f"""
            color: {theme['ACCENT_BLUE']}; background: #0d1a3a;
            border: 1px solid {theme['ACCENT_BLUE']}; border-radius: 4px;
        """)

    def _badge_off(self, lbl):
        lbl.setStyleSheet(f"""
            color: {theme['TEXT_MUTED']}; background: {theme['PANEL_BG']};
            border: 1px solid {theme['BORDER']}; border-radius: 4px;
        """)

    def _update_badges(self):
        if self.logic.angle_mode == "DEG":
            self._badge_on(self.badge_deg);  self._badge_off(self.badge_rad)
        else:
            self._badge_off(self.badge_deg); self._badge_on(self.badge_rad)
        if self.logic.memory != 0:
            self._badge_on(self.badge_mem)
        else:
            self._badge_off(self.badge_mem)
        if self.logic.inv_mode:
            self._badge_on(self.badge_inv)
        else:
            self._badge_off(self.badge_inv)

    def _build_buttons(self):
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        g = QGridLayout(w)
        g.setSpacing(5)
        g.setContentsMargins(0, 0, 0, 0)

        def add(btn, r, c, rspan=1, cspan=1):
            g.addWidget(btn, r, c, rspan, cspan)

        # ── Строка 0: режимы и очистка ──────────────────────────────────────
        btn_angle = make_btn(get_text('deg_rad'), "mode")
        btn_angle.clicked.connect(self.toggle_angle)
        add(btn_angle, 0, 0)

        btn_inv = make_btn(get_text('inv_toggle'), "mode")
        btn_inv.clicked.connect(self.toggle_inv)
        add(btn_inv, 0, 1)

        btn_x2 = make_btn(get_text('square'), "fn")
        btn_x2.clicked.connect(lambda: self.input_fn("pow2"))
        add(btn_x2, 0, 2)

        btn_xn = make_btn(get_text('power'), "fn")
        btn_xn.clicked.connect(lambda: self.input_str("**"))
        add(btn_xn, 0, 3)

        btn_pct = make_btn(get_text('pct'), "fn")
        btn_pct.clicked.connect(lambda: self.input_fn("pct"))
        add(btn_pct, 0, 4)

        btn_ac = make_btn(get_text('clear'), "clr")
        btn_ac.clicked.connect(self.clear_all)
        add(btn_ac, 0, 5)

        # ── Строка 1: тригонометрия ────────────────────────────────────────
        for col, fn in enumerate(["sin", "cos", "tan", "log", "ln"]):
            b = make_btn(get_text(fn), "fn")
            b.clicked.connect(lambda _, f=fn: self.input_fn(f))
            add(b, 1, col)

        btn_del = make_btn(get_text('delete'), "clr")
        btn_del.clicked.connect(self.del_last)
        add(btn_del, 1, 5)

        # ── Строка 2: гиперболические / доп. ─────────────────────────────
        for col, (lbl, fn) in enumerate([
            ("sinh","sinh"),("cosh","cosh"),("tanh","tanh"),
            ("log2","log2"),("exp","exp"),("sqrt","sqrt")
        ]):
            b = make_btn(get_text(lbl), "fn")
            b.clicked.connect(lambda _, f=fn: self.input_fn(f))
            add(b, 2, col)

        # ── Строка 3: константы + доп. ────────────────────────────────────
        for col, (lbl, fn) in enumerate([
            ("pi","PI"),("e_const","E"),("phi","PHI"),
            ("abs","abs"),("fact","fact"),("cbrt","cbrt")
        ]):
            kind = "const" if col < 3 else "fn"
            b = make_btn(get_text(lbl), kind)
            if col < 3:
                b.clicked.connect(lambda _, c=fn: self.input_const(c))
            else:
                b.clicked.connect(lambda _, f=fn: self.input_fn(f))
            add(b, 3, col)

        # ── Строка 4: память ─────────────────────────────────────────────
        for col, (lbl, fn) in enumerate([
            ("mc","mc"),("mr","mr"),("mplus","m+"),("mminus","m-"),
            ("inv","inv"),("floor","floor")
        ]):
            b = make_btn(get_text(lbl), "mem" if col < 4 else "fn")
            b.clicked.connect(lambda _, f=fn: self.mem_action(f))
            add(b, 4, col)

        # ── Строка 5: скобки и операции ──────────────────────────────────
        for col, (lbl, val) in enumerate([
            ("(","("), (")",")"), ("ee","e"),
            ("divide","/"),  ("multiply","*"), ("minus","-")
        ]):
            kind = "op" if col >= 3 else "fn"
            b = make_btn(get_text(lbl), kind)
            b.clicked.connect(lambda _, v=val: self.input_str(v))
            add(b, 5, col)

        # ── Цифровой блок ─────────────────────────────────────────────────
        for col, dig in enumerate(["7", "8", "9"]):
            b = make_btn(dig, "num")
            b.clicked.connect(lambda _, d=dig: self.input_num(d))
            add(b, 6, col)

        btn_neg = make_btn(get_text('neg'), "fn")
        btn_neg.clicked.connect(self.toggle_sign)
        add(btn_neg, 6, 3)

        btn_plus = make_btn(get_text('plus'), "op")
        btn_plus.clicked.connect(lambda: self.input_str("+"))
        add(btn_plus, 6, 4, 2, 1)  # span 2 rows

        btn_mod = make_btn(get_text('modulo'), "fn")
        btn_mod.clicked.connect(lambda: self.input_str("%"))
        add(btn_mod, 6, 5)

        for col, dig in enumerate(["4", "5", "6"]):
            b = make_btn(dig, "num")
            b.clicked.connect(lambda _, d=dig: self.input_num(d))
            add(b, 7, col)

        btn_ceil = make_btn(get_text('ceil'), "fn")
        btn_ceil.clicked.connect(lambda: self.input_fn("ceil"))
        add(btn_ceil, 7, 3)

        btn_rnd = make_btn(get_text('round'), "fn")
        btn_rnd.clicked.connect(lambda: self.input_fn("round"))
        add(btn_rnd, 7, 5)

        for col, dig in enumerate(["1", "2", "3"]):
            b = make_btn(dig, "num")
            b.clicked.connect(lambda _, d=dig: self.input_num(d))
            add(b, 8, col)

        btn_eq = make_btn(get_text('equals'), "eq")
        btn_eq.clicked.connect(self.calculate)
        add(btn_eq, 8, 3, 1, 2)

        btn_cbrt = make_btn(get_text('cbrt'), "fn")
        btn_cbrt.clicked.connect(lambda: self.input_fn("cbrt"))
        add(btn_cbrt, 8, 5)

        btn_0 = make_btn("0", "num")
        btn_0.clicked.connect(lambda: self.input_num("0"))
        add(btn_0, 9, 0, 1, 2)

        btn_dot = make_btn(get_text('dot'), "num")
        btn_dot.clicked.connect(self.input_dot)
        add(btn_dot, 9, 2)

        btn_pow10 = make_btn(get_text('pow10'), "fn")
        btn_pow10.clicked.connect(lambda: self.input_fn("pow10"))
        add(btn_pow10, 9, 3)

        btn_ans = make_btn(get_text('ans'), "fn")
        btn_ans.clicked.connect(self.recall_ans)
        add(btn_ans, 9, 4)

        btn_pi2 = make_btn(get_text('pi_half'), "const")
        btn_pi2.clicked.connect(lambda: self.input_str(str(math.pi / 2)[:10]))
        add(btn_pi2, 9, 5)

        return w

    def _build_history_panel(self):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {theme['PANEL_BG']};
                border: 1px solid {theme['BORDER']};
                border-radius: 12px;
            }}
        """)
        v = QVBoxLayout(frame)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(6)

        title_row = QHBoxLayout()
        lbl = QLabel(get_text('history_title'))
        lbl.setFont(QFont("Consolas", 11))
        lbl.setStyleSheet(f"color: {theme['TEXT_MUTED']}; background: transparent; border: none;")
        btn_clr = QPushButton(get_text('clear_history'))
        btn_clr.setFont(QFont("Consolas", 9))
        btn_clr.setStyleSheet(f"""
            QPushButton {{ color: {theme['ACCENT_RED']}; background: transparent; border: none; }}
            QPushButton:hover {{ color: #ff8888; }}
        """)
        btn_clr.clicked.connect(self.clear_history)
        title_row.addWidget(lbl)
        title_row.addStretch()
        title_row.addWidget(btn_clr)
        v.addLayout(title_row)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {theme['BORDER']}; background: {theme['BORDER']};")
        sep.setFixedHeight(1)
        v.addWidget(sep)

        self.hist_list = QListWidget()
        self.hist_list.setStyleSheet(f"""
            QListWidget {{
                background: transparent;
                border: none;
                color: {theme['TEXT_WHITE']};
                font-family: Consolas;
                font-size: 11px;
            }}
            QListWidget::item {{ padding: 4px 2px; border-bottom: 1px solid {theme['BORDER']}; }}
            QListWidget::item:hover {{ background: {theme['CARD_BG']}; border-radius: 4px; }}
            QListWidget::item:selected {{ background: #1f2a4a; border-radius: 4px; }}
        """)
        self.hist_list.itemClicked.connect(self._recall_history)
        self._populate_history()
        v.addWidget(self.hist_list)
        return frame

    def _populate_history(self):
        self.hist_list.clear()
        for expr, val in self.logic.get_history_items():
            item = QListWidgetItem(f"{expr}\n= {val}")
            item.setData(Qt.UserRole, val)
            self.hist_list.addItem(item)

    # ── Обработчики событий ─────────────────────────────────────────────────

    def input_num(self, d):
        self._update_display(self.logic.input_num(d))

    def input_dot(self):
        self._update_display(self.logic.input_dot())

    def input_str(self, s):
        self._update_display(self.logic.input_str(s))

    def input_const(self, c):
        self._update_display(self.logic.input_const(c))

    def toggle_sign(self):
        self._update_display(self.logic.toggle_sign())

    def input_fn(self, fn):
        """Добавляет функцию в выражение как текст"""
        self._update_display(self.logic.input_fn(fn))

    def apply_fn(self, fn):
        val, expr = self.logic.apply_fn(fn)
        self._update_display(val, expr)
        self._update_badges()
        self._populate_history()

    def calculate(self):
        val, expr = self.logic.calculate()
        self._update_display(val, expr)
        self._populate_history()

    def clear_all(self):
        val, expr = self.logic.clear_all()
        self._update_display(val, expr)

    def del_last(self):
        self._update_display(self.logic.del_last())

    def recall_ans(self):
        self._update_display(self.logic.recall_ans())

    def mem_action(self, act):
        result = self.logic.mem_action(act)
        if result:
            self._update_display(result)
        self._update_badges()

    def toggle_angle(self):
        self.logic.toggle_angle()
        self._update_badges()

    def toggle_inv(self):
        self.logic.toggle_inv()
        self._update_badges()

    def _recall_history(self, item):
        val = item.data(Qt.UserRole)
        self.logic.recall_history(val)
        self._update_display(val)

    def clear_history(self):
        self.logic.clear_history()
        self._populate_history()

    def _update_display(self, val=None, expr_text=""):
        self.lbl_display.setText(val if val is not None else (self.logic.expr or "0"))
        self.lbl_expr.setText(expr_text)

    # ── Клавиатура ─────────────────────────────────────────────────────────────
    def _connect_keyboard(self):
        # Add shortcuts
        QShortcut(QKeySequence("Ctrl+C"), self).activated.connect(self.copy_result)
        QShortcut(QKeySequence("Ctrl+V"), self).activated.connect(self.paste_expr)
        QShortcut(QKeySequence("Ctrl+H"), self).activated.connect(self.clear_history)

    def copy_result(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.lbl_display.text())

    def paste_expr(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text.replace('.', '').replace('-', '').isdigit():
            self.logic.expr = text
            self._update_display()

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        if text.isdigit():
            self.input_num(text)
        elif text == ".":
            self.input_dot()
        elif text in "+-*/":
            self.input_str(text)
        elif text == "(":
            self.input_str("(")
        elif text == ")":
            self.input_str(")")
        elif text == "^":
            self.input_str("**")
        elif text == "%":
            self.input_str("%")
        elif key in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Equal):
            self.calculate()
        elif key == Qt.Key_Backspace:
            self.del_last()
        elif key == Qt.Key_Escape:
            self.clear_all()
        else:
            super().keyPressEvent(event)