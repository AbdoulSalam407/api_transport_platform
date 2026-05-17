import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { finalize } from 'rxjs/operators';
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
  /** ID de la réservation dont le panneau détail est ouvert (null = aucun). */
  detailReservationId: number | null = null;
  detailLoading = false;
  detailReservation: Reservation | null = null;

  constructor(
    private router: Router,
    private authService: AuthService,
    private reservationService: ReservationService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    if (!this.authService.isLoggedIn() || this.authService.getRole() !== 'passager') {
      this.router.navigate(['/login']);
      return;
    }

    const user = this.authService.getUser();
    this.userName = user ? `${user.prenom} ${user.nom}` : '';

    this.reservationService
      .getMesReservations()
      .pipe(
        finalize(() => {
          this.loading = false;
          this.cdr.markForCheck();
        }),
      )
      .subscribe({
        next: (res) => {
          this.reservations = Array.isArray(res) ? res : (res.results ?? []);
        },
        error: () => {
          this.error = 'Impossible de charger les réservations.';
        },
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
      .sort((a, b) => {
        const da = a.trajet_detail?.date_depart ?? a.date_reservation ?? '';
        const db = b.trajet_detail?.date_depart ?? b.date_reservation ?? '';
        return new Date(da).getTime() - new Date(db).getTime();
      });
  }

  toggleDetails(reservation: Reservation): void {
    if (this.detailReservationId === reservation.id) {
      this.fermerDetails();
      return;
    }
    this.detailReservationId = reservation.id;
    this.detailReservation = reservation;
    this.detailLoading = true;
    this.reservationService.getReservation(reservation.id).subscribe({
      next: (full) => {
        this.detailReservation = full;
        this.detailLoading = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.detailReservation = reservation;
        this.detailLoading = false;
        this.cdr.markForCheck();
      },
    });
  }

  fermerDetails(): void {
    this.detailReservationId = null;
    this.detailReservation = null;
    this.detailLoading = false;
  }

  isDetailOpen(id: number): boolean {
    return this.detailReservationId === id;
  }

  getSiegesNumeros(reservation: Reservation): string[] {
    const raw = reservation.numero_siege ?? '';
    if (!raw.trim()) {
      return [];
    }
    return raw.split(',').map(s => s.trim()).filter(Boolean);
  }

  getSiegesTexte(reservation: Reservation): string {
    if (reservation.sieges_affichage) {
      return reservation.sieges_affichage;
    }
    const sieges = this.getSiegesNumeros(reservation);
    if (sieges.length === 0) {
      return 'Attribués après confirmation';
    }
    if (sieges.length === 1) {
      return `Siège ${sieges[0]}`;
    }
    return `Sièges ${sieges.join(', ')}`;
  }

  getPrixUnitaire(reservation: Reservation): string {
    const trajet = reservation.trajet_detail;
    if (!trajet?.prix_base || !reservation.nombre_places) {
      return '—';
    }
    const unit = Number(trajet.prix_base);
    if (Number.isNaN(unit)) {
      return '—';
    }
    return `${unit} FCFA`;
  }

  annuler(id: number): void {
    this.reservationService.annuler(id).subscribe({
      next: () => {
        const r = this.reservations.find(r => r.id === id);
        if (r) r.statut = 'annulee';
        if (this.detailReservationId === id) {
          this.fermerDetails();
        }
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

  getStatutLabel(reservation: Reservation): string {
    if (reservation.statut_affichage) {
      return reservation.statut_affichage;
    }
    const labels: Record<string, string> = {
      en_attente: 'En attente de confirmation admin',
      confirmee: 'Confirmée',
      annulee: 'Annulée',
      terminee: 'Terminée',
    };
    return labels[reservation.statut] ?? reservation.statut;
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
