import sys
import serial
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

class GraphApp(QtWidgets.QMainWindow):
    """Interface gráfica para exibir os dados do Arduino"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gráfico em Tempo Real - PyQt5 + PyQtGraph")
        self.setGeometry(100, 100, 800, 500)

        # Criar widget principal
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Criar layout vertical
        self.layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Criar botão para iniciar a leitura do Arduino
        self.btn_test = QtWidgets.QPushButton("Iniciar Leitura do Arduino")
        self.btn_test.clicked.connect(self.start_reading)
        self.layout.addWidget(self.btn_test)

        # Criar widget do gráfico
        self.graph_widget = pg.GraphicsLayoutWidget()
        self.graph_canvas = self.graph_widget.addPlot(title="Leituras do Sensor (Arduino)")
        self.graph_canvas.setLabel("left", "Valor do Sensor")
        self.graph_canvas.setLabel("bottom", "Tempo")
        self.graph_canvas.showGrid(x=True, y=True)
        self.curve = self.graph_canvas.plot(pen="y")

        # Adicionar o gráfico ao layout
        self.layout.addWidget(self.graph_widget)

        # Lista de dados recebidos do Arduino
        self.data = []

        # Criar timer para atualizar o gráfico
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)

        # Configurar conexão com o Arduino (Ajuste a porta correta!)
        try:
            self.arduino = serial.Serial("COM5", 9600, timeout=1)  # ⬅️ Troque "COM3" pela sua porta!
        except serial.SerialException:
            print("⚠️ ERRO: Não foi possível conectar ao Arduino!")
            self.arduino = None

    def start_reading(self):
        """Inicia a leitura do Arduino"""
        if self.arduino:
            self.timer.start(100)  # Atualiza o gráfico a cada 100ms

    def update_plot(self):
        """Lê o valor do Arduino e atualiza o gráfico"""
        if self.arduino:
            try:
                line = self.arduino.readline().decode().strip()  # Lê e decodifica a linha
                if line.isdigit():  # Verifica se é um número
                    value = int(line)
                    if len(self.data) > 100:
                        self.data.pop(0)  # Mantém apenas os últimos 100 pontos
                    self.data.append(value)
                    self.curve.setData(self.data)
            except:
                pass  # Ignora erros de leitura

# Executando a aplicação
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GraphApp()
    window.show()
    sys.exit(app.exec_())
