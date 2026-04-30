import math
import json
from typing import Dict, Tuple

class AircraftCalculatorExtended:
    """Расширенный калькулятор для расчета характеристик самолета Як-130"""
    
    def __init__(self, config_path: str = 'config/aircraft_params.json'):
        """Инициализация с параметрами самолета"""
        self.config = self._load_config(config_path)
        self.yak130_params = {
            'weight': 3200,
            'max_weight': 6500,
            'wing_area': 34.5,
            'wing_span': 12.3,
            'fuselage_length': 14.7,
            'fuselage_diameter': 1.0,
            'drag_coefficient_base': 0.025,
            'oswald_efficiency': 0.85,
            'wing_aspect_ratio': 4.4,
            'max_speed': 308,
            'cruise_speed': 222,
            'stall_speed': 50,
            'service_ceiling': 12000,
            'max_climb_rate': 2500,
        }
        self.atmospheric_params = {
            'sea_level_density': 1.225,
            'sea_level_pressure': 101325,
            'sea_level_temperature': 288.15,
            'temperature_lapse': 0.0065,
            'gravity': 9.81,
        }
        self.current_flight_state = self._init_flight_state()
    
    def _load_config(self, path: str) -> Dict:
        """Загрузить конфигурацию самолета"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def _init_flight_state(self) -> Dict:
        """Инициализировать состояние полета"""
        return {
            'altitude': 0,
            'velocity': 0,
            'angle_of_attack': 0,
            'pitch': 0,
            'roll': 0,
            'yaw': 0,
            'fuel_weight': 1500,
            'air_density': 1.225,
        }
    
    def calculate_air_density(self, altitude: float) -> float:
        """Расчет плотности воздуха на высоте (м)"""
        T0 = self.atmospheric_params['sea_level_temperature']
        P0 = self.atmospheric_params['sea_level_pressure']
        L = self.atmospheric_params['temperature_lapse']
        g = self.atmospheric_params['gravity']
        R = 287
        
        T = T0 - L * altitude
        P = P0 * (T / T0) ** (-g / (L * R))
        rho = P / (R * T)
        
        return max(0, rho)
    
    def calculate_temperature(self, altitude: float) -> float:
        """Расчет температуры на высоте (K)"""
        T0 = self.atmospheric_params['sea_level_temperature']
        L = self.atmospheric_params['temperature_lapse']
        return max(0, T0 - L * altitude)
    
    def calculate_pressure(self, altitude: float) -> float:
        """Расчет давления на высоте (Pa)"""
        T0 = self.atmospheric_params['sea_level_temperature']
        P0 = self.atmospheric_params['sea_level_pressure']
        L = self.atmospheric_params['temperature_lapse']
        g = self.atmospheric_params['gravity']
        R = 287
        
        T = T0 - L * altitude
        return P0 * (T / T0) ** (-g / (L * R))
    
    def calculate_lift(self, velocity: float, altitude: float, aoa: float) -> float:
        """Расчет подъемной силы (N)"""
        rho = self.calculate_air_density(altitude)
        
        Cl = 0.2 + 0.1 * math.sin(math.radians(aoa))
        
        S = self.yak130_params['wing_area']
        L = 0.5 * rho * velocity ** 2 * S * Cl
        
        return max(0, L)
    
    def calculate_drag(self, velocity: float, altitude: float, aoa: float) -> float:
        """Расчет силы сопротивления (N)"""
        rho = self.calculate_air_density(altitude)
        
        Cl = 0.2 + 0.1 * math.sin(math.radians(aoa))
        AR = self.yak130_params['wing_aspect_ratio']
        e = self.yak130_params['oswald_efficiency']
        
        Cd_induced = (Cl ** 2) / (math.pi * AR * e)
        Cd = self.yak130_params['drag_coefficient_base'] + Cd_induced
        
        S = self.yak130_params['wing_area']
        D = 0.5 * rho * velocity ** 2 * S * Cd
        
        return max(0, D)
    
    def calculate_thrust_required(self, velocity: float, altitude: float, aoa: float) -> float:
        """Расчет требуемой тяги (N)"""
        drag = self.calculate_drag(velocity, altitude, aoa)
        return drag
    
    def calculate_engine_thrust(self, throttle_percent: float, altitude: float) -> float:
        """Расчет тяги двигателя (N)"""
        max_thrust_one = 19600
        max_thrust_total = max_thrust_one * 2
        
        rho = self.calculate_air_density(altitude)
        rho_ratio = rho / self.atmospheric_params['sea_level_density']
        
        thrust = max_thrust_total * (throttle_percent / 100) * rho_ratio
        return max(0, thrust)
    
    def calculate_excess_power(self, velocity: float, altitude: float, 
                              aoa: float, throttle_percent: float) -> float:
        """Расчет избыточной мощности (W)"""
        thrust = self.calculate_engine_thrust(throttle_percent, altitude)
        drag = self.calculate_drag(velocity, altitude, aoa)
        
        excess_power = (thrust - drag) * velocity
        return excess_power
    
    def calculate_excess_thrust(self, velocity: float, altitude: float, 
                               aoa: float, throttle_percent: float) -> float:
        """Расчет избыточной тяги (N)"""
        thrust = self.calculate_engine_thrust(throttle_percent, altitude)
        drag = self.calculate_drag(velocity, altitude, aoa)
        
        return thrust - drag
    
    def calculate_climb_rate(self, velocity: float, altitude: float, 
                            aoa: float, throttle_percent: float) -> float:
        """Расчет вертикальной скорости (м/с)"""
        excess_power = self.calculate_excess_power(velocity, altitude, aoa, throttle_percent)
        total_weight = self.yak130_params['weight'] + self.current_flight_state['fuel_weight']
        weight_force = total_weight * self.atmospheric_params['gravity']
        
        if weight_force > 0:
            climb_rate = excess_power / weight_force
        else:
            climb_rate = 0
        
        return climb_rate
    
    def calculate_max_speed_at_altitude(self, altitude: float, throttle_percent: float = 100) -> float:
        """Расчет максимальной скорости на высоте (м/с)"""
        for v in range(int(self.yak130_params['max_speed']) + 1):
            thrust = self.calculate_engine_thrust(throttle_percent, altitude)
            drag = self.calculate_drag(v, altitude, 0)
            
            if thrust < drag:
                return max(0, v - 1)
        
        return self.yak130_params['max_speed']
    
    def calculate_turn_radius(self, velocity: float, altitude: float, bank_angle: float) -> float:
        """Расчет радиуса разворота (м)"""
        if velocity == 0:
            return 0
        
        g = self.atmospheric_params['gravity']
        bank_rad = math.radians(bank_angle)
        
        radius = (velocity ** 2) / (g * math.tan(bank_rad))
        
        return max(0, radius)
    
    def calculate_turn_rate(self, velocity: float, altitude: float, bank_angle: float) -> float:
        """Расчет угловой скорости разворота (град/сек)"""
        if velocity == 0:
            return 0
        
        g = self.atmospheric_params['gravity']
        bank_rad = math.radians(bank_angle)
        
        turn_rate_rad = (g * math.tan(bank_rad)) / velocity
        turn_rate_deg = math.degrees(turn_rate_rad)
        
        return turn_rate_deg
    
    def calculate_load_factor(self, velocity: float, bank_angle: float) -> float:
        """Расчет коэффициента перегрузки"""
        bank_rad = math.radians(bank_angle)
        load_factor = 1 / math.cos(bank_rad)
        
        return load_factor
    
    def calculate_stall_speed(self, altitude: float, bank_angle: float = 0) -> float:
        """Расчет скорости сваливания (м/с)"""
        rho = self.calculate_air_density(altitude)
        total_weight = self.yak130_params['weight'] + self.current_flight_state['fuel_weight']
        weight_force = total_weight * self.atmospheric_params['gravity']
        
        Cl_max = 1.5
        
        load_factor = self.calculate_load_factor(0, bank_angle)
        
        S = self.yak130_params['wing_area']
        
        if rho > 0:
            Vs = math.sqrt((2 * weight_force * load_factor) / (rho * S * Cl_max))
        else:
            Vs = self.yak130_params['stall_speed']
        
        return Vs
    
    def calculate_range(self, fuel_weight: float, cruise_speed: float, 
                       altitude: float, throttle_percent: float = 75) -> float:
        """Расчет дальности (км)"""
        if cruise_speed == 0:
            return 0
        
        fuel_consumption = 0.0004
        total_consumption = fuel_consumption * 2
        
        rho = self.calculate_air_density(altitude)
        rho_ratio = rho / self.atmospheric_params['sea_level_density']
        consumption_corrected = total_consumption * rho_ratio * (throttle_percent / 100)
        
        flight_time = fuel_weight / consumption_corrected
        distance = cruise_speed * flight_time / 1000
        
        return max(0, distance)
    
    def calculate_endurance(self, fuel_weight: float, altitude: float = 0, 
                           throttle_percent: float = 50) -> float:
        """Расчет продолжительности полета (часы)"""
        fuel_consumption = 0.0004
        total_consumption = fuel_consumption * 2
        
        rho = self.calculate_air_density(altitude)
        rho_ratio = rho / self.atmospheric_params['sea_level_density']
        consumption_corrected = total_consumption * rho_ratio * (throttle_percent / 100)
        
        flight_time = fuel_weight / consumption_corrected
        endurance_hours = flight_time / 3600
        
        return max(0, endurance_hours)
    
    def calculate_power_loading(self) -> float:
        """Расчет удельной мощности (кВт/кг)"""
        total_weight = self.yak130_params['weight'] + self.current_flight_state['fuel_weight']
        max_thrust = 39200
        max_power = max_thrust * self.yak130_params['max_speed']
        
        if total_weight > 0:
            power_loading = max_power / (total_weight * 1000)
        else:
            power_loading = 0
        
        return power_loading
    
    def calculate_wing_loading(self) -> float:
        """Расчет удельной нагрузки на крыло (кг/м²)"""
        total_weight = self.yak130_params['weight'] + self.current_flight_state['fuel_weight']
        wing_area = self.yak130_params['wing_area']
        
        return total_weight / wing_area
    
    def calculate_g_limits(self) -> Tuple[float, float]:
        """Расчет ограничений по перегрузкам"""
        max_positive_g = 6.5
        max_negative_g = -3.0
        
        return (max_negative_g, max_positive_g)
    
    def calculate_stability_margins(self, velocity: float, altitude: float) -> Dict:
        """Расчет запасов по устойчивости"""
        rho = self.calculate_air_density(altitude)
        
        static_margin = 0.05
        damping_coefficient = 0.8
        
        return {
            'static_margin': static_margin,
            'damping_coefficient': damping_coefficient,
            'phugoid_period': 45,
            'short_period': 2,
        }
    
    def update_flight_state(self, altitude: float, velocity: float, aoa: float,
                           pitch: float, roll: float, fuel: float):
        """Обновить текущее состояние полета"""
        self.current_flight_state['altitude'] = altitude
        self.current_flight_state['velocity'] = velocity
        self.current_flight_state['angle_of_attack'] = aoa
        self.current_flight_state['pitch'] = pitch
        self.current_flight_state['roll'] = roll
        self.current_flight_state['fuel_weight'] = fuel
        self.current_flight_state['air_density'] = self.calculate_air_density(altitude)
    
    def get_full_telemetry(self, velocity: float, altitude: float, aoa: float,
                          throttle_percent: float, bank_angle: float) -> Dict:
        """Получить полную телеметрию самолета"""
        self.update_flight_state(altitude, velocity, aoa, 0, bank_angle, 
                                self.current_flight_state['fuel_weight'])
        
        telemetry = {
            'atmospheric': {
                'temperature': round(self.calculate_temperature(altitude), 2),
                'pressure': round(self.calculate_pressure(altitude), 0),
                'air_density': round(self.calculate_air_density(altitude), 4),
            },
            'aerodynamic': {
                'lift': round(self.calculate_lift(velocity, altitude, aoa), 0),
                'drag': round(self.calculate_drag(velocity, altitude, aoa), 0),
                'thrust_required': round(self.calculate_thrust_required(velocity, altitude, aoa), 0),
            },
            'engine': {
                'thrust_available': round(self.calculate_engine_thrust(throttle_percent, altitude), 0),
                'excess_thrust': round(self.calculate_excess_thrust(velocity, altitude, aoa, throttle_percent), 0),
                'excess_power': round(self.calculate_excess_power(velocity, altitude, aoa, throttle_percent), 0),
            },
            'performance': {
                'climb_rate': round(self.calculate_climb_rate(velocity, altitude, aoa, throttle_percent), 2),
                'max_speed': round(self.calculate_max_speed_at_altitude(altitude, throttle_percent), 1),
                'stall_speed': round(self.calculate_stall_speed(altitude, bank_angle), 1),
                'turn_radius': round(self.calculate_turn_radius(velocity, altitude, bank_angle), 1),
                'turn_rate': round(self.calculate_turn_rate(velocity, altitude, bank_angle), 2),
            },
            'loadings': {
                'wing_loading': round(self.calculate_wing_loading(), 2),
                'power_loading': round(self.calculate_power_loading(), 4),
                'load_factor': round(self.calculate_load_factor(velocity, bank_angle), 2),
            },
            'range_endurance': {
                'range': round(self.calculate_range(self.current_flight_state['fuel_weight'], 
                                                   velocity, altitude), 1),
                'endurance': round(self.calculate_endurance(self.current_flight_state['fuel_weight'], 
                                                           altitude), 2),
            },
        }
        
        return telemetry