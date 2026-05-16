import { Component, OnInit } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';
import { ReservationService } from '../../../core/services/reservation.service';
import { Reservation } from '../../../core/models/reservation.model';

@Component({
  selector: 'app-dashboard-passager',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard-passager.component.html',
})
export class DashboardPassagerComponent implements OnInit {
  userName = '';
  reservations: Reservation[] = [];
  loading = true;
  error = '';

  constructor(
    private router: Router,
    private authService: AuthService,
    private reservationService: ReservationService
  ) {}

  ngOnInit(): void {
    if (!this.authService.isLoggedIn() || this.authService.getRole() !== 'passager') {
      this.router.navigate(['/login']);
      return;
    }

    const user = this.authService.getUser();
    this.userName = user ? `${user.prenom} ${user.nom}` : '';

    this.reservationService.getMesReservations().subscribe({
      next: (res) => {
        this.reservations = Array.isArray(res) ? res : (res.results ?? []);
        this.loading = false;
      },
      error: () => {
        this.error = 'Impossible de charger les réservations.';
        this.loading = false;
      }
    });
  }

  get totalReservations(): number {
    return this.reservations.length;
  }

  get trajetsAVenir(): number {
    return this.reservations.filter(r => r.statut === 'confirmee').length;
  }

  get reservationsEnAttente(): number {
    return this.reservations.filter(r => r.statut === 'en_attente').length;
  }

  get prochainsTrajetsList(): Reservation[] {
    return this.reservations
      .filter(r => r.statut === 'confirmee' || r.statut === 'en_attente')
      .slice(0, 5);
  }

  annuler(id: number): void {
    this.reservationService.annuler(id).subscribe({
      next: () => {
        const r = this.reservations.find(r => r.id === id);
        if (r) r.statut = 'annulee';
      },
      error: () => alert('Impossible d\'annuler cette réservation.')
    });
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: () => this.router.navigate(['/login']),
      error: () => {
        this.authService.clearSession();
        this.router.navigate(['/login']);
      }
    });
  }

  getStatutClass(statut: string): string {
    const classes: Record<string, string> = {
      confirmee: 'bg-green-100 text-green-800',
      en_attente: 'bg-yellow-100 text-yellow-800',
      annulee: 'bg-red-100 text-red-800',
      terminee: 'bg-slate-100 text-slate-600',
    };
    return classes[statut] ?? 'bg-slate-100 text-slate-600';
  }

  getBorderClass(statut: string): string {
    const classes: Record<string, string> = {
      confirmee: 'border-green-500',
      en_attente: 'border-yellow-500',
      annulee: 'border-red-400',
      terminee: 'border-slate-400',
    };
    return classes[statut] ?? 'border-slate-400';
  }
}
