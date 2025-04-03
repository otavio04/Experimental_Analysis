import sys
import random
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore

class GraphApp(QtWidgets.QMainWindow):
    """Interface gráfica para exibir os dados"""
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

        # Criar botão para iniciar o teste
        self.btn_test = QtWidgets.QPushButton("Iniciar Teste")
        self.btn_test.clicked.connect(self.start_test)
        self.layout.addWidget(self.btn_test)

        # Criar widget do gráfico
        self.graph_widget = pg.GraphicsLayoutWidget()
        self.graph_canvas = self.graph_widget.addPlot(title="Leituras do Sensor")
        self.graph_canvas.setLabel("left", "Valor do Sensor")
        self.graph_canvas.setLabel("bottom", "Tempo")
        self.graph_canvas.showGrid(x=True, y=True)
        self.curve = self.graph_canvas.plot(pen="y")

        # Adicionar o gráfico ao layout
        self.layout.addWidget(self.graph_widget)

        # Lista de dados simulados
        self.data = []

        # Criar timer para atualizar o gráfico
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)

    def start_test(self):
        """Inicia a geração de dados fictícios"""
        self.timer.start(100)  # Atualiza o gráfico a cada 100ms

    def update_plot(self):
        """Gera dados fictícios e atualiza o gráfico"""
        if len(self.data) > 100:
            self.data.pop(0)  # Mantém apenas os últimos 100 pontos

        self.data.append(random.randint(0, 100))  # Gera um valor aleatório
        self.curve.setData(self.data)

# Executando a aplicação
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GraphApp()
    window.show()
    sys.exit(app.exec_())
