import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry. """

	def __init__(self):
		"""Inicjalizacja gry i utworzenie jej zasobów. """
		pygame.init() #inicjalizacja ustawienia tła
		
		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
		pygame.display.set_caption("SHOOT 'EM")

		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		#utworzenie przycisku Gra
		self.play_button = Button(self,self.screen ,"Play / Press D")



	def run_game(self):
		"""Rozpoczęcie pętli głównej gry """
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()

			
	def _check_keydown_events(self, event):
			if event.key == pygame.K_RIGHT:
				self.ship.moving_right = True
			elif event.key == pygame.K_LEFT:
				self.ship.moving_left = True
			elif event.key == pygame.K_q:
				sys.exit()
			elif event.key == pygame.K_SPACE:
				self._fire_bullet()


	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
		elif event.key == pygame.K_d:
			self.settings.initialize_dynamic_settings()
			self._start_game_again()			

	def _check_events(self):
		#Oczekiwanie na naciśnięcie klawisza lub przycisku myszy
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)


	def _check_play_button(self, mouse_pos):
		"""Rozpoczęcie nowej gry po kliknięciu przycisku Gra"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self.settings.initialize_dynamic_settings()
			self._start_game_again()

	def _start_game_again(self):
		self.stats.reset_stats()
		self.stats.game_active = True
		self.sb.prep_score()
		self.sb.prep_level()
		self.sb.prep_ships()

		#usunięcie zawartości list aliens i bullets
		self.aliens.empty()
		self.bullets.empty()

		#utworzenie nowej floty i wyśrodkowanie statku
		self._create_fleet()
		self.ship.center_ship()

		#ukrycie kursora myszy
		pygame.mouse.set_visible(False)

	def _fire_bullet(self):
		"""Utworzenie nowego pocisku i dodanie go do grupy pocisków"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)	
	
	def _update_bullets(self):
		#Uaktualnienie położenia pocisków
		self.bullets.update()
		#usunięcie pocisków, które są poza ekranem
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collision()

	def _check_bullet_alien_collision(self):
		"""Reakcja na kolizje między pociskiem i obcym"""
		#usunięcie wszystkich pocisków i obcych, między którymi doszło do kolizji
		collision = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

		if collision:
			for aliens in collision.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			#pozbycie się istniejących pocisków i utworzenie nowej floty
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#inkrementacja poziomu
			self.stats.level += 1
			self.sb.prep_level()

	def _create_fleet(self):
		""" Utworzenie pełnej floty obcych"""
		#Utworzenie obcego i ustalenie liczby obcych, którzy zmieszczą się w rzędzie 
		#Odległosc między poszczególnymi obcymi jest równa szerokości obcego
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		#ustalenie ile rzędów sie zmiesci na ekranie
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3* alien_height) - ship_height)
		number_rows = available_space_y // (2*alien_height)

		#utworzenie pełnej floty obcych
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)
			
			
	def _create_alien(self, alien_number, row_number):
		#Utworzenie obcego i umieszczenie go w rzędzie
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _change_fleet_direction(self):
		"""Przesunięcie całej floty w dół i zmiana kierunku, w którym się ona porusza"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _check_fleet_edges(self):
		"""Odpowiednia reakcja, gdy obcy dotrze do krawędzi ekranu"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _update_aliens(self):
		"""Sprawdzenie, czy flota obcych znajduje się przy krawędzi,
		a następnie uaktualnienie położenia wszystkich wszystkichobcych we flocie"""
		self._check_fleet_edges()
		self.aliens.update()

		#wykrywanie kolizji między obcym i statkiem
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		#wyszukiwanie obcych docierajacyh do dolnej krawędzi ekranu
		self._check_aliens_bottom()

	def _check_aliens_bottom(self):
		"""Sprawdzenie, czy którykolwiek obcy dotarł do dolnej krawędzi ekranu"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#tak samo jak w przypadku zderzenia statku z obcym
				self._ship_hit()
				break

	def _ship_hit(self):
		"""Reakcja na uderzenie obcego w statek"""
		if self.stats.ships_left > 0:
			#zmniejszenie wartosci przechowywanej w ships_left
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			#usunięcie zawartosci list aliens i bullets
			self.aliens.empty()
			self.bullets.empty()

			#utworzenie nowej floty i wyśrodkowanie statku
			self._create_fleet()
			self.ship.center_ship()

			#pauza
			sleep(1)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _update_screen(self):
		#Odświeżanie ekranu w trakcie każdej iteracji pętli
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme() #wyświetlenie statku

		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		self.aliens.draw(self.screen)

		#Wyświetlenie info o punktacji
		self.sb.show_score()

		#Wyświetlenie przycisku tylko wtedy, gdy gra jest nieaktywna
		if not self.stats.game_active:
			self.play_button.draw_button()		

		#wyświetlenie ostatnio zmodyfikowanego/odświeżonego ekranu
		pygame.display.flip()

if __name__ == '__main__':
	#Utworzenie egzemplarza gry i jej uruchomienie
	ai = AlienInvasion()
	ai.run_game()