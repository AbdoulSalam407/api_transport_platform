import { Component, ChangeDetectorRef } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';
import { formatHttpErrorMessage } from '../../../core/utils/format-http-error';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  email = '';
  password = '';
  error = '';
  loading = false;

  constructor(
    private router: Router,
    private authService: AuthService,
    private cdr: ChangeDetectorRef,
  ) {}

  login(): void {
    this.error = '';
    this.loading = true;
    // Évite d'envoyer un ancien jeton invalide (403 « Invalid token »)
    this.authService.clearSession();

    this.authService.login({ email: this.email.trim(), password: this.password }).subscribe({
      next: (res) => {
        this.loading = false;
        const role = res.user?.role ?? res.role;
        if (role === 'passager') this.router.navigate(['/dashboard-passager']);
        else if (role === 'transporteur') this.router.navigate(['/dashboard-transporteur']);
        else if (role === 'admin') this.router.navigate(['/dashboard-admin']);
        else this.router.navigate(['/']);
        this.cdr.markForCheck();
      },
      error: (err) => {
        this.loading = false;
        const msg = formatHttpErrorMessage(err);
        const detail = err.error?.detail;
        const apiError = err.error?.error;
        this.error =
          msg ||
          (typeof detail === 'string' ? detail : '') ||
          (typeof apiError === 'string' ? apiError : '') ||
          (err.status === 401 || err.status === 403
            ? 'Email ou mot de passe incorrect.'
            : 'Identifiants incorrects.');
        this.cdr.markForCheck();
      },
    });
  }
}
