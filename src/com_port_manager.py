import serial
import serial.tools.list_ports
from typing import List, Optional
import time


class COMPortManager:
    """Управляет подключением к Arduino через COM-порт"""
    
    def __init__(self, baudrate: int = 9600, timeout: float = 1.0):
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_port: Optional[serial.Serial] = None
        self.connected = False
    
    def get_available_ports(self) -> List[str]:
        """Получить список доступных COM-портов"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports
    
    def get_port_info(self, port: str) -> Optional[str]:
        """Получить информацию о COM-порте"""
        for p in serial.tools.list_ports.comports():
            if p.device == port:
                return f"{p.device} - {p.description}"
        return None
    
    def connect(self, port: str) -> bool:
        """Подключиться к COM-порту"""
        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)  # Подождать инициализации Arduino
            self.connected = True
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> bool:
        """Отключиться от COM-порта"""
        try:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
                self.connected = False
                return True
        except Exception as e:
            print(f"Ошибка отключения: {e}")
        return False
    
    def send_command(self, command: str) -> bool:
        """Отправить команду на Arduino"""
        if not self.connected or not self.serial_port:
            return False
        
        try:
            self.serial_port.write((command + '\n').encode())
            return True
        except Exception as e:
            print(f"Ошибка отправки команды: {e}")
            return False
    
    def read_response(self) -> Optional[str]:
        """Получить ответ от Arduino"""
        if not self.connected or not self.serial_port:
            return None
        
        try:
            if self.serial_port.in_waiting:
                response = self.serial_port.readline().decode().strip()
                return response
        except Exception as e:
            print(f"Ошибка чтения: {e}")
        
        return None
    
    def test_connection(self) -> bool:
        """Тестировать соединение отправкой STATUS"""
        if not self.connected:
            return False
        
        self.send_command("STATUS")
        time.sleep(0.5)
        response = self.read_response()
        
        return response is not None and "OK" in response