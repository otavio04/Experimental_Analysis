// Definição do pino do potenciômetro
const int potPin = A0;
const int acompanhamento = 13;

void setup() {
    Serial.begin(9600); // Inicializa a comunicação serial
    pinMode(acompanhamento, OUTPUT);
    digitalWrite(acompanhamento, LOW);
}

void loop() {
    int valor = analogRead(potPin); // Lê o valor do potenciômetro (0-1023)
    Serial.println(valor); // Envia o valor para o PC via Serial
    digitalWrite(acompanhamento, !digitalRead(acompanhamento));
    delay(100); // Aguarda 100ms antes de enviar o próximo valor
}
