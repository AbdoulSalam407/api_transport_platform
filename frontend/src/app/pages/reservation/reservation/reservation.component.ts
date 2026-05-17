import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReservationService } from '../../../core/services/reservation.service';
import { AuthService } from '../../../core/services/auth.service';
import { Trajet } from '../../../core/models/trajet.model';
import { Reservation } from '../../../core/models/reservation.model';
import { formatHttpErrorMessage } from '../../../core/utils/format-http-error';

@Component({
  selector: 'app-reservation',
  standalone: true,
  imports: [RouterLink, CommonModule, FormsModule],
  templateUrl: './reservation.component.html',
})
export class ReservationComponent implements OnInit {
  trajet: Trajet | null = null;
  nombrePlaces = 1;
  loading = false;
  error = '';
  success = '';
  derniereReservation: Reservation | null = null;
  roleNonPassager = false;

  constructor(
    private router: Router,
    private reservationService: ReservationService,
    private authService: AuthService,
  ) {}

  ngOnInit(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login']);
      return;
    }
    if (this.authService.getRole() !== 'passager') {
      this.roleNonPassager = true;
      return;
    }
    const nav = this.router.getCurrentNavigation();
    this.trajet = nav?.extras?.state?.['trajet'] ?? history.state?.['trajet'] ?? null;
    if (!this.trajet) {
      this.router.navigate(['/recherche']);
    }
  }

  get prixTotal(): number {
    return this.trajet ? parseFloat(String(this.trajet.prix_base)) * this.nombrePlaces : 0;
  }

  decrementer(): void {
    if (this.nombrePlaces > 1) this.nombrePlaces--;
  }

  incrementer(): void {
    if (this.trajet && this.nombrePlaces < this.trajet.places_disponibles) this.nombrePlaces++;
  }

  dashboardRoute(): string {
    const role = this.authService.getRole();
    if (role === 'transporteur') return '/dashboard-transporteur';
    if (role === 'admin') return '/dashboard-admin';
    return '/';
  }

  allerMesReservations(): void {
    this.router.navigate(['/dashboard-passager']);
  }

  reserver(): void {
    if (!this.trajet) return;
    this.loading = true;
    this.error = '';
    this.success = '';
    this.derniereReservation = null;

    this.reservationService
      .creer({
        trajet: this.trajet.id,
        nombre_places: this.nombrePlaces,
      })
      .subscribe({
        next: (res) => {
          this.loading = false;
          this.derniereReservation = res.reservation;
          this.success =
            res.message ||
            'Demande enregistrée. Un administrateur doit confirmer votre réservation.';
        },
        error: (err) => {
          this.loading = false;
          this.error = formatHttpErrorMessage(err) || 'Erreur lors de la réservation.';
        },
      });
  }
}
