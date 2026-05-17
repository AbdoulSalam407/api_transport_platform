import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, timeout } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

function isPublicAuthRequest(url: string): boolean {
  return /\/users\/(login|register)\/?$/i.test(url);
}

/**
 * Intercepteur d'erreurs HTTP (sans retry automatique qui ralentit chaque requête en échec).
 */
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const publicAuth = isPublicAuthRequest(req.url);

  return next(req).pipe(
    timeout(12000),
    catchError((error: HttpErrorResponse) => {
      const errorResponse = {
        status: error.status,
        message: '',
        details: null as unknown,
        timestamp: new Date().toISOString(),
      };

      const body = error.error;
      if (body && typeof body === 'object' && !Array.isArray(body)) {
        if (typeof body.message === 'string') {
          errorResponse.message = body.message;
        } else if (typeof body.detail === 'string') {
          errorResponse.message = body.detail;
        } else if (body.errors) {
          errorResponse.details = body.errors;
        }
      }

      switch (error.status) {
        case 0:
          errorResponse.message = 'Erreur de connexion. Vérifiez votre connexion réseau.';
          break;
        case 400:
          errorResponse.message =
            errorResponse.message || 'Requête invalide. Vérifiez vos données.';
          break;
        case 401:
          if (publicAuth) {
            errorResponse.message =
              errorResponse.message || 'Email ou mot de passe incorrect.';
          } else {
            errorResponse.message = 'Votre session a expiré. Veuillez vous reconnecter.';
            authService.clearSession();
            if (!router.url.includes('/login')) {
              router.navigate(['/login']);
            }
          }
          break;
        case 403:
          if (publicAuth) {
            authService.clearSession();
            errorResponse.message =
              errorResponse.message ||
              'Session expirée ou jeton invalide. Réessayez de vous connecter.';
          } else {
            errorResponse.message =
              errorResponse.message ||
              "Vous n'avez pas les permissions pour accéder à cette ressource.";
          }
          break;
        case 404:
          errorResponse.message = errorResponse.message || 'Ressource non trouvée.';
          break;
        case 408:
          errorResponse.message = "La requête a dépassé le délai d'attente.";
          break;
        case 429:
          errorResponse.message = 'Trop de requêtes. Veuillez patienter avant de réessayer.';
          break;
        case 500:
          errorResponse.message = 'Erreur serveur. Veuillez réessayer plus tard.';
          break;
        case 502:
        case 503:
        case 504:
          errorResponse.message =
            'Le serveur est actuellement indisponible. Veuillez réessayer plus tard.';
          break;
        default:
          if ((error as Error).name === 'TimeoutError') {
            errorResponse.message = 'Le serveur met trop de temps à répondre. Réessayez.';
          } else {
            errorResponse.message =
              errorResponse.message || 'Une erreur est survenue. Veuillez réessayer.';
          }
      }

      (error as HttpErrorResponse & { customErrorResponse?: typeof errorResponse }).customErrorResponse =
        errorResponse;
      return throwError(() => error);
    }),
  );
};
