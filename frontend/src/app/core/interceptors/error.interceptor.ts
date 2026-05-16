import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, retry, timeout } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

/**
 * Intercepteur global pour gérer les erreurs HTTP
 * - Retry automatique pour les erreurs temporaires
 * - Timeout sur les requêtes
 * - Gestion centralisée des erreurs 401, 403, 500
 * - Logging des erreurs
 */
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  return next(req).pipe(
    // Timeout après 30 secondes
    timeout(30000),

    // Retry automatique pour les erreurs temporaires (max 2 tentatives)
    retry({
      count: 2,
      delay: (error, retryCount) => {
        // Retry seulement pour certains status (408, 429, 500, 502, 503, 504)
        const retryableStatusCodes = [408, 429, 500, 502, 503, 504];
        if (retryableStatusCodes.includes(error.status)) {
          console.warn(`Retry ${retryCount}/2 pour ${req.url}:`, error.status);
          return throwError(() => error);
        }
        return throwError(() => error);
      },
    }),

    // Gestion des erreurs
    catchError((error) => {
      const errorResponse = {
        status: error.status,
        message: '',
        details: null,
        timestamp: new Date().toISOString(),
      };

      // Extraire le message d'erreur du backend
      if (error.error?.message) {
        errorResponse.message = error.error.message;
      } else if (error.error?.detail) {
        errorResponse.message = error.error.detail;
      } else if (error.error?.errors) {
        errorResponse.details = error.error.errors;
      }

      // Gestion par status code
      switch (error.status) {
        case 0:
          errorResponse.message = 'Erreur de connexion. Vérifiez votre connexion réseau.';
          console.error('Network error:', error);
          break;

        case 400:
          errorResponse.message =
            errorResponse.message || 'Requête invalide. Vérifiez vos données.';
          console.warn('Bad request:', error.error);
          break;

        case 401:
          errorResponse.message = 'Votre session a expiré. Veuillez vous reconnecter.';
          authService.logout();
          router.navigate(['/login']);
          break;

        case 403:
          errorResponse.message = "Vous n'avez pas les permissions pour accéder à cette ressource.";
          console.warn('Forbidden:', error.error);
          break;

        case 404:
          errorResponse.message = errorResponse.message || 'Ressource non trouvée.';
          break;

        case 408:
          errorResponse.message = "La requête a dépassé le délai d'attente.";
          break;

        case 429:
          errorResponse.message = 'Trop de requêtes. Veuillez patienter avant de réessayer.';
          console.warn('Rate limited');
          break;

        case 500:
          errorResponse.message = 'Erreur serveur. Veuillez réessayer plus tard.';
          console.error('Server error:', error.error);
          break;

        case 502:
        case 503:
        case 504:
          errorResponse.message =
            'Le serveur est actuellement indisponible. Veuillez réessayer plus tard.';
          console.error('Service unavailable:', error.status);
          break;

        default:
          errorResponse.message = error.message || 'Une erreur est survenue. Veuillez réessayer.';
          console.error('Unexpected error:', error);
      }

      // Logger l'erreur
      console.error('HTTP Error:', {
        url: req.url,
        method: req.method,
        status: error.status,
        message: errorResponse.message,
        timestamp: errorResponse.timestamp,
      });

      // Retourner l'erreur avec le format standardisé
      error.customErrorResponse = errorResponse;
      return throwError(() => error);
    }),
  );
};
