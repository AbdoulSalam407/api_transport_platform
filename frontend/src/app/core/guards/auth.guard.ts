import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (auth.isLoggedIn()) return true;

  router.navigate(['/login']);
  return false;
};

function dashboardForRole(role: string | null): string {
  if (role === 'transporteur') return '/dashboard-transporteur';
  if (role === 'admin') return '/dashboard-admin';
  if (role === 'passager') return '/dashboard-passager';
  return '/login';
}

export const roleGuard = (role: string): CanActivateFn => () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (auth.isLoggedIn() && auth.getRole() === role) return true;

  if (auth.isLoggedIn()) {
    router.navigate([dashboardForRole(auth.getRole())]);
    return false;
  }

  router.navigate(['/login']);
  return false;
};
