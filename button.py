import pygame.font

class Button():

	def __init__(self, ai_game, screen, msg):
		"""Inicjalizacja atrybutów przycisku"""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		#zdefiniowanie wymiarów i właściwosci przycisku
		self.width, self.height = 230,50
		self.button_color = (0, 255 ,255)
		self.text_color = (0, 0, 0)
		# pierwszy argument to styl czcionki a drugi to wielkośc
		self.font = pygame.font.SysFont(None, 48) 

		#Utworzenie prostokąta przycisku i wyśrodkowanie go
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		#Komunikat wyświetlony przez przycisk trzeba przygotowa tylko jednokrotnie
		self._prep_msg(msg)

	def draw_button(self):
		#Wyświetlenie pustego przycisku a następnie komunikatu na nim
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect )

	def _prep_msg(self, msg):
		"""Umieszczenie komunikatu w wygenerowanym obrazie i wyśrodkowanie tekstu na przycisku """
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center