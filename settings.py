
class Settings:
	"""Klasa przeznaczona do przechowywania wszystkich ustawień gry. """

	def __init__(self):
		"""Inicjalizacja ustawień gry."""
		#ustawienia ekranu
		self.screen_width = 1300
		self.screen_height = 900
		self.bg_color = (255, 255, 255)

		self.ship_limit = 3

		#ustawienia dotyczące pocisku
		self.bullet_width = 5
		self.bullet_height = 15
		self.bullet_color = (0, 0, 0)
		self.bullets_allowed = 7

		#ustawienia dotyczące obcego
		# z jaką prędkoscią alieny będą spadac
		self.fleet_drop_speed = 10

		#Zmiana szybkosci gry
		self.speedup_scale = 1.1
		#Zwiększenie punktów za zestrzelenie obcego
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Inicjalizacja ustawień, które ulegają zmianie w trakcie gry"""
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0

		#wartośc fleet_direction wynoszaca 1 to prawo a -1 to lewo
		self.fleet_direction = 1

		#Punktacja
		self.alien_points = 50

	def increase_speed(self):
		"""Zmiana ustawień dotyczących szybkości gry i punktów"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)