import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { finalize } from 'rxjs/operators';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TrajetService } from '../../../core/services/trajet.service';
import { AuthService } from '../../../core/services/auth.service';
import { Trajet } from '../../../core/models/trajet.model';

@Component({
  selector: 'app-recherche',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './recherche.component.html',
})
export class RechercheComponent implements OnInit {
  userName = '';
  userRole = '';
  peutReserver = false;
  estTransporteur = false;

  depart = '';
  destination = '';
  date = '';
  uniquementAvecPlaces = false;

  trajets: Trajet[] = [];
  loading = false;
  error = '';
  listeChargee = false;

  constructor(
    private router: Router,
    private trajetService: TrajetService,
    private authService: AuthService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']);
      return;
    }
    const user = this.authService.getUser();
    this.userName = user ? `${user.prenom} ${user.nom}` : '';
    this.userRole = this.authService.getRole() ?? '';
    this.peutReserver = this.userRole === 'passager';
    this.estTransporteur = this.userRole === 'transporteur';
    this.chargerTrajets();
  }

  chargerTrajets(): void {
    this.loading = true;
    this.error = '';

    this.trajetService
      .listerTrajetsDisponibles(
        {
          depart: this.depart.trim() || undefined,
          destination: this.destination.trim() || undefined,
          date: this.date || undefined,
        },
        1,
        100,
        this.uniquementAvecPlaces,
      )
      .pipe(
        finalize(() => {
          this.loading = false;
          this.listeChargee = true;
          this.cdr.markForCheck();
        }),
      )
      .subscribe({
        next: (res) => {
          this.trajets = Array.isArray(res) ? res : (res.results ?? []);
        },
        error: () => {
          this.error = 'Impossible de charger les trajets disponibles.';
        },
      });
  }

  filtrer(): void {
    this.chargerTrajets();
  }

  reinitialiserFiltres(): void {
    this.depart = '';
    this.destination = '';
    this.date = '';
    this.uniquementAvecPlaces = false;
    this.chargerTrajets();
  }

  reserver(trajet: Trajet): void {
    if (!this.peutReserver) {
      return;
    }
    this.router.navigate(['/reservation'], { state: { trajet } });
  }
}
