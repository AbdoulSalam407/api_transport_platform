import { Routes } from '@angular/router';
import { authGuard, roleGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./shared/layouts/main-layout/main-layout.component').then(
        (m) => m.MainLayoutComponent,
      ),
    children: [
      {
        path: '',
        pathMatch: 'full',
        loadComponent: () =>
          import('./pages/home/home.component').then((m) => m.HomeComponent),
      },
      {
        path: 'home',
        redirectTo: '',
        pathMatch: 'full',
      },
      {
        path: 'login',
        loadComponent: () =>
          import('./pages/auth/login/login.component').then(
            (m) => m.LoginComponent,
          ),
      },
      {
        path: 'register',
        loadComponent: () =>
          import('./pages/auth/register/register.component').then(
            (m) => m.RegisterComponent,
          ),
      },
      {
        path: 'dashboard-passager',
        canActivate: [roleGuard('passager')],
        loadComponent: () =>
          import('./pages/passager/dashboard-passager/dashboard-passager.component').then(
            (m) => m.DashboardPassagerComponent,
          ),
      },
      {
        path: 'dashboard-transporteur',
        canActivate: [roleGuard('transporteur')],
        loadComponent: () =>
          import('./pages/transporteur/dashboard-transporteur/dashboard-transporteur.component').then(
            (m) => m.DashboardTransporteurComponent,
          ),
      },
      {
        path: 'dashboard-admin',
        canActivate: [roleGuard('admin')],
        loadComponent: () =>
          import('./pages/admin/dashboard-admin/dashboard-admin.component').then(
            (m) => m.DashboardAdminComponent,
          ),
      },
      {
        path: 'recherche',
        canActivate: [authGuard],
        loadComponent: () =>
          import('./pages/recherche/recherche/recherche.component').then(
            (m) => m.RechercheComponent,
          ),
      },
      {
        path: 'reservation',
        canActivate: [authGuard],
        loadComponent: () =>
          import('./pages/reservation/reservation/reservation.component').then(
            (m) => m.ReservationComponent,
          ),
      },
    ],
  },
  { path: '**', redirectTo: '' },
];
