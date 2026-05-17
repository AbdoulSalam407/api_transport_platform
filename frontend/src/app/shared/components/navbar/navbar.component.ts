import { Component, signal, computed } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { NgClass, CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, NgClass, CommonModule],
  templateUrl: './navbar.component.html',
})
export class NavbarComponent {
  protected readonly isOpen = signal(false);
  protected readonly user = signal<{ role: string; email: string } | null>(null);

  protected readonly dashboardRoute = computed(() => {
    const currentUser = this.user();
    if (!currentUser) return '/login';
    if (currentUser.role === 'transporteur') return '/dashboard-transporteur';
    if (currentUser.role === 'admin') return '/dashboard-admin';
    return '/dashboard-passager';
  });

  protected readonly pageTitle = computed(() => {
    const url = this.router.url;
    if (url.includes('dashboard-passager')) {
      return 'Tableau de bord';
    }
    if (url.includes('recherche')) {
      return 'Trajets disponibles';
    }
    if (url.includes('reservation')) {
      return 'Réservation';
    }
    if (url.includes('dashboard-transporteur')) {
      return 'Dashboard transporteur';
    }
    if (url.includes('dashboard-admin')) {
      return 'Dashboard admin';
    }
    return 'Transport+';
  });

  constructor(private router: Router) {
    this.loadUser();
    this.router.events.subscribe(() => this.loadUser());
  }

  toggle(): void {
    this.isOpen.set(!this.isOpen());
  }

  close(): void {
    this.isOpen.set(false);
  }

  logout(): void {
    localStorage.removeItem('transport_user');
    this.user.set(null);
    this.router.navigate(['/login']);
  }

  private loadUser(): void {
    const raw = localStorage.getItem('transport_user');
    if (!raw) {
      this.user.set(null);
      return;
    }
    this.user.set(JSON.parse(raw));
  }
}
