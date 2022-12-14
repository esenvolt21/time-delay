import random
import numpy as np

from defaults import *
from enums import SignalType, ModulationType


class SignalGenerator:
    """
    Объект для генерации опорного сигнала
    """
    def __init__(self,
                 s_r=DEFAULT_SAMPLING_RATE, s_freq=DEFAULT_SIGNAL_FREQ,
                 b_count=DEFAULT_BITS_COUNT, bps=DEFAULT_BITS_PER_SECOND,
                 t_delay=DEFAULT_TIME_DELAY, snr=DEFAULT_SNR):

        # Параметры сигнала
        self.sampling_rate = float(s_r)
        self.signal_freq = float(s_freq)
        self.bits_count = int(b_count)
        self.bits_per_second = float(bps)
        self.time_delay = float(t_delay)
        self.snr = float(snr)
        self.signal_phase = 0.

        # Буферы для хранения сигналов
        self.bits = []
        self.general_signal = []
        self.modulated_signal = []
        self.research_signal = []
        self.correlation_signal = []

        # Параметры для АМ
        # Амплитуда, B
        self.low_ampl = 1.
        self.high_ampl = 10.

        # Параметры для ФМ
        # Индекc модуляции
        self.mod_index = 1.8

        # Расчет параметров
        # Минимальная и максимальная частота,Гц
        self.low_freq = 2. * np.pi * self.signal_freq
        self.high_freq = self.mod_index * self.low_freq

        # Параметры большого сигнала
        self.rsch_signal_freq = self.signal_freq
        self.rsch_bits_count = int(self.bits_count * 3)

    @staticmethod
    def _generate_bits(bits_count):
        """
        Формирование случайной битовой информационной последовательности.
        """
        bits = []
        for i in range(int(bits_count)):
            x = random.randint(0, 1)
            bits.append(x)

        return bits

    def recalc_parameters(self):
        """
        Пересчет параметров, задаваемых с окна.
        """
        # Минимальная и максимальная частота,Гц
        self.low_freq = 2. * np.pi * self.signal_freq
        self.high_freq = self.mod_index * self.low_freq

        # Параметры большого сигнала
        self.rsch_signal_freq = self.signal_freq
        self.rsch_bits_count = int(self.bits_count * 3)

    def _get_signal_parameters(self, sf: float, bits_count: int):
        """
        Рассчитать параметры сигналов.
        """
        # Длительность одного бита
        bit_time = 1. / self.bits_per_second
        # Длительность сигнала
        signal_duration = bit_time * bits_count
        # Частота опорного сигнала
        w = 2. * np.pi * sf
        # Количество отсчётов сигнала
        n = self.sampling_rate * signal_duration
        # Шаг времени
        timestep = signal_duration / n
        return signal_duration, timestep, bit_time, w

    def calc_modulated_signal(self, signal_type: SignalType, modulation_type: ModulationType):
        """
        Построить манипулированный сигнал.
        """
        self.signal_phase = 0
        # Характеристики сигнала в зависимости от его типа
        bits_count = self.bits_count
        signal_freq = self.signal_freq
        if signal_type == SignalType.RESEARCH:
            bits_count = self.rsch_bits_count
            signal_freq = self.rsch_signal_freq

        # Перегенерация случайных бит
        bits = self._generate_bits(bits_count)

        # Перезапись случайных бит
        if signal_type == SignalType.GENERAL:
            self.bits = bits

        # Получение параметров сигнала
        x, y = [], []
        signal_duration, timestep, bit_time, w = self._get_signal_parameters(signal_freq, bits_count)
        for t in np.arange(0, signal_duration, timestep):
            # Получение текущего бита
            bit_index = int(t / bit_time)
            # Модуляция
            if modulation_type == ModulationType.AM:
                ampl_value = self.low_ampl if bits[bit_index] == 0 else self.high_ampl
                value = ampl_value * np.cos(w * t)
            elif modulation_type == ModulationType.FM:
                bit_value = -1 if bits[bit_index] == 0 else 1
                freq = self.low_freq if bit_value == -1 else self.high_freq
                value = np.cos(freq * t + self.signal_phase)
                self.signal_phase = freq * t
            elif modulation_type == ModulationType.PM:
                phase = 0 if bits[bit_index] == 0 else 180
                value = np.cos(w * t + phase)
            else:
                return None, None

            # Заполнение списка отсчетов\значений
            x.append(t)
            y.append(value)

        return x, y

    def calc_research_signal(self, modulated: list, researched: list):
        """
        Получить исследуемый сигнал, в котором присутствует сдвинутая копия опорного сигнала.
        """
        if not modulated or not researched:
            return

        researched = list(researched)

        # Полученые временной задержки
        time_delay = self.time_delay / 1000
        if time_delay > researched[0][-1] - modulated[0][-1]:
            return

        # Замена участка исследуемого сигнала на манипулированный сигнал
        idx = 0
        for i in range(len(researched[0])):
            if researched[0][i] >= time_delay:
                idx = i
                break

        signal_len = len(modulated[0])
        new_signal = researched[1][:idx] + modulated[1] + researched[1][idx+signal_len:]
        researched[1] = new_signal
        return researched

    @staticmethod
    def _calc_signal_energy(signal: list):
        """
        Расчет энергии сигнала
        """
        energy = 0.
        for i in range(len(signal[1])):
            energy += signal[1][i] ** 2
        return energy

    @staticmethod
    def _get_random_value():
        """
        Рандомизация чисел для шума
        """
        av = 20
        value = 0.
        for i in range(av):
            value += random.uniform(-1, 1)
        return value / av

    def generate_noise(self, signal_type: SignalType, signal: list):
        """
        Генерация шума для сигнала
        """
        snr = None
        if signal_type == SignalType.GENERAL:
            snr = 10
        elif signal_type == SignalType.RESEARCH:
            snr = self.snr

        if not signal:
            return

        # Расчет энергии шума
        signal_energy = self._calc_signal_energy(signal)
        noise_energy = signal_energy / (10 ** (snr / 10))

        # Случайная шумовая добавка к каждому отсчету
        noise = []
        random_energy = 0.
        for i in range(len(signal[1])):
            random_value = self._get_random_value()
            noise.append(random_value)
            random_energy += random_value ** 2

        # Зашумленный сигнал
        alpha = np.sqrt(noise_energy / random_energy)
        noise_signal = []
        noise_signal_energy = 0.
        for i in range(len(signal[1])):
            noise_signal.append(signal[1][i] + alpha * noise[i])
            noise_signal_energy += (signal[1][i] + alpha * noise[i]) ** 2

        # if signal_type == SignalType.RESEARCH:
        #     print(signal_energy, noise_energy, noise_signal_energy)
        return signal[0], noise_signal

    def get_bits_to_plot(self):
        """
        Получение информационных бит для отображения.
        """
        if not self.bits:
            return

        x = []
        y = []
        for i in range(self.bits_count):
            x.append(i)
            y.append(self.bits[i])
            if i < self.bits_count - 1:
                if self.bits[i] != self.bits[i + 1]:
                    x.append(i + 1)
                    y.append(self.bits[i])
            else:
                x.append(i + 1)
                y.append(self.bits[i])

        return x, y

    @staticmethod
    def get_correlation(modulated: list, researched: list):
        """
        Расчет взаимной корреляционной функции опорного и исследуемого сигналов.
        """
        if not modulated or not researched:
            return

        x, y = [], []
        small_signal_length = len(modulated[0])
        big_signal_length = len(researched[0])
        modulate = np.array(modulated[1])
        research = np.array(researched[1])
        for i in np.arange(0, big_signal_length - small_signal_length - 1):
            summary = np.sum(np.multiply(modulate, research[i:small_signal_length+i])) / small_signal_length

            x.append(researched[0][i])
            y.append(summary)

        return x, y

    @staticmethod
    def find_correlation_max(correlation: list):
        """
        Нахождение максимума корреляционной функции
        """
        if not correlation:
            return

        max_element_idx = correlation[1].index(max(correlation[1]))
        return correlation[0][max_element_idx] * 1000
