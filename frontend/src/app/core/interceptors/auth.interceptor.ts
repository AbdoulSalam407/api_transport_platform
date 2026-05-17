import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';

/** Routes publiques : pas de jeton (évite 403 si ancien token invalide en localStorage). */
function isPublicApiRequest(url: string): boolean {
  return (
    /\/users\/(login|register)\/?$/i.test(url) ||
    /\/trajets\/statistiques\/?$/i.test(url)
  );
}

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  if (token && !isPublicApiRequest(req.url)) {
    const authReq = req.clone({
      setHeaders: { Authorization: `Token ${token}` },
    });
    return next(authReq);
  }

  return next(req);
};
