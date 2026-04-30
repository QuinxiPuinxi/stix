from typing import Dict

class ServoController:
    """Управление сервоприводами для управления полётом"""
    
    def __init__(self, com_manager):
        self.com_manager = com_manager
        self.servo_positions = {
            "ailerons": 90,
            "elevator": 90,
            "rudder": 90,
            "flaps": 90
        }
        self.maneuvers = self._init_maneuvers()
    
    def _init_maneuvers(self) -> Dict:
        """Инициализация предопределённых манёвров"""
        return {
            "level_flight": {
                "ailerons": 90,
                "elevator": 90,
                "rudder": 90,
                "flaps": 90
            },
            "left_turn": {
                "ailerons": 70,
                "elevator": 85,
                "rudder": 70,
                "flaps": 90
            },
            "right_turn": {
                "ailerons": 110,
                "elevator": 85,
                "rudder": 110,
                "flaps": 90
            },
            "climb": {
                "ailerons": 90,
                "elevator": 60,
                "rudder": 90,
                "flaps": 70
            },
            "descent": {
                "ailerons": 90,
                "elevator": 110,
                "rudder": 90,
                "flaps": 120
            },
            "takeoff": {
                "ailerons": 90,
                "elevator": 75,
                "rudder": 90,
                "flaps": 60
            },
            "landing": {
                "ailerons": 90,
                "elevator": 100,
                "rudder": 90,
                "flaps": 130
            }
        }
    
    def set_servo_angle(self, servo_name: str, angle: float) -> bool:
        """Установить угол для сервопривода"""
        if servo_name not in self.servo_positions:
            return False
        
        angle = max(0, min(180, angle))
        self.servo_positions[servo_name] = angle
        
        command = f"{servo_name.upper()}:{int(angle)}"
        return self.com_manager.send_command(command)
    
    def set_all_servos(self, positions: Dict[str, float]) -> bool:
        """Установить углы для всех сервоприводов"""
        for servo_name, angle in positions.items():
            if not self.set_servo_angle(servo_name, angle):
                return False
        return True
    
    def get_servo_position(self, servo_name: str) -> float:
        """Получить текущий угол сервопривода"""
        return self.servo_positions.get(servo_name, 90)
    
    def get_all_positions(self) -> Dict[str, float]:
        """Получить позиции всех сервоприводов"""
        return self.servo_positions.copy()
    
    def reset_all(self) -> bool:
        """Вернуть все сервоприводы в нейтральное положение"""
        return self.com_manager.send_command("RESET")
    
    def execute_maneuver(self, maneuver_name: str, smooth: bool = True) -> bool:
        """Выполн��ть предопределённый манёвр"""
        if maneuver_name not in self.maneuvers:
            return False
        
        maneuver = self.maneuvers[maneuver_name]
        
        if smooth:
            return self._smooth_transition(maneuver)
        else:
            return self.set_all_servos(maneuver)
    
    def _smooth_transition(self, target_positions: Dict[str, float], 
                          steps: int = 10, delay_ms: int = 50) -> bool:
        """Плавный переход к целевым позициям"""
        for step in range(steps):
            current = self.get_all_positions()
            next_pos = {}
            
            for servo_name, target_angle in target_positions.items():
                current_angle = current[servo_name]
                progress = (step + 1) / steps
                next_angle = current_angle + (target_angle - current_angle) * progress
                next_pos[servo_name] = next_angle
            
            if not self.set_all_servos(next_pos):
                return False
        
        return True
    
    def create_custom_maneuver(self, name: str, positions: Dict[str, float]) -> None:
        """Создать пользовательский манёвр"""
        self.maneuvers[name] = positions
    
    def get_available_maneuvers(self) -> list:
        """Получить список доступных манёвров"""
        return list(self.maneuvers.keys())
