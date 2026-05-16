import { Component } from '@angular/core';
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

  constructor(private router: Router, private authService: AuthService) {}

  login(): void {
    this.error = '';
    this.loading = true;

    this.authService.login({ email: this.email.trim(), password: this.password }).subscribe({
      next: (res) => {
        setTimeout(() => {
          this.loading = false;
          const role = res.user?.role ?? res.role;
          if (role === 'passager') this.router.navigate(['/dashboard-passager']);
          else if (role === 'transporteur') this.router.navigate(['/dashboard-transporteur']);
          else if (role === 'admin') this.router.navigate(['/dashboard-admin']);
          else this.router.navigate(['/']);
        });
      },
      error: (err) => {
        setTimeout(() => {
          this.loading = false;
          this.error =
            formatHttpErrorMessage(err) || err.error?.error || 'Identifiants incorrects.';
        });
      },
    });
  }
}
