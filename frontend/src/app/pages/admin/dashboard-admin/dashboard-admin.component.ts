import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { finalize } from 'rxjs/operators';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../core/services/auth.service';
import { AdminService } from '../../../core/services/admin.service';
import { User } from '../../../core/models/user.model';

@Component({
  selector: 'app-dashboard-admin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard-admin.component.html',
})
export class DashboardAdminComponent implements OnInit {
  userName = '';
  users: User[] = [];
  filteredUsers: User[] = [];
  loading = true;
  error = '';
  filtreRole = '';
  filtreStatut = '';
  page = 1;
  pageSize = 10;

  trajetsEnAttente: any[] = [];
  reservationsEnAttente: any[] = [];
  loadingTrajets = false;
  loadingReservations = false;
  reservationsError = '';
  adminMessage = '';

  constructor(
    private router: Router,
    private authService: AuthService,
    private adminService: AdminService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    if (!this.authService.isLoggedIn() || this.authService.getRole() !== 'admin') {
      this.router.navigate(['/login']);
      return;
    }
    const user = this.authService.getUser();
    this.userName = user ? `${user.prenom} ${user.nom}` : 'Admin';
    this.chargerUtilisateurs();
    this.chargerTrajetsEnAttente();
    this.chargerReservationsEnAttente();
  }

  chargerUtilisateurs(): void {
    this.loading = true;
    this.adminService
      .getUsers()
      .pipe(
        finalize(() => {
          this.loading = false;
          this.cdr.markForCheck();
        }),
      )
      .subscribe({
        next: (res) => {
          this.users = Array.isArray(res) ? res : (res.results ?? []);
          this.appliquerFiltres();
        },
        error: () => {
          this.error = 'Impossible de charger les utilisateurs.';
        },
      });
  }

  appliquerFiltres(): void {
    this.filteredUsers = this.users.filter(u => {
      const roleOk = !this.filtreRole || u.role === this.filtreRole;
      const statutOk = !this.filtreStatut ||
        (this.filtreStatut === 'actif' && u.is_actif) ||
        (this.filtreStatut === 'inactif' && !u.is_actif);
      return roleOk && statutOk;
    });
    this.page = 1;
  }

  get paginatedUsers(): User[] {
    const start = (this.page - 1) * this.pageSize;
    return this.filteredUsers.slice(start, start + this.pageSize);
  }

  get totalPages(): number {
    return Math.ceil(this.filteredUsers.length / this.pageSize);
  }

  pagePrecedente(): void {
    if (this.page > 1) {
      this.page--;
    }
  }

  pageSuivante(): void {
    if (this.page < this.totalPages) {
      this.page++;
    }
  }

  get totalUtilisateurs(): number { return this.users.length; }
  get totalPassagers(): number { return this.users.filter(u => u.role === 'passager').length; }
  get totalTransporteurs(): number { return this.users.filter(u => u.role === 'transporteur').length; }

  chargerTrajetsEnAttente(): void {
    this.loadingTrajets = true;
    this.adminService.getTrajetsEnAttente().subscribe({
      next: (res) => {
        this.trajetsEnAttente = Array.isArray(res) ? res : (res.results ?? []);
        this.loadingTrajets = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.loadingTrajets = false;
        this.cdr.markForCheck();
      },
    });
  }

  chargerReservationsEnAttente(): void {
    this.loadingReservations = true;
    this.reservationsError = '';
    this.adminService.getReservationsEnAttente().subscribe({
      next: (res) => {
        this.reservationsEnAttente = Array.isArray(res) ? res : (res.results ?? []);
        this.loadingReservations = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.reservationsError =
          'Impossible de charger les réservations en attente. Vérifiez que vous êtes connecté en tant qu\'administrateur.';
        this.loadingReservations = false;
        this.cdr.markForCheck();
      },
    });
  }

  approuverTrajet(id: number): void {
    this.adminService.approuverTrajet(id).subscribe({
      next: (res) => {
        this.adminMessage = res.message || 'Trajet approuvé.';
        this.chargerTrajetsEnAttente();
      },
      error: () => alert('Impossible d\'approuver ce trajet.'),
    });
  }

  rejeterTrajet(id: number): void {
    const motif = prompt('Motif du rejet (optionnel) :') ?? '';
    this.adminService.rejeterTrajet(id, motif).subscribe({
      next: (res) => {
        this.adminMessage = res.message || 'Trajet rejeté.';
        this.chargerTrajetsEnAttente();
      },
      error: () => alert('Impossible de rejeter ce trajet.'),
    });
  }

  confirmerReservation(id: number): void {
    this.adminService.confirmerReservation(id).subscribe({
      next: (res) => {
        this.adminMessage = res.message || 'Réservation confirmée.';
        this.chargerReservationsEnAttente();
      },
      error: () => alert('Impossible de confirmer cette réservation.'),
    });
  }

  validerUtilisateur(user: User): void {
    this.adminService.verifierUser(user.id).subscribe({
      next: () => {
        user.is_verified = true;
        user.is_actif = true;
        this.adminMessage = 'Utilisateur validé.';
        this.appliquerFiltres();
        this.cdr.markForCheck();
      },
      error: () => alert('Validation impossible.'),
    });
  }

  toggleActif(user: User): void {
    const action = user.is_actif
      ? this.adminService.desactiverUser(user.id)
      : this.adminService.activerUser(user.id);

    action.subscribe({
      next: () => {
        user.is_actif = !user.is_actif;
        this.appliquerFiltres();
      },
      error: () => alert('Action impossible.')
    });
  }

  getRoleClass(role: string): string {
    const map: Record<string, string> = {
      passager: 'bg-blue-100 text-blue-700',
      transporteur: 'bg-orange-100 text-orange-700',
      admin: 'bg-red-100 text-red-700',
    };
    return map[role] ?? 'bg-slate-100 text-slate-600';
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
}
