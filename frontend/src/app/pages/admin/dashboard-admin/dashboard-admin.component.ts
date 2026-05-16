import { Component, OnInit } from '@angular/core';
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

  constructor(
    private router: Router,
    private authService: AuthService,
    private adminService: AdminService
  ) {}

  ngOnInit(): void {
    if (!this.authService.isLoggedIn() || this.authService.getRole() !== 'admin') {
      this.router.navigate(['/login']);
      return;
    }
    const user = this.authService.getUser();
    this.userName = user ? `${user.prenom} ${user.nom}` : 'Admin';
    this.chargerUtilisateurs();
  }

  chargerUtilisateurs(): void {
    this.loading = true;
    this.adminService.getUsers().subscribe({
      next: (res) => {
        this.users = Array.isArray(res) ? res : (res.results ?? []);
        this.appliquerFiltres();
        this.loading = false;
      },
      error: () => {
        this.error = 'Impossible de charger les utilisateurs.';
        this.loading = false;
      }
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
