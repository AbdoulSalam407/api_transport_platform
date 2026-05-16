import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReservationService } from '../../../core/services/reservation.service';
import { AuthService } from '../../../core/services/auth.service';
import { Trajet } from '../../../core/models/trajet.model';

@Component({
  selector: 'app-reservation',
  standalone: true,
  imports: [RouterLink, CommonModule, FormsModule],
  templateUrl: './reservation.component.html',
})
export class ReservationComponent implements OnInit {
  trajet: Trajet | null = null;
  nombrePlaces = 1;
  numeroSiege = '';
  loading = false;
  error = '';
  success = '';

  constructor(
    private router: Router,
    private reservationService: ReservationService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']);
      return;
    }
    const nav = this.router.getCurrentNavigation();
    this.trajet = nav?.extras?.state?.['trajet'] ?? null;
    if (!this.trajet) this.router.navigate(['/recherche']);
  }

  get prixTotal(): number {
    return this.trajet ? parseFloat(this.trajet.prix_base) * this.nombrePlaces : 0;
  }

  decrementer(): void {
    if (this.nombrePlaces > 1) this.nombrePlaces--;
  }

  incrementer(): void {
    if (this.trajet && this.nombrePlaces < this.trajet.places_disponibles) this.nombrePlaces++;
  }

  reserver(): void {
    if (!this.trajet) return;
    this.loading = true;
    this.error = '';

    this.reservationService.creer({
      trajet: this.trajet.id,
      nombre_places: this.nombrePlaces,
      numero_siege: this.numeroSiege
    }).subscribe({
      next: () => {
        this.loading = false;
        this.success = 'Réservation effectuée avec succès !';
        setTimeout(() => this.router.navigate(['/dashboard-passager']), 2000);
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.non_field_errors?.[0] ?? 'Erreur lors de la réservation.';
      }
    });
  }
}
