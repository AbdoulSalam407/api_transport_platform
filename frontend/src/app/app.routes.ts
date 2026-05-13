import { Routes } from '@angular/router';

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
        loadComponent: () =>
          import('./pages/passager/dashboard-passager/dashboard-passager.component').then(
            (m) => m.DashboardPassagerComponent,
          ),
      },
      {
        path: 'dashboard-transporteur',
        loadComponent: () =>
          import('./pages/transporteur/dashboard-transporteur/dashboard-transporteur.component').then(
            (m) => m.DashboardTransporteurComponent,
          ),
      },
      {
        path: 'dashboard-admin',
        loadComponent: () =>
          import('./pages/admin/dashboard-admin/dashboard-admin.component').then(
            (m) => m.DashboardAdminComponent,
          ),
      },
      {
        path: 'recherche',
        loadComponent: () =>
          import('./pages/recherche/recherche/recherche.component').then(
            (m) => m.RechercheComponent,
          ),
      },
      {
        path: 'reservation',
        loadComponent: () =>
          import('./pages/reservation/reservation/reservation.component').then(
            (m) => m.ReservationComponent,
          ),
      },
    ],
  },
  { path: '**', redirectTo: '' },
];
