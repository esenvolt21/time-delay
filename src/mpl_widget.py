from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplGraphicsResearch(FigureCanvas):
    """
    Функция отрисовки
    """
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi, facecolor=(.94, .94, .94, 0.), figsize=(4, 3))

        # Добавление области графа
        self.ax = self.fig.add_subplot(111)
        self.add_text()

        # Инициализация
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Policy.Expanding,
                                   QtWidgets.QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)

    def add_text(self):
        """
        Инициализация графика.
        """
        # Инициализация области графика модулированного сигнала
        self.ax.set_title("График зависимости BER от SNR")
        self.ax.grid(linestyle="dotted", alpha=0.65)

    def plot_graph(self, x_am: list, y_am: list, errors_am: list,
                   x_fm: list, y_fm: list, errors_fm: list,
                   x_pm: list, y_pm: list, errors_pm: list):
        """
        Построение графика функции модулированного сигнала.
        """
        self.ax.errorbar(x_am, y_am, yerr=errors_am, fmt='o', linestyle='-', markersize=3, elinewidth=0.5,
                         ecolor='black', color='r', label="AM", capsize=2, capthick=0.5)
        self.ax.errorbar(x_fm, y_fm, yerr=errors_fm, fmt='o', linestyle='-', markersize=3, elinewidth=0.5,
                         ecolor='black', color='g', label="FM", capsize=2, capthick=0.5)
        self.ax.errorbar(x_pm, y_pm, yerr=errors_pm, fmt='o', linestyle='-', markersize=3, elinewidth=0.5,
                         ecolor='black', color='b', label="PM", capsize=2, capthick=0.5)

        self.ax.legend(loc="lower right", framealpha=1.0)

    def clear_plot(self):
        """
        Очистка области графика.
        """
        self.ax.clear()
        self.add_text()


class MplGraphicsModulated(FigureCanvas):
    """
    Функция отрисовки
    """
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi, facecolor=(.94, .94, .94, 0.), figsize=(4, 3))

        # Добавление области графа
        self.ax1 = self.fig.add_subplot(411)
        self.ax2 = self.fig.add_subplot(412)
        self.ax3 = self.fig.add_subplot(413)
        self.ax4 = self.fig.add_subplot(414)
        self.add_text()

        # Инициализация
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Policy.Expanding,
                                   QtWidgets.QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)

    def add_text(self):
        """
        Инициализация графика.

        :return: None.
        """
        # Инициализация области графика модулированного сигнала
        self.ax1.grid(linestyle="dotted", alpha=0.65)
        self.ax2.grid(linestyle="dotted", alpha=0.65)
        self.ax3.grid(linestyle="dotted", alpha=0.65)
        self.ax4.grid(linestyle="dotted", alpha=0.65)

    def plot_graph_ax1(self, x_list: list, y_list: list):
        """
        Построение графика битов.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax1.plot(x_list, y_list, linestyle="-", markersize=2, color='r', label="Информационные биты")
        self.ax1.legend(loc="upper right", framealpha=1.0)
        self.ax1.margins(y=0.8)

    def plot_graph_ax2(self, x_list: list, y_list: list):
        """
        Построение графика модулированного сигнала.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax2.plot(x_list, y_list, linestyle="-", markersize=2, color='g', label="Модулированный сигнал")
        self.ax2.legend(loc="upper right", framealpha=1.0)
        self.ax2.margins(y=0.8)

    def plot_graph_ax3(self, x_list: list, y_list: list):
        """
        Построение графика исследуемого сигнала.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax3.plot(x_list, y_list, linestyle="-", markersize=2, color='b', label="Исследуемый сигнал")
        self.ax3.legend(loc="upper right", framealpha=1.0)
        self.ax3.margins(y=0.8)

    def plot_graph_ax4(self, x_list: list, y_list: list):
        """
        Построение графика корреляции.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax4.plot(x_list, y_list, linestyle="-", markersize=2, color='purple', label="Корреляционная функция")
        self.ax4.legend(loc="upper right", framealpha=1.0)
        self.ax4.margins(y=0.8)

    def clear_plot_ax1(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax1.clear()
        self.add_text()

    def clear_plot_ax2(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax2.clear()
        self.add_text()

    def clear_plot_ax3(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax3.clear()
        self.add_text()

    def clear_plot_ax4(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax4.clear()
        self.add_text()
