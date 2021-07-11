class GameStats:
	"""Monitorowanie danych statycznych w grze"""

	def __init__(self, ai_game):
		""" Inicjalizacja danych statystycznych"""
		self.settings = ai_game.settings
		self.reset_stats()

		#Najlepszy wynik nie powinien zostac wyzerowany
		self.high_score = 0

		#Uruchomienie gry w stanie niekatywnym
		self.game_active = False

	def reset_stats(self):
		"""Inicjalizacja danych, które mogą zmienia się w trakcie gry """
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1